from flask_restful import Resource
from ..models import SystemStatus
from flask import jsonify

class Status(Resource):
    def get(self):
        latest_status = SystemStatus.query.order_by(SystemStatus.timestamp.desc()).first()

        if not latest_status:
            return {'error': 'No system status available'}, 404

        return {'system_status': latest_status.system_status()}