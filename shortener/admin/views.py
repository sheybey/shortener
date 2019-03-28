from flask import redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user

from . import blueprint, login_manager, openid
from .user import User


@blueprint.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))

    return render_template('index.html')


@blueprint.route('/login')
@openid.loginhandler
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))

    error = openid.fetch_error()
    if error:
        flash(error, 'danger')

    return openid.try_login('https://steamcommunity.com/openid')


@openid.after_login
def after_login(response):
    id = response.identity_url.split('/')[-1]
    try:
        user = User(id)
        login_user(user)
        return redirect(url_for('.index'))
    except ValueError:
        return render_template('unauthorized.html', id=id)


@blueprint.route('/logout')
def logout():
    logout_user()
    return render_template('logged_out.html')
