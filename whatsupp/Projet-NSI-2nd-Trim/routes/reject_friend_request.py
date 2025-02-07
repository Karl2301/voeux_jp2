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

def reject_friend_request():
    
    data = request.get_json()
    request_id = data.get('request_id')
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        return jsonify({'error': 'Session non valide'}), 401

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        user = session.exec(statement).one_or_none()

    if not user:
        return jsonify({'error': 'Utilisateur introuvable'}), 404

    user_id = user.id

    statement = select(FriendRequest).where(FriendRequest.request_id == request_id)
    friend_request = session.exec(statement).one_or_none()

    if not friend_request or str(friend_request.receiver_id) != user_id:
        return jsonify({'error': 'Demande d\'ami introuvable ou non autorisée'}), 404

    # Supprimer la demande d'ami refusée
    session.delete(friend_request)
    session.commit()

    # Supprimer la demande d'ami de la liste d'ajout des amis
    socketio.emit('remove_friend_request', {'request_id': request_id}, room=str(user_id))

    return jsonify({'message': 'Demande d\'ami refusée et supprimée'}), 200
