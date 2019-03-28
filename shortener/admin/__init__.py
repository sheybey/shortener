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



def register_to(app):
    openid.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(blueprint)
    register_commands(app.cli)
