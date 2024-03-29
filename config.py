# -*- Mode: Python; coding: utf-8 -*-
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

ADMINS = ''

SECRET_KEY = 'SECRET_KEY_FOR_SESSION_SIGNING'

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'banco.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

DATABASE_CONNECT_OPTION = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True

CSRF_SESSION_KEY = 'SOMETHING_IMPOSSIBLE_TO_GUEES'

FLASK_ADMIN_SWATCH = 'cerulean'

TEMPLATES_AUTO_RELOAD = True