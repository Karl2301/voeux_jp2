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

def login_get():
    session_cookie = request.cookies.get('session_cookie')

    if session_cookie:
        with Session(engine) as sessionuser:
            user = sessionuser.exec(
                select(User).where(User.session_cookie == session_cookie)
            ).one_or_none()

        if user:
            return redirect(url_for('dashboard'))
        else:
            response = make_response(redirect(url_for('login_get')))
            response.set_cookie('session_cookie', '', expires=0)
            return response

    return render_template('login/login_test.html')


def login_post():
    session_cookie = request.cookies.get('session_cookie')

    username = request.form['username']
    password = request.form['password']
    client_info = request.form.get('client_info')

    # Informations de la requête (req)
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    req_headers = dict(request.headers)

    with Session(engine) as sessionuser:
        user = sessionuser.exec(
            select(User).where(User.username == username)
        ).one_or_none()

    if user and check_password_hash(user.password_hash, password):
        if user.banned:
            error_message = "Votre compte a été banni."
            return redirect(url_for('login_get'))

        session_cookie = generate_session_cookie()

        with Session(engine) as sessionuser:
            user = sessionuser.exec(
                select(User).where(User.id == user.id)
            ).one()

            session['user_id'] = user.id
            session['admin_level'] = user.admin_level

            user.session_cookie = session_cookie
            user.online = True  # Mettre l'utilisateur en ligne
            sessionuser.add(user)
            sessionuser.commit()

        # Informations de la réponse (res)
        response = make_response(redirect(url_for('dashboard')))
        response_headers = dict(response.headers)

        # Logique pour afficher ou stocker les informations du navigateur client, req et res
        if client_info:
            client_info_dict = json.loads(client_info)
            client_info_dict.update({
                'user_ip': user_ip,
                'user_agent': user_agent,
                'req_headers': req_headers,
                'res_headers': response_headers,
            })
            # print("Informations de connexion de l'utilisateur :", client_info_dict)
            # Optionnel : Stocker les informations de connexion dans la base de données

        response.set_cookie('session_cookie', session_cookie)
        return response
    else:
        error_message = "Nom d'utilisateur ou mot de passe incorrect."
        return redirect(url_for('login_get'))
