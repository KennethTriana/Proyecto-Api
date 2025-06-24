from flask import jsonify, request
from flask_restful import Api, Resource
from flaskr.modelos.modelos import db, Alerta, AlertaSchema

alerta_schema = AlertaSchema()

class VistaAlerta(Resource):
    
    def get(self):
        alertas = Alerta.query.all()
        return [alerta_schema.dump(alerta) for alerta in alertas], 200

    def post(self): 
        try:
            nueva_alerta = Alerta(
                nombre=request.json['nombre'],
                stock_minimo=request.json['stock_minimo'],
                stock=request.json['stock'],
                productos_id=request.json['productos_id']
            )

            db.session.add(nueva_alerta)
            db.session.commit()

            alerta_actualizada = alerta_schema.dump(nueva_alerta)
            return alerta_actualizada, 201
        except Exception as e:
            db.session.rollback() 
            return {'message': 'Error al crear la alerta', 'error': str(e)}, 500

    def put(self, id): 
        alerta = Alerta.query.get(id)

        if alerta:
            stock_antiguo = alerta.stock

            alerta.nombre = request.json.get('nombre', alerta.nombre)
            alerta.stock_minimo = request.json.get('stock_minimo', alerta.stock_minimo) 
            alerta.stock = request.json.get('stock', alerta.stock)
            alerta.productos_id = request.json.get('productos_id', alerta.productos_id)

            try:
                db.session.commit()

                if stock_antiguo <= 5 and alerta.stock > 5:
                    db.session.delete(alerta)
                    db.session.commit()

                alerta_actualizada = alerta_schema.dump(alerta)
                return alerta_actualizada, 200
            except Exception as e:
                db.session.rollback()
                return {'message': 'Error al actualizar la alerta', 'error': str(e)}, 500
        return {'message': 'Alerta no encontrada'}, 404

    def delete(self, id): 
        alerta = Alerta.query.get(id)

        if alerta:
            db.session.delete(alerta)
            db.session.commit()
            return {'message': 'Alerta eliminada'}, 200

        return {'message': 'Alerta no encontrada'}, 404
