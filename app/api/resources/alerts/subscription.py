from flask import request
from flask_restful import Resource
from ...models import Subscriptions

class Subscription(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        result = Subscriptions.create_new_subscriber(email)
        return result, 201

    def put(self, id):
        subscription = Subscriptions.query.get(id)
        
        if not subscription:
            return { 'error': 'Subscription not found'}, 404
        
        data = request.get_json()
        new_email = data.get('email')
        
        if new_email:
            result = subscription.update_email(new_email)
            return result, 200
        else:
            return { 'error': 'New email is required'}, 400
        
    def delete(self, id):
        result = Subscriptions.delete_subscriber(id)
        
        if result:
            return '', 204
        else: 
            return { 'error': 'Subscription not found'}, 404

