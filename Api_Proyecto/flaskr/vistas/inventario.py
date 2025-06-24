from flask import jsonify, request
from flask_restful import Api, Resource
from flaskr.modelos.modelos import db, Inventario, InventarioSchema, Productos
from marshmallow import ValidationError

inventario_schema = InventarioSchema()

class VistaInventario(Resource):
    def get(self):
        try:
            inventarios = Inventario.query.all()
            return [inventario_schema.dump(inventario) for inventario in inventarios]
        except Exception as e:
            return {'message': f'Error al obtener inventarios: {str(e)}'}, 500

    def post(self):
        try:
            data = request.json
            nuevo_inventario = Inventario(
                producto_id=data['producto_id'],
                fecha_entrada=data['fecha_entrada'],
                fecha_vence=data['fecha_vence'],
                estado=data['estado'],
            )
            db.session.add(nuevo_inventario)
            db.session.commit()
            return inventario_schema.dump(nuevo_inventario), 201  
        except ValidationError as err:
            return err.messages, 400  
        except Exception as e:
            return {'message': f'Error al crear inventario: {str(e)}'}, 500

    def put(self, id):
        try:
            inventario = Inventario.query.get(id)
            if inventario:
                data = request.json
                inventario.fecha_entrada = data.get('fecha_entrada', inventario.fecha_entrada)
                inventario.fecha_vence = data.get('fecha_vence', inventario.fecha_vence)
                inventario.estado = data.get('estado', inventario.estado)
                db.session.commit()
                return inventario_schema.dump(inventario), 200
            return {'message': 'Inventario no encontrado'}, 404
        except Exception as e:
            return {'message': f'Error al actualizar inventario: {str(e)}'}, 500

    def delete(self, id):
        try:
            inventario = Inventario.query.get(id)
            if inventario:
                db.session.delete(inventario)
                db.session.commit()
                return {'message': 'Inventario eliminado'}, 200
            return {'message': 'Inventario no encontrado'}, 404
        except Exception as e:
            return {'message': f'Error al eliminar inventario: {str(e)}'}, 500

class VistaInventarioProducto(Resource):
    def get(self, producto_id):
        try:
            producto = Productos.query.get(producto_id)
            if producto:
                inventarios = producto.inventario
                return [inventario_schema.dump(inv) for inv in inventarios]
            return {'message': 'Producto no encontrado'}, 404
        except Exception as e:
            return {'message': f'Error al obtener inventarios del producto: {str(e)}'}, 500
