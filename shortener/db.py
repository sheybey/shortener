import MySQLdb
from flask import g, current_app


class DatabaseConnection:
    """Thin DBAPI wrapper."""

    def __init__(self, connect=MySQLdb.connect, **kwargs):
        """Establishes a database connection."""

        for key in list(kwargs.keys()):
            if kwargs[key] is None:
                del kwargs[key]

        self.connection = connect(**kwargs)
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
        kwargs = {
            'host': current_app.config['MYSQL_HOST'],
            'user': current_app.config['MYSQL_USER'],
            'passwd': current_app.config['MYSQL_PASSWORD'],
            'db': current_app.config['MYSQL_DATABASE'],
            'port': current_app.config['MYSQL_PORT'],
            'use_unicode': True,
            'charset': 'utf8mb4'
        }
        db = g.db = DatabaseConnection(**kwargs)
    return db
