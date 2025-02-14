"""
Ce fichier contient la route pour la gestion de la connexion des utilisateurs dans l'application Flask.
Fonctionnalité principale:
- `login_post`: Cette fonction est appelée lorsqu'un utilisateur soumet le formulaire de connexion. Elle vérifie l'identifiant de l'utilisateur dans la base de données, génère un cookie de session unique, met à jour la base de données avec ce cookie, et le définit dans le navigateur de l'utilisateur.
Utilisation:
- Ce fichier est utilisé lorsque l'utilisateur tente de se connecter à l'application via le formulaire de connexion. Si l'identifiant est trouvé dans la base de données, l'utilisateur est redirigé vers la page d'accueil avec un cookie de session. Sinon, rien ne se passe.
"""

from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
import uuid
from flask_socketio import SocketIO, emit, join_room, leave_room

def login_post():
    """
    data = request.get_json()  # Récupérer le contenu du POST en JSON
    identifiant = data.get('identifiant')
    """

    session_cookie = request.cookies.get('session_cookie')

    identifiant = request.form['identifiant']
    password = request.form['password']

    with Session(engine) as sessionuser:
        user = sessionuser.exec(
            select(Users).where(Users.identifiant_unique == identifiant)
        ).one_or_none()

            

        if user and user.password == password:
            
            
            new_session_cookie = str(uuid.uuid4())

            session['user_id'] = user.identifiant_unique
            user.cookie = new_session_cookie
            user.online = True  # Mettre l'utilisateur en ligne
            
            sessionuser.add(user)
            sessionuser.commit()
            print("classe: ", user.niveau_classe)
            
            
            # Informations de la réponse (res)
            
            if user.professeur == True and user.password == "ProfMDP"  : # Si l'utilisateur est un professeur et n'a pas encore configuré son mot de passe
                response = make_response(redirect(url_for('configure_prof_get')))
            elif user.password == "EleveMDP": # Si l'utilisateur est un élève et n'a pas encore configuré son mot de passe
                response = make_response(redirect(url_for('configure_password_get')))
            else:
                response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('session_cookie', new_session_cookie)
            return response
        else:
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return render_template('login/index.html', error=error_message)


# EleveMDP