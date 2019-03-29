# Shortener

A simple Flask-based link shortener with an optional admin interface.

## Usage

This is your standard flask app. Customize the sample configuration and deploy
it like any other.

## Design decisions

The resolver is designed to run as quickly as possible. If the admin interface
isn't enabled, it's never loaded in the first place.

### Why no SQLAlchemy?

The schema is extremely simple; a full-blown ORM would simply be overkill.
Since the primary objective is a fast resolver, the dependencies are
deliberately as barebones as possible.
