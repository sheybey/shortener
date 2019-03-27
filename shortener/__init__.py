from getpass import getuser
from os import path
from importlib import import_module

from flask import Flask
from flask_openid import OpenID
from flask_login import LoginManager


class DefaultConfiguration:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = getuser()
    MYSQL_PASSWORD = None
    MYSQL_DATABASE = 'shortener'
    MYSQL_PORT = None


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DefaultConfiguration)
app.config.from_pyfile('shortener.cfg', silent=True)

for key in ['STEAM_API_KEY', 'DEFAULT_REDIRECT']:
    if key not in app.config:
        raise ValueError('Missing config key:', key)

openid = OpenID(app, stateless=True)
login_manager = LoginManager(app)

view = import_module('shortener.views')
cli = import_module('shortener.cli')
