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

def friend_requests():
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        return redirect(url_for('login_get'))

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.session_cookie == session_cookie)
        ).one_or_none()

    if not user:
        return redirect(url_for('login_get'))

    user_id = user.id

    with Session(engine) as session:
        statement = select(
            FriendRequest.request_id,
            FriendRequest.requester_id,
            FriendRequest.requester_first_name,
            FriendRequest.requester_last_name,
            User.profile_image
        ).join(User, User.id == FriendRequest.requester_id).where(
            FriendRequest.receiver_id == user_id
        )

        friend_requests = session.exec(statement).all()
        requests_list = [request._asdict() for request in friend_requests]

    return jsonify(requests_list)
