from flask import Flask, request
from flask_restful import Api, Resource
from models import db, DetalleFactura

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/inventario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

class VistaDetalleFactura(Resource):
    def get(self): 
        return [detalle.json() for detalle in DetalleFactura.query.all()]

    def post(self):
        nuevo_detalle = DetalleFactura(
            cantidad=request.json['cantidad'],
            producto_id=request.json['producto_id'], 
            detalle_productos_id=request.json['detalle_productos_id']
        )
        db.session.add(nuevo_detalle)
        db.session.commit()
        return nuevo_detalle.json(), 201 

    def put(self, detalle_id): 
        detalle = DetalleFactura.query.get(detalle_id)
        if detalle:
            detalle.producto_id = request.json.get('producto_id', detalle.producto_id)
            detalle.cantidad = request.json.get('cantidad', detalle.cantidad)
            detalle.detalle_productos_id = request.json.get('detalle_productos_id', detalle.detalle_productos_id)
            db.session.commit()
            return detalle.json()
        return {'message': 'Detalle de factura no encontrado'}, 404

    def delete(self, detalle_id): 
        detalle = DetalleFactura.query.get(detalle_id)
        if detalle:
            db.session.delete(detalle)
            db.session.commit()
            return {'message': 'Detalle de factura eliminado'}
        return {'message': 'Detalle de factura no encontrado'}, 404

api.add_resource(VistaDetalleFactura, '/detalle_factura', '/detalle_factura/<int:detalle_id>')

if __name__ == '__main__':
    app.run(debug=True)