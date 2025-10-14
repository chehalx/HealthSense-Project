from flask import render_template, request, jsonify, redirect, url_for
import json
import logging
from datetime import datetime, timedelta
import time

from app import app, socketio, db, health_data, predictions, alerts
from app import diabetes_model, heart_model, hypoxia_model
from models import HealthData, Prediction, Alert
from ml_models import predict_diabetes, predict_heart_disease, predict_hypoxia, get_health_alerts

logger = logging.getLogger(__name__)

# Route for the main dashboard
@app.route('/')
def index():
    return render_template('dashboard.html')

# Route for historical reports
@app.route('/reports')
def reports():
    return render_template('reports.html')

# Route for device settings
@app.route('/device-settings')
def device_settings():
    return render_template('device_settings.html')

# Route for manual data entry
@app.route('/manual-entry', methods=['GET', 'POST'])
def manual_entry():
    if request.method == 'POST':
        try:
            # Get data from form
            data = {
                'device_id': request.form.get('device_id', 'MANUAL'),
                'glucose': float(request.form.get('glucose', 0)),
                'bp_systolic': float(request.form.get('bp_systolic', 0)),
                'bp_diastolic': float(request.form.get('bp_diastolic', 0)),
                'spo2': float(request.form.get('spo2', 0)),
                'heart_rate': float(request.form.get('heart_rate', 0)),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Create HealthData object
            new_health_data = HealthData(
                device_id=data['device_id'],
                glucose=data['glucose'],
                bp_systolic=data['bp_systolic'],
                bp_diastolic=data['bp_diastolic'],
                spo2=data['spo2'],
                heart_rate=data['heart_rate'],
                timestamp=data['timestamp']
            )
            
            # Store data in the database
            db.session.add(new_health_data)
            
            # Also keep in memory for transition period
            health_data.append(new_health_data)
            if len(health_data) > 1000:
                health_data.pop(0)
            
            # Run ML predictions
            diabetes_risk = predict_diabetes(diabetes_model, new_health_data.glucose)
            heart_disease_risk = predict_heart_disease(
                heart_model, 
                new_health_data.bp_systolic, 
                new_health_data.bp_diastolic, 
                new_health_data.heart_rate
            )
            hypoxia_risk = predict_hypoxia(hypoxia_model, new_health_data.spo2, new_health_data.heart_rate)
            
            # Create Prediction object
            new_prediction = Prediction(
                health_data_id=new_health_data.id,
                diabetes_risk=diabetes_risk,
                heart_disease_risk=heart_disease_risk,
                hypoxia_risk=hypoxia_risk
            )
            
            # Store prediction in database
            db.session.add(new_prediction)
            
            # Also keep in memory for transition period
            predictions.append(new_prediction)
            if len(predictions) > 1000:
                predictions.pop(0)
            
            # Check for alerts
            health_alerts = get_health_alerts(new_health_data)
            for alert_data in health_alerts:
                new_alert = Alert(
                    health_data_id=new_health_data.id,
                    message=alert_data["message"],
                    condition=alert_data["condition"],
                    severity=alert_data["severity"]
                )
                # Store alert in database
                db.session.add(new_alert)
                
                # Also keep in memory for transition period
                alerts.append(new_alert)
                if len(alerts) > 100:
                    alerts.pop(0)
            
            # Commit changes to database
            db.session.commit()
            
            # Broadcast data to connected clients
            socketio.emit('new_health_data', {
                'health_data': new_health_data.to_dict(),
                'prediction': new_prediction.to_dict(),
                'alerts': [a.to_dict() for a in alerts if a.health_data_id == new_health_data.id]
            })
            
            # Redirect to dashboard with success message
            return redirect(url_for('index'))
            
        except Exception as e:
            logger.error(f"Error processing manual data: {e}")
            return render_template('manual_entry.html', error=str(e))
    
    return render_template('manual_entry.html')

# API endpoint to receive health data from devices
@app.route('/api/healthdata', methods=['POST'])
def receive_health_data():
    try:
        data = request.json
        logger.debug(f"Received health data: {data}")
        
        # Create HealthData object
        new_health_data = HealthData(
            device_id=data.get('device_id', 'unknown'),
            glucose=data.get('glucose', 0),
            bp_systolic=data.get('bp_systolic', 0),
            bp_diastolic=data.get('bp_diastolic', 0),
            spo2=data.get('spo2', 0),
            heart_rate=data.get('heart_rate', 0),
            timestamp=data.get('timestamp', datetime.utcnow().isoformat())
        )
        
        # Store data in database
        db.session.add(new_health_data)
        
        # Also keep in memory for transition period
        health_data.append(new_health_data)
        if len(health_data) > 1000:  # Limit storage size for MVP
            health_data.pop(0)
        
        # Run ML predictions
        diabetes_risk = predict_diabetes(diabetes_model, new_health_data.glucose)
        heart_disease_risk = predict_heart_disease(
            heart_model, 
            new_health_data.bp_systolic, 
            new_health_data.bp_diastolic, 
            new_health_data.heart_rate
        )
        hypoxia_risk = predict_hypoxia(hypoxia_model, new_health_data.spo2, new_health_data.heart_rate)
        
        # Create Prediction object
        new_prediction = Prediction(
            health_data_id=new_health_data.id,
            diabetes_risk=diabetes_risk,
            heart_disease_risk=heart_disease_risk,
            hypoxia_risk=hypoxia_risk
        )
        
        # Store prediction in database
        db.session.add(new_prediction)
        
        # Also keep in memory for transition period
        predictions.append(new_prediction)
        if len(predictions) > 1000:  # Limit storage size for MVP
            predictions.pop(0)
        
        # Check for alerts
        health_alerts = get_health_alerts(new_health_data)
        for alert_data in health_alerts:
            new_alert = Alert(
                health_data_id=new_health_data.id,
                message=alert_data["message"],
                condition=alert_data["condition"],
                severity=alert_data["severity"]
            )
            # Store in database
            db.session.add(new_alert)
            
            # Keep in memory for transition
            alerts.append(new_alert)
            if len(alerts) > 100:  # Limit alerts for MVP
                alerts.pop(0)
        
        # Commit changes to database
        db.session.commit()
        
        # Broadcast data to connected clients
        socketio.emit('new_health_data', {
            'health_data': new_health_data.to_dict(),
            'prediction': new_prediction.to_dict(),
            'alerts': [a.to_dict() for a in alerts if a.health_data_id == new_health_data.id]
        })
        
        return jsonify({
            'status': 'success',
            'message': 'Data received and processed',
            'data': new_health_data.to_dict(),
            'prediction': new_prediction.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing health data: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# API endpoint to get latest health data
@app.route('/api/latest', methods=['GET'])
def get_latest_data():
    try:
        # Get latest health data from database
        latest_db_data = HealthData.query.order_by(HealthData.timestamp.desc()).first()
        
        # If not in database, check in-memory (during transition)
        if not latest_db_data and health_data:
            latest_data = health_data[-1].to_dict()
            
            # Find associated prediction from in-memory
            latest_prediction = None
            for p in reversed(predictions):
                if p.health_data_id == latest_data['id']:
                    latest_prediction = p.to_dict()
                    break
            
            # Get associated alerts from in-memory
            data_alerts = [a.to_dict() for a in alerts if a.health_data_id == latest_data['id']]
            
        elif latest_db_data:
            # Get data from database
            latest_data = latest_db_data.to_dict()
            
            # Find associated prediction from database
            db_prediction = Prediction.query.filter_by(health_data_id=latest_data['id']).first()
            latest_prediction = db_prediction.to_dict() if db_prediction else None
            
            # Get associated alerts from database
            db_alerts = Alert.query.filter_by(health_data_id=latest_data['id']).all()
            data_alerts = [a.to_dict() for a in db_alerts]
            
        else:
            return jsonify({'status': 'error', 'message': 'No data available'}), 404
        
        return jsonify({
            'status': 'success',
            'health_data': latest_data,
            'prediction': latest_prediction,
            'alerts': data_alerts
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting latest data: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# API endpoint to get historical data
@app.route('/api/history', methods=['GET'])
def get_historical_data():
    try:
        # Get query parameters
        hours = int(request.args.get('hours', 24))
        limit = min(int(request.args.get('limit', 100)), 1000)  # Cap at 1000 records
        
        # Calculate cutoff time
        cutoff_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        
        # Query database for recent health data
        db_data = HealthData.query.filter(HealthData.timestamp >= cutoff_time).order_by(HealthData.timestamp).limit(limit).all()
        db_data_dicts = [d.to_dict() for d in db_data]
        
        # For transition period, also include in-memory data
        in_memory_data = [d.to_dict() for d in health_data if d.timestamp >= cutoff_time]
        
        # Combine data, avoiding duplicates
        all_data = db_data_dicts.copy()
        for d in in_memory_data:
            if not any(db_d['id'] == d['id'] for db_d in db_data_dicts):
                all_data.append(d)
                
        # Sort by timestamp
        all_data.sort(key=lambda x: x['timestamp'])
        
        # Limit results
        limited_data = all_data[-limit:] if limit < len(all_data) else all_data
        
        # Get associated predictions from database
        data_predictions = {}
        for d in limited_data:
            # Try database first
            db_prediction = Prediction.query.filter_by(health_data_id=d['id']).first()
            if db_prediction:
                data_predictions[d['id']] = db_prediction.to_dict()
            else:
                # Try in-memory
                for p in predictions:
                    if p.health_data_id == d['id']:
                        data_predictions[d['id']] = p.to_dict()
                        break
        
        return jsonify({
            'status': 'success',
            'data': limited_data,
            'predictions': data_predictions
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting historical data: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# API endpoint to acknowledge an alert
@app.route('/api/alerts/<alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    try:
        # First check database
        alert = Alert.query.get(alert_id)
        if alert:
            alert.acknowledged = True
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Alert acknowledged',
                'alert': alert.to_dict()
            }), 200
        
        # If not found in database, check in-memory (for transition period)
        for in_memory_alert in alerts:
            if in_memory_alert.id == alert_id:
                in_memory_alert.acknowledged = True
                return jsonify({
                    'status': 'success',
                    'message': 'Alert acknowledged',
                    'alert': in_memory_alert.to_dict()
                }), 200
        
        return jsonify({
            'status': 'error',
            'message': 'Alert not found'
        }), 404
        
    except Exception as e:
        logger.error(f"Error acknowledging alert: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# API endpoint to get all active alerts
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    try:
        # Get query parameters
        acknowledged = request.args.get('acknowledged', 'false').lower() == 'true'
        
        # Query database for alerts
        db_alerts = Alert.query.filter_by(acknowledged=acknowledged).all()
        filtered_alerts = [a.to_dict() for a in db_alerts]
        
        # For transition period, also include in-memory alerts
        for a in alerts:
            if a.acknowledged == acknowledged:
                # Only add if not already in list (avoid duplicates)
                if not any(db_alert['id'] == a.id for db_alert in filtered_alerts):
                    filtered_alerts.append(a.to_dict())
        
        return jsonify({
            'status': 'success',
            'alerts': filtered_alerts
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
