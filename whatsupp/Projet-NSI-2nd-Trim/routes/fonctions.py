from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import uuid
import os
import base64
import hashlib
import requests
import ssl
from datetime import datetime, timezone
from typing import Optional, Dict
from sqlmodel import Field, Session, SQLModel, create_engine, select, update, and_
from SQLClassDB import User, Contact, Conversation, Report, FriendRequest, Image
from uuid import UUID, uuid4
from sqlalchemy.orm import aliased
from cryptography.fernet import Fernet
from extensions import engine, app, socketio, cipher_suite, key

def encrypt_message(message: str) -> str:
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message.decode()

def decrypt_message(encrypted_message: str) -> str:
    decrypted_message = cipher_suite.decrypt(encrypted_message.encode())
    return decrypted_message.decode()


def get_db_connection():
    conn = sqlite3.connect('db.sqlite', timeout=10)  # Augmentez le timeout à 10 secondes
    conn.row_factory = sqlite3.Row
    return conn

def generate_session_cookie():
    return hashlib.sha256(os.urandom(24)).hexdigest()

def get_users_info(user1_id: str, user2_id: str) -> Optional[Dict[str, Dict[str, str]]]:
    with Session(engine) as session:
        statement = select(User).where(User.id.in_([user1_id, user2_id]))
        users = session.exec(statement).all()

    if len(users) != 2:
        return None

    user_info = {'user_requester_info': {}, 'user_contact_info': {}}
    for user in users:
        if user.id == user1_id:
            user_info['user_requester_info'] = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_image': user.profile_image
            }
        else:
            user_info['user_contact_info'] = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_image': user.profile_image
            }

    return user_info


def get_messages_between_users(user1_id: str, user2_id: str):
    with Session(engine) as session:
        statement = select(
            Conversation.id,
            Conversation.user_id.label('sender_id'),
            Conversation.last_message.label('message'),
            Conversation.type.label('type'),
            Conversation.publish_at.label('send_time'),
            Conversation.contact_id.label('recipient_id')
        ).where(
            ((Conversation.user_id == user1_id) & (Conversation.contact_id == user2_id)) |
            ((Conversation.user_id == user2_id) & (Conversation.contact_id == user1_id))
        ).order_by(Conversation.publish_at).limit(200)

        messages = session.exec(statement).all()

    # Déchiffrer les messages
    messages_list = [
        {
            'id': message.id,
            'sender_id': message.sender_id,
            'message': decrypt_message(message.message),
            'type': message.type,
            'send_time': message.send_time,
            'recipient_id': message.recipient_id
        }
        for message in messages
    ]

    return messages_list