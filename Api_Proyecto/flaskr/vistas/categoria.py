from flask import jsonify, request
from flask_restful import Api, Resource
from flaskr.modelos.modelos import db, Categoria, CategoriaSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

categoria_schema = CategoriaSchema()

class VistaCategoria(Resource):
    def get(self):
        try:
            categorias = Categoria.query.all()  
            return categoria_schema.dump(categorias, many=True), 200 
        except Exception as e:
            return {'message': f'Error al obtener las categorías: {str(e)}'}, 500

    def post(self):
        try:
            data = request.json

            if 'nombre' not in data:
                return {'message': 'El campo "nombre" es obligatorio.'}, 400

            categoria_existente = Categoria.query.filter_by(nombre=data['nombre']).first()
            if categoria_existente:
                return {'message': 'Ya existe otra categoría con el nombre.'}, 400

            nueva_categoria = Categoria(nombre=data['nombre'])
            db.session.add(nueva_categoria)
            db.session.commit()
            
            return categoria_schema.dump(nueva_categoria), 201 
        except ValidationError as err:
            return {'message': f'Error en la validación: {err.messages}'}, 400
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Ya existe otra categoría con el nombre.'}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error inesperado: {str(e)}'}, 500

    def put(self, id):
        try:
            categoria = Categoria.query.get(id)
            
            if categoria:
                data = request.json

                if 'nombre' not in data:
                    return {'message': 'El campo "nombre" es obligatorio.'}, 400

                categoria_existente = Categoria.query.filter_by(nombre=data['nombre']).filter(Categoria.id != id).first()
                if categoria_existente:
                    return {'message': 'Ya existe otra categoría con el nombre.'}, 400

                categoria.nombre = data['nombre']
                db.session.commit()

                return categoria_schema.dump(categoria), 200
            else:
                return {'message': 'Categoría no encontrada'}, 404

        except ValidationError as err:
            return {'message': f'Error en los datos: {err.messages}'}, 400
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Ya existe otra categoría con el nombre.'}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error inesperado: {str(e)}'}, 500

    def delete(self, id):
        try:
            categoria = Categoria.query.get(id)
            
            if categoria:
                db.session.delete(categoria)
                db.session.commit()
                return {'message': 'Categoría eliminada exitosamente'}, 200
            else:
                return {'message': 'Categoría no encontrada'}, 404

        except Exception as e:
            return {'message': f'Error inesperado: {str(e)}'}, 500