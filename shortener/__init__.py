from getpass import getuser
from os import path
from importlib import import_module

from flask import Flask, g


class DefaultConfiguration:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = getuser()
    MYSQL_PASSWORD = None
    MYSQL_DATABASE = 'shortener'
    MYSQL_PORT = None
    ENABLE_ADMIN = False


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DefaultConfiguration)
app.config.from_pyfile('shortener.cfg')

if 'DEFAULT_REDIRECT' not in app.config:
    raise ValueError('Missing default redirect')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


view = import_module('shortener.views')
cli = import_module('shortener.cli')

if app.config['ENABLE_ADMIN']:
    admin = import_module('shortener.admin')
    admin.register_to(app)
