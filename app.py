from flask import Flask, render_template
import sqlmodel
from routes import *
from ext_config import app, engine
from create_classes import create_all_classes



app.add_url_rule('/', view_func=home, methods=['GET'])
app.add_url_rule('/login', view_func=login_get, methods=['GET'])
app.add_url_rule('/login', view_func=login_post, methods=['POST'])
app.add_url_rule('/dashboard', view_func=dashboard, methods=['GET'])
app.add_url_rule('/logout', view_func=logout, methods=['GET'])
app.add_url_rule('/get_data', view_func=get_data, methods=['POST'])
app.add_url_rule('/update_data', view_func=update_data, methods=['POST'])
app.add_url_rule('/settings', view_func=settings, methods=['GET'])
app.add_url_rule('/lost_id', view_func=lost_id_get, methods=['GET'])
app.add_url_rule('/lost_id', view_func=lost_id_post, methods=['POST'])
app.add_url_rule('/test', view_func=vers_ma_page, methods=['GET'])
app.add_url_rule('/test', view_func=vers_ma_page_post, methods=['POST'])
app.add_url_rule('/update-theme', view_func=update_theme, methods=['POST'])
app.add_url_rule('/get-theme', view_func=get_theme, methods=['GET'])
app.add_url_rule('/change_password', view_func=change_password_get, methods=['GET'])
app.add_url_rule('/change_password', view_func=change_password_post, methods=['POST'])
app.add_url_rule('/aide', view_func=aide_get, methods=['GET'])
app.add_url_rule('/aide', view_func=aide_post, methods=['POST'])
app.add_url_rule('/configure_password', view_func=configure_password_get, methods=['GET'])
app.add_url_rule('/configure_password', view_func=configure_password_post, methods=['POST'])
app.add_url_rule('/configure_prof', view_func=configure_prof_get, methods=['GET'])
app.add_url_rule('/configure_prof', view_func=configure_prof_post, methods=['POST'])
app.add_url_rule('/get_theme', view_func=get_theme, methods=['GET'])
app.add_url_rule('/classe/<class_name>', view_func=classes_prof_get, methods=['GET'])
app.add_url_rule('/get_voeux_status', view_func=get_voeux_status, methods=['GET'])
app.add_url_rule('/validate_voeux', view_func=post_voeux_status, methods=['POST'])
app.add_url_rule('/eleve/<eleve_id>', view_func=profil_eleve_get, methods=['GET'])
app.add_url_rule('/notifications', view_func=get_notifications, methods=['GET'])


if __name__ == '__main__':
    create_all_classes()
    app.run(host="0.0.0.0", debug=True, port=8098)
    
