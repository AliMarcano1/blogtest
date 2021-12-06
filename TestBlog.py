import os
from flask import Flask
from markupsafe import escape
#necesario escape para endpoints con variables

import pymysql
from app import create_app
#from . import app


app = create_app()


"""
app = Flask(__name__)

env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


def con():
    return pymysql.connect(host='localhost',user='root',password='hirano6951015',db='RGTBlog')

@app.route("/")
@app.route('/<user>')
def index(user=None):
	secret_key = app.config.get("SECRET_KEY")
	#return f"<h1>RGT Blog in Progress</h1> {secret_key}."
	return render_template('index.html',user="user") 

@app.route('/<user>')
@app.route("/")
def banner(user=None):
    return render_template('banner.html',user="user")

@app.route('/inicio')
@app.route("/inicio/<user>")
def content(user=None):
    return render_template('content.html',user="user")



@app.route('/hello')#direcciones fijas
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    #string
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

def valid_login(user,passw):
	return False

def open_home():
	return render_template('login/templates/login.html', error=error)

@app.route('/login')
def login():
	error = None
	#if request.method == 'POST':
	#	if valid_login(request.body['username'],request.body['password']):
	#	return open_home(request.form['username'])
	#	else:
	#		return 'Invalid username/password'
	#else:
	return render_template('login.html')"""
