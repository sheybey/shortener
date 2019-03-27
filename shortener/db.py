import MySQLdb
from flask import g

from . import app


class DatabaseConnection:
    """Wraps a MySQLdb connection, using app.config."""

    def __init__(self):
        """Establishes a database connection.

        Connection details are read from app.config."""

        kwargs = {
            'host': app.config['MYSQL_HOST'],
            'user': app.config['MYSQL_USER'],
            'passwd': app.config['MYSQL_PASSWORD'],
            'db': app.config['MYSQL_DATABASE'],
            'port': app.config['MYSQL_PORT'],
            'use_unicode': True,
            'charset': 'utf8mb4'
        }

        for key in list(kwargs.keys()):
            if kwargs[key] is None:
                del kwargs[key]

        self.connection = MySQLdb.connect(**kwargs)
        self.connection.autocommit(False)

    def __enter__(self):
        """Context manager for a cursor object.

        Commits on exit. Raise an exception to cause a rollback."""

        self._cursor = self.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Commits the transaction if no exception is raised."""
        self._cursor.close()
        del self._cursor

        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()

    def cursor(self):
        """Return a cursor. The caller is responsible for closing it."""
        return self.connection.cursor()

    def close(self):
        """Close the connection."""
        self.connection.close()


def get_db():
    """Get the context database connection, opening it if necessary."""
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = DatabaseConnection()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
