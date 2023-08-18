# Configuration file for the Sphinx documentation builder.


# -- Path setup --------------------------------------------------------------

import os
import sys
from pathlib import Path
from typing import Any, Dict

import pydata_sphinx_theme
from sphinx.application import Sphinx

sys.path.insert(0, os.path.abspath("../"))


# -- Project information -----------------------------------------------------

project = "igotnews"
copyright = "2023, mraniki"
author = "mraniki"
language = "en"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "hoverxref.extension",
    "sphinx.ext.extlinks",
    "sphinx_design",
    "myst_parser",
    "sphinx_copybutton",
    "notfound.extension",
    # "autoapi.extension",
]

# -- Extension configuration ---------------------------------------------------

# -- intersphinx ------------

intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    # - :doc:`sphinx:usage/extensions/intersphinx`
    "dynaconf": ("https://www.dynaconf.com", None),
    "python": ("https://docs.python.org/3", None),
    "talky": ("https://talky.readthedocs.io/en/latest", None),
    "talky-dev": ("https://talky.readthedocs.io/en/dev/", None),
    "findmyorder": ("https://findmyorder.readthedocs.io/en/latest", None),
    "dxsp": ("https://dxsp.readthedocs.io/en/latest", None),
    "iamlistening": ("https://iamlistening.readthedocs.io/en/latest", None),
    "talkytrend": ("https://talkytrend.readthedocs.io/en/latest", None),
    "myllm": ("https://myllm.readthedocs.io/en/latest", None),
    "community": ("https://tt-plugins.readthedocs.io/en/latest", None),
}

intersphinx_disabled_reftypes = ["*"]


# -- hoverxref ----------------

hoverxref_intersphinx = [
    "readthedocs",
    "sphinx",
    "python",
    "talky",
    "findmyorder",
    "dxsp",
    "iamlistening",
    "talkytrend",
    "myllm",
]

# -- autodoc --------------------

autoclass_content = "both"
autodoc_inherit_docstrings = True
set_type_checking_flag = True
autodoc_member_order = "bysource"
add_module_names = True

# -- autoapi -------------------

# autoapi_type = "python"
# autoapi_dirs = ['../iamlistening']
# autoapi_keep_files = True
# autoapi_root = "api"
# autoapi_member_order = "groupwise"


# -- napoleon -------------------

napoleon_google_docstring = True

# -- MyST options -----------------

# This allows us to use ::: to denote directives, useful for admonitions
myst_enable_extensions = ["colon_fence", "linkify", "substitution"]
myst_heading_anchors = 2
myst_substitutions = {"rtd": "[Read the Docs](https://readthedocs.org/)"}

master_doc = "index"
source_suffix = [".rst", ".md"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Sitemap ----------------------

# ReadTheDocs has its own way of generating sitemaps, etc.
if not os.environ.get("READTHEDOCS"):
    extensions += ["sphinx_sitemap"]

    html_baseurl = os.environ.get("SITEMAP_URL_BASE", "http://127.0.0.1:8000/")
    sitemap_locales = [None]
    sitemap_url_scheme = "{link}"


# -- Options for HTML output --------

html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = "_static/logo.png"
html_favicon = "_static/favicon.ico"
html_show_sphinx = False
html_show_copyright = False
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "secondary_sidebar_items": ["page-toc"],
    "logo": {
        "link": "https://talky.readthedocs.io",
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/mraniki/tt/",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
        {
            "name": "Telegram",
            "url": "https://t.me/TTTalkyTraderChat/1",
            "icon": "fa-brands fa-telegram",
        },
        {
            "name": "Mastodon",
            "url": "https://mastodon.social/@MrAniki",
            "icon": "fa-brands fa-mastodon",
        },
        {
            "name": "Tips",
            "url": "https://coindrop.to/mraniki",
            "icon": "fa-solid fa-burger",
        },
    ],
}
html_context = {
    "default_mode": "dark",
}
