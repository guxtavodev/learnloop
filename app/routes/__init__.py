from flask import Blueprint

artigos_bp = Blueprint('artigos', __name__)
users_bp = Blueprint('users', __name__)
duvidas_bp = Blueprint('duvidas', __name__)
iaplan_bp = Blueprint('learnplan', __name__)
feciba_bp = Blueprint('feciba', __name__)

from app.routes import artigos, users, duvidas, plan, feciba