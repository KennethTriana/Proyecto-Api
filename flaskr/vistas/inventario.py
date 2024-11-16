from flask import jsonify, app
from flask_restful import Api, Resource, request
from flaskr.modelos.modelos import db, Inventario, InventarioSchema

inventario_schema = InventarioSchema()

class VistaInventario(Resource):
    def get(self): 
        return [inventario_schema.dump(Productos) for Inventario in Inventario.query.all()]

    def post(self):  
        nuevo_producto = Productos(
            nombre=request.json['nombre'],
            fecha_entrada=request.json['fecha_entrada'],
            fecha_vence=request.json['fecha_vence'],
            estado=request.json['estado'],
            stock=request.json['stock']
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        inventario_actualizado = inventario_schema.dump(nuevo_producto)
        return inventario_actualizado, 404  

    def put(self, id):
        producto = Inventario.query.get(id)
        if producto:
            producto.nombre = request.json.get('nombre', producto.nombre)
            producto.fecha_entrada = request.json.get('fecha_entrada', producto.fecha_entrada)
            producto.fecha_vence = request.json.get('fecha_vence', producto.fecha_vence)
            producto.estado = request.json.get('estado', producto.estado)
            producto.stock = request.json.get('stock', producto.stock)
            db.session.commit()
            inventario_actualizado = inventario_schema.dump(producto)
        return inventario_actualizado, 404

    def delete(self, id): 
        inventario = Inventario.query.get(id)
        if inventario:
            db.session.delete(inventario)
            db.session.commit()
            return {'message': 'Producto eliminado'}
        return {'message': 'Producto no encontrado'}, 404