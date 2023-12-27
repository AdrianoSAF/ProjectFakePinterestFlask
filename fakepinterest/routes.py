from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename

#Colocando no ar -> Link privado
@app.route("/", methods=["GET", "POST"])#methods = Permite os 2 métodos
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), formLogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id=usuario.id))
            
    return render_template("homepage.html", form=formLogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formCriarConta = FormCriarConta()

    if formCriarConta.validate_on_submit(): #Se clicou no botão submit (Enviar)
        senha = bcrypt.generate_password_hash(formCriarConta.senha.data).decode("utf-8") #Criptografa a senha do usuário para armazenar no DB
                #bcrypt.check_password_hash() Converte a senha criptografada para a senha normal

        # processo DB
        usuario = Usuario(name= formCriarConta.userName.data, 
                          email=formCriarConta.email.data, 
                          senha=senha)
        database.session.add(usuario) #adiciona o usuario no DB
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id=usuario.id))
    return render_template("criarconta.html", form=formCriarConta)

@app.route(f"/perfil/<id>", methods=["GET", "POST"])#Esses decoratos adiciona novos atributos a função 
@login_required
def perfil(id):
    if int(id) == int(current_user.id):
        #usuario está vendo o perfil dele

        formFoto = FormFoto()
        if formFoto.validate_on_submit():
            arquivo = formFoto.foto.data
            nomeSeguro = secure_filename(arquivo.filename)

            #salva o arquivo na pasta fotos_post
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), #os.caminho abissoluto( do arquivo atual) = no caso o caminho do routes
                              app.config["UPLOAD_FOLDER"], #uma constante que está no Main (caminho da fotos_post)
                              nomeSeguro)#nome do arquivo que quero salvar
            arquivo.save(caminho)
            
            #registra o arquivo no banco de dados
            foto = Foto(imagem=nomeSeguro, idUsuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            

        return render_template("perfil.html", usuario=current_user, form=formFoto)
    else:
        Usuario.query.get(int(id))
        usuario = Usuario.query.get(int(id))
    return render_template("perfil.html", usuario=usuario, form=None)

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