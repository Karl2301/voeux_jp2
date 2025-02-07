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

def change_password():
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        return jsonify({'error': 'Session non valide'}), 401

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        user = session.exec(statement).one_or_none()

    if not user:
        return jsonify({'error': 'Utilisateur introuvable'}), 404

    # Vérifie si le mot de passe actuel est correct
    if not check_password_hash(user.password_hash, current_password):
        return jsonify({'error': 'Le mot de passe actuel est incorrect'}), 400

    # Vérifie que les nouveaux mots de passe correspondent
    if not new_password or new_password == current_password:
        return jsonify({'error': 'Le nouveau mot de passe ne peut pas être le même que l\'ancien ou vide'}), 400

    # Hacher le nouveau mot de passe et mettre à jour la base de données
    user.password_hash = generate_password_hash(new_password)

    with Session(engine) as session:
        session.add(user)
        session.commit()

    return jsonify({'success': True})