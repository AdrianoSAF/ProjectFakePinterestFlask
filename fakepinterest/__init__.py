from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#criando site
app = Flask(__name__)
database = SQLAlchemy(app)

from fakepinterest import app