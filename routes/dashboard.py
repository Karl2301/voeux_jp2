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

def dashboard():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            statement = select(Student).where(Student.cookie == session_cookie)
            user = session.exec(statement).first()
            if user:
                return render_template('dashboard/index.html')
            else:
                return redirect(url_for('login_get'))

        

    return render_template('dashboard/index.html')