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

def update_user_info():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    bio = data.get('bio')
    description = data.get('description')
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        return jsonify({'error': 'Session non valide'}), 401

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        user = session.exec(statement).one_or_none()

    if not user:
        return jsonify({'error': 'Utilisateur introuvable'}), 404

    # Vérifier si le nom d'utilisateur est déjà utilisé
    if username:
        username_check = select(User).where(User.username == username, User.id != user.id)
        existing_user = session.exec(username_check).one_or_none()
        if existing_user:
            return jsonify({'error': 'Le nom d\'utilisateur est déjà utilisé'}), 409

    # Vérifier si l'email est déjà utilisé
    if email:
        email_check = select(User).where(User.email == email, User.id != user.id)
        existing_email = session.exec(email_check).one_or_none()
        if existing_email:
            return jsonify({'error': 'L\'email est déjà utilisé'}), 409

    # Mettre à jour uniquement les champs non vides
    if username:
        user.username = username
    if email:
        user.email = email
    if bio:
        user.bio = bio
    if description:
        user.description = description

    with Session(engine) as session:
        session.add(user)
        session.commit()

    return jsonify({'success': True})
