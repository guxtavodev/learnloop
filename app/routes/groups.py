from flask import render_template, redirect, session, jsonify, request, url_for, make_response
from app.routes import groups_bp
from app.models import Grupo, User, Files
from app import db
import uuid
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
import re
import urllib.parse
import openai

openai.api_key = os.environ['OPENAI']

# Função para verificar os grupos do usuário
def check_groups_user(user_id):
    groups_all = Grupo.query.all()
    groups_user = []
    for group in groups_all:
        if ',' not in group.membros:
            if user_id == group:
                groups_user.append(group)
        else:
            lista_membros = group.membros.split(",")
            if user_id in lista_membros:
                groups_user.append(group)
    return groups_user

# Função para formatar a data
def formatar_data(data_str):
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        partes = data_str.split('/')
        if len(partes) == 3:
            dia = partes[0]
            mes = partes[1]
            ano = partes[2]

            if len(dia) == 1:
                dia = '0' + dia
            if len(mes) == 1:
                mes = '0' + mes

            data_str = f"{dia}/{mes}/{ano}"
            data = datetime.strptime(data_str, "%d/%m/%Y")
        else:
            return "formato de data inválido"
    return data

# Função para fazer o upload de arquivo para o Azure Blob Storage
def upload_file_to_blob_storage(container_name, file_name, file_data):
    try:
        # Conecte-se à sua conta de armazenamento do Azure
        blob_service_client = BlobServiceClient.from_connection_string(os.environ['CONECTION'])

        # Conecte-se ao contêiner de armazenamento ou crie um novo se não existir
        container_client = blob_service_client.get_container_client(container_name)

        try:
            container_client.create_container()
        except ResourceExistsError:
            print("O contêiner já existe.")

        # Enviar arquivo para o Blob Storage
        blob_client = container_client.get_blob_client(file_name)
        blob_client.upload_blob(file_data)
        return True
    except Exception as e:
        print(f"Ocorreu um erro durante o upload do arquivo: {e}")
        return False

# Função para baixar arquivo do Azure Blob Storage
def download_file_from_blob_storage(container_name, blob_name):
    try:
        # Conecte-se à sua conta de armazenamento do Azure
        blob_service_client = BlobServiceClient.from_connection_string(os.environ['CONECTION'])

        # Conecte-se ao contêiner de armazenamento
        container_client = blob_service_client.get_container_client(container_name)

        # Baixe o arquivo do Blob Storage
        blob_client = container_client.get_blob_client(blob_name)
        file_data = blob_client.download_blob().readall()
        return file_data
    except ResourceNotFoundError:
        print("O blob não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro durante o download do arquivo: {e}")
        return None

# Rota para listar os grupos
@groups_bp.route("/groups")
def groupsList():
    try:
      user = session['user']
      user_db = User.query.filter_by(id=user).first()
      print(user_db.username)
  
      groups_user = check_groups_user(str(user_db.username))
      print(groups_user)
  
      # Ordenar os grupos com base no prazo de término
      groups_user.sort(key=lambda x: x.prazo)
  
      # Separar grupos com prazo próximo de acabar
      current_date = datetime.now()
      groups_near_end = [group for group in groups_user if (group.prazo - current_date).days < 7]
      groups_far_end = [group for group in groups_user if (group.prazo - current_date).days >= 7]
  
      # Juntar os grupos em uma lista ordenada
      sorted_groups = groups_near_end + groups_far_end
  
      return render_template("groups-list.html", user=user_db, groups=sorted_groups)
    except Exception as e:
      print(e)
      return redirect('/login')

# Rota para exibir a página do grupo
@groups_bp.route("/groups/<id>")
def groupPage(id):
    user = session['user']
    group = Grupo.query.filter_by(id=id).first()
    wikis = group.wikis.split("//")
    files = Files.query.filter_by(group=id).all()
    return render_template("group-page.html", group=group, wikis=wikis, files=files)

