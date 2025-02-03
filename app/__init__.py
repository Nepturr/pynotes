from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from werkzeug.security import generate_password_hash



db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."

    with app.app_context():
        from app import models 
        
        try:
            models.create_admin() 
        except Exception as e:
            print(f"[ERREUR] Impossible de créer l'admin : {e}")
        

    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp 
    from app.routes.main import main_bp 
    from app.routes.student import student_bp  
    from app.routes.teacher import teacher_bp  

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))
                           
    return app

