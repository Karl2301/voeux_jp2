from flask import Flask, render_template
import sqlmodel
from routes import *
from ext_config import app, engine

app.add_url_rule('/', view_func=home, methods=['GET'])
app.add_url_rule('/login', view_func=login_get, methods=['GET'])
app.add_url_rule('/login', view_func=login_post, methods=['POST'])
app.add_url_rule('/dashboard', view_func=dashboard, methods=['GET'])
app.add_url_rule('/logout', view_func=logout, methods=['GET'])
app.add_url_rule('/get_data', view_func=get_data, methods=['POST'])
app.add_url_rule('/update_data', view_func=update_data, methods=['POST'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)



# test