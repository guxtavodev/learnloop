from flask import render_template, request, session, jsonify, redirect
from flask.json import jsonify
from app.routes import users_bp
from app.models import User
from passlib.hash import bcrypt_sha256
from app import db
import uuid

# Rota para criar um novo usuário
@users_bp.route("/cadastro")
def cadastroPage():
    return render_template("signup.html")

@users_bp.route("/login")
def loginPage():
    return render_template("login.html")

@users_bp.route('/listar')
def listar_usuarios():
    usuarios = User.query.all()
    return render_template('users/listar.html', usuarios=usuarios)

def crip(dado):
  dado_criptografado = bcrypt_sha256.hash(dado)
  return str(dado_criptografado)

@users_bp.route('/api/signup', methods=["POST"])
def signup():

  username = request.form["username"]
  password = crip(request.form["password"])

  newUser = User(username=username, password=password, id=str(uuid.uuid4()))
  db.session.add(newUser)
  db.session.commit()
  session["user"] = newUser.id 
  return redirect("/")

@users_bp.route("/api/login", methods=["GET"])
def login():
  username = request.args.get("username")
  password = request.args.get("password")
  user = User.query.filter_by(username=username).first()
  if user and bcrypt_sha256.verify(password, user.password):
    session["user"] = user.id
    return redirect("/")
  else:
    return "<h1>Usuário ou senha incorreto</h1>"

@users_bp.route("/api/logout")
def logout():
  session.clear()
  return redirect("/login")

@users_bp.route("/api/user")
def user():
  user_id = session.get("user")
  user = User.query.filter_by(id=user_id).first()
  return jsonify({"user": user})

@users_bp.route("/api/delete-user", methods=["POST"])
def delete_user():
  user_id = session.get("user")
  user = User.query.filter_by(id=user_id).first()
  senha = request.get_json()["senha"]
  if bcrypt_sha256.verify(senha, user.password):
    db.session.delete(user)
    db.session.commit()
    session.clear()
    return jsonify({"msg": "usuario deletado com sucesso"})
  else:
    return jsonify({"msg": "Senha incorreta"})

@users_bp.route("/api/update-user", methods=["POST"])
def update_user():
  data = request.get_json()
  user_id = session.get("user")
  user = User.query.filter_by(id=user_id).first()
  user.username = data["username"]
  user.password = data["password"]
  db.session.commit()
  return jsonify({"msg": "usuario atualizado com sucesso"})

