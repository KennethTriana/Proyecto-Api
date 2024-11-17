from flaskr import create_app
#from flaskr.modelos.modelos import Album, Usuario, Medio, Cancion
from .modelos import db
from flask_restful import Api
from .vistas import VistaCanciones, VistaCancion, VistaSignIn, VistaLogIn, VistaAlbum, VistaAlbumsUsuario, VistaCancionesAlbum
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = create_app('default')
app_context = app.app_context()
app_context.push()

CORS(app)
db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaCanciones, '/canciones')
api.add_resource(VistaCancion, '/cancion/<int:id>')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaAlbumsUsuario, '/usuario/<int:id>/albumes')
api.add_resource(VistaAlbum, '/album/<int:id>')
api.add_resource(VistaCancionesAlbum, '/album/<int:id>/canciones')

jwt = JWTManager(app)

#with app.app_context():
#    u = Usuario(nombre='juan', contrasena='12345')
#    a = Album(titulo='prueba', anio=1999, descripcion='texto', medio=Medio.CD)
#    c = Cancion(titulo='Earth Song', minutos=6, segundos=45, interprete='Michael Jackson')
#    u.albumes.append(a)
#    a.canciones.append(c)
#    db.session.add(u)
#    db.session.add(c)
#    db.session.commit()
#    print(Usuario.query.all())
#    print(Album.query.all())
#    print(Album.query.all()[0].canciones)
#    print(Cancion.query.all())
#    db.session.delete(a)
#    print(Album.query.all())
#    print(Cancion.query.all())