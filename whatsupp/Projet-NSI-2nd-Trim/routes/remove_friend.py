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

def remove_friend():
    data = request.get_json()
    contact_id = data.get('contact_id')
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        return jsonify({'error': 'Session non valide'}), 401

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.session_cookie == session_cookie)
        ).one_or_none()

    if not user:
        return jsonify({'error': 'Utilisateur introuvable'}), 404

    user_id = user.id

    # Supprimer l'ami de la liste de contacts
    with Session(engine) as session:
        contact = session.exec(
            select(Contact).where(
                (Contact.user_id == user_id) & (Contact.contact_id == contact_id)
            )
        ).one_or_none()

        if contact:
            session.delete(contact)
            session.commit()

        # Supprimer également la relation inverse (si elle existe)
        inverse_contact = session.exec(
            select(Contact).where(
                (Contact.user_id == contact_id) & (Contact.contact_id == user_id)
            )
        ).one_or_none()

        if inverse_contact:
            session.delete(inverse_contact)
            session.commit()

    return jsonify({'message': 'Ami supprimé avec succès'}), 200
