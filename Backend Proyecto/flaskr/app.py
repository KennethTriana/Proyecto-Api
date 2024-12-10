from flaskr import create_app
from flaskr.modelos.modelos import Cargo, Usuarios, Categoria, Productos, Movimientos, Factura, Alerta
from flaskr.modelos.modelos import db 
from flask_restful import Api
from flaskr.vistas.usuarios import VistaUsuarios, VistaLogin, VistaLogout, VistaProductos, VistaPerfil, CambioImagen, VistaVentas
from flaskr.vistas.alerta import VistaAlerta
from flaskr.vistas.cargo import VistaCargo
from flaskr.vistas.categoria import VistaCategoria
from flaskr.vistas.factura import VistaFactura
from flaskr.vistas.movimientos import VistaMovimientos
from flask_jwt_extended import JWTManager
from .modelos import db 
from flask_migrate import Migrate
from datetime import datetime
from flask_cors import CORS

app = create_app('default')
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

CORS(app)
migrate = Migrate(app, db)

api = Api(app)
api.add_resource(VistaVentas, '/ventas/<id>')
api.add_resource(CambioImagen, '/imagen')
api.add_resource(VistaPerfil, '/perfil')
api.add_resource(VistaUsuarios, '/usuarios')
api.add_resource(VistaAlerta, '/alerta')
api.add_resource(VistaCargo, '/cargo')
api.add_resource(VistaCategoria, '/categoria')
api.add_resource(VistaFactura, '/factura')
api.add_resource(VistaMovimientos, '/movimientos')
api.add_resource(VistaProductos, '/productos')
api.add_resource(VistaLogin, '/login')
api.add_resource(VistaLogout, '/logout')

jwt = JWTManager(app)

@app.before_first_request
def create_initial_data():

    user = Usuarios(nombres='Kenneth Jhoan', apellidos='Triana Gonzalez', correo='Kennethtriana@gmail.com', contrasena='12345678', foto_perfil='https://images.hdqwalls.com/download/maluma-monochrome-5k-9y-2048x1152.jpg', telefono='3153183919', direccion='Cll 40c sur #82-22', cargo_id= 1)
    db.session.add(user)

    role1 = Cargo(nombre='gerente', descripcion='Administrador de la plataforma')
    role2 = Cargo(nombre='empleado', descripcion='Vendedor de productos')
    db.session.add(role1)
    db.session.add(role2)

    product = Productos(nombre='Leche', fecha_entrada=datetime(2024, 6, 12), fecha_vence=datetime(2025, 6, 12), estado='disponible', cantidad=100, precio_entrada=1000, precio_salida=1200, usuarios_id=1, categoria_id=1)
    db.session.add(product)

    product2 = Productos(nombre='Queso', fecha_entrada=datetime(2024, 6, 12), fecha_vence=datetime(2025, 6, 12), estado='disponible', cantidad=5, precio_entrada=1000, precio_salida=1200, usuarios_id=1, categoria_id=1)
    db.session.add(product2)

    category = Categoria(nombre='Lacteos', descripcion='Productos con lactosa')
    db.session.add(category)

    factury = Factura(fecha=datetime(2024, 6, 12), monto_total=10, cantidad=1, precio_unitario=1200, usuario_id=1, productos_id=1)
    db.session.add(factury)

    movimy = Movimientos(fecha=datetime(2024, 6, 12), tipo='salida', factura_id=1, productos_id=1)
    db.session.add(movimy)

    alerty = Alerta(nombre='Queso', stock_minimo=10, stock=5, productos_id=2)
    db.session.add(alerty)

    db.session.commit()