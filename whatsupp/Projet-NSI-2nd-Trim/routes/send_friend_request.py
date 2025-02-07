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

def send_friend_request():
    data = request.get_json()
    receiver_id = data.get('receiver_id')  # Convertir en UUID
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        return jsonify({'error': 'Session non valide'}), 401

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        requester = session.exec(statement).one_or_none()

        if not requester:
            return jsonify({'error': 'Utilisateur demandeur introuvable'}), 404

        requester_id = str(requester.id)  # Convertir en UUID
        requester_username = requester.username
        requester_first_name = requester.first_name
        requester_last_name = requester.last_name
        profile_image = requester.profile_image

        # Vérifier si les utilisateurs sont déjà amis
        statement = select(Contact).where(
            (Contact.user_id == requester_id) & (Contact.contact_id == receiver_id)
        )
        existing_friendship = session.exec(statement).one_or_none()

        if existing_friendship:
            return jsonify({'error': 'Les utilisateurs sont déjà amis'}), 409
            

        # Vérifier s'il existe déjà une demande d'ami
        statement = select(FriendRequest).where(
            FriendRequest.requester_id == requester_id,
            FriendRequest.receiver_id == receiver_id
        )
        existing_request = session.exec(statement).one_or_none()

        if existing_request:
            return jsonify({'error': 'Une demande d\'ami existe déjà'}), 409

        new_friend_request = FriendRequest(
            requester_id=requester_id,
            receiver_id=receiver_id,
            requester_first_name=requester_first_name,
            requester_last_name=requester_last_name
        )
        session.add(new_friend_request)
        session.commit()

        request_id = new_friend_request.request_id

        # Notifie l'utilisateur cible via WebSocket
        socketio.emit(
            'friend_request', {
                'requester_id': str(requester_id),
                'receiver_id': str(receiver_id),
                'requester_username': requester_username,
                'profile_image': profile_image,
                'requester_first_name': requester_first_name,
                'request_id': request_id,
                'requester_last_name': requester_last_name
            }, room=str(receiver_id)
        )

    return jsonify({'message': 'Demande d\'ami envoyée avec succès'}), 201
