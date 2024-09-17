# __init__.py
"""Initialize Flask app."""
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)
    # app.config.from_object("config.Config")
    
    # TODO: should look like yours
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://johnwelkener:Luge12345@localhost:5432/instabible')
    
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    

    # Initialize Database Plugin
    # db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes

        # db.create_all()  # Create database tables for our data models

        return app
    