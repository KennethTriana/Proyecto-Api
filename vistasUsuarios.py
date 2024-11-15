from flask_restful import Resource
from ..modelos import db, Usuarios, UsuariosSchema
from flask import request

usuarios_schema = UsuariosSchema()

class VistaUsuarios(Resource):

    def get(self):
        return [usuarios_schema.dump(Usuarios) for Usuarios in Usuarios.query.all()]
    
    def post(self, nombres, apellidos, correo, contraseña, telefono, direccion, cargo_id):
        nuevo_usuario_data = request.get_json()
        cargo_id = nuevo_usuario_data.get("cargo_id")
        nombres = nuevo_usuario_data.get("nombres")
        apellidos = nuevo_usuario_data.get("apellidos")
        correo = nuevo_usuario_data.get("correo")
        direccion = nuevo_usuario_data.get("dirrecion")
        telefono = nuevo_usuario_data.get("telefono")
        contraseña = nuevo_usuario_data.get("contraseña")
        if not isinstance(nombres, str):
            return {"ADVERTENCIA": "Los dos primeros nombres del usuario son requerido."}, 404
        if not isinstance(apellidos, str):
            return {"ADVERTENCIA": "Los dos priemros apellidos del usuario son requerido."}, 404
        if not isinstance(correo, str):
            return {"ADVERTENCIA": "Su correo electronico personal."},404
        if not isinstance(contraseña, int):
            return {"ADVERTENCIA": "Digite el numero de su identidad obligatorio."},404
        if not isinstance(telefono, int):
            return {"ADVERTENCIA": "Tiene que ser su telefono de contacto."},404
        if not isinstance(direccion, str):
            return {"ADVERTENCIAS": "Digite la dirrecion de su residencia actual."},404
        if cargo_id not in ["gerente", "empleado"]:
            return {"ADVERTENCIA": "El cargo_id debe ser 'gerente' o 'empleado'."}, 404
        nuevo_usuario = Usuarios(nombres = nombres, apellidos = apellidos, correo = correo, contraseña = contraseña, telefono = telefono, direccion = direccion, cargo_id = cargo_id)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return usuarios_schema.dump(nuevo_usuario), 404
    
    def put(self, usuario_id):
           usuario = Usuarios.query.get_or_404(usuario_id)
           usuario_data = request.get_json()
           usuario.nombres = usuario_data.get("nombres", usuario.nombres)
           usuario.apellidos = usuario_data.get("apellidos", usuario.apellidos)
           usuario.correo = usuario_data.get("correo", usuario.correo)
           usuario.contraseña = usuario_data.get("contraseña", usuario.contraseña)
           usuario.telefono = usuario_data.get("telefono", usuario.telefono)
           usuario.direccion = usuario_data.get("direccion", usuario.direccion)
           usuario.cargo_id = usuario_data.get("cargo_id", usuario.cargo_id)
           db.session.commit()
           return usuarios_schema.dump(usuario), 404
    
    def delete(self, usuario_id):
        usuario = Usuarios.query.get_or_404(usuario_id)
        db.session.delete(usuario)
        db.session.commit()
        return {"MENSAJE": "Usuario eliminado."}, 404  
