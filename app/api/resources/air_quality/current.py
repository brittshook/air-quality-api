from flask_restful import Resource
from ...models.air_quality_data import AirQualityData

class Current(Resource):
    def get(self):
        return AirQualityData.get_current(), 200