from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Factura

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/inventario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

class VistaFactura(Resource):
    def get(self): 
        return [factura.json() for factura in Factura.query.all()]

    def post(self): 
        nueva_factura = Factura(
            fecha=request.json['fecha'],
            monto_total=request.json['monto_total'],
            precio_total=request.json['precio_total'],
            usuario_id=request.json['usuario_id']
        )
        db.session.add(nueva_factura)
        db.session.commit()
        return nueva_factura.json(), 201 

    def put(self, factura_id): 
        factura = Factura.query.get(factura_id)
        if factura:
            factura.fecha = request.json.get('fecha', factura.fecha)
            factura.monto_total = request.json.get('monto_total', factura.monto_total)
            factura.precio_total = request.json.get('precio_total', factura.precio_total)
            factura.usuarios_id = request.json.get('usuarios_id', factura.usuarios_id)
            db.session.commit()
            return factura.json()
        return {'message': 'Factura no encontrada'}, 404

    def delete(self, factura_id): 
        factura = Factura.query.get(factura_id)
        if factura:
            db.session.delete(factura)
            db.session.commit()
            return {'message': 'Factura eliminada'}
        return {'message': 'Factura no encontrada'}, 404

api.add_resource(VistaFactura, '/factura', '/factura/<int:factura_id>')

if __name__ == '__main__':
    app.run(debug=True)