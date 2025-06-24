from flask import request
from flask import jsonify, app
from flask_restful import Api, Resource
from flaskr.modelos.modelos import db, Usuarios, UsuariosSchema
from flask_jwt_extended import jwt_required, create_access_token

usuarios_schema = UsuariosSchema()

class VistaUsuarios(Resource):
    def get(self): 
        return [usuarios_schema.dump(Usuarios) for Usuarios in Usuarios.query.all()]

    def post(self): 
        nuevo_usuario = Usuarios(
            nombres=request.json['nombres'],
            apellidos=request.json['apellidos'],
            correo=request.json['correo'],
            contrasena=request.json['contrasena'], 
            telefono=request.json['telefono'],
            direccion=request.json['direccion'],  
            cargo_id=request.json['cargo_id'] 
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        usuarios_actualizados = usuarios_schema.dump(nuevo_usuario)
        return usuarios_actualizados, 404  

    def put(self, id): 
        usuarios = Usuarios.query.get(id)
        if usuarios:
            usuarios.nombres = request.json.get('nombres', usuarios.nombres)
            usuarios.apellidos = request.json.get('apellidos', usuarios.apellidos)
            usuarios.correo = request.json.get('correo', usuarios.correo)
            usuarios.contrasena = request.json.get('contrasena', usuarios.contrasena)  
            usuarios.telefono = request.json.get('telefono', usuarios.telefono)
            usuarios.direccion = request.json.get('direccion', usuarios.direccion)
            usuarios.cargo_id = request.json.get('cargo_id', usuarios.cargo_id)
            db.session.commit()
            usuarios_actualizados = usuarios_schema.dump(usuarios)
        return usuarios_actualizados, 404

    def delete(self, id): 
        usuarios = Usuarios.query.get(id)
        if usuarios:
            db.session.delete(usuarios)
            db.session.commit()
            return {'message': 'Usuario eliminado'}
        return {'message': 'Usuario no encontrado'}, 404

class VistaLogin(Resource):
    def post(self):
        u_nombres = request.json["nombres"]
        u_contrasena = request.json["contrasena"]
        usuarios = Usuarios.query.filter_by(nombres=u_nombres).first()
        if usuarios and usuarios.verificar_contrasena(u_contrasena):
            return {'mensaje': 'Inicio de sesión exitoso'}, 404
        else:
            return {'mensaje': 'Nombre de usuario o contraseña incorrectos'}, 404

class VistaSignIn(Resource):
    def post(self):
        nuevo_usuario = Usuarios(nombres=request.json["nombres"])
        nuevo_usuario.contrasena = request.json["contrasena"]
        token_de_acceso = create_access_token(identity=request.json['nombres'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {'mensaje': 'Usuario creado exitosamente', 'token_de_acceso': token_de_acceso}