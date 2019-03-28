from click import echo, argument, pass_context
from steam.steamid import SteamID
from steam.enums.common import EType

from . import app
from .db import get_db
from .util import resolve_steam_names, string_to_steamid


@app.cli.group('db')
def database_group():
    """Database commands."""
    pass


@database_group.command('create')
def create_tables():
    """Create database tables."""
    with app.open_resource('sql/schema.sql', 'r') as file:
        with get_db() as cursor:
            cursor.execute(file.read())


@database_group.command('drop')
def drop_tables():
    """Drop database tables."""
    with app.open_resource('sql/drop.sql', 'r') as file:
        with get_db() as cursor:
            cursor.execute(file.read())


@database_group.command('seed')
def seed_data():
    """Insert seed data."""
    id64s = [76561198018347228, 76561198013023668]
    response = resolve_steam_names(id64s)

    with get_db() as cursor:
        statement = 'INSERT INTO `users` (`id`, `name`) VALUES(%s, %s)'
        cursor.executemany(
            statement,
            ((id64, response.get(id64)) for id64 in id64s)
        )


@app.cli.group('user')
def user_group():
    """User commands."""
    pass


@user_group.command('list')
def list_users():
    """List users."""
    cursor = get_db().cursor()
    cursor.execute('SELECT `id`, `name` FROM `users`')
    for id64, name in cursor.fetchall():
        print(id64, name or '<no name>', sep='\t')
    cursor.close()


@user_group.command('create')
@argument('id', metavar='<ID | URL>')
@pass_context
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


@user_group.command('delete')
@argument('id64', type=int, metavar='STEAMID64')
@pass_context
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


@app.cli.group('link')
def link_group():
    """Link commands."""
    pass


@link_group.command('list')
def list_links():
    """List links."""
    cursor = get_db().cursor()
    cursor.execute('SELECT `key`, `target` FROM `links`')
    links = list(cursor.fetchall())
    cursor.close()

    key_header = 'Key'
    target_header = 'Target'

    key_len = max(len(key_header), max(len(link[0]) for link in links))

    print(key_header.ljust(key_len), '|', target_header)
    print('-' * (key_len + len(target_header) + 3))
    for key, target in links:
        print(key.ljust(key_len), '|', target)


@link_group.command('create')
@argument('key')
@argument('target')
@pass_context
def create_link(ctx, key, target):
    """Create a link KEY -> TARGET."""
    try:
        with get_db() as cursor:
            cursor.execute(
                'INSERT INTO `links` (`key`, `target`) VALUES(%s, %s)',
                (key, target)
            )
    except MySQLdb.IntegrityError:
        echo('link "' + key + '" already exists')
        ctx.exit(1)
    except MySQLdb.DataError as e:
        echo('invalid link: ' + str(e.args[1]))
        ctx.exit(1)

    echo('added "' + key + '" -> "' + target + '"')


@link_group.command('delete')
@argument('key')
@pass_context
def delete_link(ctx, key):
    """Delete a link."""
    db = get_db()

    cursor = db.cursor()
    cursor.execute('SELECT `id`, `key` FROM `links` WHERE `key`=%s', (key,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        echo('no such link ' + key)
        ctx.exit(1)

    with db as cursor:
        cursor.execute('DELETE FROM `links` WHERE `id`=%s', (result[0],))

    echo('deleted link "' + result[1] + '"')
