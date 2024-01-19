from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from settings import config
from models import system_status as system_status_db, SystemStatus
from models import air_quality_data as air_quality_data_db, AirQualityData
from models import subscriptions as subscriptions_db, Subscriptions
from resources.alerts.subscription import Subscription
from resources.alerts.thresholds import Thresholds
from resources.air_quality.current import Current
from resources.air_quality.history import History
from resources.air_quality.pm2_5 import PM2_5
from resources.air_quality.pm10 import PM10
from resources.air_quality.aqi import AQI
from resources.status import Status

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config["db_user"]}:{config["db_password"]}@{config["db_host"]}:{config["db_port"]}/{config["db_database"]}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    system_status_db.init_app(app)
    air_quality_data_db.init_app(app)
    subscriptions_db.init_app(app)

    with app.app_context():
        system_status_db.create_all()
        air_quality_data_db.create_all()
        subscriptions_db.create_all()
        
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        response = jsonify({"error": str(error)})
        response.status_code = 400
        return response

    api = Api(app)
    register_resources(api)

    return app

def register_resources(api):
    api.add_resource(Subscription, '/api/v1/alerts/subscriptions', '/<string:id>')
    api.add_resource(Thresholds, '/api/v1/alerts/thresholds', '/<string:id>')
    api.add_resource(Current, '/api/v1/air_quality')
    api.add_resource(History, '/api/v1/air_quality/history')
    api.add_resource(PM2_5, '/api/v1/air_quality/pm2_5')
    api.add_resource(PM10, '/api/v1/air_quality/pm10')
    api.add_resource(AQI, '/api/v1/air_quality/aqi')
    api.add_resource(Status, '/api/v1/status')
