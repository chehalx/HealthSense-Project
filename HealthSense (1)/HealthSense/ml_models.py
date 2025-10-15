import logging
import numpy as np
import pickle
import os
import random
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

logger = logging.getLogger(__name__)

def create_mock_models():
    """Create mock ML models for the MVP phase"""
    # Mock diabetes model (Logistic Regression)
    diabetes_model = LogisticRegression()
    X = np.random.rand(100, 2)  # mock features (glucose, BMI)
    y = np.random.randint(0, 2, 100)  # binary outcome
    diabetes_model.fit(X, y)
    
    # Mock heart disease model (Random Forest)
    heart_model = RandomForestClassifier(n_estimators=10)
    X = np.random.rand(100, 3)  # mock features (bp_systolic, bp_diastolic, heart_rate)
    y = np.random.randint(0, 2, 100)  # binary outcome
    heart_model.fit(X, y)
    
    # Mock hypoxia model (SVM)
    hypoxia_model = SVC(probability=True)
    X = np.random.rand(100, 2)  # mock features (spo2, heart_rate)
    y = np.random.randint(0, 2, 100)  # binary outcome
    hypoxia_model.fit(X, y)
    
    return diabetes_model, heart_model, hypoxia_model

def load_models():
    """Load ML models from files or create mock models if not available"""
    try:
        logger.info("Loading ML models")
        
        # In a real application, you would load pre-trained models from files
        # For this MVP, we'll create mock models
        
        diabetes_model, heart_model, hypoxia_model = create_mock_models()
        
        logger.info("ML models loaded successfully")
        return diabetes_model, heart_model, hypoxia_model
    
    except Exception as e:
        logger.error(f"Error loading ML models: {e}")
        # Return mock models if loading fails
        return create_mock_models()

def predict_diabetes(model, glucose):
    """Predict diabetes risk based on glucose level"""
    # In a real app, more features would be used
    features = np.array([[glucose, 0.5]])  # glucose and a dummy feature
    probability = model.predict_proba(features)[0][1]
    return float(probability)

def predict_heart_disease(model, bp_systolic, bp_diastolic, heart_rate):
    """Predict heart disease risk based on blood pressure and heart rate"""
    features = np.array([[bp_systolic, bp_diastolic, heart_rate]])
    probability = model.predict_proba(features)[0][1]
    return float(probability)

def predict_hypoxia(model, spo2, heart_rate):
    """Predict hypoxia risk based on SpO2 and heart rate"""
    features = np.array([[spo2, heart_rate]])
    probability = model.predict_proba(features)[0][1]
    return float(probability)

def get_health_alerts(health_data):
    """Generate health alerts based on sensor readings"""
    alerts = []
    
    # Check glucose levels
    if health_data.glucose > 180:
        alerts.append({
            "condition": "high_glucose",
            "message": f"High glucose level detected ({health_data.glucose} mg/dL)",
            "severity": "high" if health_data.glucose > 250 else "medium"
        })
    elif health_data.glucose < 70:
        alerts.append({
            "condition": "low_glucose",
            "message": f"Low glucose level detected ({health_data.glucose} mg/dL)",
            "severity": "high" if health_data.glucose < 50 else "medium"
        })
    
    # Check blood pressure
    if health_data.bp_systolic > 140 or health_data.bp_diastolic > 90:
        alerts.append({
            "condition": "high_blood_pressure",
            "message": f"High blood pressure detected ({health_data.bp_systolic}/{health_data.bp_diastolic} mmHg)",
            "severity": "high" if health_data.bp_systolic > 180 or health_data.bp_diastolic > 120 else "medium"
        })
    
    # Check SpO2 levels
    if health_data.spo2 < 94:
        alerts.append({
            "condition": "low_oxygen",
            "message": f"Low oxygen saturation detected ({health_data.spo2}%)",
            "severity": "high" if health_data.spo2 < 90 else "medium"
        })
    
    # Check heart rate
    if health_data.heart_rate > 100:
        alerts.append({
            "condition": "high_heart_rate",
            "message": f"Elevated heart rate detected ({health_data.heart_rate} BPM)",
            "severity": "medium" if health_data.heart_rate > 120 else "low"
        })
    elif health_data.heart_rate < 50:
        alerts.append({
            "condition": "low_heart_rate",
            "message": f"Low heart rate detected ({health_data.heart_rate} BPM)",
            "severity": "medium" if health_data.heart_rate < 40 else "low"
        })
    
    return alerts
