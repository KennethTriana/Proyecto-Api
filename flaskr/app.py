from flaskr import create_app
<<<<<<< HEAD
from flaskr.modelos.modelos import Cargo, Usuarios, Categoria, DetalleProductos, DetalleProductosIngresados, ProductosIngresados, Inventario, Movimientos, DetalleFactura, Factura, Alerta
from flaskr.modelos.modelos import db 
from flask_restful import Api
from flaskr.vistas.usuarios import VistaUsuarios, VistaLogin, VistaSignIn
from flaskr.vistas.alerta import VistaAlerta
from flaskr.vistas.cargo import VistaCargo
from flaskr.vistas.categoria import VistaCategoria
from flaskr.vistas.detallefactura import VistaDetalleFactura
from flaskr.vistas.detalleproductos import VistaDetalleProductos
from flaskr.vistas.factura import VistaFactura
from flaskr.vistas.inventario import VistaInventario
from flaskr.vistas.movimientos import VistaMovimientos
from flaskr.vistas.productos import VistaProductos
from flask_jwt_extended import JWTManager
=======
from flaskr.modelos.modelos import cargo, usuarios, categoria, detalle_productos, productos, detalle_productos_ingresados, productos_ingresados, inventario, movimientos, detalle_factura, factura, alerta
from .modelos import db 
from flask_restful import Api
from vistas import vistas
>>>>>>> 6a723bdab1a4b184e29ebb36ac2d5c8a3889931c

app = create_app('default')
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

api = Api(app)
<<<<<<< HEAD
api.add_resource(VistaUsuarios, '/usuarios', '/usuarios/<int:id>')
api.add_resource(VistaAlerta, '/alerta', '/alerta/<int:id>')
api.add_resource(VistaCargo, '/cargo', '/cargo/<int:id>')
api.add_resource(VistaCategoria, '/categoria', '/categoria/<int:id>')
api.add_resource(VistaDetalleFactura, '/detalle_factura', '/detalle_factura/<int:id>')
api.add_resource(VistaDetalleProductos, '/detalle_productos', '/detalle_productos/<int:id>')
api.add_resource(VistaFactura, '/factura', '/factura/<int:id>')
api.add_resource(VistaInventario, '/inventario', '/inventario/<int:id>')
api.add_resource(VistaMovimientos, '/movimientos', '/movimientos/<int:id>')
api.add_resource(VistaProductos, '/productos', '/productos/<int:id>')
api.add_resource(VistaLogin, '/login', '/login/<int:id>')
api.add_resource(VistaSignIn, '/signin', '/signin/<int:id>')

jwt = JWTManager(app)


#with app.app_context():
    #u = Usuarios(nombres='Carlitos Andres', apellidos='Gonzalez Diaz' correo='Carlitos10@gmail.com' contrasena='12345', telefono='3209876836', direccion='Cll 40 n° 45-67 sur', cargo_id='1')
    #c = Cargo(nombre='Gerente', descripcion='Administrador del sistema')
    #ca = Categoria(nombre='Comestibles', descripcion='Comestibles directos')
    #a = Alerta(nombre= 'Escacez de productos', stock_minimo= 10, stock= 8, producto_id= 1)
    #df = Detalle_Factura(cantidad= 20, producto_id= 1, detalle_productos_id=1)
    #dpi= Detalle_Productos_Ingresados(fecha_entrada= '6-11-2024', fecha_vence= '6-11-2025', cantidad= 10, precio_entrada= 8000, precio_salida= 10000)
    #dp= Detalle_Productos(fecha_entrada= '5-11-2024', fecha_vence= '5-11-2025', cantidad= 15, precio_entrada= 8000, precio_salida=10000)
    #f = Factura(fecha= '7-11-2024', monto_total= 5, precio_total= 50000, usuario_id=1)
    #i = Inventario(stock= 25, categoria_id= 1, productos_id= 1, productos_ingresados_id= 1)
    #m = Movimientos(tipo='Entrada', fecha= '7-11-2024', factura_id= 1, productos_id= 1)
    #pi= Productos_Ingresados(nombre='Carne Enlatada', fecha_entrada= '6-11-2024', fecha_vence= '6-11-2024', estado='Existente', usuarios_id= 1, categoria_id= 1, detalle_productos_id= 1)
    #p = Productos(nombre='Carne Enlatada', fecha_entrada= '6-11-2024', fecha_vence= '6-11-2024', estado='Existente', usuarios_id= 1, categoria_id= 1, detalle_productos_id= 1)


    #db.session.add(u)
    #db.session.add(c)
    #db.session.add(ca)
    #db.session.add(a)
    #db.session.add(df)
    #db.session.add(dpi)
    #db.session.add(dp)
    #db.session.add(f)
    #db.session.add(i)
    #db.session.add(m)
    #db.session.add(pi)
    #db.session.add(p)
    #db.session.commit()
    #print(Usuarios.query.all())
    #print(Cargo.query.all())
    #print(Categoria.query.all())
    #print(Alerta.query.all())
    #print(Detalle_Factura.query.all())
    #print(Detalle_Productos.query.all())
    #print(Detalle_Productos_Ingresados.query.all())
    #print(Factura.query.all())
    #print(Inventario.query.all())
    #print(Movimientos.query.all())
    #print(Productos_Ingresados.query.all())
    #print(Productos.query.all())
=======
api.add_resource(VistaUsuarios, '/usuarios')

with app.app_context():
    #Vista Usuarios --> Nixson
    #Vista Categoria --> Nicol 
    #Vista Productos --Nelson
>>>>>>> 6a723bdab1a4b184e29ebb36ac2d5c8a3889931c
