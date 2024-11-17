from flask import Flask
from flaskr import create_app
from flaskr.modelos.modelos import Categoria
from .modelos import db
from flask_restful import Api
from flaskr.vistas.vistacategoria import VistaCategoria


app = create_app('default')
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaCategoria, '/Categoria', '/Categoria/<int:id>')

#with app.app_context():