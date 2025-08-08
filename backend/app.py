import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from . import create_app, db
except ImportError:
    # Fallback for direct execution
    import __init__ as backend_module
    create_app = backend_module.create_app
    db = backend_module.db

import logging

logger = logging.getLogger(__name__)

# Create app instance
app = create_app()

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
