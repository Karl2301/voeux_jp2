from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from sqlmodel import Field, Session, SQLModel, create_engine, select, update, and_
from cryptography.fernet import Fernet
import os
from threading import Thread, Event

# Instance SocketIO partagée
thread = None
thread_stop_event = Event()
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app, resources={"/*": {"origins": "https://whatsupp.aekio.fr"}})
app.secret_key = os.urandom(24) 
# engine = create_engine("sqlite:///db.sqlite", connect_args={"check_same_thread": False, "timeout": 10})
engine = create_engine("mysql://nsidb:123nsi!bd@localhost/nsiproject")
key = "1TKjBC04PmvtwRgU3bRAm_r3lHJxygr-PYZH7ALjYlM="
cipher_suite = Fernet(key)