#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 06/12/2024
# Sujet : Configuration de la BDD et de l'application web
#################################################

# Chargement des librairies 
from flask import Flask ,request , render_template
import secrets

# Lancement de l'application (pour le moment que la BDD)
app = Flask(__name__)

# ---- Configuration de la BDD ----
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///films.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# ---- Configuration de la clé secrète
app.config["SECRET_KEY"] = secrets.token_hex(16) # aléatoire
