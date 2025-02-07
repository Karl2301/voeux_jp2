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
from SQLClassSQL import Student
from ext_config import app, engine
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
import uuid

def get_data():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            statement = select(Student).where(Student.cookie == session_cookie)
            user = session.exec(statement).first()
            if user:
                return jsonify({
                    'identifiant_unique': user.identifiant_unique,
                    'cookie': user.cookie,
                    'niveau_classe': user.niveau_classe,
                    'voeux_etablissements': user.voeux_etablissements,
                    'online': user.online,
                    'deja_connecte': user.deja_connecte,
                    'choix_validees': user.choix_validees
                })
            else:
                return redirect(url_for('login_get'))
    else:
        return redirect(url_for('login_get'))