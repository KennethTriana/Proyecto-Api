from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Alerta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/inventario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

class VistaAlerta(Resource):
    def get(self):
        return [alerta.json() for alerta in Alerta.query.all()]

    def post(self): 
        nueva_alerta = Alerta(
            nombre=request.json['nombre'],
            stock_minimo=request.json['stock_minimo'],
            stock=request.json['stock'],
            productos_id=request.json['productos_id'] 
        )
        db.session.add(nueva_alerta)
        db.session.commit()
        return nueva_alerta.json(), 201  

    def put(self, alerta_id): 
        alerta = Alerta.query.get(alerta_id)
        if alerta:
            alerta.nombre = request.json.get('nombre', alerta.nombre)
            alerta.stock_minimo = request.json.get('stock_minimo', alerta.stock_minimo)
            alerta.stock = request.json.get('stock', alerta.stock)
            alerta.productos_id = request.json.get('productos_id', alerta.productos_id)
            db.session.commit()
            return alerta.json()
        return {'message': 'Alerta no encontrada'}, 404

    def delete(self, alerta_id): 
        alerta = Alerta.query.get(alerta_id)
        if alerta:
            db.session.delete(alerta)
            db.session.commit()
            return {'message': 'Alerta eliminada'}
        return {'message': 'Alerta no encontrada'}, 404

api.add_resource(VistaAlerta, '/alerta', '/alerta/<int:alerta_id>')

if __name__ == '__main__':
    app.run(debug=True)