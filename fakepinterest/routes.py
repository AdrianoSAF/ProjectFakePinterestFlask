from flask import render_template, url_for
from fakepinterest import app
from flask_login import login_required
from fakepinterest.forms import FormLogin, FormCriarConta

#Colocando no ar -> Link privado
@app.route("/", methods=["GET", "POST"])#methods = Permite os 2 métodos
def homepage():
    formLogin = FormLogin()
    return render_template("homepage.html", form=formLogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formCriarConta = FormCriarConta()
    return render_template("criarconta.html", form=formCriarConta)

@app.route(f"/perfil/<usuario>")#Esses decoratos adiciona novos atributos a função 
@login_required
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)