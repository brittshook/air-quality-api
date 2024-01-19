from flask_sqlalchemy import SQLAlchemy
import shortuuid
from app.utils.email_utils import is_valid_email
from .air_quality_data import db

class Subscriptions(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    email = db.Column(db.String(50))
    pm2_5_threshold = db.Column(db.Numeric, default=35)
    pm10_threshold = db.Column(db.Numeric, default=50)
    alert_sent_pm10 = db.Column(db.Boolean, default=False)
    aqi_threshold = db.Column(db.Numeric, default=100)
    alert_sent_aqi = db.Column(db.Boolean, default=False)
    alert_sent_pm2_5 = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Subscriptions(id={self.id}, email={self.email}, pm2_5_threshold={self.pm2_5_threshold}, pm10_threshold={self.pm10_threshold}, aqi_threshold={self.aqi_threshold}, alert_sent_pm2_5={self.alert_sent_pm2_5}, alert_sent_pm10={self.alert_sent_pm10}, alert_sent_aqi={self.alert_sent_aqi})>'
    
    @classmethod
    def create_new_subscriber(cls, email):
        if is_valid_email(email):
            unique_id = str(shortuuid.uuid()[:8])

            new_subscription = cls(id=unique_id, email=email)
            db.session.add(new_subscription)
            db.session.commit()
            return {'id': new_subscription.id, 'email': new_subscription.email}
        else:
            raise ValueError('Invalid email address. Email addresses must be in the format: hey@example.com')
    
    @classmethod
    def delete_subscriber(cls, subscription_id):
        subscription = cls.query.get(subscription_id)
        if subscription:
            db.session.delete(subscription)
            db.session.commit()
            return True
        return False
    
    def update_email(self, new_email):
        if is_valid_email(new_email):
            self.email = new_email
            db.session.commit()
            return {'id': self.id, 'email': self.email}
        else:
            raise ValueError('Invalid email address. Email addresses must be in the format: hey@example.com')

    def update_thresholds(self, pm2_5_threshold=None, pm10_threshold=None, aqi_threshold=None):
        if pm2_5_threshold is not None:
            pm2_5_threshold = float(pm2_5_threshold)
        if pm10_threshold is not None:
            pm10_threshold = float(pm10_threshold)
        if aqi_threshold is not None:
            aqi_threshold = float(aqi_threshold)
        
        if (
        (pm2_5_threshold is not None and pm2_5_threshold <= 0) or
        (pm10_threshold is not None and pm10_threshold <= 0) or
        (aqi_threshold is not None and aqi_threshold <= 0)
        ):
            raise ValueError("Thresholds must be greater than 0")

        if pm2_5_threshold is not None:
            self.pm2_5_threshold = pm2_5_threshold

        if pm10_threshold is not None:
            self.pm10_threshold = pm10_threshold

        if aqi_threshold is not None:
            self.aqi_threshold = aqi_threshold

        db.session.commit()
        return {
            'id': self.id, 
            'pm2_5_threshold': float(self.pm2_5_threshold), 
            'pm10_threshold': float(self.pm10_threshold), 
            'aqi_threshold': float(self.aqi_threshold)
        }
    
    def set_alert_sent(self, indicator, value):
        if indicator == 'pm2_5':
            self.alert_sent_pm2_5 = value
        elif indicator == 'pm10':
            self.alert_sent_pm10 = value
        elif indicator == 'aqi':
            self.alert_sent_aqi = value
        
        db.session.commit()
            
    def alert_sent(self, indicator):
        if indicator == 'pm2_5':
            return self.alert_sent_pm2_5
        elif indicator == 'pm10':
            return self.alert_sent_pm10
        elif indicator == 'aqi':
            return self.alert_sent_aqi