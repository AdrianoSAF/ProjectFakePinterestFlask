from flask import render_template, url_for, redirect
from ProjectFakePinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename
from ProjectFakePinterest.forms import FormLogin, FormCriarConta, FormFoto
from ProjectFakePinterest.verify import Verify
from ProjectFakePinterest.models import Usuario, Foto
from ProjectFakePinterest.db import DatabaseGet
from sqlalchemy import select

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/loginpage", methods=["GET", "POST"])
def loginPage():
    formLogin = FormLogin()

    if Verify.isLoginValido(formLogin):
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        login_user(usuario)
        return redirect(url_for("perfil", id=current_user.id)) 
    return render_template("loginPage.html", form=formLogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criarConta():
    formCriarConta = FormCriarConta()

    if formCriarConta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formCriarConta.senha.data)
        usuario = Usuario(name= formCriarConta.userName.data,
                          email=formCriarConta.email.data,
                          senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id=usuario.id))
    return render_template("criarConta.html", form=formCriarConta)

@app.route(f"/perfil/<id>", methods=["GET", "POST"])
@login_required
def perfil(id):
    if int(id) == int(current_user.id):
        formFoto = FormFoto()
        if formFoto.validate_on_submit():
            arquivo = formFoto.foto.data
            nomeSeguro = secure_filename(arquivo.filename)

            path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                app.config["UPLOAD_FOLDER"],
                                nomeSeguro)
            arquivo.save(path)

            foto = Foto(imagem=nomeSeguro, idUsuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            #TESTE
        fotosz = DatabaseGet.getFoto(current_user.id)#Foto.query.filter_by(idUsuario=current_user.id).order_by(Foto.dataCriacao.desc())#all()
        return render_template("perfil.html", usuario=current_user, form=formFoto, fotos=fotosz)
    else:
        Usuario.query.get(int(id))
        usuario = Usuario.query.get(int(id))
        fotosz = DatabaseGet.getFoto(id)#Foto.query.filter_by(idUsuario=id).order_by(Foto.dataCriacao.desc())#all()
    return render_template("perfil.html", usuario=usuario, form=None, fotos=fotosz)

@app.route(f"/deletefoto/<fotoId>", methods=["GET", "POST"])
@login_required
def deleteFoto(fotoId):
    user = database.get_or_404(Foto, fotoId)

    #if request.method == "POST":
    database.session.delete(user)
    database.session.commit()
    print(current_user.id)
    return redirect(url_for("perfil", id=current_user.id)) 
    return render_template("fotoSelected.html", usuario=current_user)

@app.route("/logout")
@login_required #obrigatório está logado
def logout():
    logout_user() #ou pode passar o current_user
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.dataCriacao.desc()).all() #pega todas as fotos do Banco de dados. para limitar a 100 [100:]
    return render_template("feed.html", fotos=fotos)









