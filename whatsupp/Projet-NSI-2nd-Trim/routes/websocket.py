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


@socketio.on('connect')
def handle_connect():
    session_cookie = request.cookies.get('session_cookie')

    if session_cookie:
        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.session_cookie == session_cookie)
            ).one_or_none()
            if user:
                user_id = str(user.id)
                user.online = True
                session.add(user)
                session.commit()

                # Rejoindre la room de l'utilisateur
                join_room(user_id)
                
                # Identifier les amis de l'utilisateur
                friends = session.exec(
                    select(Contact.contact_id).where(Contact.user_id == user.id)
                ).all()
                #print(friends)
                # Émettre un événement de connexion pour chaque ami
                for friend in friends:
                    friend_id = str(friend)
                    socketio.emit('friend_online', {'user_id': user.id}, room=friend_id)



@socketio.on('disconnect')
def handle_disconnect():
    session_cookie = request.cookies.get('session_cookie')

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.session_cookie == session_cookie)
        ).one_or_none()

        if user:
            user.online = False
            session.add(user)
            session.commit()
            emit('user_offline', {'user_id': user.id})


@socketio.on('send_message')
def handle_send_message(data):
    socketio.emit('receive_message', data, room=data['contact_id'])


@socketio.on('typing')
def handle_typing(data):
    socketio.emit('typing', data, room=data['to'])


@socketio.on('stop_typing')
def handle_stop_typing(data):
    socketio.emit('stop_typing', data, room=data['to'])

