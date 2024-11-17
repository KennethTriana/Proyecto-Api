from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Cargo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/inventario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

# Vistas para Cargo
class VistaCargo(Resource):
    def get(self):  
        return [cargo.json() for cargo in Cargo.query.all()]

    def post(self): 
        nuevo_cargo = Cargo(
            nombre=request.json['nombre'],
            descripcion=request.json['descripcion']
        )
        db.session.add(nuevo_cargo)
        db.session.commit()
        return nuevo_cargo.json(), 201  

    def put(self, cargo_id):  
        cargo = Cargo.query.get(cargo_id)
        if cargo:
            cargo.nombre = request.json.get('nombre', cargo.nombre)
            cargo.descripcion = request.json.get('descripcion', cargo.descripcion)
            db.session.commit()
            return cargo.json()
        return {'message': 'Cargo no encontrado'}, 404

    def delete(self, cargo_id): 
        cargo = Cargo.query.get(cargo_id)
        if cargo:
            db.session.delete(cargo)
            db.session.commit()
            return {'message': 'Cargo eliminado'}
        return {'message': 'Cargo no encontrado'}, 404

api.add_resource(VistaCargo, '/cargo', '/cargo/<int:cargo_id>')

if __name__ == '__main__':
    app.run(debug=True)