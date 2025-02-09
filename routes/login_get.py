"""
Ce fichier définit la route pour la méthode GET de la page de connexion dans l'application Flask.
Fonctionnalité:
- Vérifie si un cookie de session est présent dans la requête.
- Si un cookie de session est trouvé, il tente de récupérer l'utilisateur correspondant dans la base de données.
- Si l'utilisateur est trouvé, il redirige vers le tableau de bord.
- Si aucun cookie de session n'est trouvé ou si l'utilisateur n'est pas trouvé, il affiche la page de connexion.
Utilisation:
- Ce fichier est utilisé lorsque l'utilisateur accède à la page de connexion de l'application.
"""

from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json

def login_get():
    session_cookie = request.cookies.get('session_cookie')
    print(session_cookie)

    if session_cookie:
        with Session(engine) as session:
            statement = select(Student).where(Student.cookie == session_cookie)
            user = session.exec(statement).first()
            if user:
                return redirect(url_for('dashboard'))

        
    return render_template('login/index.html')