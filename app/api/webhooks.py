from flask import Blueprint, request, jsonify
import traceback
from app.api.models.air_quality_data import AirQualityData 
from app.api.models.system_status import SystemStatus 
from app.api.models.subscriptions import Subscriptions 
from app.api.models.error_log import ErrorLog
from app.api.models.db import db
from app.utils.email_utils import process_alert
from settings import config

webhooks_bp = Blueprint('webhooks', __name__, url_prefix='/webhook/v1')

@webhooks_bp.route('/data', methods=['POST'])
def handle_data_webhook():
    api_key = request.headers.get('x-api-key')

    valid_api_key = config["admin_api_key"]

    if api_key != valid_api_key:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    timestamp = data.get('timestamp')
    pm2_5 = float(data.get('pm2_5'))
    pm10 = float(data.get('pm10'))
    status = data.get('status')
    sensor_connected = data.get('sensor_connected')
    cpu_usage_percent = float(data.get('cpu_usage'))
    memory_usage_percent = float(data.get('memory_usage'))

    air_quality_data = AirQualityData(timestamp=timestamp, pm2_5=pm2_5, pm10=pm10)
    aqi = air_quality_data.calculate_aqi()
    
    system_status_data = SystemStatus(timestamp=timestamp, status=status, sensor_connected=sensor_connected, cpu_usage_percent=cpu_usage_percent, memory_usage_percent=memory_usage_percent)
    
    subscriptions = Subscriptions.query.all()

    for subscription in subscriptions:
        try:
            process_alert(subscription, 'pm2_5', pm2_5, subscription.pm2_5_threshold)
            process_alert(subscription, 'pm10', pm10, subscription.pm10_threshold)
            process_alert(subscription, 'aqi', aqi, subscription.aqi_threshold)
        except Exception as e:
            error_log = ErrorLog(error_type='Alert Processing Error', error_message=str(e), traceback=traceback.format_exc())
            db.session.add(error_log)
            db.session.commit()

    try:
        db.session.add(air_quality_data)
        db.session.add(system_status_data)
        db.session.commit()
        
        return jsonify({"message": "Data webhook received and processed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        error_log = ErrorLog(error_type='Data Receiving Error', error_message=str(e), traceback=traceback.format_exc())
        print(e)
        db.session.add(error_log)
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
