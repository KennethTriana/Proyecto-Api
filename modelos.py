from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy


from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Cargo(db.Model):
    _tablename_ = 'cargo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    descripcion = db.Column(db.String(256))
    
    #usuarios = db.relationship('Usuarios', back_populates="cargo")
    
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
    
    #cargo = db.relationship('Cargo', back_populates="usuarios")
    
    #productos_ingresados = db.relationship('ProductosIngresados', back_populates="usuarios")
    #factura = db.relationship('Factura', back_populates="usuarios")
    
class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    descripcion = db.Column(db.String(256))
    
    #productos = db.relationship('Productos', back_populates="categoria")
    #productos_ingresados = db.relationship('ProductosIngresados', back_populates="categoria")
    #inventario = db.relationship('Inventario', back_populates="categoria")
    
class DetalleProductos(db.Model):
    __tablename__ = 'detalle_productos'
    id = db.Column(db.Integer, primary_key=True)
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    cantidad = db.Column(db.Integer)
    precio_entrada = db.Column(db.Integer)
    precio_salida = db.Column(db.Integer)
    
    #productos = db.relationship('Productos', back_populates="detalle_productos")
    #detallefactura = db.relationship('DetalleFactura', back_populates="detalle_productos")
    
class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    estado = db.Column(db.String(256))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    detalle_productos_id = db.Column(db.Integer, db.ForeignKey('detalle_productos.id'))
    
    #categoria = db.relationship('Categoria', back_populates="productos")
    #detalle_productos = db.relationship('DetalleProductos', back_populates="productos") 
    #inventario = db.relationship('Inventario', back_populates="productos")
    
    #detallefactura = db.relationship('DetalleFactura', back_populates="productos")
    #movimientos = db.relationship('Movimientos', back_populates="productos")
    #alerta = db.relationship('Alerta', back_populates="productos")
    
class DetalleProductosIngresados(db.Model):
    __tablename__ = 'detalle_productos_ingresados'
    id = db.Column(db.Integer, primary_key=True)
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    cantidad = db.Column(db.Integer)
    precio_entrada = db.Column(db.Integer)
    precio_salida = db.Column(db.Integer)
    
    #productos_ingresados = db.relationship('ProductosIngresados', back_populates="detalle_productos_ingresados")  #
    
class ProductosIngresados(db.Model):
    __tablename__ = 'productos_ingresados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    fecha_entrada = db.Column(db.DateTime)
    fecha_vence = db.Column(db.DateTime)
    estado = db.Column(db.String(256))
    usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    detalle_productos_id = db.Column(db.Integer, db.ForeignKey('detalle_productos_ingresados.id'))
    
    #usuarios = db.relationship('Usuarios', back_populates="productos_ingresados")
    #categoria = db.relationship('Categoria', back_populates="productos_ingresados")
    #detalle_productos_ingresados = db.relationship('Detalle_Productos_Ingresados', back_populates="productos_ingresados")
    #inventario = db.relationship('Inventario', back_populates="productos_ingresados")

class Inventario(db.Model):
    __tablename__ = 'inventario'
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.Integer)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    productos_ingresados_id = db.Column(db.Integer, db.ForeignKey('productos_ingresados.id'))
    
    #categoria = db.relationship('Categoria', back_populates="inventario")
    #productos = db.relationship('Productos', back_populates="inventario")
    #roductos_ingresados = db.relationship('ProductosIngresados', back_populates="inventario")
    
class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    detalle_productos_id = db.Column(db.Integer, db.ForeignKey('detalle_productos.id'))  
    
    #productos = db.relationship('Productos', back_populates="detalle_factura")
    #detalle_productos = db.relationship('DetalleProductos', back_populates="detalle_factura")
    
class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    monto_total = db.Column(db.Integer)
    precio_total = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    #usuarios = db.relationship('Usuarios', back_populates="factura")
    
    #movimientos = db.relationship('Movimientos', back_populates="factura")

class Movimientos(db.Model):
    __tablename__ = 'movimientos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    tipo = db.Column(db.String(256))
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'))
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    
    #factura = db.relationship('Factura', back_populates="movimientos")
    #productos = db.relationship('Productos', back_populates="movimientos")
    
class Alerta(db.Model):
    __tablename__ = 'alerta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256))
    stock_minimo = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    
    #productos = db.relationship('Productos', back_populates="alerta")
    


class EnumDiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None 
        return{"llave": value.name, "valor": value.value}

class CargoSchema(SQLAlchemyAutoSchema):  
    class Meta:  
        model = Cargo  
        include_relationships = True  
        load_instance = True  


class UsuariosSchema(SQLAlchemyAutoSchema):  
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
    esatdo = EnumDiccionario()
    class Meta:  
        model = Productos  
        include_relationships = True  
        load_instance = True  


class Detalle_Productos_IngresadosSchema(SQLAlchemyAutoSchema):  
    class Meta:  
        model = DetalleProductosIngresados  
        include_relationships = True  
        load_instance = True  


class Productos_IngresadosSchema(SQLAlchemyAutoSchema):  
    class Meta:  
        model = ProductosIngresados  
        include_relationships = True  
        load_instance = True  


class InventarioSchema(SQLAlchemyAutoSchema):  
    class Meta:  
        model = Inventario  
        include_relationships = True  
        load_instance = True  


class Detalle_FacturaSchema(SQLAlchemyAutoSchema):  
    class Meta:  
        model = DetalleFactura
        include_relationships = True  
        load_instance = True  


class FacturaSchema(SQLAlchemyAutoSchema):  
    class Meta:  
        model = Factura 
        include_relationships = True  
        load_instance = True  


class MovimientosSchema(SQLAlchemyAutoSchema):  
    class Meta:  
        model = Movimientos
        include_relationships = True  
        load_instance = True  


class AlertaSchema(SQLAlchemyAutoSchema):  
    class Meta:  
        model = Alerta
        include_relationships = True  
        load_instance = True