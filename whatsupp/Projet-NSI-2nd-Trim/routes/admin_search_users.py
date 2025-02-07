from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import uuid
import os
import base64
import hashlib
from email_utils import send_password_reset_email, send_otp_email, generate_otp
import requests
import ssl
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, update, and_
from SQLClassDB import User, Contact, Conversation, Report, FriendRequest, Image
from uuid import UUID, uuid4
from sqlalchemy.orm import aliased
from cryptography.fernet import Fernet
import json
from .fonctions import app, engine, key, cipher_suite, encrypt_message, decrypt_message, get_db_connection, generate_session_cookie, get_users_info, get_messages_between_users
from extensions import engine, app, socketio, cipher_suite, key

def admin_search_users():
    query = request.args.get('query', '')
    limit = 10
    with Session(engine) as session:
        if query:
            users = session.exec(select(User).where(User.username.ilike(f'%{query}%')).limit(limit)).all()
        else:
            users = session.exec(select(User).limit(limit)).all()
        user_list = [{'id': user.id, 'name': user.username} for user in users]
    return jsonify(user_list)
