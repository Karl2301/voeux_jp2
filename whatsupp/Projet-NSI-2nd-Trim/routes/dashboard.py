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

def dashboard(contact_id):
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
        return response

    if not user.verified_email:
        app.logger.error('Email pas vérifié')
        return render_template('dashboard/no_verified_email.html')

    user_theme = ""
    if user.dashboard_theme:
        user_theme = "styles-light.css"
    else:
        user_theme = "styles-dark.css"


    user_content = user.model_dump()
    is_user_admin = user_content.get('admin')

    with Session(engine) as session:
        statement = select(Contact).where(Contact.user_id == user_content['id'])
        user_contacts = session.exec(statement).all()

    if user_contacts and not contact_id:
        first_contact_id = user_contacts[0].contact_id
        return redirect(url_for('dashboard', contact_id=first_contact_id))

    contact_user_dict = None

    if contact_id:
        with Session(engine) as session:
            statement = select(User).where(User.session_cookie == session_cookie)
            user = session.exec(statement).one_or_none()
            user.window_location = "/dashboard/"+str(contact_id)
            session.add(user)
            session.commit()

        with Session(engine) as session:
            statement = select(User).where(User.id == contact_id)
            contact_user = session.exec(statement).one_or_none()

        if not contact_user:
            app.logger.error('Contact user not found.')
            return render_template('page_not_found/404.html'), 404

        contact_user_dict = contact_user.model_dump()

    user_list_contacts = [contact.model_dump() for contact in user_contacts]
    has_contacts = bool(user_list_contacts)

    return render_template('dashboard/dashboard.html', user=user_content, user_conv=contact_user_dict, user_list_contacts=user_list_contacts, has_contacts=has_contacts, is_admin=is_user_admin, theme=user_theme)
