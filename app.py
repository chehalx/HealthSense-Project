import os
import logging
import pickle
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "healthsense_default_secret")

# Enable CORS
CORS(app)

# Setup SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize in-memory data storage (for MVP phase)
health_data = []
predictions = []
alerts = []

# Import ML models
from ml_models import load_models
diabetes_model, heart_model, hypoxia_model = load_models()

logger.info("HealthSense application initialized")
