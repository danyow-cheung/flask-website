import sqlite3
import click
from flask import current_app,g
from flask.cli import with_appcontext

def connect_db():
    if 'db' not in g:
        g.db=sqlite3.connect("test.db",detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory =sqlite3.Row

    return g.db

def disconnect_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()

def make_db():
    db = connect_db()

    with current_app.open_resource('create_table.sql')as f:
        db.executescript(f.read().decode('utf8'))


@click.command('make-db')
@with_appcontext
def make_db_command():
    make_db()
    #click.echo('initilize database')

def init_app(app):
    app.teardown_appcontext(disconnect_db)
    app.cli.add_command(make_db_command)
