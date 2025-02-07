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

def get_messages(contact_id):
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        return jsonify({'error': 'Session non valide'}), 401

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        user = session.exec(statement).one_or_none()

    if not user:
        return jsonify({'error': 'Utilisateur introuvable'}), 404

    user_id = user.id

    messages = get_messages_between_users(user_id, contact_id)
    users_info = get_users_info(user_id, contact_id)

    with Session(engine) as session:
        statement = (
            update(Contact)
            .where(Contact.user_id == user_id, Contact.contact_id == contact_id)
            .values(unread_messages_count=0)
        )
        session.exec(statement)
        session.commit()

    if not users_info:
        return jsonify({'error': 'Un ou les deux utilisateurs sont introuvables'}), 404

    return jsonify({'messages': messages, 'users_info': users_info})
