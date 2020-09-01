from flask import Flask, render_template, session, request, redirect, url_for, Response
from flask_socketio import SocketIO, emit, send
import os
import jinja2
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
import yaml
import logging
import time
from io import StringIO
   
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_stream = StringIO() 
logger = logging.getLogger('query_tool')
logger.setLevel(logging.DEBUG)
lh = logging.StreamHandler(log_stream)
lh.setLevel(logging.DEBUG)
lh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(lh)
logger.addHandler(ch)

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
with open('queries.yaml') as queries_file:
    queries = yaml.safe_load(queries_file)

with open('directors.yaml') as directors_file:
    directors = yaml.safe_load(directors_file)

@app.route('/')
def query_tool():
    if not session.get('username'):
        return render_template('login.html')
    return render_template("index.html", queries=queries, username=session['username'])

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET' and not session.get('username'):
        return render_template('login.html')
    else:
        session['username'] = request.form['username']
        session['pw'] = request.form['password']
        return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))

@socketio.on('send_query')
def on_send_query(data):
    log_stream.truncate(0)
    log_stream.seek(0)
    print(data)
    logger.info(data['hostname'])
    logger.info(data['port'])
    logger.info(data['query'])
    for line in log_stream.getvalue().splitlines():
        emit('log', line)

@socketio.on('environment')
def on_environment(data):
    emit('env_response', directors[data[0]])

@socketio.on('director')
def on_director(data):
    env = data['env']
    dr = data['dir']
    emit('director_response', directors[env][dr] )

@app.route('/send_query', methods=['GET','POST'])
def send_query():
    return redirect('/log_stream')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)