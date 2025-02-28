#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 27/02/2025
# Sujet : test d'un outil décsionnel (directeur)
#################################################

import pytest
from modele_bdd import Directeur

####<TEST-STRT>----------------------------------
def test_creer_directeur():
    directeur = Directeur(id=1, nom='Spielberg', prenom='Steven')

    assert directeur.id == 1
    assert directeur.nom == 'Spielberg'
    assert directeur.prenom == 'Steven'
    assert directeur.films.all() == []
####<TEST-END>-----------------------------------

