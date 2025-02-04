import pymysql
from app import create_app 
from flask_migrate import upgrade
from config import Config


db_name = Config.DB_NAME

print(f"[INFO] Vérification de l'existence de la base de données '{db_name}'...")

try:
    conn = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )
    cursor = conn.cursor()
    
    cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
    result = cursor.fetchone()

    if not result:
        print(f"[INFO] La base de données '{db_name}' n'existe pas. Création en cours...")
        cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"[INFO] Base de données '{db_name}' créée avec succès !")
    
    cursor.close()
    conn.close()

except Exception as e:
    print(f"[ERREUR] Impossible de vérifier/créer la base de données : {e}")


app = create_app()


with app.app_context():
    import os
    if not os.path.exists("migrations"):  
        print("[INFO] Initialisation des migrations...")
        from flask_migrate import init, migrate
        init()
        migrate(message="Initial migration")
    
    print("[INFO] Application des migrations...")
    upgrade()



if __name__ == "__main__":
    app.run(debug=True)
