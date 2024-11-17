from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime

app = Flask(__name__)

# Configuración de la base de datos
USER_DB = 'root'
PASS_DB = ''
URL_DB = 'localhost'
NAME_DB = 'ORM'
FULL_URL_DB = f'mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configuración de la migración; copia el siguiente código y luego ejecuta: flask db init
migrate = Migrate()
migrate.init_app(app, db)

class Cargo(db.Model):
    __tablename__ = 'cargo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    descripcion = db.Column(db.String(256))

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def json(self):
        return {'nombre': self.nombre, 'descripcion': self.descripcion}

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(256))
    apellidos = db.Column(db.String(256))
    correo = db.Column(db.String(256))
    contrasena = db.Column(db.String(256))
    telefono = db.Column(db.Integer)
    direccion = db.Column(db.String(256))
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'))

    def __init__(self, nombres, apellidos, correo, contrasena, telefono, direccion):
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.contrasena = contrasena
        self.telefono = telefono
        self.direccion = direccion


    def json(self):
        return {'nombres': self.nombres, 'apellidos': self.apellidos, 'correo': self.correo, 'contrasena': self.contrasena, 'telefono': self.telefono, 'direccion': self.direccion}
    
class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    descripcion = db.Column(db.String(256))

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def json(self):
        return {'nombre': self.nombre, 'descripcion': self.descripcion}
    
class DetalleProductos(db.Model):
    __tablename__ = 'detalle_productos'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    precio_entrada = db.Column(db.Integer)
    precio_salida = db.Column(db.Integer)

    def __init__(self, cantidad, precio_entrada, precio_salida):
        self.cantidad = cantidad
        self.precio_entrada = precio_entrada
        self.precio_salida = precio_salida

    def json(self):
        return {'cantidad': self.cantidad, 'precio_entrada': self.precio_entrada, 'precio_salida': self.precio_salida}
    
class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    estado = db.Column(db.String(256))
    usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    detalle_productos_id = db.Column(db.Integer, db.ForeignKey('detalle_productos.id'))
    
    def __init__(self, nombre, fecha_entrada, fecha_vence, estado):
        self.nombre = nombre
        self.fecha_entrada = fecha_entrada
        self.fecha_vence = fecha_vence
        self.estado = estado

    def json(self):
        return {'nombre': self.nombre, 'fecha_entrada': self.fecha_entrada, 'fecha_vence': self.fecha_vence, 'estado': self.estado}

class Inventario(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    estado = db.Column(db.String(256))
    stock = db.Column(db.Integer)

    def __init__(self, nombre, fecha_entrada, fecha_vence, estado, stock):
        self.nombre = nombre
        self.fecha_entrada = fecha_entrada
        self.fecha_vence = fecha_vence
        self.estado = estado
        self.stock = stock

    def json(self):
        return {'nombre': self.nombre, 'fecha_entrada': self.fecha_entrada, 'fecha_vence': self.fecha_vence, 'estado': self.estado, 'stock': self.stock,}
    
class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'))

    def __init__(self, cantidad):
        self.cantidad = cantidad

    def json(self):
        return {'cantidad': self.cantidad}
    
class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    monto_total = db.Column(db.Integer)
    precio_total = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    detalle_factura_id = db.Column(db.Integer, db.ForeignKey('detalle_factura.id'))

    def __init__(self, fecha, monto_total, precio_total):
        self.fecha = fecha
        self.monto_total = monto_total
        self.precio_total = precio_total

    def json(self):
        return {'fecha': self.fecha, 'monto_total': self.monto_total, 'precio_total': self.precio_total}
      
class Movimientos(db.Model):
    __tablename__ = 'movimientos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    tipo = db.Column(db.String(256))
    detalle_factura_id = db.Column(db.Integer, db.ForeignKey('detalle_factura.id'))
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'))

    def __init__(self, fecha, tipo, cantidad):
        self.fecha = fecha
        self.tipo = tipo

    def json(self):
        return {'fecha': self.fecha, 'tipo': self.tipo}
     
class Alerta(db.Model):
    __tablename__ = 'alerta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    stock_minimo = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'))

    def __init__(self, nombre, stock_minimo, stock):
        self.nombre = nombre
        self.stock_minimo = stock_minimo
        self.stock = stock

    def json(self):
        return {'nombre': self.nombre, 'stock_minimo': self.stock_minimo, 'stock': self.stock}


    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)