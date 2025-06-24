from flask import jsonify, app
from flask_restful import Api, Resource, request
from flaskr.modelos.modelos import db, Cargo, CargoSchema

cargo_schema = CargoSchema()

class VistaCargo(Resource):
    def get(self):  
        return [cargo_schema.dump(Cargo) for Cargo in Cargo.query.all()]

    def post(self): 
        nuevo_cargo = Cargo(
            nombre=request.json['nombre'],
            descripcion=request.json['descripcion']
        )
        db.session.add(nuevo_cargo)
        db.session.commit()
        cargo_actualizado = cargo_schema.dump(nuevo_cargo)
        return cargo_actualizado, 404  

    def put(self, id):  
        cargo = Cargo.query.get(id)
        if cargo:
            cargo.nombre = request.json.get('nombre', cargo.nombre)
            cargo.descripcion = request.json.get('descripcion', cargo.descripcion)
            db.session.commit()
            cargo_actualizado = cargo_schema.dump(cargo)
        return cargo_actualizado, 404

    def delete(self, id): 
        cargo = Cargo.query.get(id)
        if cargo:
            db.session.delete(cargo)
            db.session.commit()
            return {'message': 'Cargo eliminado'}
        return {'message': 'Cargo no encontrado'}, 404