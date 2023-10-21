from app import User, db
import uuid 
from passlib.hash import bcrypt_sha256

class UsersApp():
  def __init__(self, id):
    self.id = id
    self.user = User.query.get(id)

  @staticmethod
  def crip(dado):
    dado_criptografado = bcrypt_sha256.hash(dado)
    return str(dado_criptografado)

  def signup(self, username, password):
    try:
      self.user = User(username=username, password=password, id=str(uuid.uuid4()))
      db.session.add(self.user)
      db.session.commit()
      return True
    except:
      return False

  def login(self, username, password):
    user = User.query.filter_by(username=username).first()
    if user:
      if bcrypt_sha256.verify(password, user.password):
        return {
          "id": user.id,
          "msg": "success"
        }
      else:
        return {
          "msg": "senha incorreta"
        }
    else:
      return "usuario nao existe"

  def apagar_conta(self, password):
    user = User.query.filter_by(id=self.user.id).first()
    if user:
      if bcrypt_sha256.verify(password, user.password):
        db.session.delete(user)
        db.session.commit()
        return True
      else:
        return False
    else:
      return False
    
