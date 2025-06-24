from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flaskr.modelos.modelos import Historial, HistorialSchema

class VistaHistorial(Resource):
    @jwt_required()
    def get(self):
        historial = Historial.query.order_by(Historial.fecha.desc()).all()
        historial_schema = HistorialSchema(many=True)  
        historial_dump = historial_schema.dump(historial)
        return {'historial': historial_dump}, 200
