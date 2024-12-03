#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024
# Sujet : création d'une application web (lanceur)
#################################################

# Chargement des librairies
import os
from flask import Flask
from modele_bdd import db

# Attention : se placer dans le dossier app pour tester le programme
# Si base déjà créé : supprimer la base en question pour éviter le moindre problème dans la création de table si modif au niveau des colonnes/tables

# Lancement de l'application (pour le moment que la BDD)
app = Flask(__name__)

# ---- Configuration de la BDD ----
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///films.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# ---- Test provisoire sur la création du BDD ----
db.init_app(app)

if not(os.path.exists("instance/films.db")):
    with app.app_context():
        db.drop_all()
        db.create_all()
