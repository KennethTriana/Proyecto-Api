from flask import jsonify, app
from flask_restful import Api, Resource, request
from flaskr.modelos.modelos import db, Categoria, CategoriaSchema

categoria_schema = CategoriaSchema()

class VistaCategoria(Resource):
    def get(self):  
        return [categoria_schema.dump(Categoria) for Categoria in Categoria.query.all()]

    def post(self): 
        nueva_categoria = Categoria(
            nombre=request.json['nombre'],
            descripcion=request.json['descripcion']
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        categoria_actualizada = categoria_schema.dump(nueva_categoria)
        return categoria_actualizada, 404

    def put(self, id): 
        categoria = Categoria.query.get(id)
        if categoria:
            categoria.nombre = request.json.get('nombre', categoria.nombre)
            categoria.descripcion = request.json.get('descripcion', categoria.descripcion)
            db.session.commit()
            categoria_actualizada = categoria_schema.dump(categoria)
        return categoria_actualizada, 404

    def delete(self, id): 
        categoria = Categoria.query.get(id)
        if categoria:
            db.session.delete(categoria)
            db.session.commit()
            return {'message': 'Categoría eliminada'}
        return {'message': 'Categoría no encontrada'}, 404