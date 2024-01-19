from flask import request
from flask_restful import Resource
from ...models import Subscriptions


class Thresholds(Resource):
    def put(self, id):
        subscription = Subscriptions.query.get(id)
        
        if not subscription:
            return { 'error': 'Subscription not found'}, 404
        
        data = request.get_json
        pm2_5_threshold = data.get('pm2_5_threshold')
        pm10_threshold = data.get('pm10_threshold')
        aqi_threshold = data.get('aqi_threshold')
                 
        if pm2_5_threshold or pm10_threshold or aqi_threshold:
            result = subscription.update_thresholds(pm2_5_threshold, pm10_threshold, aqi_threshold)
            if result: 
                return result, 201
        else:
            return { 'error': 'At least one threshold value is required'}, 400