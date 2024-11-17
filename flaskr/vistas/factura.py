from flask import jsonify, app
from flask_restful import Api, Resource, request
from flaskr.modelos.modelos import db, Factura, FacturaSchema

factura_schema = FacturaSchema()

class VistaFactura(Resource):
    def get(self): 
        return [factura_schema.dump(Factura) for Factura in Factura.query.all()]

    def post(self): 
        nueva_factura = Factura(
            fecha=request.json['fecha'],
            monto_total=request.json['monto_total'],
            precio_total=request.json['precio_total'],
            usuario_id=request.json['usuario_id'],
            detalle_factura_id=request.json['detalle_factura_id']
        )
        db.session.add(nueva_factura)
        db.session.commit()
        factura_actualizada = factura_schema.dump(nueva_factura)
        return factura_actualizada, 404

    def put(self, id): 
        factura = Factura.query.get(id)
        if factura:
            factura.fecha = request.json.get('fecha', factura.fecha)
            factura.monto_total = request.json.get('monto_total', factura.monto_total)
            factura.precio_total = request.json.get('precio_total', factura.precio_total)
            factura.usuarios_id = request.json.get('usuarios_id', factura.usuarios_id)
            factura.detalle_factura_id = request.json.get('detalle_factura_id', factura.detalle_factura_id)
            db.session.commit()
            factura_actualizada = factura_schema.dump(factura)
        return factura_actualizada, 404

    def delete(self, id): 
        factura = Factura.query.get(id)
        if factura:
            db.session.delete(factura)
            db.session.commit()
            return {'message': 'Factura eliminada'}
        return {'message': 'Factura no encontrada'}, 404