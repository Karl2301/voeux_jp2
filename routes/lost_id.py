from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
import uuid
import datetime

def lost_id_get():
    return render_template('lost_id/index.html')

def lost_id_post():

    prenom_user = request.form.get('prenom')
    nom_user= request.form.get('nom')
    classe_user = request.form.get('classe')

    with Session(engine) as session:
        new_user = IdentifiantPerdue(
            nom=nom_user,
            prenom=prenom_user,
            classe=classe_user,
            created_at = str(datetime.datetime.now())
        )

        session.add(new_user)
        session.commit()

    return redirect(url_for('home'))
