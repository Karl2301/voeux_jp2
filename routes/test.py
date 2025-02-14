from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json

def vers_ma_page():
    return render_template("test/index.html")

def vers_ma_page_post():

    name = request.form.get('name')

    print("Nom reçu : ", name)

    new_post = IdentifiantPerdus(
        nom=name
    )

    with Session(engine) as session:
        session.add(new_post)
        session.commit()

    return redirect(url_for('vers_ma_page'))