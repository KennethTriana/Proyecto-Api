from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configuración de la base de datos
USER_DB = 'root'
PASS_DB = ''
URL_DB = 'localhost'
NAME_DB = 'noviembre'
FULL_URL_DB = f'mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configuración de la migración; copia el siguiente código y luego ejecuta: flask db init
migrate = Migrate()
migrate.init_app(app, db)

class Cargo(db.Model):
    _tablename_ = 'cargo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    descripcion = db.Column(db.String(256))

    def _init_(self, nombre):
        self.nombre = nombre

    def json(self):
        return {'nombre': self.nombre}

class Usuarios(db.Model):
    _tablename_ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(256))
    apellidos = db.Column(db.String(256))
    correo = db.Column(db.String(256))
    contrasena = db.Column(db.String(256))
    telefono = db.Column(db.Integer)
    direccion = db.Column(db.String(256))
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'))

    def _init_(self, nombres, apellidos, correo, contrasena, telefono, direccion):
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.contrasena = contrasena
        self.telefono = telefono
        self.direccion = direccion


    def json(self):
        return {'nombres': self.nombres, 'apellidos': self.apellidos, 'correo': self.correo, 'contrasena': self.contrasena, 'telefono': self.telefono, 'direccion': self.direccion}
    
class Categoria(db.Model):
    _tablename_ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    descripcion = db.Column(db.String(256))

    def _init_(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def json(self):
        return {'nombre': self.nombre, 'descripcion': self.descripcion}
    
class DetalleProductos(db.Model):
    _tablename_ = 'detalle_productos'
    id = db.Column(db.Integer, primary_key=True)
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    cantidad = db.Column(db.Integer)
    precio_entrada = db.Column(db.Integer)
    precio_salida = db.Column(db.Integer)

    def _init_(self, fecha_entrada, fecha_vence, cantidad, precio_entrada, precio_salida):
        self.fecha_entrada = fecha_entrada
        self.fecha_vence = fecha_vence
        self.cantidad = cantidad
        self.precio_entrada = precio_entrada
        self.precio_salida = precio_salida

    def json(self):
        return {'fecha_entrada': self.fecha_entrada, 'fecha_vence': self.fecha_vence, 'cantidad': self.cantidad, 'precio_entrada': self.precio_entrada, 'precio_salida': self.precio_salida}
    
class Productos(db.Model):
    _tablename_ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    estado = db.Column(db.String(256))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    detalle_productos_id = db.Column(db.Integer, db.ForeignKey('detalle_productos.id'))
    
    def _init_(self, nombre, fecha_entrada, fecha_vence, estado):
        self.nombre = nombre
        self.fecha_entrada = fecha_entrada
        self.fecha_vence = fecha_vence
        self.estado = estado

    def json(self):
        return {'nombre': self.nombre, 'fecha_entrada': self.fecha_entrada, 'fecha_vence': self.fecha_vence, 'estado': self.estado}
    
class DetalleProductosIngresados(db.Model):
    _tablename_ = 'detalle_productos_ingresados'
    id = db.Column(db.Integer, primary_key=True)
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    cantidad = db.Column(db.Integer)
    precio_entrada = db.Column(db.Integer)
    precio_salida = db.Column(db.Integer)

    def _init_(self, fecha_entrada, fecha_vence, cantidad, precio_entrada, precio_salida):
        self.fecha_entrada = fecha_entrada
        self.fecha_vence = fecha_vence
        self.cantidad = cantidad
        self.precio_entrada = precio_entrada
        self.precio_salida = precio_salida

    def json(self):
        return {'fecha_entrada': self.fecha_entrada, 'fecha_vence': self.fecha_vence, 'cantidad': self.cantidad, 'precio_entrada': self.precio_entrada, 'precio_salida': self.precio_salida}
    
class ProductosIngresados(db.Model):
    _tablename_ = 'productos_ingresados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    estado = db.Column(db.String(256))
    usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    detalle_productos_id = db.Column(db.Integer, db.ForeignKey('detalle_productos_ingresados.id'))

    def _init_(self, nombre, fecha_entrada, fecha_vence, estado):
        self.nombre = nombre
        self.fecha_entrada = fecha_entrada
        self.fecha_vence = fecha_vence
        self.estado = estado

    def json(self):
        return {'nombre': self.nombre, 'fecha_entrada': self.fecha_entrada, 'fecha_vence': self.fecha_vence, 'estado': self.estado}
class Inventario(db.Model):
    _tablename_ = 'inventario'
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.Integer)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    productos_ingresados_id = db.Column(db.Integer, db.ForeignKey('productos_ingresados.id'))

    def _init_(self, cantidad_producto, stock, fecha_entrada):
        self.cantidad_producto = cantidad_producto
        self.stock = stock
        self.fecha_entrada = fecha_entrada

    def json(self):
        return {'cantidad_producto': self.cantidad_producto, 'stock': self.stock, 'fecha_entrada': self.fecha_entrada}
    
class DetalleFactura(db.Model):
    _tablename_ = 'detalle_factura'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    detalle_productos_id = db.Column(db.Integer, db.ForeignKey('detalle_productos.id'))  

    def _init_(self, producto, precio, cantidad):
        self.producto = producto
        self.precio = precio
        self.cantidad = cantidad

    def json(self):
        return {'producto': self.producto, 'precio': self.precio, 'cantidad': self.cantidad}
    
class Factura(db.Model):
    _tablename_ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    monto_total = db.Column(db.Integer)
    precio_total = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    def _init_(self, fecha, monto_total, precio_total):
        self.fecha = fecha
        self.monto_total = monto_total
        self.precio_total = precio_total

    def json(self):
        return {'fecha': self.fecha, 'monto_total': self.monto_total, 'precio_total': self.precio_total}
      
class Movimientos(db.Model):
    _tablename_ = 'movimientos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    tipo = db.Column(db.String(256))
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'))
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))

    def _init_(self, fecha, tipo, cantidad):
        self.fecha = fecha
        self.tipo = tipo
        self.cantidad = cantidad

    def json(self):
        return {'fecha': self.fecha, 'tipo': self.tipo, 'cantidad': self.cantidad}
     
class Alerta(db.Model):
    _tablename_ = 'alerta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    stock_minimo = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))

    def _init_(self, nombre, stock_minimo, stock):
        self.nombre = nombre
        self.stock_minimo = stock_minimo
        self.stock = stock

    def json(self):
        return {'nombre': self.nombre, 'stock_minimo': self.stock_minimo, 'stock': self.stock}


    def _str_(self):
        return str(self._class) + ": " + str(self.dict_)