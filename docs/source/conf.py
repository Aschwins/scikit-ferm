# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


project = "scikit-ferm"
copyright = "2025, Aschwin Schilperoort"
author = "Aschwin Schilperoort"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.duration",
              "sphinx.ext.autodoc",
              "sphinx.ext.viewcode",
              "sphinx.ext.napoleon",
              "sphinx.ext.intersphinx",
              "sphinx.ext.autosummary",
              "sphinx_design"
              ]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_favicon = "_static/favicon.ico"
html_css_files = [
    "custom.css",
]

html_theme_options = {
    "github_url": "https://github.com/aschwins/scikit-ferm",
    "navbar_end": ["navbar-icon-links.html"],
    "show_toc_level": 2,
    "navigation_depth": 2,
}

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'imported-members': False
}
add_module_names = False
autosummary_generate = True

# -- Napoleon configuration --------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# -- Intersphinx configuration ------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
}
suppress_warnings = ['autodoc.imported_members', 'ref.footnote']
