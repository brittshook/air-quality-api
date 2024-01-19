from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from app.utils.aqi_utils import AQI_CATEGORIES

db = SQLAlchemy()

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
            raise ValueError("No records available.")

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