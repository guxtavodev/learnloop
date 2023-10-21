from flask import render_template
from app.routes import artigos_bp
from app.models import Artigo

@artigos_bp.route('/listar')
def listar_artigos():
    artigos = Artigo.query.all()
    return render_template('artigos/listar.html', artigos=artigos)

@artigos_bp.route("/")
def home():
  return "ok"