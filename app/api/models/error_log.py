from datetime import datetime
from .db import db

class ErrorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    error_type = db.Column(db.String(255))
    error_message = db.Column(db.TEXT)
    traceback = db.Column(db.TEXT)

    def __repr__(self):
        return f'<ErrorLog {self.id}>'
