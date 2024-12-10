from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '54321'
    app.config['JWT_SECRET_KEY'] = '12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Inventario.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_RUN_PORT'] = 5001

    return app