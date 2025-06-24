from flask import jsonify, request
from flask_restful import Api, Resource
from flaskr.modelos.modelos import db, Cargo, CargoSchema
from marshmallow import ValidationError

cargo_schema = CargoSchema()

class VistaCargo(Resource):
    def get(self):
        return [cargo_schema.dump(cargo) for cargo in Cargo.query.all()]

    def post(self):
        try:
            data = cargo_schema.load(request.json)
            nuevo_cargo = Cargo(**data)
            db.session.add(nuevo_cargo)
            db.session.commit()
            return cargo_schema.dump(nuevo_cargo), 201  # Código de estado correcto para creación
        except ValidationError as err:
            return err.messages, 400

    def put(self, id):
        cargo = Cargo.query.get(id)
        if cargo:
            try:
                data = cargo_schema.load(request.json, partial=True)
                for key, value in data.items():
                    setattr(cargo, key, value)
                db.session.commit()
                return cargo_schema.dump(cargo), 200
            except ValidationError as err:
                return err.messages, 400
        return {'message': 'Cargo no encontrado'}, 404

    def delete(self, id):
        cargo = Cargo.query.get(id)
        if cargo:
            db.session.delete(cargo)
            db.session.commit()
            return {'message': 'Cargo eliminado'}, 200
        return {'message': 'Cargo no encontrado'}, 404