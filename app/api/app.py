from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import config
from models import db

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)
    register_resources(api)

    return app

def register_resources(api):
    # import resources
    # api.add_resource(YourResource1, '/resource1')