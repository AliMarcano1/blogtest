from flask import Flask
from flask_mysqldb import MySQL
from flask import Blueprint

db =  MySQL()
def create_app():
	app = Flask(__name__)
	UPLOAD_FOLDER = '/static/img/users'
	ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
	app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///db.mysql'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost:5432/miniblog'
	#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	#login_manager.init_app(app)
	#login_manager.login_view = "auth.login"
	#db.init_app(app)
	# Registro de los Blueprints
	from .publicaciones import publicaciones
	app.register_blueprint(publicaciones)
	from .users import users
	app.register_blueprint(users)
	db.init_app(app)
	return app