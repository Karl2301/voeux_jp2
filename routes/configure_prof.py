from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
from flask_socketio import SocketIO, emit, join_room, leave_room

# Route pour afficher la page de configuration du mot de passe professeur



def configure_prof_get():
    session_cookie = request.cookies.get('session_cookie')

    with Session(engine) as session:
        statement = select(Users).where(Users.cookie == session_cookie)
        user = session.exec(statement).one_or_none()
        if user and user.password !="ProfMDP" :
            flash("Vous avez déjà configuré votre compte.", "error")
            return redirect(url_for('dashboard'))

    return render_template('configure_prof/index.html') 


def configure_prof_post():
    session_cookie = request.cookies.get('session_cookie')

    print("Cookie de session : ", session_cookie)
    if session_cookie is None:
        with Session(engine) as session:
            statement = select(Users).where(Users.cookie == session_cookie)
            user = session.exec(statement).one_or_none()
            if user == None:
                print("Vous devez être connecté pour configurer votre compte.")
                return redirect(url_for('login_get'))  

    prenom = request.form.get('prenom')
    nom = request.form.get('nom')
    
    password = request.form.get('password')
    password_confirm = request.form.get('confirm_password')


    print("Prénom reçu : ", prenom)
    print("Nom reçu : ", nom)
    
    print("Mot de passe reçu : ", password)
    print("Mot de passe confirmé reçu : ", password_confirm)


    
    if not password or not password_confirm or not prenom or not nom:
        print("Veuillez remplir tous les champs.")
        return redirect(url_for('configure_prof_get'))
    
    # Vérifier si les mots de passe correspondent
    if password != password_confirm:
        print("Les mots de passe ne correspondent pas.")
        return redirect(url_for('configure_prof_get'))
    

    
    with Session(engine) as session:
        user = session.exec(
            select(Users).where(Users.cookie == session_cookie)
        ).one_or_none()

        if user:
            user.password = password
            user.prenom = prenom
            user.nom = nom  
            session.add(user)
            session.commit()
            flash("Votre compte est bien configuré.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Utilisateur non trouvé.", "error")
            return redirect(url_for('login_get'))
