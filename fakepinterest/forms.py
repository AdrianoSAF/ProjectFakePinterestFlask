#Criar os formularios do nosso site
from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario 


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botaoConfirmacao = SubmitField("Fazer Login")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    userName = StringField("Nome de Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirmacaoSenha = PasswordField("Confirmar senha", validators=[DataRequired(), Length(6, 20)])
    botaoConfirmacao = SubmitField("Criar conta")

    def validateEmail(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() #da uma Lista de usuários
        if usuario():                     #email da classe usuário  #email do campo - .data = as informações do campo
            return ValidationError("E-mail já cadastrado, faça login para cintinuar")


