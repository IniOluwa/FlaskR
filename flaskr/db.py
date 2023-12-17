# Import Dependencies
import sqlite
import click
from flask import current_app, g


# Get / Open Database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        
    # Return Database
    return g.db
    
# Close Database
def close_db():
    db = g.pop('db', None)
    
    if db is not None:
        db.close()
    
# Initialize Database
def init_db():
    db = get_db
    
    with current_app.open_resource as app_db:
        db.executescript(app_db.read().decode('utf8'))
        
# Database Initialization Command / Clear Existing Data and Create New Tables
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database Initialized.')
    
# Register DB Functions With Application
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
