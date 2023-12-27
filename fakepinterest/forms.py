#Criar os formularios do nosso site
from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario 


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botaoConfirmacao = SubmitField("Fazer Login")

    def validate_email(self, email): #se quiser validar algo precisa colocar nesse padrão validate_O nome do campo
        usuario = Usuario.query.filter_by(email=email.data).first() #da uma Lista de usuários
        if not usuario:                     #email da classe usuário  #email do campo - .data = as informações do campo
            raise ValidationError("Usuario inexistente")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    userName = StringField("Nome de Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirmacaoSenha = PasswordField("Confirmar senha", validators=[DataRequired(), EqualTo("senha")])
    botaoConfirmacao = SubmitField("Criar conta")

    #se quiser validar algo precisa colocar nesse padrão validate_O nome do campo
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() #da uma Lista de usuários
        if usuario:                     #email da classe usuário  #email do campo - .data = as informações do campo
            raise ValidationError("E-mail já cadastrado, faça login para continuar")

class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botaoConfirmacao = SubmitField("Enviar")

