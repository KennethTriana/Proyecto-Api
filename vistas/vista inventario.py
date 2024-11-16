from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Inventario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/inventario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

class VistaInventario(Resource):
    def get(self):  
        return [item.json() for item in Inventario.query.all()]

    def post(self):  
        nuevo_item = Inventario(
            stock=request.json['stock'],
            categoria_id=request.json['categoria_id'],
            productos_id=request.json['productos_id'],
            productos_ingresados_id=request.json['productos_ingresados_id']
        )
        db.session.add(nuevo_item)
        db.session.commit()
        return nuevo_item.json(), 201  

    def put(self, inventario_id):
        item = Inventario.query.get(inventario_id)
        if item:
            item.stock = request.json.get('stock', item.stock)
            item.productos_id = request.json.get('productos_id', item.productos_id)
            item.productos_ingresados_id = request.json.get('productos_ingresados_id', item.productos_ingresados_id)
            item.categoria_id = request.json.get('categoria_id', item.categoria_id)
            db.session.commit()
            return item.json()
        return {'message': 'Registro de inventario no encontrado'}, 404

    def delete(self, inventario_id):  
        item = Inventario.query.get(inventario_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return {'message': 'Registro de inventario eliminado'}
        return {'message': 'Registro de inventario no encontrado'}, 404

api.add_resource(VistaInventario, '/inventario', '/inventario/<int:inventario_id>')

if __name__ == '__main__':
    app.run(debug=True)