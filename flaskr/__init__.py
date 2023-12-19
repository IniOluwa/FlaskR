# Import Dependencies
import os
from flask import Flask
from os import environ

# Import Modules
from . import db, auth


# Create & Configure Flask App
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = environ.get('SECRET_KEY'),
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    
    # Load Instance Config If It Exits, When Not Testing
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load Test Config If Available
        app.config.from_mapping(test_config)
        
    # Make Sure Instance Folder Exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # Say Hello
    @app.route('/hello')
    def hello():
        return "Hello, World!"
        
    # Register Database With Application
    db.init_app(app)
    
    # Register Authentication Blueprint
    app.register_blueprint(auth.bp)
        
    # Return Created Application
    return app
