# Sphinx configuration for cdh-ansible documentation.
# Docs: https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

import sys
from pathlib import Path

# Make local extensions in docs/_ext/ importable.
sys.path.insert(0, str(Path(__file__).parent / "_ext"))

# -- Project information -----------------------------------------------------
project = "CDH Ansible"
author = "Princeton CDH"
copyright = "Princeton University"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinxcontrib.mermaid",
    # sphinx-datatables requires sphinxcontrib.jquery (jQuery is loaded on
    # pages that use the .sphinx-datatable class).
    "sphinxcontrib.jquery",
    "sphinx_datatables",
    # Ansible-specific RST roles/directives (``ansible-option-*``, ``O(...)``
    # cross-references, etc.) used by antsibull-docs generated pages.
    "sphinx_antsibull_ext",
    # Local extension: generates docs/inventory.md from inventory/.
    "inventory_docs",
    # Local extension: shims selected roles into a collection layout and
    # runs antsibull-docs to generate per-role RST.
    "role_docs",
]

# DataTables options applied to every ``.sphinx-datatable`` table on the site.
# Reference: https://datatables.net/reference/option
datatables_options = {
    "paging": False,       # inventory is small; show everything
    "info": False,         # hide "Showing X of Y" footer
    "order": [],           # respect the source order until the user sorts
}

# antsibull-docs default option-table CSS is light-only. ``default-autodark``
# ships both light and dark palettes and swaps between them via
# ``@media (prefers-color-scheme: dark)``. Furo's manual theme toggle uses
# ``data-theme`` attributes and is not covered here — visitors who flip the
# toggle against their OS preference will see the wrong palette. Acceptable
# trade-off for a small doc site; revisit with a custom CSS override if
# multiple readers hit it.
antsibull_ext_color_scheme = "default-autodark"

# Treat Markdown as the primary source format.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# MyST features we want available in prose docs.
myst_enable_extensions = [
    "colon_fence",     # ::: fenced directives, easier than ```{directive}
    "deflist",
    "linkify",         # bare URLs become links
    "substitution",
    "tasklist",
]
myst_heading_anchors = 3  # auto-generate slug anchors for h1-h3

# Treat ```mermaid fenced blocks as the mermaid directive so diagrams render
# without changing the Markdown source (which stays GitHub-compatible).
myst_fence_as_directive = ["mermaid"]

# Files/dirs to exclude from the doc build.
exclude_patterns = [
    "_build",
    "_ext",
    # antsibull-docs shim tree + intermediate RST (see role_docs.py).
    # The published role RST files live under docs/roles/ and are picked up.
    "_antsibull",
    # ADR template is a copy source, not a decision record; hide it from
    # the built site while keeping it visible on GitHub.
    "adr/template.md",
    "Thumbs.db",
    ".DS_Store",
]

# -- HTML output -------------------------------------------------------------
html_theme = "furo"
html_title = "CDH Ansible"
html_static_path: list[str] = []  # add "_static" here if we introduce assets

# Silence warnings for external anchors we don't control.
suppress_warnings = ["myst.header"]
