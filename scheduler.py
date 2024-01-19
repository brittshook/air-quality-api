import schedule
import time
from app.utils.email_utils import send_alert_email
from app.api.models import Subscriptions, AirQualityData
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def monitor_and_send_alerts():
    try:
        subscriptions = Subscriptions.query.all()
        latest_air_quality_data = AirQualityData.query.order_by(AirQualityData.timestamp.desc()).first()
            
        if latest_air_quality_data:
            current_pm2_5 = latest_air_quality_data.pm2_5
            current_pm10 = latest_air_quality_data.pm10
            current_aqi = latest_air_quality_data.aqi.aqi

            for subscription in subscriptions:
                pm2_5_threshold = subscription.pm2_5_threshold
                pm10_threshold = subscription.pm10_threshold
                aqi_threshold = subscription.aqi_threshold
                
                if current_pm2_5 > pm2_5_threshold:
                    if not subscription.alert_sent('pm2_5'):
                        send_alert_email(subscription.email, 'alert_message', 'PM2.5', pm2_5_threshold, current_pm2_5)
                        subscription.set_alert_sent('pm2_5', True)
                        db.session.commit()
                elif current_pm2_5 <= pm2_5_threshold:
                    if subscription.alert_sent('pm2_5'):
                        send_alert_email(subscription.email, 'clear_alert_message', 'PM2.5', pm2_5_threshold, current_pm2_5)
                        subscription.set_alert_sent('pm2_5', False)
                        db.session.commit()

                if current_pm10 > pm10_threshold:
                    if not subscription.alert_sent('pm10'):
                        send_alert_email(subscription.email, 'alert_message', 'PM10', pm10_threshold, current_pm10)
                        subscription.set_alert_sent('pm10', True)
                        db.session.commit()
                elif current_pm10 <= pm10_threshold:
                    if subscription.alert_sent('pm10'):
                        send_alert_email(subscription.email, 'clear_alert_message', 'PM10', pm10_threshold, current_pm10)
                        subscription.set_alert_sent('pm10', False)
                        db.session.commit()
                        
                if current_aqi > aqi_threshold:
                    if not subscription.alert_sent('aqi'):
                        send_alert_email(subscription.email, 'alert_message', 'AQI', aqi_threshold, current_aqi)
                        subscription.set_alert_sent('aqi', True)
                        db.session.commit()
                elif current_aqi <= aqi_threshold:
                    if subscription.alert_sent('aqi'):
                        send_alert_email(subscription.email, 'clear_alert_message', 'AQI', aqi_threshold, current_aqi)
                        subscription.set_alert_sent('aqi', False)
                        db.session.commit()
    except Exception as e:
        print(f'Error monitoring and sending alerts: {e}')
    finally:
        db.session.close()

schedule.every(15).minutes.do(monitor_and_send_alerts)

while True:
    schedule.run_pending()
    time.sleep(1)
