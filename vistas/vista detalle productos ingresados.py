from flask import Flask, request
from flask_restful import Api, Resource
from models import db, DetalleProductosIngresados

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/inventario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

class VistaDetalleProductosIngresados(Resource):
    def get(self): 
        return [detalle.json() for detalle in DetalleProductosIngresados.query.all()]

    def post(self): 
        nuevo_detalle = DetalleProductosIngresados(
            fecha_entrada=request.json['fecha_entrada'],
            fecha_vence=request.json['fecha_vence'],
            cantidad=request.json['cantidad'],
            precio_entrada=request.json['precio_entrada'],
            precio_salida=request.json['precio_salida']
        )
        db.session.add(nuevo_detalle)
        db.session.commit()
        return nuevo_detalle.json(), 201  

    def put(self, detalle_id): 
        detalle = DetalleProductosIngresados.query.get(detalle_id)
        if detalle:
            detalle.fecha_entrada = request.json.get('fecha_entrada', detalle.fecha_entrada)
            detalle.fecha_vence = request.json.get('fecha_vence', detalle.fecha_vence)
            detalle.cantidad = request.json.get('cantidad', detalle.cantidad)
            detalle.precio_entrada = request.json.get('precio_entrada', detalle.precio_entrada)
            detalle.precio_salida = request.json.get('precio_salida', detalle.precio_salida)
            db.session.commit()
            return detalle.json()
        return {'message': 'Detalle de productos ingresados no encontrado'}, 404

    def delete(self, detalle_id):
        detalle = DetalleProductosIngresados.query.get(detalle_id)
        if detalle:
            db.session.delete(detalle)
            db.session.commit()
            return {'message': 'Detalle de productos ingresados eliminado'}
        return {'message': 'Detalle de productos ingresados no encontrado'}, 404

api.add_resource(VistaDetalleProductosIngresados, '/detalle_productos_ingresados', '/detalle_productos_ingresados/<int:detalle_id>')

if __name__ == '__main__':
    app.run(debug=True)