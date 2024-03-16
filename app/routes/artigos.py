# Importação dos módulos e classes necessárias
from flask import render_template, redirect, session, jsonify, request, url_for, make_response, send_file, send_from_directory, Blueprint
from app.routes import artigos_bp
from app.models import Artigo, User, buscas
from app import db
from passlib.hash import bcrypt_sha256
import uuid
import markdown
import os
from docx import Document
import json
import openai 



openai.api_key = os.environ["OPENAI"]

@artigos_bp.route("/")
def homepage():
  return render_template("index.html")

@artigos_bp.route("/avaliar-redacao")
def redacion():
  return render_template("treino-redacao.html")

# Rota para criar um artigo (pode ser acessada via POST ou GET)
@artigos_bp.route("/create-artigo", methods=["POST", "GET"])
def criarArtigo():
    # Verifica se a requisição é um POST (envio de formulário)
    if request.method == "POST":
        # Obtém os dados do formulário
        title = request.form["title-art"]
        conteudo = request.form["conteudo-art"]
        categoria = request.form["category"]
        tags = request.form["tags"]

        # Valida os dados do formulário
        if title == "" or title == " " or len(conteudo) < 1:
            return "Digite algo válido!"

        try:
            user = session["user"]
        except:
            user = "visit"

        # Verifica se o usuário está logado
        if user == "visit":
            return "Você precisa estar logado."

        data = "sla"  # Defina o valor para 'data'

        # Cria um novo objeto de Artigo e o adiciona ao banco de dados
        newArtigo = Artigo(titulo=title, texto=markdown.markdown(conteudo), autor=user, data=data, categoria=categoria, tags=tags, likes=0, id=str(uuid.uuid4()))
        db.session.add(newArtigo)
        db.session.commit()

        # Redireciona para a página do novo artigo
        return redirect("/artigo/"+newArtigo.id)

    try:
      user = session['user']
    except:
      return redirect("/login")

    # Se a requisição não for POST, exibe o formulário de criação de artigo
    return render_template("create-artigo.html")

# Rota para excluir um artigo
@artigos_bp.route("/delete-artigo/<id>", methods=["GET"])
def deleteArtigo(id):
    artigo = Artigo.query.filter_by(id=id).first()
    
    user = User.query.filter_by(id=artigo.autor).first()
    
    if artigo:
        senha = request.args.get("senha")

        # Verifica a senha usando o bcrypt_sha256
        if bcrypt_sha256.verify(senha, user.password):
            db.session.delete(artigo)
            db.session.commit()
            return jsonify({
              "msg": "success"
            })
        else:
            return redirect("/artigo/"+artigo.id)
    else:
        return "Artigo Não Existe"

# Rota para adicionar um 'like' a um artigo
@artigos_bp.route("/add-like/<id>")
def likePost(id):
    artigo = Artigo.query.filter_by(id=id).first()
    artigo.likes = artigo.likes + 1
    db.session.commit()
    return redirect("/artigo/"+id)

# Rota para remover um 'like' de um artigo
@artigos_bp.route("/delete-like/<id>")
def deslikePost(id):
    artigo = Artigo.query.filter_by(id=id).first()
    artigo.likes = artigo.likes - 1
    db.session.commit()
    return redirect("/artigo/"+id)

# Rota para visualizar um artigo por ID
@artigos_bp.route("/artigo/<id>")
def artigoPage(id):
    try:
      user = session['user']
    except:
      user = 'visit'

    artigo = Artigo.query.filter_by(id=id).first()
    autor = User.query.filter_by(id=artigo.autor).first()
    if artigo:
        return render_template("post.html", artigo=artigo, autor=autor)
    else:
        return "<h1>Artigo Não Existe</h1"

# Rota para exibir a página de pesquisa
@artigos_bp.route("/search")
def pageSearch():
    categorias = Artigo.query.with_entities(Artigo.categoria).distinct().all()
    nomesCategorias = [categoria[0] for categoria in categorias]
    return render_template("search.html", categorys=nomesCategorias)

# Rota para buscar artigos por categoria
@artigos_bp.route("/search/category/<categoria>")
def buscar_artigo_categoria(categoria):
    artigos = Artigo.query.filter_by(categoria=categoria).all()

    if artigos:
        return jsonify(artigos)
    else:
        response = make_response(jsonify({"message": "Nenhum artigo encontrado para esta categoria"}), 404)
        return response


def search_word_files(directory, search_terms):
  results = set()  # Usando um conjunto para evitar duplicatas
  
  for filename in os.listdir(directory):
      if filename.endswith(".docx"):
          file_path = os.path.join(directory, filename)
          document = Document(file_path)
  
          for paragraph in document.paragraphs:
              for run in paragraph.runs:
                  text = run.text
                  for term in search_terms:
                      if term.lower() in text.lower():
                          results.add(filename)  # Adicione o nome do arquivo ao conjunto
  
  return [{"file_name": filename} for filename in results]

