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

def user_contacts():
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        return jsonify({'error': 'Session non valide'}), 401

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        user = session.exec(statement).one_or_none()

    if not user:
        return jsonify({'error': 'Utilisateur introuvable'}), 404

    user_id = user.id

    statement = (
        select(Contact, User)
        .join(User, Contact.contact_id == User.id)
        .where(Contact.user_id == user_id)
    )
    contacts = session.exec(statement).all()

    contacts_list = [
        {
            'id': contact.Contact.id,
            'user_id': contact.Contact.user_id,
            'contact_id': contact.Contact.contact_id,
            'last_message': contact.Contact.last_message,
            'last_message_date': contact.Contact.last_message_date,
            'unread_messages_count': contact.Contact.unread_messages_count,
            'first_name': contact.User.first_name,
            'last_name': contact.User.last_name,
            'profile_image': contact.User.profile_image,
        }
        for contact in contacts
    ]
    return jsonify(contacts_list)
