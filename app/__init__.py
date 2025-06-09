from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import os.path
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua_chave_secreta_muito_complexa_e_aleatoria'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://fernandatanaka:13112003@localhost:5433/curso_flask_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

db = SQLAlchemy()
migrate = Migrate()

lm = LoginManager(app)

def create_app():
    app.config.from_object(Config)

    db.init_app(app)
    from app import models
    migrate.init_app(app, db)

    from app.controllers.default import bp as default_bp
    app.register_blueprint(default_bp)

    from app.models import tables

    return app