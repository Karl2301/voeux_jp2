from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response
from ext_config import *
from sqlmodel import Session, select
import json
from flask_socketio import SocketIO, emit, join_room, leave_room


def change_password_get():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            statement = select(Users).where(Users.cookie == session_cookie)
            user = session.exec(statement).one_or_none()
            if user:
                return render_template('change_password/index.html', user=user)
    flash('Veuillez vous connecter.')
    return redirect(url_for('login_get'))

def change_password_post():
    session_cookie = request.cookies.get('session_cookie')
    if not session_cookie:
        flash('Veuillez vous connecter.')
        return redirect(url_for('login_get'))
    
    # Récupération des valeurs du formulaire
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not current_password or not new_password or not confirm_password:
        flash('Veuillez remplir tous les champs.')
        return redirect(url_for('change_password_get'))
    
    if new_password != confirm_password:
        flash('Les nouveaux mots de passe ne correspondent pas.')
        return redirect(url_for('change_password_get'))
    
    with Session(engine) as session:
        statement = select(Users).where(Users.cookie == session_cookie)
        user = session.exec(statement).one_or_none()
        if user:
            # Vérifier que le mot de passe actuel saisi correspond au mot de passe enregistré
            if user.password != current_password:
                flash('Mot de passe actuel invalide.')
                return redirect(url_for('change_password_get'))
            # Mise à jour du mot de passe de l'utilisateur
            user.password = new_password
            session.add(user)
            session.commit()
            flash('Mot de passe mis à jour avec succès.')
            return redirect(url_for('dashboard'))
        else:
            flash('Utilisateur non trouvé.')
            return redirect(url_for('login_get'))