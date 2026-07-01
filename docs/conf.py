# Sphinx configuration for cdh-ansible documentation.
# Docs: https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

# -- Project information -----------------------------------------------------
project = "CDH Ansible"
author = "Princeton CDH"
copyright = "Princeton University"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinxcontrib.mermaid",
]

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
    "Thumbs.db",
    ".DS_Store",
]

# -- HTML output -------------------------------------------------------------
html_theme = "furo"
html_title = "CDH Ansible"
html_static_path: list[str] = []  # add "_static" here if we introduce assets

# Silence warnings for external anchors we don't control.
suppress_warnings = ["myst.header"]
