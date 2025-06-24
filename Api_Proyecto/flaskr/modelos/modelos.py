from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# ==================== MODELOS ====================

class Cargo(db.Model):
    __tablename__ = 'cargo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(256))
    apellidos = db.Column(db.String(256))
    correo = db.Column(db.String(256))
    contrasena_hash = db.Column(db.String(128)) 
    foto_perfil = db.Column(db.String(255))
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.String(256))
    eliminado = db.Column(db.Boolean, default=False)
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'))
    productos = db.relationship('Productos', backref='usuario', cascade='all, delete-orphan')

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
    nombre = db.Column(db.String(255), nullable=False)


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
    stock_minimo = db.Column(db.Integer, nullable=False, default=5)  # 👈 ESTE
    usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    
    categoria = db.relationship('Categoria', backref='productos')

    historial = db.relationship('Historial', back_populates='producto', cascade='all, delete-orphan', passive_deletes=True)



class Historial(db.Model):
    __tablename__ = 'historial'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad = db.Column(db.Integer, nullable=True)
    accion = db.Column(db.String(256))  
    descripcion = db.Column(db.String(255))  
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id', ondelete='CASCADE'), nullable=False)


    usuario = db.relationship('Usuarios', backref='historial')
    producto = db.relationship('Productos', back_populates='historial')



class Alerta(db.Model):
    __tablename__ = 'alerta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    stock_minimo = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    producto = db.relationship('Productos', backref='alertas')


class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad_a_vender = db.Column(db.Integer)
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    Productos = db.relationship('Productos', backref='Venta')


# ==================== SCHEMAS ====================

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
        sqla_session = db.session  
        include_relationships = True
        load_instance = True
        include_fk = True
        
        nombre = fields.Str(required=True) 


class ProductosSchema(SQLAlchemyAutoSchema):
    categoria = fields.Nested(CategoriaSchema)
    usuarios = fields.Nested(UsuariosSchema)
    class Meta:
        model = Productos
        include_relationships = True
        load_instance = True
        include_fk = True


class ProductoHistorialSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Productos
        fields = ("nombre", "fecha_entrada")  


class HistorialSchema(SQLAlchemyAutoSchema):
    producto = fields.Nested(ProductoHistorialSchema)
    usuario_nombre = fields.Function(lambda obj: obj.usuario.nombres if obj.usuario else None)
    class Meta:
        model = Historial
        include_fk = True
        load_instance = True
        include_relationships = True


class AlertaSchema(SQLAlchemyAutoSchema):
    productos = fields.Nested(ProductosSchema)
    productos_nombre = fields.Function(lambda obj: obj.producto.nombre if obj.producto else None)
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
