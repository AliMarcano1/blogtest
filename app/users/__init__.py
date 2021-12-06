from flask import Blueprint
users = Blueprint('users', __name__, template_folder='../',static_url_path='/users/static/',static_folder='static')
from . import routes