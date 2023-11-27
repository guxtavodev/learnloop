# Importação dos módulos e classes necessárias
from flask import render_template, redirect, session, jsonify, request, url_for, make_response
from app.routes import duvidas_bp
from app.models import Duvidas, Respostas, User
from app import db
import uuid

@duvidas_bp.route("/create-duvidas", methods=["POST"])
def createDuvida():
  data = request.get_json()
  texto = data["texto"]
  try:
    autor = session["user"]
  except:
    return jsonify({
      'msg': 'error'
    })
  id = str(uuid.uuid4())

  newDuvida = Duvidas(id=id, texto=texto, autor=autor)
  db.session.add(newDuvida)
  db.session.commit()

  return jsonify({
    "msg": "success",
    "id": id
  })

@duvidas_bp.route("/feed/duvidas")
def duvidasPage():
  duvidas = Duvidas.query.all()
  return render_template("duvidas.html", duvidas=duvidas)


def serialize_duvida(duvida):
    return {
        'id': duvida.id,
        'texto': duvida.texto,
        'autor': User.query.filter_by(id=duvida.autor).first().username,
        # Outros campos do objeto Duvidas
    }

def serialize_resposta(resposta):
    print(resposta.autor)
    return {
        'id': resposta.id,
        'texto': resposta.texto,
        'autor': User.query.filter_by(id=resposta.autor).first().username or "não indentificado",
        'referencia': resposta.referencia,
        # Outros campos do objeto Respostas
    }

@duvidas_bp.route('/get-duvida/<id>', methods=['GET'])
def getDuvida(id):
    duvida = Duvidas.query.filter_by(id=id).first()
    respostas = Respostas.query.filter_by(referencia=id).all()

    serialized_respostas = [serialize_resposta(resposta) for resposta in respostas]
    serialized_duvida = serialize_duvida(duvida) if duvida else None

    return jsonify({
        "msg": "success",
        "dados": serialized_duvida,
        "respostas": serialized_respostas
    })


@duvidas_bp.route('/responder-duvida', methods=['POST'])
def responderDuvida():
  data = request.get_json()
  texto = data['resposta']
  autor = session['user']
  duvida = data['duvidaId']

  newReposta = Respostas(id=str(uuid.uuid4()), texto=texto, autor=autor, referencia=duvida)
  db.session.add(newReposta)
  db.session.commit()

  return jsonify({
    'msg': 'success'
  })
  