from flaskr import create_app
from flaskr.modelos.modelos import Cargo, Usuarios, Categoria, Productos, Alerta
from flaskr.modelos.modelos import db 
from flask_restful import Api
from flaskr.vistas.historial import VistaHistorial
from flaskr.vistas.usuarios import RecuperarContrasena, RestablecerContrasena, VistaRegistro, VistaLogin, VistaLogout, VistaProductos, VistaPerfil, CambioImagen, VistaUsuarios, VistaVentas
from flaskr.vistas.alerta import VistaAlerta
from flaskr.vistas.cargo import VistaCargo
from flaskr.vistas.categoria import VistaCategoria
from flask_jwt_extended import JWTManager
from .modelos import db 
from flask_migrate import Migrate
from flask_cors import CORS

app = create_app('default')
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
db.create_all()

db.create_all()

def crear_cargos_por_defecto():
    if not Cargo.query.get(1):
        admin = Cargo(id=1, nombre='Administrador')
        db.session.add(admin)
    if not Cargo.query.get(2):
        empleado = Cargo(id=2, nombre='Empleado')
        db.session.add(empleado)
    db.session.commit()

crear_cargos_por_defecto()

CORS(app)
migrate = Migrate(app, db)

api = Api(app)
api.add_resource(VistaVentas, '/ventas/<id>')
api.add_resource(CambioImagen, '/imagen')
api.add_resource(VistaPerfil, '/perfil')
api.add_resource(VistaRegistro, '/usuarios')
api.add_resource(VistaUsuarios, '/user', '/user/<int:id>')
api.add_resource(VistaAlerta, '/alerta')
api.add_resource(VistaCargo, '/cargo')
api.add_resource(VistaCategoria, '/categorias', '/categorias/<int:id>')
api.add_resource(VistaHistorial, '/historial')
api.add_resource(VistaProductos, '/productos', '/productos/<int:id>')
api.add_resource(VistaLogin, '/login')
api.add_resource(RecuperarContrasena, '/recuperar-contrasena')
api.add_resource(RestablecerContrasena, '/restablecer-contrasena')
api.add_resource(VistaLogout, '/logout')

jwt = JWTManager(app)