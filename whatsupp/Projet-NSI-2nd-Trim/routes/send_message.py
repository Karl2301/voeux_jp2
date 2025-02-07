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

def send_message():
    session_cookie = request.cookies.get('session_cookie')
    data = request.get_json()
    contact_id = data.get('contact_id')
    message_content = data.get('message')
    message_type = data.get('message_type')  # Récupérer le type du message
    # print(message_type)
    uuid_id = data.get('id')

    if not session_cookie:
        return jsonify({'error': 'Session non valide'}), 401

    if not contact_id or not message_content or not message_type:
        return jsonify({'error': 'Contact ID, message et type de message requis'}), 400

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        user = session.exec(statement).one_or_none()

    if not user:
        return jsonify({'error': 'Utilisateur introuvable'}), 404

    with Session(engine) as session:
        statement = select(User).where(User.id == contact_id)
        user_in_contact = session.exec(statement).one_or_none()

    user_id = user.id
    contact_location = str(user_in_contact.window_location).replace("/dashboard/", "")
    is_both_on_the_same_page = contact_location == user_id

    now = datetime.now(timezone.utc)
    message_id = str(uuid_id)  # Générer un identifiant unique pour le message

    if message_type == 'base64':
        encrypted_message = message_content  # Si le message est en base64, ne pas le chiffrer
    else:
        encrypted_message = encrypt_message(message_content)  # Sinon, chiffrer le message

    new_conversation = Conversation(
        id=message_id,
        user_id=user_id,
        contact_id=contact_id,
        last_message=encrypted_message,
        publish_at=now,  # Utiliser un objet datetime au lieu d'une chaîne
        type=message_type  # Ajouter le type de message
    )
    session.add(new_conversation)

    statement = select(Contact).where(
        and_(Contact.user_id == contact_id, Contact.contact_id == user_id)
    ).limit(1)
    contact = session.exec(statement).one_or_none()


    if message_type == 'image':
        # print("base64")
        message_content = "Piece jointe"


    socketio.emit('update_unread_message', {
        'contact_id': user_id,
        'unread_messages': message_content,
        'message_type': message_type
        }, room=contact_id)
    
    socketio.emit('update_unread_message', {
        'contact_id': contact_id,
        'unread_messages': message_content,
        'message_type': message_type
        }, room=user_id)
    
    
    
    if is_both_on_the_same_page:
        # Envoyer le message via WebSocket
        socketio.emit('receive_message', {
            'id': message_id,
            'sender_id': user_id,
            'message': message_content,
            'send_time': now.isoformat(),  # Utiliser datetime maintenant avec timezone UTC
            'to': contact_id,
            'message_type': message_type
        }, room=contact_id)

    else:
        if contact:
            contact.unread_messages_count += 1
            session.add(contact)

        socketio.emit('update_unread_counter', {
            'contact_id': user_id,
            'unread_messages': 1,
            'message_type': message_type
            }, room=contact_id)

    session.commit()

    return jsonify({'success': True, 'message_id': message_id})
