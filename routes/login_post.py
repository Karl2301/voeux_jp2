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

def login_post():
    
    identifiant = request.form['identifiant']

    with Session(engine) as session:
        statement = select(Student).where(Student.identifiant_unique == identifiant)
        user_eleve = session.exec(statement).one_or_none()

        statement = select(Professeurs).where(Professeurs.username == identifiant)
        user_prof = session.exec(statement).one_or_none()


        if user_eleve:
            print("eleve")
            cookie_value = str(uuid.uuid4())

            user_eleve.cookie = cookie_value
            session.add(user_eleve)
            session.commit()

            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('session_cookie', cookie_value)
            return response
        
        elif user_prof:
            print("prof")
            print(user_prof)
            password=request.form.get('password')
            username=request.form.get('identifiant_hidden')
            if password != None:                    #si on recupere un mdp alors on verifie le login
                if password == user_prof.password and username == user_prof.username :
                    return redirect(url_for('login_get'))           #faut tester je n'ai pas accès
            return redirect(url_for('login_get'))
        
        else:
            flash('Identifiant non trouvé', 'error')
            return redirect(url_for('login_get'))
        