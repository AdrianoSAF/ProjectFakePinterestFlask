from flask import render_template, url_for
from fakepinterest import app

#Colocando no ar -> Link privado
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route(f"/perfil/<usuario>")
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)