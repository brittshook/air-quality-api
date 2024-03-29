from flask import Flask, jsonify, request
from flask_restful import Api
from settings import config
from .models.db import db
from .resources.alerts.subscription import CreateSubscription, ManageSubscription
from .resources.alerts.thresholds import Thresholds
from .resources.air_quality.current import Current
from .resources.air_quality.history import History
from .resources.air_quality.pm2_5 import PM2_5
from .resources.air_quality.pm10 import PM10
from .resources.air_quality.aqi import AQI
from .resources.status import Status
from .webhooks import webhooks_bp

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = config['database_url']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    @app.before_request
    def handle_not_found():
        request.not_found_error = False
            
    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return jsonify({"error": str(e)}), 400
    
    @app.errorhandler(404)
    def handle_not_found_error(e):
        request.not_found_error = True
        return jsonify({'error': 'Resource not found'}), 404

    api = Api(app)
    register_resources(api)
    app.register_blueprint(webhooks_bp)

    return app

def register_resources(api):
    api_base_uri = '/api'
    version = '/v1'
    
    api.add_resource(CreateSubscription, f'{api_base_uri}{version}/alerts')
    api.add_resource(ManageSubscription, f'{api_base_uri}{version}/alerts/<string:id>')
    api.add_resource(Thresholds, f'{api_base_uri}{version}/alerts/thresholds/<string:id>')
    api.add_resource(Current, f'{api_base_uri}{version}/current')
    api.add_resource(History, f'{api_base_uri}{version}/history')
    api.add_resource(PM2_5, f'{api_base_uri}{version}/pm2_5')
    api.add_resource(PM10, f'{api_base_uri}{version}/pm10')
    api.add_resource(AQI, f'{api_base_uri}{version}/aqi')
    api.add_resource(Status, f'{api_base_uri}{version}/status')
   
if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)