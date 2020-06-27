from .config import Config
from .auth import auth
from .admin import admin
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .models import UserModel

login_manager=LoginManager()
login_manager.login_view='auth.login'

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(Config)
    login_manager.init_app(app)
    app.register_blueprint(auth) #Registramos el blueprint
    app.register_blueprint(admin)
    
    return app

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)