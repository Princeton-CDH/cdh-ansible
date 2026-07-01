"""Sphinx extension: generate an inventory reference page from ``inventory/``.

On ``builder-inited`` we shell out to ``ansible-inventory`` (which lives in
the same environment Sphinx is running in) and render a Markdown page listing
applications, environments, and hostnames.

The generated file is written to ``docs/inventory.generated.md`` and marked
``:orphan:`` so it does not need to appear in any toctree. This keeps the page
build-checked but unlinked from the site nav until the team decides whether to
publish hostnames publicly.

Design notes:

- No variable values are emitted. Only group structure and hostnames — the
  same information that is already in ``inventory/all_hosts``.
- ``ansible-inventory`` is invoked with ``ANSIBLE_VAULT_IDENTITY_LIST`` cleared
  so the build does not attempt to decrypt vault variables. Structure and
  hostnames do not require decryption.
- We use ``--list --yaml`` for structured data and ``--graph`` for a raw tree
  view; both are appended to the page.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

import yaml
from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)

# Groups that are pure organizational containers, not applications.
# Excluded from the "Applications" table but still appear in the full graph.
_META_GROUPS = {"all", "ungrouped", "staging", "production", "prod", "dev"}


def _run_ansible_inventory(repo_root: Path, args: list[str]) -> str:
    """Invoke ``ansible-inventory`` from the repo root without vault access."""
    env = os.environ.copy()
    # Prevent any attempt to load the vault password script during build.
    env.pop("ANSIBLE_VAULT_IDENTITY_LIST", None)
    result = subprocess.run(
        ["ansible-inventory", *args],
        cwd=repo_root,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


class _VaultTolerantLoader(yaml.SafeLoader):
    """SafeLoader that treats unknown YAML tags (e.g. ``!vault``) as plain text.

    ``ansible-inventory --list --yaml`` emits ``!vault`` tagged scalars for
    encrypted values. We do not need their contents — this loader lets us
    parse the structure without importing Ansible's vault machinery.
    """


def _ignore_unknown_tag(loader: yaml.Loader, tag_suffix: str, node: yaml.Node) -> str:
    return "<encrypted>"


_VaultTolerantLoader.add_multi_constructor("!", _ignore_unknown_tag)


def _load_inventory(repo_root: Path) -> dict[str, Any]:
    """Return the parsed ``--list --yaml`` inventory as a dict."""
    raw = _run_ansible_inventory(repo_root, ["--list", "--yaml"])
    data = yaml.load(raw, Loader=_VaultTolerantLoader)  # noqa: S506 - safe: custom loader
    if not isinstance(data, dict):
        raise RuntimeError("ansible-inventory returned unexpected shape")
    return data


def _walk_groups(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Flatten the nested inventory dict into ``{group_name: merged_node}``.

    ``ansible-inventory --list --yaml`` repeats group definitions wherever
    they appear in the hierarchy — e.g. ``cdhweb_staging`` shows up both
    under ``cdhweb`` (with hosts) and under ``staging`` (as an empty
    reference). We merge hosts and children across all occurrences so the
    lookup returns the full picture.
    """
    flat: dict[str, dict[str, Any]] = {}

    def _visit(name: str, node: dict[str, Any] | None) -> None:
        if not isinstance(node, dict):
            return
        merged = flat.setdefault(name, {"hosts": {}, "children": {}})
        for host_name, host_vars in (node.get("hosts") or {}).items():
            merged["hosts"].setdefault(host_name, host_vars)
        for child_name, child_node in (node.get("children") or {}).items():
            merged["children"].setdefault(child_name, True)
            _visit(child_name, child_node)

    for name, node in (inventory.get("all") or {}).get("children", {}).items():
        _visit(name, node)
    return flat


def _app_groups(groups: dict[str, dict[str, Any]]) -> list[str]:
    """Return application group names, sorted.

    Heuristic: a group is an "application" if it has ``children`` that look
    like ``<name>_staging`` / ``<name>_production``. This matches the
    convention documented in ``AGENTS.md``.
    """
    apps: list[str] = []
    for name, node in groups.items():
        if name in _META_GROUPS:
            continue
        children = node.get("children") or {}
        if any(
            c == f"{name}_staging" or c == f"{name}_production" for c in children
        ):
            apps.append(name)
    return sorted(apps)


def _hosts_in(groups: dict[str, dict[str, Any]], group: str) -> list[str]:
    """Return the direct + descendant hosts of ``group``, deduplicated."""
    node = groups.get(group)
    if not node:
        return []
    # ``hosts`` in --list --yaml is a mapping {hostname: {vars...}}
    hosts: set[str] = set((node.get("hosts") or {}).keys())
    for child in (node.get("children") or {}):
        hosts.update(_hosts_in(groups, child))
    return sorted(hosts)


def _render(inventory: dict[str, Any], graph: str) -> str:
    groups = _walk_groups(inventory)
    lines: list[str] = [
        "---",
        "orphan: true",
        "---",
        "",
        "# Inventory Reference",
        "",
        "_This page is generated from `inventory/` at documentation build time._ "
        "It shows only host and group structure; no variable values are included.",
        "",
        "## Applications",
        "",
        "| Application | Staging Hosts | Production Hosts |",
        "| --- | --- | --- |",
    ]

    for app in _app_groups(groups):
        staging = _hosts_in(groups, f"{app}_staging")
        production = _hosts_in(groups, f"{app}_production")
        lines.append(
            "| `{app}` | {s} | {p} |".format(
                app=app,
                s="<br>".join(f"`{h}`" for h in staging) or "—",
                p="<br>".join(f"`{h}`" for h in production) or "—",
            )
        )

    lines += [
        "",
        "## Full group graph",
        "",
        "```",
        graph.rstrip(),
        "```",
        "",
    ]
    return "\n".join(lines)


def _generate(app: Sphinx) -> None:
    repo_root = Path(app.srcdir).parent  # docs/ -> repo root
    try:
        inventory = _load_inventory(repo_root)
        graph = _run_ansible_inventory(repo_root, ["--graph"])
    except (subprocess.CalledProcessError, FileNotFoundError, RuntimeError) as exc:
        logger.warning(
            "inventory_docs: could not generate inventory page (%s); "
            "the inventory reference page will be missing from this build.",
            exc,
        )
        return

    out = Path(app.srcdir) / "inventory.generated.md"
    out.write_text(_render(inventory, graph), encoding="utf-8")
    logger.info("inventory_docs: wrote %s", out.relative_to(repo_root))


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("builder-inited", lambda a: _generate(a))
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
