#[ NOTE ]# [A: dobigny ryan] pytest .\tests\units\test_director.py -v --capture=no

import pytest
from modele_bdd import Directeur

####<TEST-STRT>----------------------------------
def test_creer_directeur():
    directeur = Directeur(nom='Spielberg', prenom='Steven')

    assert directeur.nom == 'Spielberg'
    assert directeur.prenom == 'Steven'
    assert directeur.films.all() == []
####<TEST-END>-----------------------------------

