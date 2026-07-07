"""Sphinx extension: generate inventory CSV from ``inventory/``.

Parses ``inventory/all_hosts`` as INI at build time and writes
``docs/_inventory.csv``, which is consumed by the static
``docs/inventory.md`` via the ``csv-table`` directive's ``:file:`` option.
"""

from __future__ import annotations

import configparser
import csv
import io
from collections import defaultdict
from pathlib import Path
from typing import Any

from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)

_ENV_GROUPS = {"staging", "production", "prod", "dev"}


def _parse_inventory(path: Path) -> dict[str, set[str]]:
    parser = configparser.ConfigParser(allow_no_value=True, delimiters=("=",))
    parser.optionxform = str
    parser.read(path, encoding="utf-8")

    direct_hosts: dict[str, set[str]] = {}
    children: dict[str, set[str]] = defaultdict(set)

    for section in parser.sections():
        # [foo:children] indicates an ansible host group
        if section.endswith(":children"):
            # the name of the group is the section label before :children
            group = section[: -len(":children")]
            # add all entries to the set for this group
            children[group].update(parser.options(section))
        # otherwise, section is an ansible host group with hostnames
        else:
            direct_hosts.setdefault(section, set()).update(parser.options(section))

    resolved: dict[str, set[str]] = {}

    def _resolve(group: str, seen: set[str]) -> set[str]:
        if group in resolved:
            return resolved[group]
        if group in seen:
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
    # identify application host groups, based on the presence
    # of names that have _staging and _production subgroups
    apps: list[str] = []
    for name in groups:
        if name in _ENV_GROUPS:
            continue
        if name.endswith("_staging") or name.endswith("_production"):
            continue
        if f"{name}_staging" in groups or f"{name}_production" in groups:
            apps.append(name)
    return sorted(apps)


def _generate(app: Sphinx) -> None:
    repo_root = Path(app.srcdir).parent
    inventory_file = repo_root / "inventory" / "all_hosts"
    try:
        groups = _parse_inventory(inventory_file)
    except (OSError, configparser.Error) as exc:
        logger.warning(
            "inventory_docs: could not parse %s (%s); "
            "generating empty inventory CSV.",
            inventory_file,
            exc,
        )
        groups = {}

    inventory_csv = Path(app.srcdir) / "_inventory.csv"
    with inventory_csv.open("w") as inventory_csv_filehandle:
        writer = csv.writer(inventory_csv_filehandle)
        writer.writerow(["Application", "Staging hosts", "Production hosts"])
        for app_name in _app_groups(groups):
            staging = groups.get(f"{app_name}_staging", set())
            production = groups.get(f"{app_name}_production", set())
            writer.writerow([
                app_name,
                "<br>".join(f"``{h}``" for h in sorted(staging)) if staging else "—",
                "<br>".join(f"``{h}``" for h in sorted(production)) if production else "—",
            ])
    logger.info("inventory_docs: wrote %s", inventory_csv.relative_to(repo_root))


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("builder-inited", lambda a: _generate(a))
    return {
        "version": "0.5",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
