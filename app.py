from flask import Flask , request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from flask.json.provider import DefaultJSONProvider
from datetime import datetime, date
from dbUtils import create_database
from models import Reminder, db

class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)
    
migrate = Migrate()
# Create the database if it doesn't exist
create_database()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    app.json = UpdatedJSONProvider(app)
    CORS(app)

    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
      try:
          db.create_all()
      except Exception as exception:
          print("got the following exception when attempting db.create_all() in app.py: " + str(exception))
    
    # Register blueprints
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5010,debug=True)
    


