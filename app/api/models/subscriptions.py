from flask_sqlalchemy import SQLAlchemy
import shortuuid
from app.utils.helpers import is_valid_email

db = SQLAlchemy()

class Subscriptions(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    email = db.Column(db.String(50))
    pm2_5_threshold = db.Column(db.Numeric, default=35)
    pm10_threshold = db.Column(db.Numeric, default=50)
    alert_sent = db.Column(db.Boolean, default=False)
    aqi_threshold = db.Column(db.Numeric, default=100)

    def __repr__(self):
        return f'<Subscriptions(id={self.id}, email={self.email}, pm2_5_threshold={self.pm2_5_threshold}, pm10_threshold={self.pm10_threshold}, aqi_threshold={self.aqi_threshold}, alert_sent={self.alert_sent})>'
    
    @classmethod
    def create_new_subscriber(cls, email):
        if is_valid_email(email):
            unique_id = str(shortuuid.uuid()[:8])

            new_subscription = cls(id=unique_id, email=email)
            db.session.add(new_subscription)
            db.session.commit()
            return {'id': new_subscription.id, 'email': new_subscription.email}
        else:
            return {'error': 'Invalid email address. Email addresses must be in the format: hey@example.com'}
    
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
            return {'error': 'Invalid email address. Email addresses must be in the format: hey@example.com'}

    
    def update_thresholds(self, pm2_5_threshold=None, pm10_threshold=None, aqi_threshold=None):
        if pm2_5_threshold is not None:
            self.pm2_5_threshold = pm2_5_threshold
        if pm10_threshold is not None:
            self.pm10_threshold = pm10_threshold
        if aqi_threshold is not None:
            self.aqi_threshold = aqi_threshold

        db.session.commit()

        return {'id': self.id, 'pm2_5_threshold': self.pm2_5_threshold, 'pm10_threshold': self.pm10_threshold, 'aqi_threshold': self.aqi_threshold}