from app import app, socketio  # noqa: F401

# Import views to register routes
from views import *  # noqa: F401

# Run the app if executed directly
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
