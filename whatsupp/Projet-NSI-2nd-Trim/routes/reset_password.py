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
from .fonctions import app, engine, key, cipher_suite, encrypt_message, decrypt_message, get_db_connection, generate_session_cookie, get_users_info, get_messages_between_users
from extensions import engine, app, socketio, cipher_suite, key

def reset_password():
    if request.method == 'POST':
        email = request.get_json()['email']

        with Session(engine) as session:
            statement = select(User).where(User.email == email)
            user = session.exec(statement).one_or_none()

        # print(user)

        with Session(engine) as session:
            statement = select(ResetPassword).where(ResetPassword.user_id == user.id)
            exist = session.exec(statement).one_or_none()
        token = str(uuid4())
        if user and not exist:
            new_reset = ResetPassword(
                user_id=user.id,
                token=token
            )

            new_reset_session = Session(engine)
            new_reset_session.add(new_reset)
            new_reset_session.commit()

            send_password_reset_email(email, token)  # Envoi de l'email de réinitialisation
            return jsonify(success=True)
        else:
            error_message = "Aucun utilisateur trouvé avec cette adresse e-mail."
            return jsonify(success=False, error_message=error_message)

    return render_template('mdp_oublier/index.html')