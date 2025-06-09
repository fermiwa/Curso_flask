from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import os.path
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua_chave_secreta_muito_complexa_e_aleatoria'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://fernandatanaka:13112003@localhost:5433/curso_flask_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

db = SQLAlchemy()
migrate = Migrate()

lm = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    lm.init_app(app)
    lm.login_view = 'default.login'

    from app import models

    @lm.user_loader 
    def load_user(user_id):
        from app.models.tables import User
        return User.query.get(int(user_id))
    
    from app.controllers.default import bp as default_bp
    app.register_blueprint(default_bp)

    migrate.init_app(app, db)

    return app