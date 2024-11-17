from flask import jsonify, app
from flask_restful import Api, Resource, request
from flaskr.modelos.modelos import db, DetalleFactura, DetalleFacturaSchema

detalle_factura_schema = DetalleFacturaSchema()

class VistaDetalleFactura(Resource):
    def get(self): 
        return [detalle_factura_schema.dump(DetalleFactura) for DetalleFactura in DetalleFactura.query.all()]

    def post(self):
        nuevo_detalle_factura = DetalleFactura(
            cantidad=request.json['cantidad'],
            inventario_id=request.json['inventario_id']
        )
        db.session.add(nuevo_detalle)
        db.session.commit()
        detalle_factura_actualizado = detalle_factura_schema.dump(nuevo_detalle_factura)
        return detalle_factura_actualizado, 404 

    def put(self, id): 
        detalle = DetalleFactura.query.get(id)
        if detalle:
            detalle.inventario_id = request.json.get('inventario_id', detalle.inventario_id)
            detalle.cantidad = request.json.get('cantidad', detalle.cantidad)
            db.session.commit()
            detalle_factura_actualizado = detalle_factura_schema.dump(detalle)
        return detalle_factura_actualizado, 404

    def delete(self, id): 
        detalle_factura = DetalleFactura.query.get(id)
        if detalle_factura:
            db.session.delete(detalle_factura)
            db.session.commit()
            return {'message': 'Detalle de factura eliminado'}
        return {'message': 'Detalle de factura no encontrado'}, 404