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

def user_info_admin(user_id):
    session_cookie = request.cookies.get('session_cookie')

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        user = session.exec(statement).one_or_none()    
        if not session_cookie or not user:
            return redirect(url_for('login_get'))

    return render_template('high_admin_panel/user_info.html')


def get_user_info(user_id):
    session_cookie = request.cookies.get('session_cookie')

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        user_requester = session.exec(statement).one_or_none()    
        if not session_cookie or not user_requester.admin:
            return jsonify({"error": "Not permitted"}), 404
    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).one_or_none()
        if user:
            return jsonify({
                "requester_lvl_admin": user_requester.admin_level,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "bio": user.bio,
                "description": user.description,
                "admin_level": user.admin_level,
                "admin": user.admin
            })
        else:
            return jsonify({"error": "User not found"}), 404


def update_user_admin_info(user_id):
    session_cookie = request.cookies.get('session_cookie')
    if not session_cookie:
        return redirect(url_for('login_get'))
        

    with Session(engine) as session:
        user = session.exec(select(User).where(User.session_cookie == session_cookie)).one_or_none()

    if not user or not user.admin:
        return redirect(url_for('login_get'))

    with Session(engine) as session:
        user_to_update = session.exec(select(User).where(User.id == user_id)).one_or_none()
        # print(user.admin_level < user_to_update.admin_level)
        # print(user.admin_level == 4)
        if user_to_update and (user.admin_level < user_to_update.admin_level):
            return jsonify({"success": False}), 500
        
        if user_to_update:
            data = request.get_json()
            user_to_update.first_name = data.get('first_name')
            user_to_update.last_name = data.get('last_name')
            user_to_update.username = data.get('username')
            user_to_update.email = data.get('email')
            user_to_update.bio = data.get('bio')
            user_to_update.description = data.get('description')
            user_to_update.admin = data.get('admin')
            if data.get('admin_level') and user_to_update.admin:
                user_to_update.admin_level = data.get('admin_level')
            else:
                user_to_update.admin_level = 0

            session.add(user_to_update)
            session.commit()
            return jsonify({"success": True})
        else:
            return jsonify({"success": False}), 404
