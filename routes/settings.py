from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify, abort
from ext_config import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlmodel import Session, select
import json
from flask_socketio import SocketIO, emit, join_room, leave_room


def settings():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            statement = select(Users).where(Users.cookie == session_cookie)
            user = session.exec(statement).one_or_none()
            if user:
                return render_template('settings/settings.html', dashboard_theme=user.dashboard_theme)
            else:
                return redirect(url_for('login_get'))

    else:
        return redirect(url_for('login_get'))
    

    

def settings_get_theme():
    session_cookie = request.cookies.get('session_cookie')
    if session_cookie:
        with Session(engine) as session:
            statement = select(Users).where(Users.cookie == session_cookie)
            user = session.exec(statement).one_or_none()
            if user:
                return jsonify({'darkTheme': user.dashboard_theme})
            else:
                return jsonify({'error': 'User not found'}), 404

    else:
        return redirect(url_for('login_get'))