from flask_login import login_required, login_user
from ProjectFakePinterest.models import Usuario
from ProjectFakePinterest import app, database, bcrypt
from ProjectFakePinterest.db import Database


class Verify:

    def isLoginValido(formLogin):
        if formLogin.validate_on_submit():
            email = Database.checkEmail(email=formLogin.email.data)
            senha = Database.checkPassword(senha=formLogin.senha.data, email=formLogin.email.data)
            if email and senha:
                return True
            return False
        return False