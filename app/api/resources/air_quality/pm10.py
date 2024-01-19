from flask import request
from flask_restful import Resource
from ...models.air_quality_data import AirQualityData
from datetime import datetime

class PM10(Resource):
    def get(self):
        start = request.args.get('start')
        end = request.args.get('end')
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        
        if (start and not end) or (not start and end):
            return {'error': 'To filter results by specified time range, both start and end must be provided'}, 400
        
        if start and end:
            start = datetime.fromisoformat(start)
            end = datetime.fromisoformat(end)
            data = AirQualityData.get_history(indicator='pm10', start=start, end=end, limit=limit, offset=offset)
        else:
            data = [AirQualityData.get_current(indicator='pm10')]
            
        return {'pm10': data}, 200