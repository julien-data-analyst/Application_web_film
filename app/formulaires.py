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
    """
    Classe : crée un formulaire de recherche des réalisateurs

    Inputs :
    - Champ de texte  : StringField (nom_real)
    - Champ d'envoie des informations : SubmitField (envoyer)

    """

    # Création de la barre de recherche pour le nom du réalisateur
    nom_real = StringField(label="Nom du réalisateur : ",
              validators = [DataRequired(message="Veuillez saisir un nom !!!")])

    # Création du bouton rechercher
    envoyer = SubmitField(label="Rechercher")

# Création du formulaire de recherche de genre/titre 
class TitGenForm(FlaskForm):
    """
    Classe : crée un formulaire de recherche des films selon le genre/titre

    Inputs :
    - Champ de boutons : RadioField (type)
    - Champ de texte  : StringField (word)
    - Champ d'envoie des informations : SubmitField (envoyer)
    
    """

    # Création des différents blocs de formulaires
    type = RadioField('Recherche par : ', choices=["Genre", "Titre"], validators = [DataRequired()]) 
    word = StringField('Insérez ici : ', validators = [DataRequired()])

    # Création du bouton rechercher
    envoyer = SubmitField('Rechercher') 