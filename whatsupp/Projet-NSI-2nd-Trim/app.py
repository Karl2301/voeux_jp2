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
from datetime import datetime, timezone, UTC
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, update, and_
from SQLClassDB import *
from uuid import UUID, uuid4
from sqlalchemy.orm import aliased
from cryptography.fernet import Fernet
from routes import *
from threading import Thread, Event
from extensions import engine, app, socketio, cipher_suite, key, thread_stop_event, thread
import time
from sqlalchemy.sql import func
from typing import List
import json


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.before_request
def before_request():
    try:
        # Essayez de lire l'en-tête de la requête
        request.headers.get('User-Agent')
    except ssl.SSLError:
        # Si une erreur SSL est détectée, renvoyer une erreur 400
        abort(400)


app.add_url_rule('/', view_func=home)
app.add_url_rule('/about_us', view_func=about_us)
app.add_url_rule('/about_among_us', view_func=about_among_us)
app.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=login_get, methods=['GET'])
app.add_url_rule('/login', view_func=login_post, methods=['POST'])
app.add_url_rule('/dashboard',defaults={'contact_id': None} , view_func=dashboard)
app.add_url_rule('/dashboard/<contact_id>/', view_func=dashboard)
app.add_url_rule('/reset_password', view_func=reset_password, methods=['GET', 'POST'])
app.add_url_rule('/admin', view_func=admin, methods=['GET'])
app.add_url_rule('/report_user', view_func=report_user, methods=['POST'])
app.add_url_rule('/reports', view_func=reports, methods=['GET'])
app.add_url_rule('/get_messages/<contact_id>', 'get_messages', get_messages, methods=['GET'])
app.add_url_rule('/update_user/<user_id>', view_func=update_user, methods=['POST'])
app.add_url_rule('/delete_user/<user_id>', view_func=delete_user, methods=['POST'])
app.add_url_rule('/new_user_conv', view_func=search_user, methods=['POST'])
app.add_url_rule('/search_users', 'search_users', search_users, methods=['GET'])
app.add_url_rule('/send_friend_request', view_func=send_friend_request, methods=['POST'])
app.add_url_rule('/friend_requests', view_func=friend_requests)
app.add_url_rule('/accept_friend_request', view_func=accept_friend_request, methods=['POST'])
app.add_url_rule('/reject_friend_request', view_func=reject_friend_request, methods=['POST'])
app.add_url_rule('/user_contacts', view_func=user_contacts, methods=['GET'])
app.add_url_rule('/user_conversations', view_func=user_conversations, methods=['POST'])
app.add_url_rule('/logout', view_func=logout, methods=['POST'])
app.add_url_rule('/send_message', view_func=send_message, methods=['POST'])
app.add_url_rule('/delete_message', view_func=delete_message, methods=['DELETE'])
app.add_url_rule('/update_user_info', view_func=update_user_info, methods=['POST'])
app.add_url_rule('/change_password', view_func=change_password, methods=['POST'])
app.add_url_rule('/handle_report', view_func=handle_report, methods=['POST'])
app.add_url_rule('/remove_friend', view_func=remove_friend, methods=['POST'])
app.add_url_rule('/upload_image', view_func=upload_image, methods=['POST'])
app.add_url_rule('/get_user_id', view_func=get_user_id, methods=['GET'])
app.add_url_rule('/otp_verif', view_func=otp_verif, methods=['POST'])
app.add_url_rule('/new_password/<token>/', view_func=new_password, methods=['GET', 'POST'])
app.add_url_rule('/email_sent', view_func=email_sent, methods=['GET'])
app.add_url_rule('/admin_panel', view_func=admin_panel, methods=['GET'])
app.add_url_rule('/admin_panel_users', view_func=list_user_on_app, methods=['GET'])
app.add_url_rule('/user_info/<user_id>', view_func=user_info_admin, methods=['GET'])
app.add_url_rule('/user_info_get/<user_id>', view_func=get_user_info, methods=['GET'])
app.add_url_rule('/update_user_admin_info/<user_id>', view_func=update_user_admin_info, methods=['POST'])
app.add_url_rule('/user_banned', view_func=user_banned, methods=['GET'])
app.add_url_rule('/update-dashboard-theme', view_func=update_dashboard_theme, methods=['POST'])
app.add_url_rule('/unban_user/<userId>', view_func=user_banned_post, methods=['POST'])
app.add_url_rule('/user_report', view_func=user_report_page, methods=['GET'])
app.add_url_rule('/user_report_post', view_func=user_report_post, methods=['POST'])


