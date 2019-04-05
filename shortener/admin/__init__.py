from importlib import import_module

from flask import Blueprint
from flask_openid import OpenID
from flask_login import LoginManager

from .cli import register_commands


openid = OpenID(stateless=True)
login_manager = LoginManager()

blueprint = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static'
)

views = import_module('.views', __name__)


def register_to(app, url_prefix='/admin'):
    if 'SECRET_KEY' not in app.config:
        raise ValueError('Missing secret key')

    openid.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    app.register_blueprint(blueprint, url_prefix=url_prefix)
    register_commands(app.cli)
