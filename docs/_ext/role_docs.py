"""Sphinx extension: generate per-role RST via antsibull-docs.

Antsibull-docs is built around Ansible collections, not standalone roles.
This extension bridges the gap by:

1. Discovering every local role under ``roles/`` that has a
   ``meta/argument_specs.yml`` file.
2. Assembling a *shim* collection tree at ``docs/_antsibull/collections/``
   with a synthesized ``galaxy.yml`` and symlinks to the selected roles.
3. Running ``antsibull-docs collection --use-current --squash-hierarchy``
   with ``ANSIBLE_COLLECTIONS_PATH`` pointing at the shim, so antsibull
   sees a legitimate collection and produces one ``<role>_role.rst`` file
   per role plus an index page.
4. Post-processing the generated RST to strip artifacts that only make
   sense for a published collection: the verbose ``{fqcn} role -- ...``
   H1 is replaced with just the role name; the "install from Galaxy"
   note is removed; the redundant inline ``.. contents::`` block is
   removed (Furo renders its own on-page TOC); and for roles with a
   single entrypoint the extra ``Entry point`` H2 is flattened away.
5. Copying the transformed RST into ``docs/roles/``.
6. Auto-updating the toctree in ``docs/roles/index.md`` so newly discovered
   roles appear without manual edits.

Everything under ``docs/_antsibull/`` and every generated ``docs/roles/*.rst``
is regenerated on every build and is gitignored.

Design notes:

- Roles are *symlinked* into the shim so antsibull always sees the live
  role directory. The shim tree is rebuilt from scratch on every build
  so stale symlinks are not a concern. Windows is not supported.
- If antsibull-docs is missing or fails, we log a warning and continue the
  build without the role pages. This mirrors ``inventory_docs.py``'s
  behavior and avoids blocking the whole doc build on optional content.
- We deliberately do *not* import antsibull-docs; instead we shell out to
  its CLI. This keeps the extension resilient to antsibull-docs internal
  API changes.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)

# Namespace/name for the shim collection. Not published anywhere; only used
# to satisfy antsibull-docs' collection assumptions.
_SHIM_NAMESPACE = "princeton_cdh"
_SHIM_NAME = "cdh"


def _find_roles_with_argument_specs(roles_dir: Path) -> list[Path]:
    """Return sorted list of role directories that have ``meta/argument_specs.yml``.

    We use presence of the arg spec as the opt-in signal — roles without
    a spec are not ready to be rendered by antsibull-docs.
    """
    if not roles_dir.is_dir():
        return []
    # glob yields ``<role>/meta/argument_specs.yml``; .parent.parent -> ``<role>/``.
    return sorted(
        spec.parent.parent
        for spec in roles_dir.glob("*/meta/argument_specs.yml")
    )


def _build_shim(shim_root: Path, roles: list[Path]) -> Path:
    """Assemble the shim collection tree; return the collections search path.

    Layout produced::

        <shim_root>/collections/                 <-- returned (goes in
                                                     ANSIBLE_COLLECTIONS_PATH)
            ansible_collections/<ns>/<name>/
                galaxy.yml
                README.md
                roles/
                    <role>/    (symlink to the live role dir in repo)
    """
    collections_search_path = shim_root / "collections"
    collection_root = (
        collections_search_path
        / "ansible_collections"
        / _SHIM_NAMESPACE
        / _SHIM_NAME
    )

    # Start clean so removed roles don't linger in the shim between builds
    # (symlinks would otherwise persist across renames/deletions).
    if collections_search_path.exists():
        shutil.rmtree(collections_search_path)
    (collection_root / "roles").mkdir(parents=True)

    (collection_root / "galaxy.yml").write_text(
        # Synthetic manifest; version is a placeholder because this shim is
        # never published to Galaxy.
        "---\n"
        f"namespace: {_SHIM_NAMESPACE}\n"
        f"name: {_SHIM_NAME}\n"
        "version: 0.0.0\n"
        "readme: README.md\n"
        "authors:\n"
        "  - Center for Digital Humanities @ Princeton\n"
        "description: >-\n"
        "  Documentation-only shim wrapping selected local roles from the\n"
        "  cdh-ansible repository so antsibull-docs can render them.\n"
        "license:\n"
        "  - Apache-2.0\n"
        "repository: https://github.com/Princeton-CDH/cdh-ansible\n",
        encoding="utf-8",
    )
    (collection_root / "README.md").write_text(
        "# princeton_cdh.cdh (docs shim)\n\n"
        "Placeholder collection used only by antsibull-docs. See the real\n"
        "repository at https://github.com/Princeton-CDH/cdh-ansible.\n",
        encoding="utf-8",
    )

    for role in roles:
        (collection_root / "roles" / role.name).symlink_to(role)

    return collections_search_path


def _run_antsibull(collections_search_path: Path, dest_dir: Path) -> None:
    """Invoke ``antsibull-docs collection`` against the shim.

    ``--use-current`` tells antsibull to use the collection at
    ``ANSIBLE_COLLECTIONS_PATH`` rather than downloading from Galaxy.
    ``--squash-hierarchy`` drops the ``collections/<ns>/<name>/`` prefix in
    the output tree so files land directly in ``dest_dir``.
    """
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True)

    env = os.environ.copy()
    env["ANSIBLE_COLLECTIONS_PATH"] = str(collections_search_path)
    # Don't try to load the vault script during doc generation.
    env.pop("ANSIBLE_VAULT_IDENTITY_LIST", None)

    subprocess.run(
        [
            "antsibull-docs",
            "collection",
            "--use-current",
            "--squash-hierarchy",
            "--fail-on-error",
            "--dest-dir",
            str(dest_dir),
            f"{_SHIM_NAMESPACE}.{_SHIM_NAME}",
        ],
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Post-processing of antsibull's generated RST.
#
# Antsibull emits a header block that assumes the collection is a published,
# Galaxy-installable artifact. Ours is a doc-only shim, so several parts of
# that output are actively misleading or redundant in our Furo-themed site:
#
#   * The H1 is ``{fqcn} role -- {short_description}``; the FQCN prefix is
#     meaningless to readers and clutters Furo's sidebar/TOC.
#   * The "Collection note" tells readers to
#     ``ansible-galaxy collection install princeton_cdh.cdh``, which does not
#     exist on Galaxy.
#   * An inline ``.. contents::`` block duplicates Furo's on-page TOC.
#   * The ``Entry point`` H2 is redundant for single-entrypoint roles (the
#     common case) and adds a wasted level of nesting.
#
# Each of those is handled by a dedicated transform below. Everything else
# (options table, Collection links, cross-reference anchors, etc.) is left
# untouched so antsibull's structure and anchors keep working.
# ---------------------------------------------------------------------------

# Matches an antsibull-emitted title line + its ``+``-underline:
#   ``princeton_cdh.cdh.<role> role -- <short_description>``
#   ``++++++++++++++++++++++++++++++++++++++++++++++++++++``
# ``[A-Za-z0-9_]+`` matches the full range of legal Ansible role names.
_TITLE_RE = re.compile(
    r"^"
    rf"{re.escape(_SHIM_NAMESPACE)}\.{re.escape(_SHIM_NAME)}\."
    r"(?P<role>[A-Za-z0-9_]+) role -- .*\n"  # title line
    r"\++\n",                                # underline of ``+`` chars
    re.MULTILINE,
)

# Matches the whole "Collection note" block: from the ``.. Collection note``
# comment to (and including) the closing blank line before the next section.
# We're strict about the marker on the leading line so we don't strip other
# ``.. note::`` blocks that might legitimately appear in role docs later.
_COLLECTION_NOTE_RE = re.compile(
    r"^\.\. Collection note\n"
    r"(?:.*\n)*?"                       # any lines...
    r"    To use it in a playbook.*\n"  # ...up through the last bullet
    r"\s*\n",                           # trailing blank line (tolerate whitespace)
    re.MULTILINE,
)

# Matches antsibull's inline ``.. contents::`` block (the whole directive
# including its ``:local:`` / ``:depth:`` options and the trailing blank
# line). Furo renders an on-page TOC in the right sidebar automatically,
# so an inline contents block is redundant and looks broken.
# The 3-space indent is coupled to antsibull's current output; option lines
# under an RST directive can technically use any consistent indent.
_CONTENTS_DIRECTIVE_RE = re.compile(
    r"^\.\. contents::\n"
    r"(?:   [^\n]*\n)*"          # any indented option lines (may be empty)
    r"\s*\n",                    # trailing blank line
    re.MULTILINE,
)

# Matches the "Entry point" H2 that antsibull emits for each role
# entrypoint. For a role that only has ``main`` (the common case for
# local roles), this heading is pure noise. Antsibull emits:
#
#     .. _ansible_collections.<ns>.<name>.<role>_role__entrypoint-main:
#
#     .. Entry point title
#
#     Entry point ``main`` -- <short_description>
#     -------------------------------------------
#
# This regex strips only the comment + blank + title + underline (i.e.
# the four lines starting from ``.. Entry point title``). The preceding
# anchor label is deliberately preserved so cross-references to
# ``__entrypoint-main`` continue to resolve.
_ENTRY_POINT_HEADING_RE = re.compile(
    r"^\.\. Entry point title\n"
    r"\n"
    r"Entry point ``[A-Za-z0-9_]+`` -- .*\n"
    r"-+\n",
    re.MULTILINE,
)


def _sub_expected(
    pattern: re.Pattern[str],
    repl: str,
    text: str,
    *,
    role_name: str,
    transform: str,
) -> str:
    """Run ``pattern.sub`` and warn if it didn't fire.

    Every post-processing transform expects to match exactly once against
    antsibull's output; a silent miss usually means antsibull changed its
    emitted format and this extension needs updating. Surface that as a
    build warning so the mismatch is diagnosable.
    """
    new_text, count = pattern.subn(repl, text, count=1)
    if count == 0:
        logger.warning(
            "role_docs: %s transform did not match for role %r; "
            "antsibull-docs output format may have changed.",
            transform,
            role_name,
        )
    return new_text


def _rewrite_title(rst: str, role_name: str) -> str:
    """Replace antsibull's verbose H1 with just the role name."""
    replacement = f"{role_name}\n{'=' * len(role_name)}\n"
    return _sub_expected(
        _TITLE_RE, replacement, rst,
        role_name=role_name, transform="rewrite-title",
    )


