from flask import Blueprint

artigos_bp = Blueprint('artigos', __name__)
users_bp = Blueprint('users', __name__)
materiais = Blueprint('materiais', __name__)
arquivos = Blueprint('arquivos', __name__)
groups = Blueprint('groups', __name__)

from app.routes import artigos, users
