from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta
from fakepinterest.models import Usuario, Foto


#Colocando no ar -> Link privado
@app.route("/", methods=["GET", "POST"])#methods = Permite os 2 métodos
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", usuario=usuario.name))
            
    return render_template("homepage.html", form=formLogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formCriarConta = FormCriarConta()

    if formCriarConta.validate_on_submit(): #Se clicou no botão submit (Enviar)
        senha = bcrypt.generate_password_hash(formCriarConta.senha.data) #Criptografa a senha do usuário para armazenar no DB
                #bcrypt.check_password_hash() Converte a senha criptografada para a senha normal

        # processo DB
        usuario = Usuario(name= formCriarConta.userName.data, 
                          email=formCriarConta.email.data, 
                          senha=senha)
        database.session.add(usuario) #adiciona o usuario no DB
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", usuario=usuario.name))
    return render_template("criarconta.html", form=formCriarConta)

@app.route(f"/perfil/<usuario>")#Esses decoratos adiciona novos atributos a função 
@login_required
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)

@app.route("/logout")
@login_required #obrigatório está logado
def logout():
    logout_user() #ou pode passar o current_user
    return redirect(url_for("homepage"))