from flask import Flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
from os import path
from os.path import join, dirname, realpath
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "virtual_lab"
UPLOAD_FOLDER = join(dirname(realpath(__file__)), './static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
MAX_CONTENT_LENGTH = 2*1000*1000

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dattebayo'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    db.init_app(app)

  
    from projects.routes import views
    from projects.auth import auth
    from projects.eksperimen import vlab


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(vlab, url_prefix='/')

    from projects.models import Users

    creater_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app

def creater_database(app):
    if not path.exists('projects/'+DB_NAME):
        db.create_all(app=app)
        print('Create Database!')
