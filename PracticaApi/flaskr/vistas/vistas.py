from flask import request
from flask_restful import Resource
from ..modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
album_schema = AlbumSchema()

class VistaCanciones(Resource):
    def get(self):
        return [cancion_schema.dump(Cancion) for Cancion in Cancion.query.all()]

        
    def post(self):
        nueva_cancion = Cancion(titulo=request.json['titulo'],\
                                minutos=request.json['minutos'],\
                                segundos=request.json['segundos'],\
                                interprete=request.json['interprete'])

        db.session.add(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion), 201       

class VistaCancion(Resource):
    def get(self, id):
        return cancion_schema.dump(Cancion.query.get_or_404(id))
    
    def put (self, id):
        cancion = Cancion.query.get_or_404(id)
        cancion.titulo = request.json("titulo", cancion.titulo)
        cancion.minutos = request.json("minutos", cancion.minutos)
        cancion.segundos = request.json("segundos", cancion.segundos)
        cancion.interprete = request.json("interprete", cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)
    
    def delete(self, id):
        cancion = Cancion.query.get_or_404(id)
        db.session.delete(cancion)
        db.session.commit()
        return '', 204
    
class VistaLogIn(Resource):
    def post(self):
        u_nombre = request.json["nombre"]
        u_contrasena = request.json["contrasena"]
        usuario = Usuario.query.filter_by(nombre=u_nombre, contrasena=u_contrasena).all()
        if usuario:
            return {'mensaje': 'Inicio de sesión exitoso'}, 200
        else:
            return {'mensaje': 'Nombre de usuario o contraseña incorrectos'}, 401
        
class VistaSignIn(Resource):
    def post(self):
        nuevo_usuario = Usuario (nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        token_de_acceso = create_access_token(identity=request.json['nombre'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {'mensaje': 'Usuario creado exitosamente', 'token_de_acceso': token_de_acceso}
    
    def put(self, id):
        usuario = Usuario.query.get_or_404(id)
        usuario.contrasena = request.json["contrasena"]
        db.session.commit()
        return usuario_schema.dump(usuario)
    
    def delete(self, id):
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class VistaAlbumsUsuario(Resource):

    @jwt_required()
    def post (self, id):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre', 400

        return album_schema.dump(nuevo_album)

    @jwt_required()
    def get(self, id):
        usuario = Usuario.query.get_or_404(id)
        return [album_schema.dump(al) for al in usuario.albumes]


class VistaCancionesAlbum(Resource):

    def post(self, id):
        album = Album.query.get_or_404(id)

        if "id" in request.json.keys():
            nueva_cancion = Cancion.query.get(request.json["id"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea', 404

        else:
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)
    
    def get(self, id):
        album = Album.query.get_or_404(id)
        return [cancion_schema.dump(ca) for ca in album.canciones]
    
class VistaAlbum(Resource):

    def get(self,id):
        return album_schema.dump(Album.query.get_or_404(id))
    
    def put(self,id):
        album = Album.query.get_or_404(id)
        album.titulo = request.json.get("titulo", album.titulo)
        album.anio = request.json.get("anio", album.anio)
        album.descripcion = request.json.get("descripcion", album.descripcion)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)
    
    def delete(self, id):
        album = Album.query.get_or_404(id)
        db.session.delete(album)
        db.session.commit()
        return '', 204
    
    