def serialize_datetime(obj):
    """Convertit les objets datetime en chaîne de caractères ISO 8601."""
    if isinstance(obj, datetime):
        return obj.isoformat()  # ISO 8601 format
    return obj  # Retourne l'objet tel quel s'il n'est pas un datetime


def serialize_user(user):
    """Convertit un objet User et ses propriétés pour être sérialisé en JSON."""
    user_data = user.model_dump()  # Convertit l'objet User en dictionnaire
    user_data = {key: serialize_datetime(val) for key, val in user_data.items()}
    return user_data


def fetch_stats():
    """Récupère les statistiques depuis la base de données."""
    with Session(engine) as session:
        # Récupération des statistiques globales
        total_users = len(session.exec(select(User)).all())
        active_users = len(session.exec(select(User).where(User.online == True)).all())
        total_messages = len(session.exec(select(Conversation)).all())
        messages_today = len(session.exec(select(Conversation).where(Conversation.publish_at >= datetime.now(UTC).date())).all())
        total_friend_requests = len(session.exec(select(FriendRequest)).all())
        total_accepted_friend_requests = int(len(session.exec(select(Contact)).all()) / 2)
        total_reports = len(session.exec(select(Report)).all())
        new_users_today = len(session.exec(select(User).where(User.created_at >= datetime.now(UTC).date())).all())
        unread_messages_result = session.exec(select(Contact.unread_messages_count))
        unread_messages = sum(unread_messages_result)
        banned_users = len(session.exec(select(User).where(User.banned == True)).all())
        password_reset_requests = len(session.exec(select(ResetPassword)).all())
        resolved_reports = len(session.exec(select(Report).where(Report.status == "resolved")).all())
        total_friends = len(session.exec(select(Contact)).all())
        avg_friends_per_user = total_friends / total_users if total_users > 0 else 0
        avg_messages_per_user = total_messages / total_users if total_users > 0 else 0
        one_week_ago = datetime.now(UTC) - timedelta(days=7)
        users_last_week = len(session.exec(select(User).where(User.created_at >= one_week_ago)).all())
        messages_last_week = len(session.exec(select(Conversation).where(Conversation.publish_at >= one_week_ago)).all())
        total_contacts = len(session.exec(select(Contact)).all())
        active_conversations = len(session.exec(select(Conversation).where(Conversation.last_message.isnot(None))).all())
        avg_messages_per_conversation = total_messages / active_conversations if active_conversations > 0 else 0

        # Récupérer la liste des utilisateurs en ligne
        verified_users_counter = len(session.exec(select(User).where(User.verified_email == True)).all())
        online_users_query = session.exec(select(User).where(User.online == True)).all()
        banned_users_query = session.exec(select(User).where(User.banned == True)).all()
        pending_reports_query = session.exec(
            select(Report, User)
            .join(User, Report.reported_user_id == User.id)
            .where(Report.status == "pending")
        ).all()

        pending_reports = [
            {
            "report_id": report.id,
            "reported_user": serialize_user(reported_user),
            "reporter_user": serialize_user(session.get(User, report.reporter_user_id)),
            "reason": report.reason
            }
            for report, reported_user in pending_reports_query
        ]

        # Sérialiser les utilisateurs en ligne
        online_users = [
            serialize_user(user)  # Utiliser la fonction de sérialisation pour convertir les utilisateurs en ligne
            for user in online_users_query
        ]

        banned_users_list = [
            serialize_user(user)  # Utiliser la fonction de sérialisation pour convertir les utilisateurs en ligne
            for user in banned_users_query
        ]

        total_users_query = session.exec(select(User)).all()
        total_users_info = [
            serialize_user(user)  # Utiliser la fonction de sérialisation pour convertir les utilisateurs en ligne
            for user in total_users_query
        ]

        # Récupérer les 10 utilisateurs ayant envoyé le plus de messages
        most_active_users_query = session.exec(
            select(User, func.count(Conversation.id).label('message_count'))
            .join(Conversation, Conversation.user_id == User.id)
            .group_by(User.id)
            .order_by(func.count(Conversation.id).desc())
            .limit(10)
        ).all()

        most_active_users = [
            {**serialize_user(user), "message_count": message_count}
            for user, message_count in most_active_users_query
        ]

        # Récupérer les 10 utilisateurs les plus récents
        recent_users_query = session.exec(
            select(User)
            .order_by(User.created_at.desc())
            .limit(10)
        ).all()

        recent_users = [
            {**serialize_user(user), "message_count": session.exec(
                select(func.count(Conversation.id))
                .where(Conversation.user_id == user.id)
            ).one()}
            for user in recent_users_query
        ]

        # Convertir toutes les dates en chaînes de caractères (ISO 8601)
        stats = {
            'total_users': total_users,
            'banned_users_list': banned_users_list,
            'report_users_list': pending_reports,
            'total_users_info': total_users_info,
            'active_users': active_users,
            'verified_users': verified_users_counter,
            'total_messages': total_messages,
            'messages_today': messages_today,
            'total_friend_requests': total_friend_requests,
            'total_accepted_friend_requests': total_accepted_friend_requests,
            'total_reports': total_reports,
            'new_users_today': new_users_today,
            'unread_messages': unread_messages,
            'banned_users': banned_users,
            'password_reset_requests': password_reset_requests,
            'resolved_reports': resolved_reports,
            'avg_friends_per_user': avg_friends_per_user,
            'avg_messages_per_user': avg_messages_per_user,
            'users_last_week': users_last_week,
            'messages_last_week': messages_last_week,
            'total_contacts': total_contacts,
            'active_conversations': active_conversations,
            'avg_messages_per_conversation': avg_messages_per_conversation,
            'most_active_users': most_active_users,
            'recent_users': recent_users,
            'online_users': online_users
        }

        about_us = {"online_users":active_users, "total_users":total_users}
        stats = {key: serialize_datetime(val) if isinstance(val, datetime) else val for key, val in stats.items()}

        return {"stats":stats, "about_us": about_us}



