# Importação dos módulos e classes necessárias
from flask import render_template, redirect, session, jsonify, request, url_for, make_response, send_file
from app.routes import iaplan_bp
from app.models import LearnPlan
from app import db
from passlib.hash import bcrypt_sha256
import uuid
import markdown
import openai 
import os

openai.api_key = os.environ["OPENAI"]

@iaplan_bp.route("/plan")
def planPage():
  try:
    user = session['user']
  except:
    return redirect('/login')
  plano = LearnPlan.query.filter_by(autor=session["user"]).first()
  return render_template("plan.html", plano=plano)

@iaplan_bp.route("/plan/save", methods=["POST"])
def savePlan():
  plano = LearnPlan.query.filter_by(autor=session["user"]).first()
  if not plano:
    plano = LearnPlan(id=str(uuid.uuid4()), autor=session["user"], titulo=request.form['titulo'], texto=request.form['texto'])
    db.session.add(plano)
    db.session.commit()

    return redirect("/plan")
  plano.titulo = request.form["titulo"]
  plano.texto = request.form["texto"]
  db.session.commit()
  return redirect(url_for("iaplan_bp.planPage"))

@iaplan_bp.route("/gerar-plano-ai", methods=["POST"])
def gerarArtigoPorIa():
  data = request.get_json()
  user_message = {"role": "user", "content": f"O que o usuário quer: {data['resumo']}"}

  # Defina a conversa com a mensagem do sistema e a mensagem do usuário
  conversation = [
      {"role": "system", "content": "Você é um sistema AI que gera plano de estudos personalizado com o que o estudante de Ensino Médio quer, com passo a passo, dias e o que precisa estudar."},
      user_message
  ]

  # Obtenha a resposta do GPT-3
  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=conversation
  )

  # Obtenha a mensagem de resposta do assistente
  assistant_response = response.choices[0].message["content"]
  print(assistant_response)

  return jsonify({
    "msg": "success",
    "response": assistant_response
  })

@iaplan_bp.route("/download-db")
def download_file():
    # Diretório onde os documentos do Word estão localizados
    directory_path = os.path.abspath("instance")

    file_path = os.path.join(directory_path, "data-learnloop-feciba.db")

    # Verifica se o arquivo existe e retorna-o para download
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Arquivo não encontrado", 404