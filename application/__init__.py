from .config import Config
from .auth import auth
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .models import UserModel

login_manager=LoginManager()
login_manager.login_view='auth.login'

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)
    login_manager.init_app(app)
    app.register_blueprint(auth) #Registramos el blueprint
    
    return app

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)