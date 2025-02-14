"""
Ce fichier contient une fonction pour récupérer les données d'un utilisateur connecté à partir de la base de données.

Fonctionnalités :
- Vérifie si un cookie de session est présent dans la requête.
- Si le cookie est présent, récupère les informations de l'utilisateur associé à ce cookie depuis la base de données.
- Retourne les informations de l'utilisateur sous forme de JSON si l'utilisateur est trouvé.
- Redirige vers la page de connexion si le cookie de session est absent ou si l'utilisateur n'est pas trouvé.

Ce fichier est utilisé pour gérer les requêtes de récupération de données utilisateur dans une application Flask.
"""

from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
import uuid
from flask_socketio import SocketIO, emit, join_room, leave_room

def get_data():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            statement = select(Users).where(Users.cookie == session_cookie)
            user = session.exec(statement).first()
            if user:
                if user.professeur == 0: # C'est un élève
                    return jsonify({
                        'identifiant_unique': user.identifiant_unique,
                        'cookie': user.cookie,
                        'niveau_classe': user.niveau_classe,
                        'voeux_etablissements': user.voeux_etablissements,
                        'online': user.online,
                        'deja_connecte': user.deja_connecte,
                        'choix_validees': user.choix_validees,
                        'professeur': user.professeur,
                        'status_class': 'status.delivered' if user.online else 'status.offline'
                    })
                else: # c'est un prof
                    eleve_online_count = len(session.exec(select(Users).where((Users.online == 1) & (Users.professeur == 0))).all())
                    eleve_choix_validees_count = len(session.exec(select(Users).where(Users.choix_validees == 1)).all())
                    # Récupérer le tableau niveau_classe du professeur dans le tableau mysql "utilisateurs"
                    niveau_classe = json.loads(user.niveau_classe)
                    
                    # Récupérer les demandes d'identifiants perdus pour les classes spécifiées
                    identifiant_perdus_count = len(session.exec(select(IdentifiantPerdus).where(IdentifiantPerdus.classe.in_(niveau_classe))).all())

                    niveau_classe_list = json.loads(session.exec(select(Users).where(Users.cookie == session_cookie)).one_or_none().niveau_classe)
                    
                    # Calculer le nombre d'élèves dans les classes spécifiées

                    return jsonify({
                        'identifiant_unique': user.identifiant_unique,
                        'cookie': user.cookie,
                        'niveau_classe': user.niveau_classe,
                        'online': user.online,
                        'deja_connecte': user.deja_connecte,
                        'professeur': user.professeur,
                        'eleve_online': eleve_online_count,
                        'eleve_choix_validees': eleve_choix_validees_count,
                        'identifiant_perdus': identifiant_perdus_count,
                        'classes': len(niveau_classe_list),
                        'status_class': 'status.delivered' if user.online else 'status.offline'
                    })
            else:
                return redirect(url_for('login_get'))
    else:
        return redirect(url_for('login_get'))


def get_voeux_status():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            statement = select(Users).where(Users.cookie == session_cookie)
            user = session.exec(statement).first()
            if user:
                return jsonify({
                    'choix_validees': user.choix_validees
                })
            else:
                return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify({'error': 'No session cookie'}), 400
    

def post_voeux_status():
    session_cookie = request.cookies.get('session_cookie')
    data = request.get_json()  # Récupérer le contenu du POST en JSON
    choix_validees = data.get('validate')
    
    if session_cookie:
        with Session(engine) as session:
            statement = select(Users).where(Users.cookie == session_cookie)
            user = session.exec(statement).one_or_none()
            if user:
                user.choix_validees = choix_validees
                session.add(user)
                session.commit()
                return {'status': 'success'}
            else:
                return redirect(url_for('login_get'))
    else:
        return redirect(url_for('login_get'))