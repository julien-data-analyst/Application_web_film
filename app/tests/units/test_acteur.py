#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 27/02/2025
# Sujet : test d'un outil décsionnel (directeur)
#################################################

 
from modele_bdd import Collection ,Acteur , Directeur #import to instantiate the Collection



def test_creer_acteur (acteur):
    assert acteur.id == 1
    assert acteur.nom == 'Todd'
    assert acteur.prenom == 'Jean'
    