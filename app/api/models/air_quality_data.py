from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, event
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from .db import db
from .subscriptions import Subscriptions
from ...utils.aqi_utils import AQI_CATEGORIES
from ...utils.email_utils import process_alert

class AirQualityData(db.Model):
    timestamp = db.Column(db.TIMESTAMP, primary_key=True, default=db.func.current_timestamp())
    pm2_5 = db.Column(db.Numeric)
    pm10 = db.Column(db.Numeric)
    aqi = db.Column(db.JSON)

    def __repr__(self):
        return f'<AirQualityData(timestamp={self.timestamp}, pm2_5={self.pm2_5}, pm10={self.pm10}, aqi={self.aqi}, aqi_threshold={self.aqi_threshold})>'

    @classmethod
    def get_current(cls, indicator=None):
        latest_entry = AirQualityData.query.order_by(AirQualityData.timestamp.desc()).first()

        if not latest_entry:
            return {'error': 'No records available'}, 404

        if indicator:
            return {
                'timestamp': latest_entry.timestamp.isoformat(),
                indicator: getattr(latest_entry, indicator) if indicator == 'aqi' else float(getattr(latest_entry, indicator))
            }

        return {
            'timestamp': latest_entry.timestamp.isoformat(),
            'pm2_5': float(latest_entry.pm2_5),
            'pm10': float(latest_entry.pm10),
            'aqi': latest_entry.aqi
        }

    @classmethod
    def get_history(cls, indicator=None, start=None, end=None, limit=None, offset=None):
        limit = limit or 5000
        offset = offset or 0
        
        limit = int(limit)
        offset = int(offset)
        
        if limit < 1 or limit > 5000:
            raise ValueError(f"Limit must be between 1 and 5000.")
        
        if (start and not end) or (not start and end):
            raise ValueError("To filter results by specified time range, both start and end must be provided")

        if start and end and start > end:
            raise ValueError("Start time should be before or equal to end time.")
      
        if start and end:
            records = AirQualityData.query.filter(
                AirQualityData.timestamp.between(start, end)
            ).order_by(desc(AirQualityData.timestamp)).limit(limit).offset(offset).all()
        else:
            records = AirQualityData.query.order_by(desc(AirQualityData.timestamp)).limit(limit).offset(offset).all()
            
        if indicator:
            return [{'timestamp': entry.timestamp.isoformat(), 
                     indicator: getattr(entry, indicator) if indicator == 'aqi' else float(getattr(entry, indicator)) 
            } for entry in records]
        else:
            return [{
                'timestamp': entry.timestamp.isoformat(),
                'pm2_5': float(entry.pm2_5),
                'pm10': float(entry.pm10),
                'aqi': entry.aqi
            } for entry in records]
    
    def calculate_aqi(self):
        twelve_hours_ago = datetime.utcnow() - timedelta(hours=12)

        hourly_data = db.session.query(
            AirQualityData.timestamp,
            AirQualityData.pm2_5,
            AirQualityData.pm10
        ).filter(
            AirQualityData.timestamp >= twelve_hours_ago
        ).all()

        concentrations_pm2_5 = [float(data.pm2_5) for data in hourly_data]
        concentrations_pm10 = [float(data.pm10) for data in hourly_data]
        
        if not concentrations_pm2_5 or not concentrations_pm10:
            return None

        range_pm2_5 = max(concentrations_pm2_5) - min(concentrations_pm2_5)
        range_pm10 = max(concentrations_pm10) - min(concentrations_pm10)

        max_concentration_pm2_5 = max(concentrations_pm2_5)
        max_concentration_pm10 = max(concentrations_pm10)

        scaled_rate_pm2_5 = range_pm2_5 / max_concentration_pm2_5
        scaled_rate_pm10 = range_pm10 / max_concentration_pm10

        weight_factor_pm2_5 = max(1 - scaled_rate_pm2_5, 0.5)
        weight_factor_pm10 = max(1 - scaled_rate_pm10, 0.5)

        nowcast_pm2_5 = sum(
            (float(data.pm2_5) * (weight_factor_pm2_5 ** i)) for i, data in enumerate(hourly_data)
        ) / sum(weight_factor_pm2_5 ** i for i in range(len(hourly_data)))

        nowcast_pm10 = sum(
            (float(data.pm10) * (weight_factor_pm10 ** i)) for i, data in enumerate(hourly_data)
        ) / sum(weight_factor_pm10 ** i for i in range(len(hourly_data)))

        aqi = round(max(nowcast_pm2_5, nowcast_pm10)) if nowcast_pm2_5 and nowcast_pm10 else None
        
        if aqi:
            aqi_category = None
            aqi_description = None

            for category, values in AQI_CATEGORIES.items():
                if values['min'] <= aqi <= values['max']:
                    aqi_category = category
                    aqi_description = values['description']
                    break

            self.aqi = {'aqi': aqi, 'category': aqi_category, 'description': aqi_description}
            return aqi