# Importação dos módulos e classes necessárias
from flask import render_template, redirect, session, jsonify, request, url_for, make_response
from app.routes import artigos_bp
from app.models import Artigo, User
from app import db
from passlib.hash import bcrypt_sha256
import uuid
import markdown

@artigos_bp.route("/")
def homepage():
  return render_template("index.html")

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
    print(session['user'])
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

# Rota para buscar artigos por termos de pesquisa
@artigos_bp.route("/search/artigos")
def artigosSearch():
    pesquisa = request.args.get("pesquisa")
    pesquisa = pesquisa.lower()  # Converter a pesquisa para letras minúsculas para pesquisa insensível a maiúsculas/minúsculas

    # Realize a pesquisa em várias colunas usando operadores 'ilike' para correspondência parcial e insensível a maiúsculas/minúsculas
    artigos = Artigo.query.filter(
        (Artigo.titulo.ilike(f"%{pesquisa}%")) |
        (Artigo.autor.ilike(f"%{pesquisa}%")) |
        (Artigo.categoria.ilike(f"%{pesquisa}%")) |
        (Artigo.data.ilike(f"%{pesquisa}%")) |
        (Artigo.tags.ilike(f"%{pesquisa}%"))
    ).all()

    return jsonify({"artigos": artigos})
