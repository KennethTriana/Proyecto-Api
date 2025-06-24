from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app(config_name):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '12345'  
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=365*10)  
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  
    app.config['JWT_SECRET_KEY'] = '12345'  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/InventarioLGC'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_RUN_PORT'] = 5001
    app.config['DEBUG'] = True
    
    
    CORS(app, origins=["http://localhost:3000"])
    CORS(app)

    jwt = JWTManager(app)
    
    return app

