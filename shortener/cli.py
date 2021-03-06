from click import echo, argument, pass_context

from . import app
from .db import get_db


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
    db = get_db()
    try:
        with db as cursor:
            cursor.execute(
                'INSERT INTO `links` (`key`, `target`) VALUES(%s, %s)',
                (key, target)
            )
    except db.IntegrityError:
        echo('link "' + key + '" already exists')
        ctx.exit(1)
    except db.DataError as e:
        echo('invalid link: ' + str(e.args[1]))
        ctx.exit(1)

    echo('added "' + key + '" -> "' + target + '"')


@link_group.command('delete')
@argument('key')
@pass_context
def delete_link(ctx, key):
    """Delete a link."""
    with get_db() as cursor:
        cursor.execute('DELETE FROM `links` WHERE `key`=%s', (key,))
        if cursor.rowcount != 1:
            echo('no such link ' + key)
            ctx.exit(1)

    echo('deleted link "' + key + '"')
