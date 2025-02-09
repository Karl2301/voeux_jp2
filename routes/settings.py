from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json

def settings():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            statement = select(Student).where(Student.cookie == session_cookie)
            user = session.exec(statement).one_or_none()
            if user:
                return render_template('settings/settings.html')
            else:
                return redirect(url_for('login_get'))

        

    return render_template('settings/settings.html')