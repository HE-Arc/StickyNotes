# StickyNotes
Application qui permet d'ajouter des post-its sur un chalkboard partagé.

# Guide d'installation
## Étape 1 - Initialisation
### Windows
- Ouvrir un nouveau terminal (cmd.exe)
- Cloner le projet : `git clone https://github.com/HE-Arc/StickyNotes.git`
- Aller dans le dossier StickyNotes : `cd StickyNotes`
- Créer un nouvel environnement virtuel avec virtualvenv : `python -m venv .`
- Activer virtualvenv : `Scripts\activate.bat`
- Installer le package python : `pip install -r requirements.txt`

### Linux
- Ouvrir un nouveau terminal
- Cloner le projet : `git clone https://github.com/HE-Arc/StickyNotes.git`
- Aller dans le dossier StickyNotes : `cd StickyNotes`
- Créer un nouvel environnement virtuel avec virtualvenv : `python -m venv .`
- Activer virtualvenv : `source bin/activate`
- Installer le package python : `pip install -r requirements.txt`

#### Requirements dans la présente version
- libmysqlclient-dev
- bcrypt==3.1.4
- certifi==2018.1.18
- cffi==1.11.4
- chardet==3.0.4
- Django==2.0.2
- django-bootstrap4==0.0.6
- django-crispy-forms==1.7.0
- django-embed-video==1.1.2
- django-enumfields==0.9.0
- django-environ==0.4.4
- django-guardian==1.4.9
- django-simple-menu==1.2.1
- django-tables2==1.21.1
- django-widget-tweaks==1.4.1
- flake8==3.5.0
- idna==2.6
- mccabe==0.6.1
- mysqlclient==1.3.12
- pycodestyle==2.3.1
- pycparser==2.18
- pyflakes==1.6.0
- pytz==2018.3
- requests==2.18.4
- six==1.11.0
- urllib3==1.22

## Étape 2 - Configuration
- Copier ou renommer le fichier **stickynotes/stickynotes/.env.default** en **.env**
- Ouvrir **.env** avec un éditeur de texte
- Configurer les variables avec vos données (notamment les informations de la base de données)

## Étape 3 - Migration
- Aller **.\StickyNotes\stickynotes**
- Préparer la migration : `python manage.py makemigrations`
- Appliquer la migration : `python manage.py migrate`
- Lancer le serveur server : `python manage.py runserver`
