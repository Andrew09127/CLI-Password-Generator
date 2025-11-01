# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Добавляем путь к вашему проекту, чтобы Sphinx мог найти модули
sys.path.insert(0, os.path.abspath('..'))

project = 'CLI PASSWORD GENERATOR'
copyright = '2025, Andrew09127'
author = 'Andrew09127'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Добавляем необходимые расширения
extensions = [
    'sphinx.ext.autodoc',      # Автоматическая документация из docstrings
    'sphinx.ext.viewcode',     # Показывать исходный код
    'sphinx.ext.napoleon',     # Поддержка Google-style docstrings
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ru'

# -- Настройки для autodoc ---------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# -- Настройки для Napoleon (Google-style docstrings) ------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = None

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Меняем тему на более современную (опционально)
html_theme = 'sphinx_rtd_theme'  # Нужно установить: pip install sphinx-rtd-theme

# Если хотите оставить alabaster, раскомментируйте строку ниже:
# html_theme = 'alabaster'

html_static_path = ['_static']

# Дополнительные настройки для лучшего отображения
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True