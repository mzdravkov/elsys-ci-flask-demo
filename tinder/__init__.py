from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/dev.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "eusehuccuhosn23981pcgid1xth4dn"

socketio = SocketIO(app)
db = SQLAlchemy(app)

from tinder.routes import *
