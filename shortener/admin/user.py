from flask_login import UserMixin

from . import login_manager
from ..db import get_db


class User(UserMixin):
    def __init__(self, id):
        cursor = get_db().cursor()
        cursor.execute('SELECT `name` FROM `users` WHERE `id`=%s', (id,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            raise ValueError('No such user', id)

        self.id = id
        self.name = result[0]


@login_manager.user_loader
def user_loader(id):
    try:
        return User(int(id))
    except ValueError:
        return None
    