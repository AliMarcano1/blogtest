from flask import Blueprint
publicaciones = Blueprint('publicaciones', __name__, template_folder='templates',static_url_path='/publicaciones/static/',static_folder='static' )
from . import routes