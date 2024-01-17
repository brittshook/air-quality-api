from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AirQualityData(db.Model):
    timestamp = db.Column(db.TIMESTAMP, primary_key=True, default=db.func.current_timestamp())
    pm2_5 = db.Column(db.Numeric)
    pm10 = db.Column(db.Numeric)
    aqi = db.Column(db.JSON)

    def __repr__(self):
        return f'<AirQualityData(timestamp={self.timestamp}, pm2_5={self.pm2_5}, pm10={self.pm10}, aqi={self.aqi}, aqi_threshold={self.aqi_threshold})>'