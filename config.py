import os
from datetime import timedelta
from cryptography.fernet import Fernet


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change_this_secret_key')  # Doit être défini dans l'environnement

    # MYSQL (Ne stockez pas d'identifiants en dur !)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')  
    DB_NAME = os.getenv('DB_NAME', 'pynotes')

    # Google Recaptcha (NE JAMAIS METTRE LA CLÉ PRIVÉE EN DUR)
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY', '')
    ENCRYPTION_KEY = Fernet.generate_key()  # Clé pour le chiffrement des données
    MAX_LOGIN_ATTEMPTS = 3
    LOGIN_TIMEOUT = 300 

    
    # Sécurité session
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(os.getenv('SESSION_LIFETIME', 30)))

    # Connexion SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
