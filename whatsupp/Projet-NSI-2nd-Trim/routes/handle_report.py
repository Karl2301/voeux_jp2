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

def handle_report():
    data = request.get_json()
    report_id = data.get('report_id')
    action = data.get('action')  # 'ban', 'refuse', 'warn'

    if not report_id or not action:
        return jsonify({'error': 'Report ID and action are required'}), 400

    with Session(engine) as session:
        # Récupération du signalement dans la même session
        statement = select(Report).where(Report.id == report_id)
        report = session.exec(statement).one_or_none()

        if not report:
            return jsonify({'error': 'Signalement non trouvé'}), 404

        if action == 'ban':
            # Récupérer les informations sur l'utilisateur signalé
            statement = select(User).where(User.id == report.reported_user_id)
            user = session.exec(statement).one_or_none()

            if user:
                user.banned = True
                user.reason = report.reason  # Enregistrez la raison du ban si nécessaire
                session.add(user)

        elif action == 'warn':
            # Envoi d'un email d'avertissement (à implémenter)
            statement = select(User).where(User.id == report.reported_user_id)
            user = session.exec(statement).one_or_none()

            if user:
                pass
                #send_warning_email(user.email)  # Assurez-vous que cette fonction existe

        # Supprimer le signalement traité
        session.delete(report)
        session.commit()

    return jsonify({'success': True})
