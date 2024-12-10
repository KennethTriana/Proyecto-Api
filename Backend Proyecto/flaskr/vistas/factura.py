from flask import jsonify, request
from flask_restful import Resource
from flaskr.modelos.modelos import db, Factura, FacturaSchema

factura_schema = FacturaSchema()

class VistaFactura(Resource):
    def get(self):
        return [factura_schema.dump(factura) for factura in Factura.query.all()]

    def post(self):
        nueva_factura = Factura(
            fecha=request.json['fecha'],
            monto_total=request.json['monto_total'],
            cantidad=request.json['cantidad'],
            precio_unitario=request.json['precio_unitario'],
            usuario_id=request.json['usuario_id'],
            productos_id=request.json['productos_id']
        )
        db.session.add(nueva_factura)
        db.session.commit()
        factura_actualizada = factura_schema.dump(nueva_factura)
        return factura_actualizada, 201

    def put(self, id):
        factura = Factura.query.get(id)
        if factura:
            factura.fecha = request.json.get('fecha', factura.fecha)
            factura.monto_total = request.json.get('monto_total', factura.monto_total)
            factura.cantidad = request.json.get('cantidad', factura.cantidad)
            factura.precio_unitario = request.json.get('precio_unitario', factura.precio_unitario)
            factura.usuario_id = request.json.get('usuario_id', factura.usuario_id)
            factura.productos_id = request.json.get('productos_id', factura.productos_id)
            db.session.commit()
            factura_actualizada = factura_schema.dump(factura)
        return factura_actualizada, 200
        return {'message': 'Factura no encontrada'}, 404

    def delete(self, id):
        factura = Factura.query.get(id)
        if factura:
            db.session.delete(factura)
            db.session.commit()
            return {'message': 'Factura eliminada'}, 200
        return {'message': 'Factura no encontrada'}, 404