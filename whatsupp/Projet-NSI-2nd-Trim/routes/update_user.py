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
from .fonctions import app, engine, key, cipher_suite, encrypt_message, decrypt_message, get_db_connection, generate_session_cookie, get_users_info, get_messages_between_users
from extensions import engine, app, socketio, cipher_suite, key


def update_user(user_id):
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        return redirect(url_for('login_get'))

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.session_cookie == session_cookie)
        ).first()

    if not user or user.admin_level < 3:
        return redirect(url_for('login_get'))

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    email = request.form['email']
    admin = bool(int(request.form['admin']))
    admin_level = int(request.form['admin_level'])

    with Session(engine) as session:
        user_to_update = session.get(User, user_id)
        if user_to_update:
            user_to_update.first_name = first_name
            user_to_update.last_name = last_name
            user_to_update.username = username
            user_to_update.email = email
            user_to_update.admin = admin
            user_to_update.admin_level = admin_level
            session.add(user_to_update)
            session.commit()

    return redirect(url_for('admin'))
