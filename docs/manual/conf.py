# -*- coding: utf-8 -*-
import sys, os

source_suffix = '.rst'
master_doc = 'index'
project = u'udis86'
copyright = u'2013, Vivek Thampi'
version = '1.7'
release = '1.7.1'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

pygments_style = 'sphinx'
html_theme = 'pyramid'
html_theme_options = { "nosidebar" : True }
html_static_path = ['static']
html_style = "udis86.css"
htmlhelp_basename = 'udis86doc'

latex_documents = [
  ('index', 'udis86.tex', u'udis86 Documentation',
   u'Vivek Thampi', 'manual'),
]

man_pages = [
    ('index', 'udis86', u'udis86 Documentation',
     [u'Vivek Thampi'], 1)
]

texinfo_documents = [
  ('index', 'udis86', u'udis86 Documentation',
   u'Vivek Thampi', 'udis86', 'Disassembler library for x86.',
   'Miscellaneous', True),
]
