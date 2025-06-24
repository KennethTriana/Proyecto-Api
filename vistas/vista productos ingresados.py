from flask import Flask, request
from flask_restful import Api, Resource
from models import db, ProductosIngresados

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/inventario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

class VistaProductosIngresados(Resource):
    def get(self):  
        return [producto.json() for producto in ProductosIngresados.query.all()]

    def post(self): 
        nuevo_producto_ingresado = ProductosIngresados(
            nombre=request.json['nombre'],
            fecha_entrada=request.json['fecha_entrada'],
            fecha_vence=request.json['fecha_vence'],
            estado=request.json['estado'],
            usuarios_id=request.json['usuarios_id'], 
            categoria_id=request.json['categoria_id'],
            detalle_productos_ingresados_id=request.json['detalle_productos_ingresados_id']
        )
        db.session.add(nuevo_producto_ingresado)
        db.session.commit()
        return nuevo_producto_ingresado.json(), 201 

    def put(self, producto_ingresado_id): 
        producto_ingresado = ProductosIngresados.query.get(producto_ingresado_id)
        if producto_ingresado:
            producto_ingresado.nombre = request.json.get('nombre', producto_ingresado.nombre)
            producto_ingresado.fecha_entrada = request.json.get('fecha_entrada', producto_ingresado.fecha_entrada)
            producto_ingresado.fecha_vence = request.json.get('fecha_vence', producto_ingresado.fecha_vence)
            producto_ingresado.estado = request.json.get('fecha_estado', producto_ingresado.estado)
            producto_ingresado.usuarios_id = request.json.get('usuarios_id', producto_ingresado.usuarios_id)
            producto_ingresado.categoria_id = request.json.get('categoria_id', producto_ingresado.categoria_id)
            producto_ingresado.detalle_productos_ingresados_id = request.json.get('detalle_productos_ingresados_id', producto_ingresado.detalle_productos_ingresados_id)
            db.session.commit()
            return producto_ingresado.json()
        return {'message': 'Producto ingresado no encontrado'}, 404

    def delete(self, producto_ingresado_id): 
        producto_ingresado = ProductosIngresados.query.get(producto_ingresado_id)
        if producto_ingresado:
            db.session.delete(producto_ingresado)
            db.session.commit()
            return {'message': 'Producto ingresado eliminado'}
        return {'message': 'Producto ingresado no encontrado'}, 404

api.add_resource(VistaProductosIngresados, '/productos_ingresados', '/productos_ingresados/<int:producto_ingresado_id>')

if __name__ == '__main__':
    app.run(debug=True)