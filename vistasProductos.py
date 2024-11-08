from flask_restful import Resource, request
from ..modelos import db, Productos, ProductosSchema
from flask import jsonify, app


Productos_schema = ProductosSchema()

class VistaProductos(Resource):
    def get(self):
        return Productos_schema.dump(Productos.query.all(), many=True)
    
    def post(self):
        nuevo_producto = Productos(
            nombre=request.json['nombre'],
            fecha_entrada=request.json['fecha_entrada'],
            fecha_vence=request.json['fecha_vence'],
            estado=request.json['estado']
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        Productos_actualizados = Productos_schema.dump(nuevo_producto)
        return Productos_actualizados, 402
        

    def delete(self, id):
        producto = Productos.query.get(id) 
        
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({'Mensaje': 'Producto eliminado exitosamente'}), 200
        else:
            return jsonify({'Mensaje': 'Producto no encontrado'}), 404
        
        
    def put(self, id):
        producto = Productos.query.get(id)
        
        if not producto:
            return jsonify({'Mensaje': 'Producto no encontrado'}), 404

        data = request.get_json()  
        
        producto.nombre = data.get('nombre', producto.nombre)
        producto.descripcion = data.get('descripcion', producto.descripcion)
        producto.precio = data.get('precio', producto.precio)
        
        db.session.commit()
        

        return Productos_schema.dump(producto), 200
    
    

    

