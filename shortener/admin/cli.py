from click import echo, argument, pass_context

from shortener.db import get_db
from shortener.admin.util import resolve_steam_names, string_to_steamid


def list_users():
    """List users."""
    cursor = get_db().cursor()
    cursor.execute('SELECT `id`, `name` FROM `users`')
    for id64, name in cursor.fetchall():
        print(id64, name or '<no name>', sep='\t')
    cursor.close()



def create_user(ctx, id):
    """Create a user from Steam ID or custom URL."""
    steamid = string_to_steamid(id)
    if not steamid.is_valid():
        echo('invalid steam id')
        ctx.exit(1)
    if not steamid.type == EType.Individual:
        echo('steam id must be of type Individual')
        ctx.exit(1)

    id64 = steamid.as_64
    name = resolve_steam_names([id64]).get(id64)
    try:
        with get_db() as cursor:
            cursor.execute(
                'INSERT INTO `users` (`id`, `name`) VALUES(%s, %s)',
                (steamid, name)
            )
    except MySQLdb.IntegrityError:
        echo('user ' + str(id64) + ' already exists')
        ctx.exit(1)

    echo('added "' + (name or '<no name>') + '" ' + str(id64))


def delete_user(ctx, id64):
    """Delete a user by STEAMID64."""
    db = get_db()

    cursor = db.cursor()
    cursor.execute('SELECT `id`, `name` FROM `users` WHERE `id`=%s', (id64,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        echo('no such user ' + str(id64))
        ctx.exit(1)

    with db as cursor:
        cursor.execute('DELETE FROM `users` WHERE `id`=%s', (id64,))

    echo('deleted "' + result[1] + '" ' + str(id64))


def seed_users():
    """Insert seed users."""
    id64s = [76561198018347228, 76561198013023668]
    response = resolve_steam_names(id64s)

    with get_db() as cursor:
        statement = 'INSERT INTO `users` (`id`, `name`) VALUES(%s, %s)'
        cursor.executemany(
            statement,
            ((id64, response.get(id64)) for id64 in id64s)
        )


def register_commands(click):
    @click.group('user')
    def user_group():
        """User commands."""
        pass

    user_group.command('list')(list_users)

    user_group.command('create')(
        argument('id', metavar='<ID | URL>')(
            pass_context(create_user)
        )
    )

    user_group.command('delete')(
        argument('id64', type=int, metavar='STEAMID64')(
            pass_context(delete_user)
        )
    )

    user_group.command('seed')(seed_users)
