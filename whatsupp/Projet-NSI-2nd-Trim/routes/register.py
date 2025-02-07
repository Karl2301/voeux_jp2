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
from datetime import datetime, timezone, UTC
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, update, and_
from SQLClassDB import User, Contact, Conversation, Report, FriendRequest, Image
from uuid import UUID, uuid4
from sqlalchemy.orm import aliased
from cryptography.fernet import Fernet
from .fonctions import app, engine, key, cipher_suite, encrypt_message, decrypt_message, get_db_connection, generate_session_cookie, get_users_info, get_messages_between_users
from extensions import engine, app, socketio, cipher_suite, key

def register():
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password-confirm']

        with Session(engine) as sessionuser:
            username_existe = sessionuser.exec(
                select(User).where(User.username == username)
            ).one_or_none()

        with Session(engine) as sessionuser:
            email_exist = sessionuser.exec(
                select(User).where(User.email == email)
            ).one_or_none()

        if username_existe or email_exist:
            error_message = "Ce nom d'utilisateur ou cette adresse e-mail est déjà utilisé."
            return render_template('register/signup.html', error=error_message)

        if not first_name or not last_name or not username or not email or not password or not password_confirm:
            error_message = "Veuillez remplir tous les champs"
            return render_template('register/signup.html', error=error_message)

        if password != password_confirm:
            error_message = "Les mots de passe ne correspondent pas."
            return render_template('register/signup.html', error=error_message)

        hashed_password = generate_password_hash(password)
        otp = generate_otp()  # Génération d'un code OTP

        try:
            user_id = str(uuid.uuid4())  # Génération d'un UUID
            session_cookie = generate_session_cookie()  # Génération d'un cookie de session
            image_url = 'https://ui-avatars.com/api/?size=1000&name='+str(first_name)
            # Récupérer l'image depuis l'URL
            response = requests.get(image_url)
            image_base64 = ""
            # Vérifier si la requête a réussi
            if response.status_code == 200:
                # Encoder l'image en base64
                image_base64 = base64.b64encode(response.content).decode('utf-8')
            else:
                raise Exception(f"Erreur lors de la récupération de l'image: {response.status_code}")

            # URL de l'imag
            now = datetime.now()

            new_user = User(
                id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password_hash=hashed_password,
                otp=otp,
                admin=False,
                created_at= datetime.now(timezone.utc),
                session_cookie=session_cookie,
                profile_image=image_base64
            )

            new_user_session = Session(engine)
            new_user_session.add(new_user)
            new_user_session.commit()
            send_otp_email(email, otp) 

            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('session_cookie', session_cookie)
            session['user_id'] = user_id
            session['admin'] = False
            return response
        except sqlite3.IntegrityError:
            error_message = "Ce nom d'utilisateur ou cette adresse e-mail est déjà utilisé."
            return render_template('register/signup.html', error=error_message)
        except sqlite3.OperationalError as e:
            error_message = f"Erreur de base de données : {str(e)}"
            return render_template('register/signup.html', error=error_message)

    return render_template('register/register_test.html')