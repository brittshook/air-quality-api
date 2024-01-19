from flask_restful import Resource
from ...models import AirQualityData

class Current(Resource):
    def get(self):
        return AirQualityData.get_current()