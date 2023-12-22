from flask import render_template, url_for
from fakepinterest import app
from flask_login import login_required

#Colocando no ar -> Link privado
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route(f"/perfil/<usuario>")#Esses decoratos adiciona novos atributos a função 
@login_required
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)