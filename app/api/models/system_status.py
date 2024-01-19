from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SystemStatus(db.Model):
    timestamp = db.Column(db.TIMESTAMP, primary_key=True, default=db.func.current_timestamp())
    status = db.Column(db.String(10))
    sensor_connected = db.Column(db.Boolean)
    cpu_usage_percent = db.Column(db.Numeric)
    memory_usage_percent = db.Column(db.Numeric)

    def __repr__(self):
        return f'<SystemStatus(timestamp={self.timestamp}, status={self.status}, sensor_connected={self.sensor_connected}, cpu_usage_percent={self.cpu_usage_percent}, memory_usage_percent={self.memory_usage_percent})>'
    
    def system_status(self):
        return {
            'timestamp': self.timestamp,
            'status': self.status,
            'sensor_connected': self.sensor_connected,
            'cpu_usage_percent': self.cpu_usage_percent,
            'memory_usage_percent': self.memory_usage_percent
        }
    



