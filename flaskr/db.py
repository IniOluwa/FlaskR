# Import Dependencies
import sqlite
import click
from flask import current_app, g


# Get / Open Database
def get():
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
