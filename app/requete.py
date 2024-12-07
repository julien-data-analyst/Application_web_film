#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024
# Sujet : requête SQL pour les visualisations graphiques + indicateurs 
#################################################

from modele_bdd import db, Genre, Film, Directeur, Langage
from config import app
import os 

# Attention : se placer dans le dossier app pour tester le programme
# Si base déjà créée : supprimer la base en question pour éviter le moindre problème dans la création de table si modif au niveau des colonnes/tables

# ---- Test provisoire sur la création du BDD ----
db.init_app(app)

# ---- Préparation des différentes requêtes SQL ----
# cmd.produits.extend(prod_sel) # Ajout des produits sélecitonnées (liste des classes)
with app.app_context():

    db.drop_all()
    db.create_all()

    new_genre = Genre(genre="drama")
    new_langage = Langage(langage="French")
    new_dir = Directeur(nom="Dir", prenom='Dir')
    db.session.add_all([new_langage, new_genre, new_dir])
    db.session.commit()


    #print(Genre.query.first().films)
    #print(Directeur.query.first().films)


