from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# ✅ Déclaration des extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."

    # ✅ Importation différée pour éviter l'import circulaire
    with app.app_context():
        from app import models  # Import des modèles seulement après init du db
        print("[INFO] Vérification et application des migrations...")
        models.create_admin()

    # 📌 Import des blueprints ici
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp  # Vérifie qu'il est bien importé ici
    from app.routes.main import main_bp  # S'il y a une page principale

    # 📌 Enregistrement des blueprints
    app.register_blueprint(auth_bp)  # Assure-toi qu'il est défini une seule fois
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # ✅ Importer ici pour éviter l'import circulaire
        return User.query.get(int(user_id))
                           
    return app
