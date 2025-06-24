from flask import jsonify, request
from flask_restful import Api, Resource
from flaskr.modelos.modelos import db, DetalleProductos, DetalleProductosSchema, Productos
from marshmallow import ValidationError

detalle_productos_schema = DetalleProductosSchema()

class VistaDetalleProductos(Resource):
    def get(self):
        try:
            detalles = DetalleProductos.query.all()
            return [detalle_productos_schema.dump(detalle) for detalle in detalles], 200
        except Exception as e:
            return {'message': f'Error al obtener los detalles de productos: {str(e)}'}, 500

    def post(self):
        try:
            data = request.json
            if not all(key in data for key in ('cantidad', 'precio_entrada', 'precio_salida', 'producto_id')):
                return {'message': 'Faltan datos requeridos.'}, 400
            
            producto = Productos.query.get(data['producto_id'])
            if not producto:
                return {'message': 'Producto no encontrado.'}, 404

            nuevo_detalle = DetalleProductos(
                cantidad=data['cantidad'],
                precio_entrada=data['precio_entrada'],
                precio_salida=data['precio_salida'],
                producto_id=data['producto_id']
            )
            db.session.add(nuevo_detalle)
            db.session.commit()
            return detalle_productos_schema.dump(nuevo_detalle), 201 
        except ValidationError as err:
            return err.messages, 400
        except Exception as e:
            return {'message': f'Error al crear detalle de producto: {str(e)}'}, 500

    def put(self, id):
        try:
            detalle = DetalleProductos.query.get(id)
            if detalle:
                data = request.json
                detalle.cantidad = data.get('cantidad', detalle.cantidad)
                detalle.precio_entrada = data.get('precio_entrada', detalle.precio_entrada)
                detalle.precio_salida = data.get('precio_salida', detalle.precio_salida)
                db.session.commit()
                return detalle_productos_schema.dump(detalle), 200
            return {'message': 'Detalle de producto no encontrado'}, 404
        except Exception as e:
            return {'message': f'Error al actualizar detalle de producto: {str(e)}'}, 500

    def delete(self, id):
        try:
            detalle_productos = DetalleProductos.query.get(id)
            if detalle_productos:
                db.session.delete(detalle_productos)
                db.session.commit()
                return '', 204  
            return {'message': 'Detalle de producto no encontrado'}, 404
        except Exception as e:
            return {'message': f'Error al eliminar detalle de producto: {str(e)}'}, 500