# Sua rota para buscar artigos por termos de pesquisa
@artigos_bp.route("/search/artigos")
def artigosSearch():
    pesquisa_i = request.args.get("pesquisa")
    pesquisa = pesquisa_i.lower()  # Converter a pesquisa para letras minúsculas para pesquisa insensível a maiúsculas/minúsculas
    try:
      user = session["user"]
    except:
      user = "visit"
    newBsc = buscas(user=user, termo=pesquisa)
    db.session.add(newBsc)
    db.session.commit()
    # Realize a pesquisa em várias colunas usando operadores 'ilike' para correspondência parcial e insensível a maiúsculas/minúsculas
    artigos = Artigo.query.filter(
        (Artigo.titulo.ilike(f"%{pesquisa}%")) |
        (Artigo.autor.ilike(f"%{pesquisa}%")) |
        (Artigo.categoria.ilike(f"%{pesquisa}%")) |
        (Artigo.data.ilike(f"%{pesquisa}%")) |
        (Artigo.tags.ilike(f"%{pesquisa}%"))
    ).all()

    # Diretório onde os documentos do Word estão localizados
    directory_path = "app/static/feciba"
    # Termos de pesquisa
    search_terms = pesquisa_i.split(" ")
    print(search_terms)
    # Realiza a pesquisa nos documentos do Word
    word_search_results = search_word_files(directory_path, search_terms)
    print(word_search_results)
    # Exibe os resultados da pesquisa nos artigos e nos documentos do Word
    return render_template("feed.html", artigos=artigos, feciba_results=word_search_results)

@artigos_bp.route("/download-file/<filename>")
def download_file(filename):
    # Diretório onde os documentos do Word estão localizados
    directory_path = os.path.abspath("app/static/feciba")

    file_path = os.path.join(directory_path, filename)

    # Verifica se o arquivo existe e retorna-o para download
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Arquivo não encontrado", 404

@artigos_bp.route("/feed/projetos-feciba")
def feed_projetos_feciba():
    # Diretório onde os documentos do Word dos projetos FECIBA estão localizados
    directory_path = "app/static/feciba"

    # Lista todos os arquivos no diretório FECIBA
    projetos_feciba = [{"file_name": filename} for filename in os.listdir(directory_path) if filename.endswith(".docx")]

    return render_template("feed.html", artigos=None, feciba_results=projetos_feciba)

@artigos_bp.route("/feed/artigos")
def feed_artigos():
    # Lógica para obter e exibir o feed de artigos normais
    artigos = Artigo.query.all()
    return render_template("feed.html", artigos=artigos, feciba_results=None)

@artigos_bp.route("/learn-ai/redacao", methods=["POST"])
def gerarAvaliacaoPorIa():
  
  data = request.get_json()
  user_message = {"role": "user", "content": f"Título: {data['title']} \n Redação: {data['content']}"}

  # Defina a conversa com a mensagem do sistema e a mensagem do usuário
  conversation = [
      {"role": "system", "content": "Você é uma IA que avalia redações, foque nas informações do usuário, e forneça insights com base em redações nota mil no ENEM"},
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

@artigos_bp.route("/api/gerar-artigo-ai", methods=["POST"])
def gerarArtigoPorIa():

  data = request.get_json()
  user_message = {"role": "user", "content": f"Conteúdo do usuário: {data['resumo']}"}

  # Defina a conversa com a mensagem do sistema e a mensagem do usuário
  conversation = [
      {"role": "system", "content": "Como a IA Learn.Ai, você gera artigos autônomos longos e bem estruturados, com base nas entradas dos usuários. Os artigos devem ser descontraídos e autênticos, permitindo referências externas de forma moderada e uma linguagem informal. Acrescente informações relevantes para evitar superficialidade, com orientação para estudantes do Ensino Médio. Use emojis de forma atrativa e incentive os leitores a clicar no botão 'Tirar Dúvida' em caso de questionamentos."},
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

@artigos_bp.route("/gerar/quiz", methods=["POST"])
def gerarQuizPorIa():
  data = request.get_json()
  user_message = {"role": "user", "content": f"O que o usuário tem dificuldade: {data['dificuldades']}"}

  # Defina a conversa com a mensagem do sistema e a mensagem do usuário
  conversation = [
      {"role": "system", "content": "Você é uma Inteligência Artificial que gera quizzes automático de acordo com algum resumo que o usuário enviar, se não for um resumo, o usuário enviará apenas o assunto que ele tem dificuldade, e você vai gerar um quiz básico sobre o assunto. Crie com uma linguagem descontraída e autêntica, sem referências a outros sites, blogs, ou artigos já publicados. Modelo onde o usuário vai inserir a resposta: '(Resposta:  )' deixe sempre o campo de resposta vazio, você não vai responder nada."},
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

@artigos_bp.route("/corrigir/quiz", methods=["POST"])
def corrigeQuizPorIa():
  data = request.get_json()
  user_message = {"role": "user", "content": f"{data['quiz']}"}

  # Defina a conversa com a mensagem do sistema e a mensagem do usuário
  conversation = [
      {"role": "system", "content": "Você é uma Inteligência Artificial que faz a correção de um quiz com perguntas e respostas que o usuário enviar, você vai explicar onde o usuário errou ou acertou, e vai dar dicas de como acertar na próxima, corrija de forma descontraída e leve."},
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

@artigos_bp.route("/quiz")
def quiz():
  return render_template("quiz.html")

@artigos_bp.route('/api/tirar-duvida-artigo', methods=["POST"])
def tiraDuvidaArtigo():
  data = request.get_json()
  user_message = {"role": "user", "content": f"Artigo: {data['conteudo_artigo']}. Dúvida: {data['duvida']}"}

  # Defina a conversa com a mensagem do sistema e a mensagem do usuário
  conversation = [
      {"role": "system", "content": "Você é uma Inteligência Artificial, que tira dúvida de um artigo, você pode pegar a base do artigo, ou, pegar outras referências. O importante é o usuário entender de vez o assunto. Responda de forma descontraída. E não deixe o usuário fugir muito do artigo."},
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
    "resposta": assistant_response
  })