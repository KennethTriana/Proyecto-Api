from sqlite3 import IntegrityError
import bcrypt
from flask import abort, app, logging, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity, unset_jwt_cookies, create_access_token
import pytz
from flaskr.modelos.modelos import Alerta, Categoria, Historial, db, Usuarios, UsuariosSchema, Productos, ProductosSchema, Venta, VentaSchema
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
import cloudinary
import cloudinary.api
import cloudinary.uploader

colombia = pytz.timezone('America/Bogota')

cloudinary.config(
    cloud_name='dsttrqkar',
    api_key='877739988135735',
    api_secret='QOSMszuWyZfmJx4XyxnU9LchZmk'
)

usuarios_schema = UsuariosSchema(many=True)  
usuario_schema = UsuariosSchema()           

productos_schema = ProductosSchema()
venta_schema = VentaSchema()

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

class VistaPerfil(Resource):
    @jwt_required()  
    def get(self):
        try:
 
            current_user_id = get_jwt_identity()
            

            if not current_user_id or not current_user_id.isdigit():
                return jsonify({'message': 'ID de usuario no válido'}), 400
            
            usuario = Usuarios.query.get(int(current_user_id)) 
            

            if usuario:
                return usuario_schema.dump(usuario), 200
            else:
                return jsonify({'message': 'Usuario no encontrado'}), 404
        except Exception as e:
            app.logger.error(f'Error al obtener el perfil: {str(e)}')
            return jsonify({'message': 'Error interno del servidor'}), 500

