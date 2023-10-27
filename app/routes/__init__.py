from flask import Blueprint

artigos_bp = Blueprint('artigos', __name__)
users_bp = Blueprint('users', __name__)
duvidas_bp = Blueprint('duvidas', __name__)

from app.routes import artigos, users, duvidas
