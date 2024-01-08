from ProjectFakePinterest.models import Usuario, Foto
from ProjectFakePinterest import bcrypt

class Database:

    def checkEmail(email):
        usuario = Usuario.query.filter_by(email=email).first() #da uma Lista de usuários
        if usuario:                     #email da classe usuário  #email do campo - .data = as informações do campo
            return True
        return False
        
    
    def checkPassword(senha, email):
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
            return True
        return False
    

class DatabaseGet:

    def getFoto(idUsuario):
        return Foto.query.filter_by(idUsuario=idUsuario).order_by(Foto.dataCriacao.desc())