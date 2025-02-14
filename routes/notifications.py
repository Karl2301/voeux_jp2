from flask import Flask, render_template
from datetime import datetime
from sqlmodel import Session, select
from ext_config import *

def format_datetime(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%d/%m %H:%M")
    except Exception:
        return value

# Enregistrer le filtre dans l'environnement Jinja de l'app
app.jinja_env.filters['formatdatetime'] = format_datetime

def get_notifications():
    """
    Récupère toutes les demandes d'aide en affichant l'id, le titre, le message et la classe.
    """
    with Session(engine) as session:
        statement = select(DemandeAide)
        demandes = session.exec(statement).all()
        
    with Session(engine) as session:
        statement = select(NotificationsVoeux)
        voeux = session.exec(statement).all()

    return render_template('notifications/index.html', demandes=demandes, voeux=voeux)