# Rota para adicionar wiki
@groups_bp.route("/api/wikis/add", methods=["POST"])
def addWiki():
    data = request.get_json()
    user = session['user']
    group = Grupo.query.filter_by(id=data['group']).first()
    group.wikis = group.wikis + "//" + data['wiki']
    db.session.commit()
    return jsonify({"msg": "Wiki adicionada"})

# Rota para criar grupo
@groups_bp.route("/api/create-group", methods=["POST"])
def createGroup():
    data = request.get_json()
    user = session['user']
    user_message = {"role": "user", "content": f"Título: {data['nome']} \n Descrição: {data['descricao']} \n Membros: {data['membros']}."}
  
    # Defina a conversa com a mensagem do sistema e a mensagem do usuário
    conversation = [
        {"role": "system", "content": "Você é uma assistente virtual especializada em orientação para trabalhos acadêmicos, desde seminários até rodas de conversa. Seu objetivo é fornecer estratégias e dicas para desenvolver e apresentar trabalhos de alta qualidade. Com base no título, descrição e membros do grupo, você orienta os participantes, oferecendo insights para estimular o pensamento crítico, planejamento estratégico e uma apresentação eficaz. Além disso, você pode fornecer um resumo sobre o tema do trabalho e sugerir questões que o grupo pode explorar para enriquecer o conteúdo ou a discussão. Sua missão é garantir que os membros compreendam claramente o que precisa ser feito e estejam preparados para criar um trabalho acadêmico excepcional."},
        user_message
    ]
  
    # Obtenha a resposta do GPT-3
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
  
    # Obtenha a mensagem de resposta do assistente
    assistant_response = response.choices[0].message["content"]
    prazo = formatar_data(data['prazo'])
    newGroup = Grupo(id=str(uuid.uuid4()), nome=data['nome'], descricao=data['descricao'], membros=data['membros'], organizacao=assistant_response, wikis="O grupo foi criado no LearnLoop!", prazo=prazo)
    db.session.add(newGroup)
    db.session.commit()

    # Criar um contêiner no Azure Blob Storage para o novo grupo
    container_name = str(newGroup.id)
    if not upload_file_to_blob_storage(container_name, "", b""):
        return jsonify({"msg": "Erro ao criar o contêiner no Blob Storage"}), 500

    return jsonify({"msg": "grupo criado"})

# Rota para deletar grupo
@groups_bp.route("/api/delete-group/<id>", methods=["GET"])
def deleteGroup(id):
    group = Grupo.query.filter_by(id=id).first()
    db.session.delete(group)
    db.session.commit()
    return jsonify({"msg": "grupo deletado"})

# Rota para fazer upload de arquivo
@groups_bp.route('/api/upload-file/group/<id>', methods=["POST"])
def uploadFile(id):
    arquivo = request.files['arquivo']
    arquivo_db = Files(id=str(uuid.uuid4()), nome=arquivo.filename, group=id)
    db.session.add(arquivo_db)
    db.session.commit()
    container_name = id  # Nome do contêiner é o mesmo que o ID do grupo
    file_name = arquivo.filename  # Nome do arquivo
    if upload_file_to_blob_storage(container_name, file_name, arquivo):
        return "Arquivo enviado com sucesso para o Blob Storage"
    else:
        return "Ocorreu um erro durante o envio do arquivo para o Blob Storage", 500

# Rota para baixar arquivo
@groups_bp.route('/api/download-file/<group_id>/<file_name>', methods=["GET"])
def downloadFile(group_id, file_name):
      container_name = group_id  # Nome do contêiner é o mesmo que o ID do grupo
      # Remover caracteres < e > do nome do arquivo usando expressão regular
      file_name = re.sub(r'[<>]', '', file_name)
      # Codificar o nome do arquivo para garantir que caracteres especiais sejam tratados corretamente na URL
      file_name_encoded = urllib.parse.quote(file_name)
      blob_name = file_name  # Nome do blob é o mesmo que o nome do arquivo
      file_data = download_file_from_blob_storage(container_name, blob_name)
      if file_data:
          response = make_response(file_data)
          response.headers["Content-Disposition"] = f"attachment; filename={file_name_encoded}"
          return response
      else:
          return "Ocorreu um erro durante o download do arquivo", 500
