from datetime import datetime
import uuid
from app import db

class HealthData(db.Model):
    """Database model to hold health data from wearable devices"""
    __tablename__ = 'health_data'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = db.Column(db.String(50), nullable=False)
    glucose = db.Column(db.Float, nullable=False)  # mg/dL
    bp_systolic = db.Column(db.Float, nullable=False)  # mmHg
    bp_diastolic = db.Column(db.Float, nullable=False)  # mmHg
    spo2 = db.Column(db.Float, nullable=False)  # %
    heart_rate = db.Column(db.Float, nullable=False)  # BPM
    timestamp = db.Column(db.String(30), default=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    predictions = db.relationship('Prediction', backref='health_data', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='health_data', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, device_id, glucose, bp_systolic, bp_diastolic, 
                 spo2, heart_rate, timestamp=None):
        self.id = str(uuid.uuid4())
        self.device_id = device_id
        self.glucose = glucose
        self.bp_systolic = bp_systolic
        self.bp_diastolic = bp_diastolic
        self.spo2 = spo2
        self.heart_rate = heart_rate
        self.timestamp = timestamp or datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'glucose': self.glucose,
            'bp_systolic': self.bp_systolic,
            'bp_diastolic': self.bp_diastolic,
            'spo2': self.spo2,
            'heart_rate': self.heart_rate,
            'timestamp': self.timestamp
        }

class Prediction(db.Model):
    """Database model to hold disease predictions"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    health_data_id = db.Column(db.String(36), db.ForeignKey('health_data.id'), nullable=False)
    diabetes_risk = db.Column(db.Float, nullable=False)  # probability (0-1)
    heart_disease_risk = db.Column(db.Float, nullable=False)  # probability (0-1)
    hypoxia_risk = db.Column(db.Float, nullable=False)  # probability (0-1)
    timestamp = db.Column(db.String(30), default=lambda: datetime.utcnow().isoformat())
    
    def __init__(self, health_data_id, diabetes_risk, heart_disease_risk, 
                 hypoxia_risk, timestamp=None):
        self.id = str(uuid.uuid4())
        self.health_data_id = health_data_id
        self.diabetes_risk = diabetes_risk
        self.heart_disease_risk = heart_disease_risk
        self.hypoxia_risk = hypoxia_risk
        self.timestamp = timestamp or datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'health_data_id': self.health_data_id,
            'diabetes_risk': self.diabetes_risk,
            'heart_disease_risk': self.heart_disease_risk,
            'hypoxia_risk': self.hypoxia_risk,
            'timestamp': self.timestamp
        }

class Alert(db.Model):
    """Database model to hold health alerts"""
    __tablename__ = 'alerts'
    
    SEVERITY_LOW = 'low'
    SEVERITY_MEDIUM = 'medium'
    SEVERITY_HIGH = 'high'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    health_data_id = db.Column(db.String(36), db.ForeignKey('health_data.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    condition = db.Column(db.String(50), nullable=False)  # e.g., 'high_glucose', 'low_spo2'
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high
    timestamp = db.Column(db.String(30), default=lambda: datetime.utcnow().isoformat())
    acknowledged = db.Column(db.Boolean, default=False)
    
    def __init__(self, health_data_id, message, condition, severity, timestamp=None):
        self.id = str(uuid.uuid4())
        self.health_data_id = health_data_id
        self.message = message
        self.condition = condition
        self.severity = severity
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.acknowledged = False
    
    def to_dict(self):
        return {
            'id': self.id,
            'health_data_id': self.health_data_id,
            'message': self.message,
            'condition': self.condition,
            'severity': self.severity,
            'timestamp': self.timestamp,
            'acknowledged': self.acknowledged
        }
