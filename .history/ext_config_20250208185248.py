from flask import Flask, request, jsonify, render_template
from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Optional
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 

# Configuration de la base de données MariaDB
# DATABASE_URL = "mysql+pymysql://nsidb:123nsi!bd@localhost/jp2_voeux_parcoursup"
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)