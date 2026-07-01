"""Sphinx extension: generate an inventory reference page from ``inventory/``.

Parses ``inventory/all_hosts`` as INI at build time and writes
``docs/inventory.md``, which contains a single sortable/filterable table
(via ``sphinx-datatables``) with one row per application and columns for
staging vs production hosts.

Design notes:

- We parse the inventory file directly rather than shelling out to
  ``ansible-inventory``. The file is a static INI-ish document; ``configparser``
  handles it in ~50 lines and avoids any need to worry about vault decryption
  or Ansible being importable at doc-build time.
- Only group/host membership is emitted. No variable values are read.
- The generated page is linked from ``index.md``'s toctree; the extension
  overwrites it on every build.
- The table is rendered with the ``csv-table`` directive and given the
  ``sphinx-datatable`` CSS class so ``sphinx-datatables`` upgrades it to a
  sortable/searchable table in the HTML output.
"""

from __future__ import annotations

import configparser
from pathlib import Path
from typing import Any

from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)

# Purely organizational groups; not applications. Excluded from the app list.
_ENV_GROUPS = {"staging", "production", "prod", "dev"}


def _parse_inventory(path: Path) -> dict[str, set[str]]:
    """Return ``{group_name: set(hostnames)}`` with children fully expanded.

    Handles the two INI section styles used in ``inventory/all_hosts``:

    - ``[group]`` — one host per line
    - ``[group:children]`` — one child *group* per line
    """
    parser = configparser.ConfigParser(allow_no_value=True, delimiters=("=",))
    # Preserve case; Ansible group names are case-sensitive by convention.
    parser.optionxform = str  # type: ignore[assignment]
    parser.read(path, encoding="utf-8")

    direct_hosts: dict[str, set[str]] = {}
    children: dict[str, set[str]] = {}

    for section in parser.sections():
        if section.endswith(":children"):
            group = section[: -len(":children")]
            children.setdefault(group, set()).update(parser.options(section))
        else:
            direct_hosts.setdefault(section, set()).update(parser.options(section))

    # Recursively expand children into a flat hosts-per-group map.
    resolved: dict[str, set[str]] = {}

    def _resolve(group: str, seen: set[str]) -> set[str]:
        if group in resolved:
            return resolved[group]
        if group in seen:  # defensive: cycle guard
            return set()
        seen = seen | {group}
        hosts = set(direct_hosts.get(group, ()))
        for child in children.get(group, ()):
            hosts |= _resolve(child, seen)
        resolved[group] = hosts
        return hosts

    for group in set(direct_hosts) | set(children):
        _resolve(group, set())
    return resolved


def _app_groups(groups: dict[str, set[str]]) -> list[str]:
    """Return application group names, sorted.

    An app is any group with either an ``<name>_staging`` or
    ``<name>_production`` counterpart — matching the AGENTS.md convention.
    Groups ending in ``_staging``/``_production`` themselves and the
    top-level environment containers are excluded.
    """
    apps: list[str] = []
    for name in groups:
        if name in _ENV_GROUPS:
            continue
        if name.endswith("_staging") or name.endswith("_production"):
            continue
        if f"{name}_staging" in groups or f"{name}_production" in groups:
            apps.append(name)
    return sorted(apps)


def _format_hosts(hosts: set[str]) -> str:
    """Render a set of hostnames as monospaced, line-separated cell content."""
    if not hosts:
        return "—"
    # ``<br>`` inside a csv-table cell renders as a line break in HTML output.
    return "<br>".join(f"``{h}``" for h in sorted(hosts))


def _csv_escape(value: str) -> str:
    """Quote a cell for the csv-table directive.

    csv-table uses standard CSV rules: cells containing commas or quotes must
    be double-quoted, and embedded quotes are doubled.
    """
    if "," in value or '"' in value:
        return '"' + value.replace('"', '""') + '"'
    return value


def _render(groups: dict[str, set[str]]) -> str:
    lines: list[str] = [
        "# Inventory Reference",
        "",
        "_Generated from `inventory/all_hosts` at documentation build time._ "
        "Only host and group structure is included — no variable values.",
        "",
        "Click a column header to sort; use the search box in the top-right "
        "of the table to filter by application or hostname.",
        "",
        "```{csv-table}",
        ":header: Application, Staging hosts, Production hosts",
        ":class: sphinx-datatable",
        ":widths: 20, 40, 40",
        "",
    ]

    for app in _app_groups(groups):
        row = [
            f"``{app}``",
            _format_hosts(groups.get(f"{app}_staging", set())),
            _format_hosts(groups.get(f"{app}_production", set())),
        ]
        lines.append(", ".join(_csv_escape(cell) for cell in row))

    lines += ["```", ""]
    return "\n".join(lines)


def _generate(app: Sphinx) -> None:
    repo_root = Path(app.srcdir).parent  # docs/ -> repo root
    inventory_file = repo_root / "inventory" / "all_hosts"
    try:
        groups = _parse_inventory(inventory_file)
    except (OSError, configparser.Error) as exc:
        logger.warning(
            "inventory_docs: could not parse %s (%s); "
            "the inventory reference page will be missing from this build.",
            inventory_file,
            exc,
        )
        return

    out = Path(app.srcdir) / "inventory.md"
    out.write_text(_render(groups), encoding="utf-8")
    logger.info("inventory_docs: wrote %s", out.relative_to(repo_root))


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("builder-inited", lambda a: _generate(a))
    return {
        "version": "0.4",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
