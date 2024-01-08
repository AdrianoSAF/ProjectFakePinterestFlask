from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from ProjectFakePinterest.models import Usuario
from ProjectFakePinterest.db import Database

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botaoConfirmacao = SubmitField("Fazer Login")

    def validate_email(self, email):
        if not Database.checkEmail(email=email.data):
            raise ValidationError("Usuario inexistente")
        
    def validate_senha(self, senha):
        if not Database.checkPassword(senha=senha.data, email=self.email.data):
            raise ValidationError("Senha incorreta")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    userName = StringField("Nome de Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacaoSenha = PasswordField("Confirmar Senha", validators=[EqualTo("senha")])
    botaoConfirmacao = SubmitField("Criar Conta")

    def validate_email(self, email):
        if Database.checkEmail(email): #MELHORIA if Database.checkUser(column=email, columnName='email'):
            raise ValidationError("E-mail já cadastrado, Faça login para continuar")
        
class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botaoConfirmacao = SubmitField("Enviar")



