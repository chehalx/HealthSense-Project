import os
import logging
import pickle
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create SQLAlchemy base class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "healthsense_default_secret")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)

# Enable CORS
CORS(app)

# Setup SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize in-memory data storage (for transition phase)
health_data = []
predictions = []
alerts = []

# Initialize database tables
with app.app_context():
    # Import models here to avoid circular imports
    import models
    db.create_all()
    logger.info("Database tables created")

# Import ML models
from ml_models import load_models
diabetes_model, heart_model, hypoxia_model = load_models()

logger.info("HealthSense application initialized")
