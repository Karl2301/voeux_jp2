from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
from flask_socketio import SocketIO, emit, join_room, leave_room

# Route pour afficher la page de configuration du mot de passe



def configure_password_get():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie is None:
        flash("Vous devez être connecté pour configurer votre mot de passe.")
        return redirect(url_for('login_get'))
    
    with Session(engine) as session:
        statement = select(Users).where(Users.cookie == session_cookie)
        user = session.exec(statement).one_or_none()

        if user:
            if user.password != "EleveMDP":
                flash("Vous avez déjà configuré votre mot de passe.", "info")
                return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login_get'))

    return render_template('configure_password/index.html') 



def configure_password_post():
    session_cookie = request.cookies.get('session_cookie')

    print("Cookie de session : ", session_cookie)
    if session_cookie is None:
        with Session(engine) as session:
            statement = select(Users).where(Users.cookie == session_cookie)
            user = session.exec(statement).one_or_none()
            if user == None:
                print("Vous devez être connecté pour configurer votre mot de passe.")
                return redirect(url_for('login_get'))  

    
    password = request.form.get('password')
    password_confirm = request.form.get('confirm_password')
    classe=request.form.get('classe')

    print("Mot de passe reçu : ", password)
    print("Mot de passe confirmé reçu : ", password_confirm)
    print("Classe reçue : ", classe)


    
    if not password or not password_confirm or not classe:
        print("Veuillez remplir tous les champs.")
        return redirect(url_for('configure_password_get'))
    
    # Vérifier si les mots de passe correspondent
    if password != password_confirm:
        print("Les mots de passe ne correspondent pas.")
        return redirect(url_for('configure_password_get'))
    

    
    with Session(engine) as session:
        user = session.exec(
            select(Users).where(Users.cookie == session_cookie)
        ).one_or_none()

        if user:
            user.password = password  
            user.niveau_classe = classe
            session.add(user)
            session.commit()
            flash("Mot de passe configuré avec succès.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Utilisateur non trouvé.", "error")
            return redirect(url_for('login_get'))
