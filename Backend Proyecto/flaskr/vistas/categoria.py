from flask import jsonify, request
from flask_restful import Api, Resource
from flaskr.modelos.modelos import db, Categoria, CategoriaSchema
from marshmallow import ValidationError

categoria_schema = CategoriaSchema()

class VistaCategoria(Resource):
    def get(self):
        return [categoria_schema.dump(categoria) for categoria in Categoria.query.all()]

    def post(self):
        try:
            data = categoria_schema.load(request.json)
            nueva_categoria = Categoria(**data)
            db.session.add(nueva_categoria)
            db.session.commit()
            return categoria_schema.dump(nueva_categoria), 201  # Código de estado correcto para creación
        except ValidationError as err:
            return err.messages, 400

    def put(self, id):
        categoria = Categoria.query.get(id)
        if categoria:
            try:
                data = categoria_schema.load(request.json, partial=True)
                for key, value in data.items():
                    setattr(categoria, key, value)
                db.session.commit()
                return categoria_schema.dump(categoria), 200
            except ValidationError as err:
                return err.messages, 400
        return {'message': 'Categoría no encontrada'}, 404

    def delete(self, id):
        categoria = Categoria.query.get(id)
        if categoria:
            db.session.delete(categoria)
            db.session.commit()
            return {'message': 'Categoría eliminada'}, 200
        return {'message': 'Categoría no encontrada'}, 404