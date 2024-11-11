from flask_restful import Resource
from ..modelos import db, Usuarios, UsuariosSchema
from flask import request

usuarios_schema = UsuariosSchema()

class VistaUsuarios(Resource):
    def get(self):
        return [usuarios_schema.dump(Usuarios) for Usuarios in Usuarios.query.all()]
    
    def post(self, Cargo, Nombres, Apellidos, Edad, Calle, Telefono, Correo, Genero, Identidad, Numero_Identidad):
        nuevo_usuario_data = request.get_json()
        Cargo = nuevo_usuario_data.get("Cargo")
        Nombres = nuevo_usuario_data.get("Nombres")
        Apellidos = nuevo_usuario_data.get("Apellidos")
        Edad = nuevo_usuario_data.get("Edad")
        Calle = nuevo_usuario_data.get("Calle")
        Telefono = nuevo_usuario_data.get("Telefono")
        Correo = nuevo_usuario_data.get("Correo")
        Genero = nuevo_usuario_data.get("Genero")
        Identidad = nuevo_usuario_data.get("Identidad")
        Numero_Identidad = nuevo_usuario_data.get("Numero_Identidad")

        if Cargo not in ["gerente", "empleado"]:
            return {"ADVERTENCIA": "El cargo debe ser 'gerente' o 'empleado'."}, 400
        if not isinstance(Nombres, str):
            return {"ADVERTENCIA": "Los dos primeros nombres del usuario son requerido."}, 400
        if not isinstance(Apellidos, str):
            return {"ADVERTENCIA": "Los dos priemros apellidos del usuario son requerido."}, 400
        if not isinstance(Edad, int):
            return {"ADVERTENCIA": "La edad debe ser mayor de 18."}, 400
        if not isinstance(Calle, str):
            return {"ADVERTENCIA": "Debe ser la casa o dirrecion donde vive usted."},400
        if not isinstance(Telefono, int):
            return {"ADVERTENCIA": "Tiene que ser su telefono de contacto."},400
        if not isinstance(Correo, str):
            return {"ADVERTENCIA": "Su correo electronico personal."},400
        if Genero not in ["Hombre", "Mujer"]:
            return {"ADVERTENCIA": "El genero es obligatorio y es 'hombre' o 'mujer'."}, 400
        if Identidad not in ["Cedula", "Cedula Extranger"]:
            return {"ADVERTENCIA": "Digite que tipo es su identificacion si es 'Cedula' o 'Cedula Extrangera'."}, 400        
        if not isinstance(Numero_Identidad, int):
            return {"ADVERTENCIA": "Digite el numero de su identidad obligatorio."},400

        nuevo_usuario = Usuarios(Cargo = Cargo, Nombres = Nombres, Apellidos = Apellidos, Edad = Edad, Calle = Calle, Telefono = Telefono, Correo = Correo, Genero = Genero, Identidad = Identidad, Numero_Identidad = Numero_Identidad)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return usuarios_schema.dump(nuevo_usuario), 201
