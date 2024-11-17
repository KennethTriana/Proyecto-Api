from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Movimientos

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/inventario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

class VistaMovimientos(Resource):
    def get(self): 
        return [movimientos.json() for movimientos in Movimientos.query.all()]

    def post(self): 
        nuevo_movimiento = Movimientos(
            productos_id=request.json['productos_id'], 
            factura_id=request.json['factura_id'],  
            tipo=request.json['tipo'], 
            fecha=request.json['fecha']
        )
        db.session.add(nuevo_movimiento)
        db.session.commit()
        return nuevo_movimientos.json(), 201  

    def put(self, movimientos_id): 
        movimiento = Movimientos.query.get(movimientos_id)
        if movimiento:
            movimiento.productos_id = request.json.get('productos_id', movimiento.productos_id)
            movimiento.factura_id = request.json.get('factura_id', movimiento.factura_id)
            movimiento.tipo = request.json.get('tipo', movimiento.tipo)
            movimiento.fecha = request.json.get('fecha', movimiento.fecha)
            db.session.commit()
            return movimiento.json()
        return {'message': 'Movimiento no encontrado'}, 404

    def delete(self, movimientos_id): 
        movimiento = Movimientos.query.get(movimiento_id)
        if movimiento:
            db.session.delete(movimientos)
            db.session.commit()
            return {'message': 'Movimiento eliminado'}
        return {'message': 'Movimiento no encontrado'}, 404

api.add_resource(VistaMovimientos, '/movimientos', '/movimientos/<int:movimiento_id>')

if __name__ == '__main__':
    app.run(debug=True)