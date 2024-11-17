from flask import jsonify, app
from flask_restful import Api, Resource, request
from flaskr.modelos.modelos import db, DetalleProductos, DetalleProductosSchema

detalle_productos_schema = DetalleProductosSchema()

class VistaDetalleProductos(Resource):
    def get(self): 
        return [detalle_productos_schema.dump(DetalleProductos) for DetalleProductos in DetalleProductos.query.all()]

    def post(self): 
        nuevo_detalle = DetalleProductos(
            cantidad=request.json['cantidad'],
            precio_entrada=request.json['precio_entrada'],
            precio_salida=request.json['precio_salida']
        )
        db.session.add(nuevo_detalle)
        db.session.commit()
        detalle_productos_actualizado = detalle_productos_schema.dump(nuevo_detalle)
        return detalle_productos_actualizado, 404  

    def put(self, id): 
        detalle = DetalleProductos.query.get(id)
        if detalle:
            detalle.cantidad = request.json.get('cantidad', detalle.cantidad)
            detalle.precio_entrada = request.json.get('precio_entrada', detalle.precio_entrada)
            detalle.precio_salida = request.json.get('precio_salida', detalle.precio_salida)
            db.session.commit()
            detalle_productos_actualizado = detalle_productos_schema.dump(detalle)
        return detalle_productos_actualizado, 404

    def delete(self, id):
        detalle_productos = DetalleProductos.query.get(id)
        if detalle_productos:
            db.session.delete(detalle_productos)
            db.session.commit()
            return {'message': 'Detalle de producto eliminado'}
        return {'message': 'Detalle de producto no encontrado'}, 404