def _strip_collection_note(rst: str, role_name: str) -> str:
    """Remove the Galaxy-install note; our shim is not on Galaxy."""
    return _sub_expected(
        _COLLECTION_NOTE_RE, "", rst,
        role_name=role_name, transform="strip-collection-note",
    )


def _strip_local_contents(rst: str, role_name: str) -> str:
    """Remove the inline ``.. contents::`` block; Furo shows its own TOC."""
    return _sub_expected(
        _CONTENTS_DIRECTIVE_RE, "", rst,
        role_name=role_name, transform="strip-contents-directive",
    )


def _promote_underline(rst: str, old_char: str, new_char: str) -> str:
    """Replace every RST section underline of ``old_char`` with ``new_char``.

    Matches only lines composed of at least two of the underline character
    (with optional trailing whitespace) so we don't hit prose that happens
    to start with a stray ``^`` or ``~``. RST underlines are conventionally
    ≥3 chars, so ``{2,}`` is safely conservative.
    """
    pattern = re.compile(rf"^{re.escape(old_char)}{{2,}}\s*$", re.MULTILINE)
    return pattern.sub(lambda m: new_char * len(m.group(0).rstrip()), rst)


def _flatten_single_entrypoint(rst: str) -> str:
    """Remove the redundant ``Entry point`` H2 when there is exactly one.

    Antsibull always emits an ``Entry point <name> -- <desc>`` heading for
    each entrypoint. Local roles almost always have only ``main``; showing
    that heading adds a wasted level of nesting to both the on-page TOC
    and Furo's sidebar. After stripping it we promote the following
    ``^^^`` subheadings (Synopsis, Parameters, Authors) up one level to
    ``---`` so they sit at H2 alongside "Collection links".

    Roles with two or more entrypoints are left untouched; promoting
    underlines across multiple sections would collide heading levels.
    Roles with zero matches (unexpected) are also left untouched — a
    warning is emitted from ``_transform_role_rst`` for those.
    """
    if len(_ENTRY_POINT_HEADING_RE.findall(rst)) != 1:
        return rst
    stripped = _ENTRY_POINT_HEADING_RE.sub("", rst, count=1)
    # Promote both former H3 (^^^) and former H4 (~~~) up one level so the
    # doc ends up with a clean H1 / H2-only structure.
    stripped = _promote_underline(stripped, "^", "-")
    stripped = _promote_underline(stripped, "~", "-")
    return stripped


