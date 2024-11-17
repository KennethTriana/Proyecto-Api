from flask import jsonify, app
from flask_restful import Api, Resource, request
from flaskr.modelos.modelos import db, Alerta, AlertaSchema

alerta_schema = AlertaSchema()

class VistaAlerta(Resource):
    def get(self):
        return [alerta_schema.dump(Alerta) for Alerta in Alerta.query.all()]

    def post(self): 
        nueva_alerta = Alerta(
            nombre=request.json['nombre'],
            stock_minimo=request.json['stock_minimo'],
            stock=request.json['stock'],
            inventario_id=request.json['inventario_id'] 
        )
        db.session.add(nueva_alerta)
        db.session.commit()
        alerta_actualizada = alerta_schema.dump(nueva_alerta)
        return alerta_actualizada, 404  

    def put(self, id): 
        alerta = Alerta.query.get(id)
        if alerta:
            alerta.nombre = request.json.get('nombre', alerta.nombre)
            alerta.stock_minimo = request.json.get('stock minimo', alerta.stock_minimo) 
            alerta.stock = request.json.get('stock', alerta.stock)
            alerta.inventario_id = request.json.get('inventario_id', alerta.inventario_id)
            db.session.commit()
            alerta_actualizada = alerta_schema.dump(alerta)
        return alerta_actualizada, 404

    def delete(self, id): 
        alerta = Alerta.query.get(id)
        if alerta:
            db.session.delete(alerta)
            db.session.commit()
            return {'message': 'Alerta eliminada'}
        return {'message': 'Alerta no encontrada'}, 404