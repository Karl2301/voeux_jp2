"""
Ce fichier contient la fonction `update_data` qui est utilisée pour mettre à jour les données des étudiants dans la base de données.

Fonctionnalités :
- Vérifie l'existence d'un cookie de session pour identifier l'utilisateur.
- Récupère les données mises à jour envoyées dans la requête JSON.
- Met à jour les voeux des établissements de l'utilisateur dans la base de données.
- Gère les erreurs potentielles et effectue un rollback en cas d'échec de la mise à jour.

Ce fichier est utilisé lorsque l'utilisateur souhaite mettre à jour ses voeux d'établissements via une requête HTTP.
"""

from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json



def update_data():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            statement = select(Student).where(Student.cookie == session_cookie)
            user = session.exec(statement).first()
            if user:
                try:
                    updated_data = request.json
                    voeux_etablissements = json.loads(user.voeux_etablissements)

                    user.voeux_etablissements = str(updated_data).replace("'", '"')
                    session.add(user)
                    session.commit()
                    return jsonify({'success': True})
                except Exception as e:
                    session.rollback()
                    return jsonify({'success': False, 'message': str(e)})
            else:
                return redirect(url_for('login_get'))
    return jsonify({'success': False, 'message': 'No session cookie found'})
