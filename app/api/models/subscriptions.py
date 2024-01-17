from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subscriptions(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    email = db.Column(db.String(50))
    pm2_5_threshold = db.Column(db.Numeric, default=35)
    pm10_threshold = db.Column(db.Numeric, default=50)
    alert_sent = db.Column(db.Boolean, default=False)
    aqi_threshold = db.Column(db.Numeric)

    def __repr__(self):
        return f'<Subscriptions(id={self.id}, email={self.email}, pm2_5_threshold={self.pm2_5_threshold}, pm10_threshold={self.pm10_threshold}, aqi_threshold={self.aqi_threshold}, alert_sent={self.alert_sent})>'