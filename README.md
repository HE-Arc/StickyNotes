# StickyNotes
Application qui permet d'ajouter des post-its sur un chalkboard partagé.

# Installation guide
## Windows
- Open new console (cmd.exe)
- Clone project : `git clone https://github.com/HE-Arc/StickyNotes.git`
- Go to the folder StickyNotes : `cd StickyNotes`
- Create new virtualvenv : `python -m venv .`
- Active virtualvenv : `Scripts\activate.bat`
- Install python package : `pip install -r requirements.txt`
- ... (soon)
- Go to **.\StickyNotes\stickynotes** : `cd stickynotes`
- Migrate database : `python manage.py migrate`
- Run server : `python manage.py runserver`

## Linux
- Open new console
- Clone project : `git clone https://github.com/HE-Arc/StickyNotes.git`
- Go to the folder StickyNotes : `cd StickyNotes`
- Create new virtualvenv : `python -m venv .`
- Active virtualvenv : `source bin/activate`
- Install python package : `pip install -r requirements.txt`
- ... (soon)
- Go to **./StickyNotes/stickynotes** : `cd stickynotes`
- Migrate database : `python manage.py migrate`
- Run server : `python manage.py runserver`

### Requirements
- libmysqlclient-dev
- ....

# Configuration
- Copy or rename file **stickynotes/stickynotes/.env.default** to **.env**
- Open file **.env** with text editor
- Configure variable with your data's
- ...
