#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Cathleen Li'
SITENAME = u'cathleen.li'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['writing','about']
ARTICLE_PATHS = ['writing']
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{slug}.html'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Github', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github', 'http://github.com/catli'),
          ('linkedin', 'http://www.linkedin.com/in/cathleenli'),
          ('twitter', 'http://twitter.com/catlichatter'))

DEFAULT_PAGINATION = False


THEME = 'pelican-blueidea' 
THEME_STATIC_PATHS = ['static']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
