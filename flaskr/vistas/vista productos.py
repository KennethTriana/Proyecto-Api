#Nelson
from flask import jsonify, app
from flask_restful import Api, Resource, request
from flaskr.modelos.modelos import db, Productos, ProductosSchema

productos_schema = ProductosSchema()

class VistaProductos(Resource):
    def get(self):  
        return [productos_schema.dump(Productos) for Productos in Productos.query.all()]

    def post(self): 
        nuevo_producto = Productos(
            nombre=request.json['nombre'],
            fecha_entrada=request.json['fecha_entrada'],
            fecha_vence=request.json['fecha_vence'],
            estado=request.json['estado'],
            usuarios_id=request.json['usuarios_id'], 
            categoria_id=request.json['categoria_id'],
            detalle_productos_id=request.json['detalle_productos_id']
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        productos_actualizados = productos_schema.dump(nuevo_producto)
        return productos_actualizados, 404

    def put(self, id): 
        productos = Productos.query.get(id)
        if productos:
            productos.nombre = request.json.get('nombre', productos.nombre)
            productos.fecha_entrada = request.json.get('fecha_entrada', productos.fecha_entrada)
            productos.fecha_vence = request.json.get('fecha_vence', productos.fecha_vence)
            productos.estado = request.json.get('estado', productos.estado)
            productos.usuarios_id = request.json.get('usuarios_id', productos.usuarios_id)
            productos.categoria_id = request.json.get('categoria_id', productos.categoria_id)
            productos.detalle_productos_id = request.json.get('detalle_productos_id', productos.detalle_productos_id)
            db.session.commit()
            productos_actualizados = productos_schema.dump(productos)
        return productos_actualizados, 404

    def delete(self, id): 
        productos = Productos.query.get(id)
        if productos:
            db.session.delete(productos)
            db.session.commit()
            return {'message': 'Producto ingresado eliminado'}
        return {'message': 'Producto ingresado no encontrado'}, 404