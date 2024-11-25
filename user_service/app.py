import logging
import json
import re
import os

from flask import Flask, request, has_request_context
from flask_migrate import Migrate

from config import config
from models import db
from routes import user_bp

# os.environ['WERKZEUG_RUN_MAIN'] = 'true'

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)


class CustomJSONFormatter(logging.Formatter):
    ANSI_ESCAPE = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

    def format(self, record):
        message = record.getMessage()
    
        # Remove ANSI escape codes
        cleaned_message = self.ANSI_ESCAPE.sub('', message)
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'service': 'user_service',
            'message': cleaned_message,
            'error': record.exc_info if record.exc_info else None
        }

        # Add request-specific information only if a request context is active
        if has_request_context():
            log_entry['request_id'] = request.headers.get('X-Request-ID', 'N/A')
            log_entry['user_id'] = getattr(request, 'user_id', 'N/A')  # Customize as per your need

        return json.dumps(log_entry)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(CustomJSONFormatter())
logger.addHandler(handler)

app.register_blueprint(user_bp, url_prefix='/user')
app.logger = logger

@app.route('/')
def get_users():
    return """Hello Welcome to ECom Platfrom...
            Users: /user"""


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", debug=debug_mode)