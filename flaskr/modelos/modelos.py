<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 1eec5f1ca3b1ae543c77fc627043c268114a0236
=======
>>>>>>> 7e7301d4683567745a9015d3cc9b53150fb3f653
from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
import enum

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

<<<<<<< HEAD
<<<<<<< HEAD
from werkzeug.security import generate_password_hash, check_password_hash

=======
>>>>>>> 1eec5f1ca3b1ae543c77fc627043c268114a0236
=======
>>>>>>> 7e7301d4683567745a9015d3cc9b53150fb3f653
db = SQLAlchemy()

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
<<<<<<< HEAD
<<<<<<< HEAD
    contrasena_hash = db.Column(db.String(255))
=======
    contrasena = db.Column(db.String(256))
>>>>>>> 1eec5f1ca3b1ae543c77fc627043c268114a0236
=======
    contrasena = db.Column(db.String(256))
>>>>>>> 7e7301d4683567745a9015d3cc9b53150fb3f653
    telefono = db.Column(db.Integer)
    direccion = db.Column(db.String(256))
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'))

<<<<<<< HEAD
<<<<<<< HEAD
    @property
    def contrasena(self):
        raise attributeError("La contraseña no es un atributo legible.")

    @contrasena.setter
    def contrasena(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def verificar_contrasena(self, password):
        return check_password_hash(self.contrasena_hash, password) 

=======
>>>>>>> 1eec5f1ca3b1ae543c77fc627043c268114a0236
=======
>>>>>>> 7e7301d4683567745a9015d3cc9b53150fb3f653
class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    descripcion = db.Column(db.String(256))

class Inventario(db.Model):
    __tablename__ = 'inventario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    estado = db.Column(db.String(256))
    stock = db.Column(db.Integer)

class DetalleProductos(db.Model):
    __tablename__ = 'detalle_productos'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    precio_entrada = db.Column(db.Integer)
    precio_salida = db.Column(db.Integer)

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

class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'))

class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    monto_total = db.Column(db.Integer)
    precio_total = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    detalle_factura_id = db.Column(db.Integer, db.ForeignKey('detalle_factura.id'))

class Movimientos(db.Model):
    __tablename__ = 'movimientos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    tipo = db.Column(db.String(256))
    detalle_factura_id = db.Column(db.Integer, db.ForeignKey('detalle_factura.id'))
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'))

class Alerta(db.Model):
    __tablename__ = 'alerta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    stock_minimo = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'))

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

class UsuariosSchema(SQLAlchemyAutoSchema):
    cargo = fields.Nested(CargoSchema)  
    class Meta:
        model = Usuarios
        include_relationships = True
        load_instance = True

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        include_relationships = True
        load_instance = True

class DetalleProductosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DetalleProductos
        include_relationships = True
        load_instance = True

class ProductosSchema(SQLAlchemyAutoSchema):
    categoria = fields.Nested(CategoriaSchema)  
    detalle_productos = fields.Nested(DetalleProductosSchema)  
    class Meta:
        model = Productos
        include_relationships = True
        load_instance = True

class InventarioSchema(SQLAlchemyAutoSchema):
    productos = fields.Nested(ProductosSchema)  
    class Meta:
        model = Inventario
        include_relationships = True
        load_instance = True

class DetalleFacturaSchema(SQLAlchemyAutoSchema):
    productos = fields.Nested(ProductosSchema)  
    class Meta:
        model = DetalleFactura
        include_relationships = True
        load_instance = True

class FacturaSchema(SQLAlchemyAutoSchema):
    usuario = fields.Nested(UsuariosSchema)
    detalle_factura = fields.Nested(DetalleFacturaSchema, many=True) 
    class Meta:
        model = Factura
        include_relationships = True
        load_instance = True

class MovimientosSchema(SQLAlchemyAutoSchema):
    factura = fields.Nested(FacturaSchema) 
    inventario = fields.Nested(InventarioSchema)
    class Meta:
        model = Movimientos
        include_relationships = True
        load_instance = True

class AlertaSchema(SQLAlchemyAutoSchema):
    inventario = fields.Nested(InventarioSchema)
    class Meta:
        model = Alerta
        include_relationships = True
<<<<<<< HEAD
<<<<<<< HEAD
        load_instance = True
=======
=======
>>>>>>> 7e7301d4683567745a9015d3cc9b53150fb3f653
        load_instance = True
=======
#Tablas de la base de datos y serealización -> Nelson
>>>>>>> 5f37b97a19a2008d137279961b76fc0fd7f1a86b
<<<<<<< HEAD
>>>>>>> 1eec5f1ca3b1ae543c77fc627043c268114a0236
=======
>>>>>>> 7e7301d4683567745a9015d3cc9b53150fb3f653
