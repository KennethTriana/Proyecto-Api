from flask import jsonify, app
from flask_restful import Api, Resource, request
from flaskr.modelos.modelos import db, Movimientos, MovimientosSchema

movimientos_schema = MovimientosSchema()

class VistaMovimientos(Resource):
    def get(self): 
        return [movimientos_schema.dump(Movimientos) for Movimientos in Movimientos.query.all()]

    def post(self): 
        nuevo_movimiento = Movimientos(
            inventario_id=request.json['inventario_id'], 
            detalle_factura_id=request.json['detalle_factura_id'],  
            tipo=request.json['tipo'], 
            fecha=request.json['fecha']
        )
        db.session.add(nuevo_movimiento)
        db.session.commit()
        movimiento_actualizado = movimientos_schema.dump(nuevo_movimiento)
        return movimiento_actualizado, 404

    def put(self, id): 
        movimiento = Movimientos.query.get(id)
        if movimiento:
            movimiento.inventario_id = request.json.get('inventario_id', movimiento.inventario_id)
            movimiento.detalle_factura_id = request.json.get('detalle_factura_id', movimiento.detalle_factura_id)
            movimiento.tipo = request.json.get('tipo', movimiento.tipo)
            movimiento.fecha = request.json.get('fecha', movimiento.fecha)
            db.session.commit()
            movimiento_actualizado = movimientos_schema.dump(movimiento)
        return movimiento_actualizado, 404

    def delete(self, id): 
        movimientos = Movimientos.query.get(id)
        if movimientos:
            db.session.delete(movimientos)
            db.session.commit()
            return {'message': 'Movimiento eliminado'}
        return {'message': 'Movimiento no encontrado'}, 404