def _transform_role_rst(text: str, role_name: str) -> str:
    """Apply all post-processing transforms to one role's antsibull RST."""
    text = _rewrite_title(text, role_name)
    text = _strip_collection_note(text, role_name)
    text = _strip_local_contents(text, role_name)
    # _flatten_single_entrypoint is intentionally silent for multi-entrypoint
    # roles, so we don't route it through _sub_expected.
    text = _flatten_single_entrypoint(text)
    return text


def _publish_generated(rst_dir: Path, target_dir: Path) -> list[str]:
    """Copy role RST files from antsibull output into the Sphinx source tree.

    Only files matching ``*_role.rst`` are published; antsibull's other
    output (index page, environment_variables page) would collide with our
    own toctree structure. Returns the list of published RST basenames
    (without extension) so the caller can log what was produced.
    """
    target_dir.mkdir(parents=True, exist_ok=True)

    # Clean any previously-published role RST so removed roles don't linger.
    # Scoped narrowly to ``*_role.rst`` on purpose: ``target_dir`` also
    # contains the hand-authored ``index.md`` that owns the toctree.
    for stale in target_dir.glob("*_role.rst"):
        stale.unlink()

    published: list[str] = []
    for src in sorted(rst_dir.glob("*_role.rst")):
        role_name = src.stem.removesuffix("_role")
        transformed = _transform_role_rst(
            src.read_text(encoding="utf-8"), role_name
        )
        (target_dir / src.name).write_text(transformed, encoding="utf-8")
        published.append(src.stem)
    return published


