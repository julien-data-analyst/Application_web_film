#[ NOTE ]# [A: dobigny ryan] pytest .\tests\systeme\test_director.py -v --capture=no

import pytest
import datetime
from app import *
from modele_bdd import db, Directeur, Film, Language

####<TEST-STRT>----------------------------------
def test_aff_film(client):
    directeur = Directeur(nom='Spielberg', prenom='Steven')
    db.session.add(directeur)
    db.session.commit()

    film = Film(id=1, title="Wakfu le film", release_date=datetime.datetime(2012, 2, 14), popularity=1, runtime=120, budget=15.5, revenue=30.5, tagline="Quête des six dofus",
        overwiew = "Deux cents ans ont passé depuis le grand déluge qui a mis fin à l'Âge des Dofus…",
        poster_path="", vote_count=50000, vote_average=4.253, id_directeur=1, id_collection=2, id_original_language=3
    )
    db.session.add(film)
    db.session.commit()
    
    rep = client.get("/films_realisateur/1")
    html_page = rep.data.decode("utf-8")

    assert rep.status_code == 200

'''
def test_get_films_par_langue(client):
    film = Film(id=1, title="Wakfu le film", release_date=datetime.datetime(2012, 2, 14), popularity=1, runtime=120, budget=15.5, revenue=30.5, tagline="Quête des six dofus",
        overwiew = "Deux cents ans ont passé depuis le grand déluge qui a mis fin à l'Âge des Dofus…",
        poster_path="", vote_count=50000, vote_average=4.253, id_directeur=1, id_collection=2, id_original_language=3
    )
    db.session.add(film)
    db.session.commit()

    langage = Language(language='english')
    db.session.add(langage)
    db.session.commit()

    rep = client.get(f'/api/data/films_par_langue')
    assert rep.status_code == 200
'''
####<TEST-END>-----------------------------------

