from flaskr import create_app
from flaskr.modelos.modelos import cargo, usuarios, categoria, detalle_productos, productos, detalle_productos_ingresados, productos_ingresados, inventario, movimientos, detalle_factura, factura, alerta
from .modelos import db 
from flask_restful import Api
from vistas import vistas

app = create_app('default')
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaUsuarios, '/usuarios')

with app.app_context():
    #Vista Usuarios --> Nixson
    #Vista Categoria --> Nicol 
    #Vista Productos --Nelson