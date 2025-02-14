"""
Ce fichier définit les routes pour la gestion de l'aide pour l'application Flask.
Fonctionnalités principales:
- aide_get : Affiche le formulaire d’aide si l’utilisateur est authentifié, sinon redirige vers login_get.
- submit_help : Traite le formulaire d’aide soumis et redirige vers le dashboard s’il y a un cookie de session, sinon vers login_get.
"""

from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
from flask_socketio import SocketIO, emit, join_room, leave_room
import datetime

def aide_get():
    """
    Affiche le formulaire d’aide si un cookie de session est présent, sinon redirige vers la page de connexion.
    """
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        return render_template('aide/index.html')
    else:
        return redirect(url_for('login_get'))

def aide_post():
    """
    Traite le formulaire d’aide soumis par POST.
    Si un cookie de session est présent, récupère les données du formulaire, affiche éventuellement un message de confirmation,
    puis redirige l’utilisateur vers le dashboard. Sinon, il est redirigé vers la page de connexion.
    """
    session_cookie = request.cookies.get('session_cookie')
    if not session_cookie:
        return redirect(url_for('login_get'))

    
    
    with Session(engine) as session:
        user = session.exec(
            select(Users).where(Users.cookie == session_cookie)
        ).one_or_none()

        if user:
            nouvelle_demande = DemandeAide(
                identifiant_eleve=user.identifiant_unique,  # On lie la demande à l'élève
                classe=user.niveau_classe,
                titre=request.form.get("titre"),
                message=request.form.get("message"),
                created_at= str(datetime.datetime.now())
            )
            session.add(nouvelle_demande)
            session.commit()
            flash("Votre demande d'aide a bien été envoyée.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Utilisateur non trouvé.", "error")
            return redirect(url_for('login_get'))
    
    return redirect(url_for('dashboard'))