def data_stream():
    """Envoie les statistiques toutes les 1 seconde."""
    while not thread_stop_event.is_set():
        stats_all = fetch_stats()
        stats = stats_all["stats"]
        about_us = stats_all["about_us"]
        socketio.emit('update_data_about_us', about_us)
        with Session(engine) as sessionuser:
            users = sessionuser.exec(
                select(User).where(User.admin == True)
            ).all()
            for u in users:
                userid = u.id
                is_admin = u.admin
                admin_level = u.admin_level

                # Séparation des niveaux d'admin et impression des informations
                if admin_level == 0:
                    #print(f"UUID: {userid}, Admin: {is_admin}, Niveau Admin: {admin_level} (Niveau 0)")
                    pass
                elif admin_level == 1:
                    #print(f"UUID: {userid}, Admin: {is_admin}, Niveau Admin: {admin_level} (Niveau 1)")
                    pass
                elif admin_level == 2:
                    #print(f"UUID: {userid}, Admin: {is_admin}, Niveau Admin: {admin_level} (Niveau 2)")
                    pass
                elif admin_level == 3:
                    #print(f"UUID: {userid}, Admin: {is_admin}, Niveau Admin: {admin_level} (Niveau 3)")
                    pass
                elif admin_level == 4:
                    #print(f"UUID: {userid}, Admin: {is_admin}, Niveau Admin: {admin_level} (Niveau 4)")
                    pass

                # Envoyer les statistiques à l'utilisateur
                socketio.emit('update_data', stats, room=userid)
                
            time.sleep(0.5)




@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found/404.html'), 404

if __name__ == '__main__':
    create_db_and_tables()
    thread = Thread(target=data_stream)
    thread.daemon = True
    thread.start()
    socketio.run(app, host='0.0.0.0', port=8098, debug=True)

