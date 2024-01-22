from flask import request
from flask_restful import Resource
from ...models.air_quality_data import AirQualityData
from datetime import datetime

class History(Resource):
    def get(self):
        start = request.args.get('start')
        end = request.args.get('end')
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        
        if start and end:
            start = datetime.fromisoformat(start)
            end = datetime.fromisoformat(end)
        
        historical_data = AirQualityData.get_history(start=start, end=end, limit=limit, offset=offset)

        return {'historical_data': historical_data}, 200