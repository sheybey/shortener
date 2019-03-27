from . import app
from .db import get_db


@app.route('/', defaults={'path': None})
@app.route('/<path:path>')
def lookup_redirect(path):
    if not path:
        return redirect(app.config['DEFAULT_REDIRECT'])

    cursor = get_db().cursor()
    cursor.execute('SELECT `target` FROM `links` WHERE `key`=%s', (path,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return redirect(app.config['DEFAULT_REDIRECT'])
    return redirect(result[0])
