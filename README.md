# 📚 PyNotes - Gestion Scolaire avec Flask

PyNotes est une application web inspirée de Pronote, développée avec Flask et MySQL. L'objectif principal de ce projet est d'étudier l'architecture d'un tel système, d'analyser ses vulnérabilités et d'appliquer des principes de DevSecOps pour améliorer sa sécurité.

## ✨ Fonctionnalités

### 🛠️ Admin
- Compte par défaut :
  - **Email** : `admin@example.com`
  - **Mot de passe** : `admin`
- Créer et gérer les classes/matières
- Ajouter de nouveaux comptes (professeurs et élèves)
- Assigner des matières aux professeurs et des classes aux élèves

### 🎓 Élève
- Voir son emploi du temps *(actuellement statique, futur lien avec BDD)*
- Modifier son profil
- Consulter ses notes

### 👨‍🏫 Professeur
- Attribuer des notes aux élèves selon leur classe
- Modifier son profil

---

## 🚀 Installation & Lancement

### 1️⃣ Prérequis
- **Python** (3.8 ou supérieur recommandé)
- **MySQL** installé et configuré

### 2️⃣ Installation
```bash
# Cloner le projet
git clone https://github.com/ton-utilisateur/pynotes.git
cd pynotes

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3️⃣ Configuration
Créer un fichier `.env` à la racine du projet avec le contenu suivant :

```ini
# Configuration de l'application
SECRET_KEY=VotreCléSecrèteIci

# Configuration de la base de données
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
DB_NAME=pynotes
DATABASE_URL=mysql+pymysql://root:votre_mot_de_passe@localhost:3306/pynotes

# Clés reCAPTCHA (remplacez-les par vos propres clés)
RECAPTCHA_PUBLIC_KEY=VotreCléPubliqueIci
RECAPTCHA_PRIVATE_KEY=VotreCléPrivéeIci

# Configuration de la session
SESSION_LIFETIME=30
```

### 4️⃣ Lancer le projet
```bash
python run.py
```
L'application sera accessible à l'adresse : `http://127.0.0.1:5000`

---

## 🛡️ Objectifs DevSecOps
- **Analyse des failles** : Identifier les vulnérabilités du projet
- **Sécurisation** : Appliquer des correctifs et bonnes pratiques
- **Amélioration continue** : Intégration des principes DevSecOps

---

## 📜 Licence
MIT License

---

## 🤝 Contribution
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

🚀 **Développé avec Flask & ❤️**
