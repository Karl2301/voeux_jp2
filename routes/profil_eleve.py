from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
from flask_socketio import SocketIO, emit, join_room, leave_room




def profil_eleve_get(eleve_id):
    # Vérifier la présence du cookie de session
    session_cookie = request.cookies.get('session_cookie')
    if not session_cookie:
        return redirect(url_for('login_get'))

    with Session(engine) as session:
        
        statement = select(Users).where(Users.cookie == session_cookie)
        user = session.exec(statement).first()

        if not user:
            return redirect(url_for('login_get'))

        # Seuls les professeurs ont accès à cette page
        if user.professeur == 0:
            flash("Accès interdit pour les élèves", "error")
            return redirect(url_for('dashboard'))

        # Recup la liste des classes auxquelles le professeur a accès
        user_classes = json.loads(user.niveau_classe)

        # Récupérer l'élève dont l'identifiant est fourni et vérifier qu'il s'agit bien d'un élève
        eleve_statement = select(Users).where(Users.identifiant_unique == eleve_id, Users.professeur == 0)
        eleve = session.exec(eleve_statement).first()

        if not eleve:
            flash("Élève non trouvé", "error")
            return redirect(url_for('dashboard'))

        # Vérifier que l'élève appartient bien à une classe accessible par le professeur
        if eleve.niveau_classe not in user_classes:
            flash("Vous n'avez pas accès à cette classe", "error")
            return redirect(url_for('dashboard'))

        # Afficher le profil de l'élève via le template dédié
        return render_template('eleve/index.html', eleve=eleve)
