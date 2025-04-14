from datetime import datetime
import uuid

class HealthData:
    """Data structure to hold health data from wearable devices"""
    def __init__(self, device_id, glucose, bp_systolic, bp_diastolic, 
                 spo2, heart_rate, timestamp=None):
        self.id = str(uuid.uuid4())
        self.device_id = device_id
        self.glucose = glucose  # mg/dL
        self.bp_systolic = bp_systolic  # mmHg
        self.bp_diastolic = bp_diastolic  # mmHg
        self.spo2 = spo2  # %
        self.heart_rate = heart_rate  # BPM
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

class Prediction:
    """Data structure to hold disease predictions"""
    def __init__(self, health_data_id, diabetes_risk, heart_disease_risk, 
                 hypoxia_risk, timestamp=None):
        self.id = str(uuid.uuid4())
        self.health_data_id = health_data_id
        self.diabetes_risk = diabetes_risk  # probability (0-1)
        self.heart_disease_risk = heart_disease_risk  # probability (0-1)
        self.hypoxia_risk = hypoxia_risk  # probability (0-1)
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

class Alert:
    """Data structure to hold health alerts"""
    SEVERITY_LOW = 'low'
    SEVERITY_MEDIUM = 'medium'
    SEVERITY_HIGH = 'high'
    
    def __init__(self, health_data_id, message, condition, severity, timestamp=None):
        self.id = str(uuid.uuid4())
        self.health_data_id = health_data_id
        self.message = message
        self.condition = condition  # e.g., 'high_glucose', 'low_spo2'
        self.severity = severity  # low, medium, high
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
