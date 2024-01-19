from flask_sqlalchemy import SQLAlchemy, func, event
from datetime import datetime, timedelta
from app.utils.aqi_utils import AQI_CATEGORIES

db = SQLAlchemy()

class AirQualityData(db.Model):
    timestamp = db.Column(db.TIMESTAMP, primary_key=True, default=db.func.current_timestamp())
    pm2_5 = db.Column(db.Numeric)
    pm10 = db.Column(db.Numeric)
    aqi = db.Column(db.JSON)

    def __repr__(self):
        return f'<AirQualityData(timestamp={self.timestamp}, pm2_5={self.pm2_5}, pm10={self.pm10}, aqi={self.aqi}, aqi_threshold={self.aqi_threshold})>'
    
    def calculate_aqi(self):
        twelve_hours_ago = datetime.utcnow() - timedelta(hours=12)

        hourly_data = db.session.query(
            AirQualityData.timestamp,
            AirQualityData.pm2_5,
            AirQualityData.pm10
        ).filter(
            AirQualityData.timestamp >= twelve_hours_ago
        ).all()

        concentrations_pm2_5 = [data.pm2_5 for data in hourly_data]
        concentrations_pm10 = [data.pm10 for data in hourly_data]

        range_pm2_5 = max(concentrations_pm2_5) - min(concentrations_pm2_5)
        range_pm10 = max(concentrations_pm10) - min(concentrations_pm10)

        max_concentration_pm2_5 = max(concentrations_pm2_5)
        max_concentration_pm10 = max(concentrations_pm10)

        scaled_rate_pm2_5 = range_pm2_5 / max_concentration_pm2_5
        scaled_rate_pm10 = range_pm10 / max_concentration_pm10

        weight_factor_pm2_5 = max(1 - scaled_rate_pm2_5, 0.5)
        weight_factor_pm10 = max(1 - scaled_rate_pm10, 0.5)

        nowcast_pm2_5 = sum(
            (data.pm2_5 * (weight_factor_pm2_5 ** i)) for i, data in enumerate(hourly_data)
        ) / sum(weight_factor_pm2_5 ** i for i in range(len(hourly_data)))

        nowcast_pm10 = sum(
            (data.pm10 * (weight_factor_pm10 ** i)) for i, data in enumerate(hourly_data)
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

            return {'aqi': aqi, 'category': aqi_category, 'description': aqi_description}
        return {'aqi': 'Unavailable'}

    @classmethod
    def get_current(cls, indicator=None):
        latest_entry = AirQualityData.query.order_by(AirQualityData.timestamp.desc()).first()

        if not latest_entry:
            raise ValueError("No records available.")

        if indicator:
            return [(latest_entry.timestamp, getattr(latest_entry, indicator))]

        return {
            'timestamp': latest_entry.timestamp,
            'pm2_5': latest_entry.pm2_5,
            'pm10': latest_entry.pm10,
            'aqi': latest_entry.aqi
            }

    @classmethod
    def get_history(cls, indicator=None, start=None, end=None):
        first_entry = AirQualityData.query.order_by(AirQualityData.timestamp.asc()).first()

        if not first_entry:
            raise ValueError("No records available.")

        if end and end < first_entry.timestamp:
            raise ValueError(f"End time occurs before the timestamp of the first record. End time must be equal to or after {first_entry.timestamp}")

        if start and end and start > end:
            raise ValueError("Start time should be before or equal to end time.")

        if start and end:
            records = AirQualityData.query.filter(
                AirQualityData.timestamp.between(start, end)
            ).all()
            return [(entry.timestamp, getattr(entry, indicator)) for entry in records] if indicator else records

        latest_entry = AirQualityData.query.order_by(AirQualityData.timestamp.desc()).first()
        return [(latest_entry.timestamp, getattr(latest_entry, indicator))] if indicator else {
            'timestamp': latest_entry.timestamp,
            'pm2_5': latest_entry.pm2_5,
            'pm10': latest_entry.pm10,
            'aqi': latest_entry.aqi
        }

@event.listens_for(AirQualityData, 'after_insert')    
def after_insert_listener(mapper, connection, target):
    target.calculate_aqi()