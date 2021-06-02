from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "virtual_lab"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jhjhjdshjshdj'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'
    db.init_app(app)

  
    from projects.routes import views
    from projects.auth import auth


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

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
