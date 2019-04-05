from itertools import chain

from flask import redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user, login_required

from . import blueprint, openid
from .user import User
from .forms import LinkForm, DeleteLinkForm
from ..db import get_db


@blueprint.route('/login')
@openid.loginhandler
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.links'))

    error = openid.fetch_error()
    if error:
        flash(error, 'error')

    return openid.try_login('https://steamcommunity.com/openid')


@openid.after_login
def after_login(response):
    id = response.identity_url.split('/')[-1]
    try:
        user = User(id)
        login_user(user)
        return redirect(url_for('.links'))
    except ValueError:
        return render_template('unauthorized.html', id=id)


@blueprint.route('/logout')
def logout():
    logout_user()
    return render_template('logged_out.html')


@blueprint.route('/')
@blueprint.route('/links')
@login_required
def links():
    cursor = get_db().cursor()
    cursor.execute('SELECT `id`, `key`, `target` FROM `links`')
    links = cursor.fetchall()
    cursor.close()
    return render_template(
        'links.html',
        links=(
            {'id': id, 'key': key, 'target': target}
            for id, key, target in links
        ),
        save_form=LinkForm(),
        delete_form=DeleteLinkForm()
    )


@blueprint.route('/users')
@login_required
def users():
    return 'users'


@blueprint.route('/links/new', methods=['POST'])
@login_required
def new_link():
    form = LinkForm()
    if form.validate():
        db = get_db()
        try:
            with db as cursor:
                cursor.execute(
                    'INSERT INTO `links` (`key`, `target`) VALUES (%s, %s)',
                    (form.key.data, form.target.data)
                )
            flash('Link "' + form.key.data + '" created', 'success')
        except db.IntegrityError:
            flash('Link "' + form.key.data + '" already exists', 'error')
    else:
        for error in chain.from_iterable(form.errors.values()):
            flash(error, 'error')

    return redirect(url_for('.links'))


@blueprint.route('/links/save/<int:id>', methods=['POST'])
@login_required
def save_link(id):
    form = LinkForm()
    if form.validate():
        with get_db() as cursor:
            cursor.execute(
                'UPDATE `links` SET `key`=%s, `target`=%s WHERE `id`=%s',
                (form.key.data, form.target.data, id)
            )
            if cursor.rowcount == 1:
                flash('Link "' + form.key.data + '" updated', 'success')
            else:
                flash('No such link', 'error')
    else:
        for error in chain.from_iterable(form.errors.values()):
            flash(error, 'error')

    return redirect(url_for('.links'))


@blueprint.route('/links/delete/<int:id>', methods=['POST'])
@login_required
def delete_link(id):
    if DeleteLinkForm().validate():
        db = get_db()
        with db as cursor:
            cursor.execute('DELETE FROM `links` WHERE `id`=%s', (id,))
            if cursor.rowcount != 1:
                flash('No such link', 'error')
            else:
                flash('Link deleted', 'success')
    else:
        for error in chain.from_iterable(form.errors.values()):
            flash(error, 'error')

    return redirect(url_for('.links'))
