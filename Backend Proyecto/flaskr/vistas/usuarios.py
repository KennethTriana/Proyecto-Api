from flask import request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from flaskr.modelos.modelos import db, Usuarios, UsuariosSchema
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.modelos.modelos import db, Productos, ProductosSchema, Venta, VentaSchema
from datetime import datetime
import cloudinary
import cloudinary.api
import cloudinary.uploader
from flask_login import current_user, login_required

cloudinary.config(
    cloud_name='dsttrqkar',  
    api_key='877739988135735',       
    api_secret='QOSMszuWyZfmJx4XyxnU9LchZmk'   
)

class CambioImagen(Resource):
    def post(self):
        archivo = request.files['archivo']
        resultado = cloudinary.uploader.upload(archivo)
        foto_perfil = resultado['url']

        current_user.profile_image = foto_perfil
        db.session.commit()

        return jsonify({
            "message": "Imagen subida con éxito",
            "url": foto_perfil
        })

def generate_token(usuarios_id):
    token = create_access_token(identity=usuarios_id)
    return token

usuarios_schema = UsuariosSchema()

class VistaPerfil(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity() 
        usuario = Usuarios.query.get(current_user_id) 

        if usuario:
            return usuarios_schema.dump(usuario), 200 
        return jsonify({'message': 'Usuario no encontrado'}), 404

class VistaUsuarios(Resource):
    @jwt_required()
    def get(self): 
        return [usuarios_schema.dump(usuario) for usuario in Usuarios.query.all()]

    @jwt_required()
    def post(self): 
        try:
            usuario = get_jwt_identity()
            usuario = Usuarios.query.get(usuario)
            if usuario is None:
                return {"msg": "Usuario no autenticado"}, 401

            if usuario.cargo_id != 1:
                return {"msg": "No tienes permiso para realizar esta acción"}, 403

            nuevo_usuario = Usuarios(
                nombres=request.json['nombres'],
                apellidos=request.json['apellidos'],
                correo=request.json['correo'],
                contrasena=request.json['contrasena'], 
                foto_perfil=request.json['foto_perfil'],
                telefono=request.json['telefono'],
                direccion=request.json['direccion'],  
                cargo_id=request.json['cargo_id'] 
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            usuarios_actualizados = usuarios_schema.dump(nuevo_usuario)
            return usuarios_actualizados, 201 

            return {'mensaje': 'Usuario registrado exitosamente'}, 201
        except Exception as e:
            return {'error': 'Error al registrar el usuario'}, 500

    @jwt_required()
    def delete(self, id): 

        current_user = get_jwt_identity()
        usuario_actual = Usuarios.query.filter_by(nombres=current_user).first()

        if usuario_actual.cargo_id != 1: 
            return jsonify({'message': 'No tienes permiso para eliminar usuarios.'}), 403

        usuario = Usuarios.query.get(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({'message': 'Usuario eliminado'}), 200
        return jsonify({'message': 'Usuario no encontrado'}), 404

    @jwt_required()
    def put(self, id): 
        usuario = Usuarios.query.get(id)
        if usuario:
            usuario.nombres = request.json.get('nombres', usuario.nombres)
            usuario.apellidos = request.json.get('apellidos', usuario.apellidos)
            usuario.correo = request.json.get('correo', usuario.correo)
            usuario.contrasena = request.json.get('contrasena', usuario.contrasena) 
            usuario.foto_perfil = request.json.get('foto_perfil', usuario.foto_perfil) 
            usuario.telefono = request.json.get('telefono', usuario.telefono)
            usuario.direccion = request.json.get('direccion', usuario.direccion)
            usuario.cargo_id = request.json.get('cargo_id', usuario.cargo_id)
            db.session.commit()
            usuarios_actualizados = usuarios_schema.dump(usuario)
            return jsonify(usuarios_actualizados), 200
        return jsonify({'message': 'Usuario no encontrado'}), 404

class VistaLogin(Resource):
    def post(self):
        u_nombres = request.json["nombres"]
        u_contrasena = request.json["contrasena"]
        user = Usuarios.query.filter_by(nombres=u_nombres).first()
        if user and user.verificar_contrasena(u_contrasena):
            token = create_access_token(identity=str(user.id))
            return {'mensaje': f'¡Bienvenido, {user.nombres}!', 'token': token}, 200
        else:
            return {'mensaje': 'Nombre de usuario o contraseña incorrectos'}, 401

class VistaLogout(Resource):
    @jwt_required()

    def post(self):
        jti = get_jwt_identity()
        response = jsonify({'message': 'Sesión cerrada exitosamente'})
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            db.session.add(revoked_token)
            db.session.commit()
        except Exception as e:
            return jsonify({'message': 'Error al cerrar sesión'}), 500
        unset_jwt_cookies(response)
        return response

productos_schema = ProductosSchema()

class VistaProductos(Resource):
    @jwt_required()
    def get(self):  
        return jsonify([productos_schema.dump(producto) for producto in Productos.query.all()])

    @jwt_required()
    def post(self):
        try:
            usuario = get_jwt_identity()
            usuario = Usuarios.query.get(usuario)
            if usuario is None:
                return {"msg": "Usuario no autenticado"}, 401

            if usuario.cargo_id != 1:
                return {"msg": "No tienes permiso para realizar esta acción"}, 403

            nuevo_producto = Productos(
                nombre=request.json['nombre'],
                fecha_entrada = datetime.strptime(request.json['fecha_entrada'], '%Y-%m-%d').date(),
                fecha_vence = datetime.strptime(request.json['fecha_vence'], '%Y-%m-%d').date(),
                estado=request.json['estado'],
                cantidad=request.json['cantidad'],
                precio_entrada=request.json['precio_entrada'],
                precio_salida=request.json['precio_salida'],
                usuarios_id=request.json['usuarios_id'], 
                categoria_id=request.json['categoria_id']
            )

            db.session.add(nuevo_producto)
            db.session.commit()
            productos_actualizados = productos_schema.dump(nuevo_producto)
            return {"msg": "Producto creado exitosamente", "producto": productos_actualizados}, 201

        except Exception as e:
            db.session.rollback()
            return {"msg": "Error interno del servidor", "error": str(e)}, 500

    @jwt_required()
    def put(self, id): 
        producto = Productos.query.get(id)
        if producto:
            producto.nombre = request.json.get('nombre', producto.nombre)
            producto.fecha_entrada = request.json.get('fecha_entrada', producto.fecha_entrada)
            producto.fecha_vence = request.json.get('fecha_vence', producto.fecha_vence)
            producto.estado = request.json.get('estado', producto.estado)
            producto.cantidad = request.json.get('cantidad', producto.cantidad)
            producto.precio_entrada = request.json.get('precio_entrada', producto.precio_entrada)
            producto.precio_salida = request.json.get('precio_salida', producto.precio_salida)
            producto.usuarios_id = request.json.get('usuarios_id', producto.usuarios_id)
            producto.categoria_id = request.json.get('categoria_id', producto.categoria_id)
            db.session.commit()
            productos_actualizados = productos_schema.dump(producto)
            return jsonify(productos_actualizados), 200
        return jsonify({'message': 'Producto no encontrado'}), 404

    @jwt_required()
    def delete(self, id): 
        current_user = get_jwt_identity()
        usuario_actual = Usuarios.query.filter_by(nombres=current_user).first()

        if usuario_actual.cargo_id != 1: 
            return jsonify({'message': 'No tienes permiso para eliminar productos.'}), 403

        producto = Productos.query.get(id)
        if producto:
            producto.eliminado = True
            db.session.commit()
            return jsonify({'message': 'Producto eliminado'}), 200

        return jsonify({'message': 'Producto no encontrado'}), 404

venta_schema = VentaSchema()

class VistaVentas(Resource):
    def post(self, id):
        try:
            producto = Productos.query.get(id)
            if not producto:
                return jsonify({'message': 'Producto no encontrado'}), 404

            cantidad_a_vender = request.json.get('cantidad')
            if producto.cantidad < cantidad_a_vender:
                return jsonify({'message': 'No hay suficiente cantidad disponible.'}), 400

            producto.cantidad -= cantidad_a_vender
            db.session.commit()

            return jsonify({'message': 'Venta realizada con éxito', 'producto': productos_schema.dump(producto)}), 200
        except Exception as e:
            return jsonify({'error': 'Error al vender el producto', 'details': str(e)}), 500

    def put(self, id): 
        try:
            venta = Productos.query.get(id)
            if venta:
                venta.cantidad_a_vender = request.json.get('cantidad', venta.cantidad)
                db.session.commit()
                return jsonify(productos_schema.dump(venta)), 200
            return jsonify({'message': 'Venta no encontrada'}), 404
        except Exception as e:
            return jsonify({'error': 'Error al actualizar la venta', 'details': str(e)}), 500