from flask import render_template
from app.routes import users_bp
from app.models import User

@users_bp.route('/listar')
def listar_usuarios():
    usuarios = User.query.all()
    return render_template('users/listar.html', usuarios=usuarios)
