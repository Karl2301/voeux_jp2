from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
from flask_socketio import SocketIO, emit, join_room, leave_room


def classes_prof_get(class_name):
    session_cookie = request.cookies.get('session_cookie')
    print("classe",class_name)
    if not session_cookie:
        return redirect(url_for('login_get'))

    with Session(engine) as session:
        # Récupérer l'utilisateur en fonction du cookie de session
        statement = select(Users).where(Users.cookie == session_cookie)
        user = session.exec(statement).one_or_none()
        statement_online_students = session.exec(select(Users).where((Users.niveau_classe == class_name) & (Users.professeur == 0) & (Users.online == True)))
        student_connected_for_class = len(statement_online_students.all())  

        statement_validate_students = session.exec(select(Users).where((Users.niveau_classe == class_name) & (Users.professeur == 0) & (Users.choix_validees == True)))
        student_validate_for_class = len(statement_validate_students.all())  

        if not user:
            return redirect(url_for('login_get'))

        # Vérifier si c'est un élève (accès interdit)
        if user.professeur == 0:
            flash("Accès interdit pour les élèves", "error")
            return redirect(url_for('dashboard'))  # Redirection vers le dashboard

        # Charger la liste des classes du professeur 
        prof_classe = json.loads(user.niveau_classe)
        if class_name not in prof_classe:
            flash("vous n'avez pas accès à cette classe")  # vous n'avez pas accès à cette classe
        

        # Vérifier si la classe appartient bien à ce professeur
        if class_name not in prof_classe:
            flash("Vous n'avez pas accès à cette classe", "error")
            return redirect(url_for('dashboard'))


        # Récupérer les élèves appartenant à cette classe
        statement_eleves = select(Users).where(
            (Users.niveau_classe == class_name) & (Users.professeur == 0)
        )
        eleves = session.exec(statement_eleves).all()

        
        return render_template('classes/index.html' , eleves=eleves, class_name=class_name, eleve_online_count=student_connected_for_class, eleve_choix_validees_count=student_validate_for_class)
    
    # {{ class_name }}
