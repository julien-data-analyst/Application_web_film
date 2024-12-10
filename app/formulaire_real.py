#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 09/12/2024
# Sujet : création du formulaire de recherche pour les directeurs (WTFForms)
#################################################

from wtforms import (StringField, SubmitField, RadioField) # Les différents inputs
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

# Création du formulaire de recherche de réalisateur
class RealForm(FlaskForm):

    # Création de la barre de recherche pour le nom du réalisateur
    nom_real = StringField(label="Nom du réalisateur : ",
              validators = [DataRequired(message="Veuillez saisir un nom !!!")])

    # Création du bouton rechercher
    envoyer = SubmitField(label="Chercher")

# Création du formulaire de recherche de genre/titre 
class TitGenForm(FlaskForm):

    # Création des différents blocs de formulaires
    type = RadioField('Recherche par : ', choices=["Genre", "Titre / Mot(s) clé(s)"], validators = [DataRequired()]) 
    word = StringField('Insérez ici : ', validators = [DataRequired()])

    find = SubmitField('Rechercher') 