"""
Fonctionnalité:
- La fonction `logout` gère la déconnexion de l'utilisateur en supprimant le cookie de session de l'utilisateur et en réinitialisant le cookie stocké dans la base de données.

Utilisation:
- Cette route est appelée lorsque l'utilisateur souhaite se déconnecter de l'application. Elle vérifie si un cookie de session est présent, et si oui, elle réinitialise le cookie associé à l'utilisateur dans la base de données et supprime le cookie de session du navigateur de l'utilisateur.

Modules importés:
- flask: Pour gérer les requêtes HTTP et les sessions.
- SQLClassSQL: Pour interagir avec la classe `Student`.
- ext_config: Pour obtenir l'application Flask et le moteur de base de données.
- werkzeug.security: Pour les fonctions de hachage de mot de passe.
- sqlmodel: Pour les sessions et les requêtes SQL.
- json, uuid: Pour la manipulation de données JSON et la génération d'identifiants uniques.
"""

from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from SQLClassSQL import Student
from ext_config import app, engine
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
import uuid

def logout():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            statement = select(Student).where(Student.cookie == session_cookie)
            user = session.exec(statement).first()
            if user:
                user.cookie = None
                session.add(user)
                session.commit()
    response = make_response(redirect(url_for('home')))
    response.set_cookie('session_cookie', '', expires=0)
    return response