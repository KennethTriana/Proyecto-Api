from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
<<<<<<< HEAD
    app.config['SECRET_KEY'] = '54321'
    app.config['JWT_SECRET_KEY'] = '12345'
=======
<<<<<<< HEAD
    app.config['SECRET_KEY'] = '54321'
    app.config['JWT_SECRET_KEY'] = '12345'
=======
<<<<<<< HEAD
<<<<<<< HEAD
    app.config['SECRET_KEY'] = '54321'
    app.config['JWT_SECRET_KEY'] = '12345'
=======
>>>>>>> 6a723bdab1a4b184e29ebb36ac2d5c8a3889931c
>>>>>>> 5f37b97a19a2008d137279961b76fc0fd7f1a86b
>>>>>>> 1eec5f1ca3b1ae543c77fc627043c268114a0236
=======
>>>>>>> 6a723bdab1a4b184e29ebb36ac2d5c8a3889931c
>>>>>>> 5f37b97a19a2008d137279961b76fc0fd7f1a86b
>>>>>>> 7e7301d4683567745a9015d3cc9b53150fb3f653
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Inventario.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_RUN_PORT'] = 5001

    return app