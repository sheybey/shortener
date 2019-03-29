from flask import redirect, abort

from . import app
from .db import get_db


@app.route('/', defaults={'path': None})
@app.route('/<path:path>')
def lookup_redirect(path):
    if not path:
        return redirect(app.config['DEFAULT_REDIRECT'])

    if (
        (app.config['IGNORE_FAVICON'] and path == 'favicon.ico')
        or (app.config['IGNORE_ROBOTS'] and path == 'robots.txt')
    ):
        abort(404)

    cursor = get_db().cursor()
    cursor.execute('SELECT `target` FROM `links` WHERE `key`=%s', (path,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return redirect(app.config['DEFAULT_REDIRECT'])
    return redirect(result[0])
