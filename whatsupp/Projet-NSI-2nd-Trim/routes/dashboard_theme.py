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


def update_dashboard_theme():
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        app.logger.error('Session cookie is not present.')
        return redirect(url_for('login_get'))

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        user = session.exec(statement).one_or_none()

    if not user:
        app.logger.error('User with the given session cookie not found.')
        response = make_response(redirect(url_for('login_get')))
        response.set_cookie('session_cookie', '', expires=0)
        return {"success": False}

    user.dashboard_theme = not user.dashboard_theme

    with Session(engine) as session:
        session.add(user)
        session.commit()

    return {"success": True}