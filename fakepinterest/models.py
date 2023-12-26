#Estrutura banco de dados

from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin #dis qual a classe que gera a estrutura de login

@login_manager.user_loader
def load_usuario(id):#é obrigatório quando você cria uma estrutura de login
    return Usuario.query.get(int(id))#retorna um usuario especifico. Quando vai filtrar por E-mail usa o get()

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto = database.relationship("Foto", backref="usuario", lazy=True)


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="static/default.png") #armazena o nome do arquivo, não o arquivo em si, ele fica na fotos_post
    dataCriacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    idUsuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)


