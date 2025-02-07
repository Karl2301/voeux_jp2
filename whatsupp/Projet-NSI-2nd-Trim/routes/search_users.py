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
from sqlmodel import Field, Session, SQLModel, create_engine, select, update, and_, or_
from SQLClassDB import User, Contact, Conversation, Report, FriendRequest, Image
from uuid import UUID, uuid4
from sqlalchemy.orm import aliased
from cryptography.fernet import Fernet
from .fonctions import app, engine, key, cipher_suite, encrypt_message, decrypt_message, get_db_connection, generate_session_cookie, get_users_info, get_messages_between_users
from extensions import engine, app, socketio, cipher_suite, key

def search_users():
    session_cookie = request.cookies.get('session_cookie')

    if not session_cookie:
        return jsonify({'error': 'Session non valide'}), 401

    query = request.args.get('query', '').strip().lower()
    query_parts = query.split()

    with Session(engine) as session:
        statement = select(User).where(User.session_cookie == session_cookie)
        user = session.exec(statement).one_or_none()

    if not user:
        return jsonify({'error': 'Utilisateur introuvable'}), 404

    user_id = user.id

    with Session(engine) as session:
        if len(query_parts) == 2:
            first_name_query, last_name_query = query_parts
            statement = (
                select(User)
                .where(
                    and_(
                        User.id != user_id,
                        User.first_name.ilike(f"{first_name_query}%"),
                        User.last_name.ilike(f"{last_name_query}%")
                    )
                )
                .limit(10)
            )
        else:
            statement = (
                select(User)
                .where(
                    and_(
                        User.id != user_id,
                        or_(
                            User.username.ilike(f"{query}%"),
                            User.first_name.ilike(f"{query}%"),
                            User.last_name.ilike(f"{query}%")
                        )
                    )
                )
                .limit(10)
            )
        users = session.exec(statement).all()

    user_list = [
        {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_image': user.profile_image
        }
        for user in users
    ]
    return jsonify(user_list)
