from flask import Flask , request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from flask.json.provider import DefaultJSONProvider
from datetime import datetime, date
from dbUtils import create_database

class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)
    
# Create the database if it doesn't exist
create_database()

app = Flask(__name__)
app.json = UpdatedJSONProvider(app)
CORS(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

with app.app_context():
    db.create_all()

from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010,debug=True)


