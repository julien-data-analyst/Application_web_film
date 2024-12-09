#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 09/12/2024
# Sujet : création du formulaire de recherche pour les directeurs (WTFForms)
#################################################

from wtforms import (StringField, SubmitField) # Les différents inputs
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

# Création du formulaire 
class FormulaireRealisateur(FlaskForm):

    # Création de la barre de recherche pour le nom du réalisateur
    nom_pre = StringField(label="Nom du réalisateur : ",
              validators = [DataRequired(message="Saisir NOM Prénom Valide !!!")])

    # Création du bouton rechercher
    envoyer = SubmitField(label="Chercher")