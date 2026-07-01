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
    # Local extension: generates docs/inventory.generated.md from inventory/.
    "inventory_docs",
]

# DataTables options applied to every ``.sphinx-datatable`` table on the site.
# Reference: https://datatables.net/reference/option
datatables_options = {
    "paging": False,       # inventory is small; show everything
    "info": False,         # hide "Showing X of Y" footer
    "order": [],           # respect the source order until the user sorts
}

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
    "Thumbs.db",
    ".DS_Store",
]

# -- HTML output -------------------------------------------------------------
html_theme = "furo"
html_title = "CDH Ansible"
html_static_path: list[str] = []  # add "_static" here if we introduce assets

# Silence warnings for external anchors we don't control.
suppress_warnings = ["myst.header"]
