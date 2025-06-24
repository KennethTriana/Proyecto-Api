from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cargo(db.Model):
    __tablename__ = 'cargo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    descripcion = db.Column(db.String(256))

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(256))
    apellidos = db.Column(db.String(256))
    correo = db.Column(db.String(256))
    contrasena_hash = db.Column(db.String(255))
    foto_perfil = db.Column(db.String(255))
    telefono = db.Column(db.Integer)
    direccion = db.Column(db.String(256))
    eliminado = db.Column(db.Boolean, default=False)
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'))

    @property
    def contrasena(self):
        raise AttributeError("La contraseña no es un atributo legible.")

    @contrasena.setter
    def contrasena(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def verificar_contrasena(self, password):
        return check_password_hash(self.contrasena_hash, password)

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    descripcion = db.Column(db.String(256))

class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    fecha_entrada = db.Column(db.Date)
    fecha_vence = db.Column(db.Date)
    estado = db.Column(db.String(256))
    cantidad = db.Column(db.Integer)
    precio_entrada = db.Column(db.Integer)
    precio_salida = db.Column(db.Integer)
    eliminado = db.Column(db.Boolean, default=False)
    usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))

class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    monto_total = db.Column(db.Float) 
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Float) 
    productos_id = db.Column(db.Integer, ForeignKey('productos.id'))
    usuario_id = db.Column(db.Integer, ForeignKey('usuarios.id'))
    usuario = db.relationship('Usuarios', backref='factura')

class Movimientos(db.Model):
    __tablename__ = 'movimientos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    tipo = db.Column(db.String(256))
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'))
    factura = db.relationship('Factura', backref='movimientos')
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    productos = db.relationship('Productos', backref='movimientos')

class Alerta(db.Model):
    __tablename__ = 'alerta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    stock_minimo = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    Productos = db.relationship('Productos', backref='alertas')

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad_a_vender = db.Column(db.Integer)
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    Productos = db.relationship('Productos', backref='Venta')


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class CargoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cargo
        include_relationships = True
        load_instance = True
        include_fk = True

class UsuariosSchema(SQLAlchemyAutoSchema):
    cargo = fields.Nested(CargoSchema)  
    class Meta:
        model = Usuarios
        include_relationships = True
        load_instance = True
        include_fk = True

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        include_relationships = True
        load_instance = True
        include_fk = True

class ProductosSchema(SQLAlchemyAutoSchema):
    categoria = fields.Nested(CategoriaSchema)
    usuarios = fields.Nested(UsuariosSchema)
    class Meta:
        model = Productos
        include_relationships = True
        load_instance = True
        include_fk = True

class FacturaSchema(SQLAlchemyAutoSchema):
    usuario = fields.Nested(UsuariosSchema)
    class Meta:
        model = Factura
        include_relationships = True
        load_instance = True
        include_fk = True

class MovimientosSchema(SQLAlchemyAutoSchema):
    factura = fields.Nested(FacturaSchema) 
    productos = fields.Nested(ProductosSchema)
    class Meta:
        model = Movimientos
        include_relationships = True
        load_instance = True
        include_fk = True

class AlertaSchema(SQLAlchemyAutoSchema):
    productos = fields.Nested(ProductosSchema)
    class Meta:
        model = Alerta
        include_relationships = True
        load_instance = True
        include_fk = True

class VentaSchema(SQLAlchemyAutoSchema):
    productos = fields.Nested(ProductosSchema)
    class Meta:
        model = Venta
        include_relationships = True
        load_instance = True
        include_fk = True
    