class VistaRegistro(Resource):
    def post(self):
        try:
            total_usuarios = Usuarios.query.count()
        except Exception as e:
            return {'error': f'Error al verificar usuarios: {str(e)}'}, 500

        campos = ['nombres', 'apellidos', 'correo', 'contrasena', 'telefono', 'direccion', 'cargo_id']
        if not all(k in request.json for k in campos):
            return {'msg': 'Faltan campos requeridos'}, 400

        print("Datos recibidos:", request.json)  

        correo_existente = Usuarios.query.filter_by(correo=request.json['correo']).first()
        if correo_existente:
            return {'msg': 'Ya existe un usuario registrado con este correo electrónico'}, 400

        cargo_id = request.json['cargo_id']
        if cargo_id not in [1, 2]:
            return {'msg': 'El cargo debe ser 1 o 2'}, 400

        contrasena_encriptada = bcrypt.hashpw(
            request.json['contrasena'].encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        nuevo_usuario = Usuarios(
            nombres=request.json['nombres'],
            apellidos=request.json['apellidos'],
            correo=request.json['correo'],
            foto_perfil=request.json.get('foto_perfil', ''),
            telefono=request.json['telefono'],  
            direccion=request.json['direccion'],
            cargo_id=cargo_id,
            contrasena_hash=contrasena_encriptada
        )

        print(f"Nuevo usuario a insertar: {nuevo_usuario}") 

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return usuario_schema.dump(nuevo_usuario), 201
        except IntegrityError:
            db.session.rollback()
            return {'msg': 'Ya existe un usuario registrado con este correo electrónico'}, 400
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar el usuario: {str(e)}")  
            return {'error': f'Error al registrar el usuario: {str(e)}'}, 500

class VistaLogin(Resource):
    def post(self):
        data = request.get_json()

        if not data or 'correo' not in data or 'contrasena' not in data:
            return {'mensaje': 'Se requieren correo y contraseña'}, 400

        u_correo = data["correo"]
        u_contrasena = data["contrasena"]

        user = Usuarios.query.filter_by(correo=u_correo).first()

        if not user:
            return {'mensaje': 'El correo no está registrado'}, 401

        if bcrypt.checkpw(u_contrasena.encode('utf-8'), user.contrasena_hash.encode('utf-8')):
            token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
            return {
                'mensaje': f'¡Bienvenido, {user.nombres}!',
                'token': token,
                'usuario': {
                    'id': user.id,
                    'nombres': user.nombres,
                    'apellidos': user.apellidos,
                    'correo': user.correo,
                    'cargo_id': user.cargo_id
                }
            }, 200
        else:
            return {'mensaje': 'Contraseña incorrecta'}, 401
        

class RecuperarContrasena(Resource):
    def post(self):
        data = request.get_json()

        if not data or 'correo' not in data or 'nombres' not in data or 'apellidos' not in data:
            return {'mensaje': 'Se requieren correo, primer nombre y primer apellido'}, 400

        correo = data['correo']
        nombres = data['nombres']
        apellidos = data['apellidos']

        usuario = Usuarios.query.filter_by(correo=correo, nombres=nombres, apellidos=apellidos).first()

        if not usuario:
            return {'mensaje': 'Los datos proporcionados no coinciden con ningún usuario'}, 404

        token_recuperacion = create_access_token(identity=str(usuario.id), expires_delta=timedelta(minutes=10))
        
        return {
            'mensaje': f'Datos verificados para {usuario.nombres}.',
            'token_recuperacion': token_recuperacion
        }, 200
        
        
class RestablecerContrasena(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()

        if not data or 'nueva_contrasena' not in data:
            return {'mensaje': 'Se requiere la nueva contraseña'}, 400

        nueva_contrasena = data['nueva_contrasena']
        user_id = get_jwt_identity()

        usuario = Usuarios.query.get(user_id)
        if not usuario:
            return {'mensaje': 'Usuario no encontrado'}, 404

        import bcrypt
        hashed = bcrypt.hashpw(nueva_contrasena.encode('utf-8'), bcrypt.gensalt())
        usuario.contrasena_hash = hashed.decode('utf-8')

        db.session.commit()

        return {'mensaje': 'Contraseña restablecida correctamente'}, 200

      
class VistaLogout(Resource):
    @jwt_required()
    def post(self):
        response = jsonify({'message': 'Sesión cerrada exitosamente'})
        unset_jwt_cookies(response)
        return response
    
class VistaUsuarios(Resource):

    @jwt_required()
    def get(self):
        usuario_id = get_jwt_identity()
        usuario_actual = Usuarios.query.get(usuario_id)

        if not usuario_actual or usuario_actual.cargo_id != 1:
            return {'mensaje': 'Acceso denegado. Solo administradores pueden ver usuarios.'}, 403

        usuarios = Usuarios.query.all()
        return usuarios_schema.dump(usuarios), 200

    @jwt_required()
    def put(self, id):
        usuario_id = get_jwt_identity()
        admin = Usuarios.query.get(usuario_id)

        if not admin or admin.cargo_id != 1:
            return {'mensaje': 'Acceso denegado. Solo administradores pueden editar usuarios.'}, 403

        usuario = Usuarios.query.get(id)
        if not usuario:
            return {'mensaje': 'Usuario no encontrado.'}, 404

        data = request.get_json()

        campos_obligatorios = ['nombres', 'apellidos', 'correo', 'telefono', 'direccion', 'foto_perfil', 'cargo_id']
        for campo in campos_obligatorios:
            valor = data.get(campo)
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                return {'error': f'El campo "{campo}" es obligatorio y no puede estar vacío.'}, 400

        if 'contrasena' in data:
            if not data['contrasena'].strip():
                return {'error': 'El campo "contrasena" no puede estar vacío.'}, 400
            usuario.contrasena_hash = bcrypt.hashpw(
                data['contrasena'].encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

        usuario.nombres = data['nombres']
        usuario.apellidos = data['apellidos']
        usuario.correo = data['correo']
        usuario.telefono = data['telefono']
        usuario.direccion = data['direccion']
        usuario.foto_perfil = data['foto_perfil']
        usuario.cargo_id = data['cargo_id']

        try:
            db.session.commit()
            return usuario_schema.dump(usuario), 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Error al actualizar usuario: {str(e)}'}, 500

    @jwt_required()
    def delete(self, id):
        usuario_id = get_jwt_identity()
        admin = Usuarios.query.get(usuario_id)

        if not admin or admin.cargo_id != 1:
            return {'mensaje': 'Acceso denegado. Solo administradores pueden eliminar usuarios.'}, 403

        usuario = Usuarios.query.get(id)
        if not usuario:
            return {'mensaje': 'Usuario no encontrado.'}, 404

        try:
            db.session.delete(usuario)
            db.session.commit()
            return {'mensaje': 'Usuario eliminado exitosamente'}, 200
        except Exception as e:
            db.session.rollback()
            print(f"ERROR al eliminar usuario: {e}")  # <-- Agrega este log
            return {'error': f'Error al eliminar usuario: {str(e)}'}, 500

class VistaProductos(Resource):
    @jwt_required()
    def get(self):
        try:
            productos = Productos.query.all()
            return [productos_schema.dump(producto) for producto in productos], 200
        except SQLAlchemyError as e:
            return {"msg": "Error al obtener productos", "error": str(e)}, 500

    @jwt_required()
    def post(self):
        try:
            usuario_id = get_jwt_identity()
            usuario = Usuarios.query.get(usuario_id)
            if not usuario:
                return {"msg": "Usuario no autenticado"}, 401

            data = request.get_json()
            required_fields = [
                'nombre', 'fecha_entrada', 'fecha_vence', 'estado',
                'cantidad', 'precio_entrada', 'precio_salida', 'categoria_id'
            ]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return {"msg": "Faltan campos requeridos", "faltantes": missing_fields}, 400

            try:
                fecha_entrada = datetime.strptime(data['fecha_entrada'], '%Y-%m-%d').date()
                fecha_vence = datetime.strptime(data['fecha_vence'], '%Y-%m-%d').date()
            except ValueError as e:
                return {"msg": "Formato de fecha inválido (esperado: YYYY-MM-DD)", "error": str(e)}, 400

            if not isinstance(data['cantidad'], (int, float)) or data['cantidad'] <= 0:
                return {"msg": "La cantidad debe ser un número positivo"}, 400
            if not isinstance(data['precio_entrada'], (int, float)) or data['precio_entrada'] <= 0:
                return {"msg": "El precio de entrada debe ser un número positivo"}, 400
            if not isinstance(data['precio_salida'], (int, float)) or data['precio_salida'] <= 0:
                return {"msg": "El precio de salida debe ser un número positivo"}, 400
            if not isinstance(data['categoria_id'], int) or data['categoria_id'] <= 0:
                return {"msg": "El ID de categoría debe ser un número entero positivo"}, 400

            categoria_existente = Categoria.query.get(data['categoria_id'])
            if not categoria_existente:
                return {"msg": f"La categoría con ID {data['categoria_id']} no existe"}, 404

            producto_existente = Productos.query.filter_by(nombre=data['nombre']).first()
            if producto_existente:
                producto_existente.cantidad += data['cantidad']
                producto_existente.fecha_entrada = fecha_entrada
                producto_existente.fecha_vence = fecha_vence
                producto_existente.precio_entrada = data['precio_entrada']
                producto_existente.precio_salida = data['precio_salida']
                producto_existente.estado = data['estado']
                producto_existente.categoria_id = data['categoria_id']
                db.session.commit()

                alertas_asociadas = Alerta.query.filter_by(productos_id=producto_existente.id).all()
                for alerta in alertas_asociadas:
                    alerta.stock = producto_existente.cantidad
                db.session.commit()
                
                if producto_existente.cantidad == 5 and usuario.cargo_id in [1, 2]:
                    alerta = Alerta(
                        mensaje=f"El producto '{producto_existente.nombre}' está agotado.",
                        productos_id=producto_existente.id,
                        stock=producto_existente.cantidad
                    )
                    db.session.add(alerta)
                    db.session.commit()

                historial = Historial(
                    accion="Ingreso adicional de producto",
                    usuario_id=usuario_id,
                    producto_id=producto_existente.id,
                    descripcion=f"Se añadieron {data['cantidad']} unidades al producto '{producto_existente.nombre}'.",
                    fecha=datetime.now(colombia)
                )
                db.session.add(historial)
                db.session.commit()

                return {
                    "msg": "Producto actualizado exitosamente",
                    "producto": productos_schema.dump(producto_existente)
                }, 200

            nuevo_producto = Productos(
                nombre=data['nombre'],
                fecha_entrada=fecha_entrada,
                fecha_vence=fecha_vence,
                estado=data['estado'],
                cantidad=data['cantidad'],
                precio_entrada=data['precio_entrada'],
                precio_salida=data['precio_salida'],
                usuarios_id=usuario_id,
                categoria_id=data['categoria_id']
            )
            db.session.add(nuevo_producto)
            db.session.commit()
            if nuevo_producto.cantidad == 0 and usuario.cargo_id in [1, 2]:
                alerta = Alerta(
                    mensaje=f"El producto '{nuevo_producto.nombre}' está agotado.",
                    productos_id=nuevo_producto.id,
                    stock=nuevo_producto.cantidad
                )
                db.session.add(alerta)
                db.session.commit()

            nuevo_historial = Historial(
                accion="Creación de producto",
                usuario_id=usuario_id,
                producto_id=nuevo_producto.id,
                descripcion=f"Producto '{data['nombre']}' creado con {data['cantidad']} unidades.",
                fecha=datetime.now(colombia)
            )
            db.session.add(nuevo_historial)
            db.session.commit()

            return {
                "msg": "Producto creado exitosamente",
                "producto": productos_schema.dump(nuevo_producto)
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"msg": "Error al guardar el producto en la base de datos", "error": str(e)}, 500
        except Exception as e:
            db.session.rollback()
            return {"msg": "Error interno del servidor", "error": str(e)}, 500

    @jwt_required()
    def put(self, id):
        try:
            producto = Productos.query.get(id)
            if not producto:
                return {"msg": "Producto no encontrado"}, 404

            usuario_id = get_jwt_identity()
            usuario = Usuarios.query.get(usuario_id)

            if not usuario or usuario.cargo_id != 1:
                return {"msg": "No tienes permiso para editar productos"}, 403

            data = request.get_json()
            cantidad_antigua = producto.cantidad

            producto.nombre = data.get('nombre', producto.nombre)
            producto.fecha_entrada = data.get('fecha_entrada', producto.fecha_entrada)
            producto.fecha_vence = data.get('fecha_vence', producto.fecha_vence)
            producto.estado = data.get('estado', producto.estado)
            producto.cantidad = data.get('cantidad', producto.cantidad)
            producto.precio_entrada = data.get('precio_entrada', producto.precio_entrada)
            producto.precio_salida = data.get('precio_salida', producto.precio_salida)
            producto.categoria_id = data.get('categoria_id', producto.categoria_id)

            if producto.cantidad != cantidad_antigua:
                alertas_asociadas = Alerta.query.filter_by(productos_id=producto.id).all()
                for alerta in alertas_asociadas:
                    alerta.stock = producto.cantidad

            db.session.commit()

            nuevo_historial = Historial(
                accion="Edición de producto",
                usuario_id=usuario_id,
                producto_id=producto.id,
                descripcion=f"Producto '{producto.nombre}' fue actualizado.",
                fecha=datetime.now(colombia)
            )
            db.session.add(nuevo_historial)
            db.session.commit()

            return {
                "msg": "Producto actualizado correctamente",
                "producto": productos_schema.dump(producto)
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"msg": "Error al actualizar el producto", "error": str(e)}, 500
        
    @jwt_required()
    def delete(self, id):
        try:
            producto = Productos.query.get(id)
            if not producto:
                    return {"msg": "Producto no encontrado"}, 404

            usuario_id = get_jwt_identity()
            usuario = Usuarios.query.get(usuario_id)

            if not usuario:
                return {"msg": "Usuario no autenticado"}, 401

            if usuario.cargo_id != 1:
                return {"msg": "No tienes permiso para eliminar productos"}, 403

            Alerta.query.filter_by(productos_id=producto.id).delete()
            Historial.query.filter_by(producto_id=producto.id).delete()

            historial = Historial(
                accion="Eliminación de producto",
                usuario_id=usuario_id,
                producto_id=producto.id,
                descripcion=f"Producto '{producto.nombre}' fue eliminado.",
                fecha=datetime.now(colombia)
            )
            db.session.add(historial)

            db.session.delete(producto)
            db.session.commit()

            return {"msg": "Producto eliminado correctamente"}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            import traceback
            traceback.print_exc()
            return {"msg": "Error al eliminar el producto", "error": str(e)}, 500

class VistaVentas(Resource):
    @jwt_required()
    def post(self, id):
        try:
            current_user = get_jwt_identity()
            producto = Productos.query.get(id)
            if not producto:
                return {'message': 'Producto no encontrado'}, 404
            cantidad_a_vender = request.json.get('cantidad')
            if cantidad_a_vender is None:
                return {'message': 'Cantidad a vender es obligatoria'}, 400

            if producto.cantidad < cantidad_a_vender:
                return {'message': 'No hay suficiente cantidad disponible.'}, 400

            producto.cantidad -= cantidad_a_vender
            db.session.commit()

            if producto.cantidad <= producto.stock_minimo:
                alerta_existente = Alerta.query.filter_by(productos_id=producto.id).first()
                if not alerta_existente:
                    nueva_alerta = Alerta(
                        nombre=f"Stock bajo para '{producto.nombre}'",
                        stock_minimo=producto.stock_minimo,
                        stock=producto.cantidad,
                        productos_id=producto.id
                    )
                    db.session.add(nueva_alerta)
                    db.session.commit()
            venta = Venta(
                cantidad_a_vender=cantidad_a_vender,
                productos_id=producto.id
            )
            db.session.add(venta)
            db.session.commit()

            nuevo_historial = Historial(
                accion="Venta de producto",
                usuario_id=current_user,
                producto_id=producto.id,
                descripcion=f"Se vendieron {cantidad_a_vender} unidades del producto '{producto.nombre}'.",
                fecha=datetime.now(colombia)
            )
            db.session.add(nuevo_historial)
            db.session.commit()

            return {
                'message': 'Venta realizada con éxito',
                'producto': productos_schema.dump(producto),
                'venta_id': venta.id
            }, 200
        except Exception as e:
            return {'error': 'Error al vender el producto', 'details': str(e)}, 500



