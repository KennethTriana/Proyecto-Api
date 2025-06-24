from flask import Flask, request
from flask_restful import Api, Resource
from models import db, DetalleProducto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/inventario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

class VistaDetalleProductos(Resource):
    def get(self): 
        return [detalle_productos.json() for detalle_productos in DetalleProductos.query.all()]

    def post(self): 
        nuevo_detalle = DetalleProductos(
            fecha_entrada=request.json['fecha_entrada'],  
            fecha_vence=request.json['fecha_vence'],  
            cantidad=request.json['cantidad'],
            precio_entrada=request.json['precio_entrada'],
            precio_salida=request.json['precio_salida']
        )
        db.session.add(nuevo_detalle)
        db.session.commit()
        return nuevo_detalle.json(), 201  

    def put(self, detalle_id): 
        detalle_productos = DetalleProducto.query.get(detalle_id)
        if detalle_productos:
            detalle_productos.fecha_entrada = request.json.get('fecha_entrada', detalle_productos.fecha_entrada)
            detalle_productos.fecha_vence = request.json.get('fecha_vence', detalle_productos.fecha_vence)
            detalle_productos.cantidad = request.json.get('cantidad', detalle_productos.cantidad)
            detalle_productos.precio_entrada = request.json.get('precio_entrada', detalle_productos.precio_entrada)
            detalle_productos.precio_salida = request.json.get('precio_salida', detalle_productos.precio_salida)
            db.session.commit()
            return detalle_productos.json()
        return {'message': 'Detalle de producto no encontrado'}, 404

    def delete(self, detalle_id):
        detalle_productos = DetalleProductos.query.get(detalle_id)
        if detalle_productos:
            db.session.delete(detalle_productos)
            db.session.commit()
            return {'message': 'Detalle de producto eliminado'}
        return {'message': 'Detalle de producto no encontrado'}, 404

api.add_resource(VistaDetalleProductos, '/detalle_productos', '/detalle_productos/<int:detalle_id>')

if __name__ == '__main__':
    app.run(debug=True)