_TOCTREE_RE = re.compile(
    r"(```\{toctree\}\n"   # opening fence
    r":maxdepth: \d+\n"    # maxdepth option
    r"\n"                   # blank line before entries
    r")"                    # capture group ends here
    r".*?"                  # existing entries (non-greedy)
    r"(\n```)",             # closing fence
    re.DOTALL,
)


def _update_toctree(target_dir: Path, published: list[str]) -> None:
    """Rewrite the toctree in ``docs/roles/index.md`` to match ``published``.

    The header prose above the toctree is preserved; only the list of role
    entries inside the ``{toctree}`` fence is replaced.  If the file or
    toctree block is missing, a minimal ``index.md`` is created from scratch.
    """
    index_file = target_dir / "index.md"
    header = (
        "# Roles\n"
        "\n"
        "Reference documentation for local Ansible roles in the `roles/` directory.\n"
        "Pages listed below are generated by\n"
        "[antsibull-docs](https://ansible.readthedocs.io/projects/antsibull-docs/) from\n"
        "each role's `meta/argument_specs.yml` file; the generator lives at\n"
        "`docs/_ext/role_docs.py` and runs during every documentation build.\n"
        "\n"
        "Only roles that opt in by providing an `argument_specs.yml` appear here.\n"
    )

    entries = "\n".join(f"{name}" for name in sorted(published))
    toctree_block = (
        "```{toctree}\n"
        ":maxdepth: 1\n"
        "\n"
        f"{entries}\n"
        "```\n"
    )

    if index_file.exists():
        text = index_file.read_text(encoding="utf-8")
        new_text, count = _TOCTREE_RE.subn(
            r"\g<1>" + entries + r"\g<2>",
            text,
            count=1,
        )
        if count == 0:
            # toctree block not found — append to end of file
            new_text = text.rstrip() + "\n\n" + toctree_block
    else:
        new_text = header + "\n" + toctree_block

    index_file.write_text(new_text, encoding="utf-8")


def _generate(app: Sphinx) -> None:
    repo_root = Path(app.srcdir).parent  # docs/ -> repo root
    roles_dir = repo_root / "roles"

    roles = _find_roles_with_argument_specs(roles_dir)
    if not roles:
        logger.info(
            "role_docs: no roles with meta/argument_specs.yml found; "
            "nothing to generate."
        )
        return

    shim_root = Path(app.srcdir) / "_antsibull"
    rst_dir = shim_root / "rst"
    target_dir = Path(app.srcdir) / "roles"

    try:
        collections_search_path = _build_shim(shim_root, roles)
        _run_antsibull(collections_search_path, rst_dir)
        published = _publish_generated(rst_dir, target_dir)
        _update_toctree(target_dir, published)
    except FileNotFoundError as exc:
        logger.warning(
            "role_docs: antsibull-docs CLI not found (%s); "
            "role reference pages will be missing from this build.",
            exc,
        )
        return
    except subprocess.CalledProcessError as exc:
        # ``capture_output=True`` above means the failure detail is in
        # exc.stderr; surface it so build logs are actionable.
        logger.warning(
            "role_docs: antsibull-docs failed (exit %s): %s",
            exc.returncode,
            exc.stderr.strip() if exc.stderr else exc,
        )
        return

    logger.info(
        "role_docs: generated %d role page(s): %s",
        len(published),
        ", ".join(published) or "(none)",
    )


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("builder-inited", _generate)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
