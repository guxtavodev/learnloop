
import uuid 
from passlib.hash import bcrypt_sha256

class ArtigosApp():
  from app import Artigo, Complementos, User, db
  def __init__(self, id) -> None:
    self.artigo = id
    self.artigo = Artigo.query.get(id)

  def create_artigo(self, titulo, texto, autor, data, categoria, tags):
    try:
      self.artigo = Artigo(
        titulo=titulo,
        texto=texto,
        autor=autor,
        data=data,
        categoria=categoria,
        tags=tags,
        id=str(uuid.uuid4())
      )
      db.session.add(self.artigo)
      db.session.commit()
      return {
        "msg": "success",
        "id": self.artigo.id
      }
    except:
      return {
        "msg": 'error'
      }

  def apagar_artigo(self, id, password):
    artigo = Artigo.query.filter_by(id=id).first()
    user = User.query.filter_by(id=artigo.autor).first()
    if artigo:
      if bcrypt_sha256.verify(password, user.password):
        db.session.delete(artigo)
        db.session.commit()
        return True
      else:
        return False
    else:
      return False

  def editar_artigo(self, titulo, texto):
    if self.artigo:
      self.artigo.titulo = titulo
      self.artigo.texto = texto
      db.session.commit()
      return True
    else:
      return False

  def buscar_artigo(self, id):
    artigo = Artigo.query.filter_by(id=id).first()
    complementos = Complementos.query.filter_by(artigo=id).all()
    if artigo:
      return {
        "id": artigo.id,
        "titulo": artigo.titulo,
        "texto": artigo.texto,
        "autor": artigo.autor,
        "data": artigo.data,
        "categoria": artigo.categoria,
        "tags": artigo.tags,
        "complementos": complementos
      }

    else:
      return False 

  def buscar_artigo_categoria(self, categoria):
    artigo = Artigo.query.filter_by(categoria=categoria).all()
    if artigo:
      return {
        "artigo": artigo
      }
    else:
      return False

  def buscar_artigo_tag(self, tag):
    artigo = Artigo.query.filter_by(tags=tag).all()
    if artigo:
      return {
        "artigo": artigo
      }
    else:
      return False

  def buscar_artigo_autor(self, autor):
    artigo = Artigo.query.filter_by(autor=autor).all()
    if artigo:
      return {
        "artigo": artigo
      }
    else:
      return False

  def buscar_artigo_data(self, data):
    artigo = Artigo.query.filter_by(data=data).all()
    if artigo:
      return {
        "artigo": artigo
      }
    else:
      return False

  def buscar_artigo_titulo(self, titulo):
    artigo = Artigo.query.filter_by(titulo=titulo).all()
    if artigo:
      return {
        "artigo": artigo
      }
    else:
      return False

  def list_artigos_recentes(self):
    artigo = Artigo.query.order_by(Artigo.data.desc()).all()
    if artigo:
      return {
        "artigo": artigo
      }
    else:
      return False

  def list_artigos_populares(self):
    artigo = Artigo.query.order_by(Artigo.likes.desc()).all()
    if artigo:
      return {
        "artigo": artigo
      }
    else:
      return False