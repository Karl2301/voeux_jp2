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
from SQLClassDB import User, Contact, Conversation, Report, FriendRequest, Image, ResetPassword
from uuid import UUID, uuid4
from sqlalchemy.orm import aliased
from cryptography.fernet import Fernet
import json
from .fonctions import app, engine, key, cipher_suite, encrypt_message, decrypt_message, get_db_connection, generate_session_cookie, get_users_info, get_messages_between_users
from extensions import engine, app, socketio, cipher_suite, key

def new_password(token):
    session_token = token

    if not session_token:
        return redirect(url_for('login_get'))

    with Session(engine) as session:
        statement = select(ResetPassword).where(ResetPassword.token == session_token)
        resetPassword_user = session.exec(statement).one_or_none()

    if not resetPassword_user:
        return redirect(url_for('login_get'))
    
    with Session(engine) as session:
        statement = select(User).where(User.id == resetPassword_user.user_id)
        user = session.exec(statement).one_or_none()

    if not user:
        return redirect(url_for('login_get'))
    
    if not user.verified_email:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas', 'error')
            return jsonify(success=False)
        
        user.password_hash = generate_password_hash(password)
        session.add(user)
        session.commit()

        with Session(engine) as session:
            statement = select(ResetPassword).where(ResetPassword.token == session_token)
            results = session.exec(statement)
            token_request = results.one()

            session.delete(token_request)
            session.commit()

        return jsonify(success=True)
    
    else:
        return render_template('page_OTP/index.html')