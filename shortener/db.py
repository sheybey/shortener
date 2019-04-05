from importlib import import_module

from flask import g, current_app


class DatabaseConnection:
    """Thin DBAPI wrapper."""

    def __init__(self, dbapi, **kwargs):
        """Establishes a database connection."""
        dbapi = import_module(dbapi)
        self.connection = dbapi.connect(**kwargs)
        self.connection.autocommit(False)

        for name in [
            'InterfaceError',
            'DatabaseError',
            'DataError',
            'OperationalError',
            'IntegrityError',
            'InternalError',
            'ProgrammingError',
            'NotSupportedError'
        ]:
            setattr(self, name, getattr(dbapi, name))

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
            key[3:].lower(): current_app.config[key]
            for key in current_app.config
            if key.startswith('DB_')
        }
        db = g.db = DatabaseConnection(current_app.config['DBAPI'], **kwargs)
    return db
