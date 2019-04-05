from getpass import getuser
from importlib import import_module

from flask import Flask, g


class DefaultConfiguration:
    DBAPI = 'MySQLdb'
    DB_HOST = 'localhost'
    DB_USER = getuser()
    DB_DATABASE = 'shortener'
    DB_USE_UNICODE = True
    DB_CHARSET = 'utf8mb4'
    ENABLE_ADMIN = False
    IGNORE_FAVICON = True
    IGNORE_ROBOTS = True


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


views = import_module('.views', __name__)
cli = import_module('.cli', __name__)

if app.config['ENABLE_ADMIN']:
    admin = import_module('shortener.admin')
    admin.register_to(app)
