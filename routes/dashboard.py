"""
Ce fichier définit la route pour le tableau de bord (dashboard) de l'application Flask.
Fonctionnalité:
- La fonction `dashboard` gère la logique d'affichage du tableau de bord pour les utilisateurs authentifiés.
- Elle vérifie la présence d'un cookie de session et récupère l'utilisateur correspondant dans la base de données.
- Si l'utilisateur est trouvé, elle affiche la page du tableau de bord.
- Sinon, elle redirige l'utilisateur vers la page de connexion.
Utilisation:
- Ce fichier est utilisé lorsque l'utilisateur tente d'accéder à la route du tableau de bord.
"""

from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
from flask_socketio import SocketIO, emit, join_room, leave_room

def dashboard():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            user = session.exec(select(Users).where(Users.cookie == session_cookie)).first()
            if user:
                user_role = "Professeur" if user.professeur else "Élève"
                # Passez d'autres variables au template si nécessaire
                return render_template('dashboard/index.html', user_role=user_role)
    return redirect(url_for('login_get'))