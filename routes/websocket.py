from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
from flask_socketio import SocketIO, emit, join_room, leave_room

connected_users = {}

@socketio.on('connect')
def handle_connect():
    """Détecte une nouvelle connexion WebSocket"""
    print(f"Nouvelle connexion WebSocket: {request.sid}")


@socketio.on('join')
def handle_join(data):
    """L'utilisateur rejoint une room basée sur son cookie"""
    session_cookie = data.get('session_cookie')

    if not session_cookie:
        print("Aucun cookie de session fourni")
        return

    # Supprimer les anciens SID associés au même session_cookie
    for sid, cookie in list(connected_users.items()):
        if cookie == session_cookie:
            del connected_users[sid]

    # Associer request.sid au session_cookie
    connected_users[request.sid] = session_cookie

    join_room(session_cookie)

    with Session(engine) as session:
        # Récupérer l'utilisateur
        statement = select(Users).where(Users.cookie == session_cookie)
        user = session.exec(statement).first()
        if user:
            user.online = True
            session.add(user)
            session.commit()

            # Si l'utilisateur est un professeur, ne pas envoyer de message
            if user.professeur:
                print(f"Professeur connecté: {user.identifiant_unique}")
            else:
                # Récupérer les classes de l'utilisateur (élève)
                user_classes = [user.niveau_classe]

                # Mettre à jour le nombre d'élèves en ligne pour chaque classe
                for classe in user_classes:
                    statement = select(Classes).where(Classes.classe == classe)
                    class_record = session.exec(statement).first()
                    if class_record:
                        class_record.online_student = (class_record.online_student or 0) + 1
                        session.add(class_record)
                        session.commit()

                # Récupérer les professeurs concernés
                statement = select(Users).where(Users.professeur == True)
                professors = session.exec(statement).all()

                # Calculer la somme des élèves en ligne pour chaque professeur
                for professor in professors:
                    professor_classes = json.loads(professor.niveau_classe)
                    if any(classe in professor_classes for classe in user_classes):
                        total_online_students = 0
                        for classe in professor_classes:
                            statement = select(Classes).where(Classes.classe == classe)
                            class_record = session.exec(statement).first()
                            if class_record:
                                total_online_students += class_record.online_student

                        # Envoyer un message aux professeurs concernés
                        for sid, cookie in connected_users.items():
                            if cookie == professor.cookie:
                                emit('message', {'msg': f'L\'utilisateur {user.identifiant_unique} a rejoint la room {session_cookie}', 'total_online_students': total_online_students}, room=sid)

    print(f"Utilisateur connecté avec session_cookie: {session_cookie} (SID: {request.sid})")
    print(f"Utilisateur connecté: {connected_users}")

    # Envoyer une confirmation au client
    emit('message', {'msg': f'Connecté à la room {session_cookie}'}, room=session_cookie)


@socketio.on('disconnect')
def on_disconnect():
    """Gestion de la déconnexion automatique"""
    sid = request.sid
    session_cookie = connected_users.pop(sid, None)

    print(f"Déconnexion détectée pour SID: {sid}")

    with Session(engine) as session:
        statement = select(Users).where(Users.cookie == session_cookie)
        user = session.exec(statement).first()
        if user:
            user.online = False
            session.add(user)
            session.commit()

            # Si l'utilisateur est un professeur, ne pas envoyer de message
            if not user.professeur:
                # Récupérer les classes de l'utilisateur (élève)
                user_classes = [user.niveau_classe]

                # Mettre à jour le nombre d'élèves en ligne pour chaque classe
                for classe in user_classes:
                    statement = select(Classes).where(Classes.classe == classe)
                    class_record = session.exec(statement).first()
                    if class_record:
                        class_record.online_student = max((class_record.online_student or 0) - 1, 0)
                        session.add(class_record)
                        session.commit()

                # Récupérer les professeurs concernés
                statement = select(Users).where(Users.professeur == True)
                professors = session.exec(statement).all()

                # Calculer la somme des élèves en ligne pour chaque professeur
                for professor in professors:
                    professor_classes = json.loads(professor.niveau_classe)
                    if any(classe in professor_classes for classe in user_classes):
                        total_online_students = 0
                        for classe in professor_classes:
                            statement = select(Classes).where(Classes.classe == classe)
                            class_record = session.exec(statement).first()
                            if class_record:
                                total_online_students += class_record.online_student

                        # Envoyer un message aux professeurs concernés
                        for sid, cookie in connected_users.items():
                            if cookie == professor.cookie:
                                emit('message', {'msg': f'L\'utilisateur {user.identifiant_unique} s\'est déconnecté', 'total_online_students': total_online_students}, room=sid)

    if session_cookie:
        leave_room(session_cookie)
        print(f"Utilisateur déconnecté avec session_cookie: {session_cookie} (SID: {sid})")
        print(f"Utilisateur déconnecté: {connected_users}")