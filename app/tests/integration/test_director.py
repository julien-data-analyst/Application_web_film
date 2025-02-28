#[ NOTE ]# [A: dobigny ryan] pytest .\tests\integration\test_director.py -v --capture=no

import pytest
import datetime
from modele_bdd import db, Directeur, Film

####<TEST-STRT>----------------------------------
def test_creer_directeur_sans_films(client):
    directeur = Directeur(nom='Spielberg', prenom='Steven')
    db.session.add(directeur)
    db.session.commit()
    directeur = Directeur.query.filter_by(nom=directeur.nom).first()
    
    assert directeur is not None, 'un directeur doit exister !'
    assert directeur.films.all() == [], 'normalement égal à 0 !'


def test_crud_directeur(client):
    directeur = Directeur.query.get(1)
    assert directeur is None, 'le directeur ne doit pas exister !'

    #CREATION
    directeur = Directeur(nom='Spielberg', prenom='Steven')
    db.session.add(directeur)
    db.session.commit()
    directeur = Directeur.query.get(1)

    assert directeur is not None, 'un directeur doit exister !'
    
    #LECTURE
    directeur = Directeur.query.get(1)
    assert directeur.nom == 'Spielberg'
    assert directeur.prenom == 'Steven'
    assert directeur.films.all() == []

    #MAJ
    directeur.nom = 'Nolan'
    directeur.prenom = 'Christopher'
    db.session.commit()

    #LECTURE -second-
    directeur = Directeur.query.get(1)
    assert directeur.nom == 'Nolan'
    assert directeur.prenom == 'Christopher'
    assert directeur.films.all() == []
    
    #SUPPR
    db.session.delete(directeur)
    db.session.commit()

    #LECTURE -final-
    directeur = Directeur.query.get(1)
    assert directeur is None, 'le directeur ne doit pas exister !'


def test_relation_avec_films(client):
    directeur = Directeur(nom='Spielberg', prenom='Steven')
    db.session.add(directeur)
    db.session.commit()
    directeur = Directeur.query.get(1)

    film = Film(id=1, title="Wakfu le film", release_date=datetime.datetime(2012, 2, 14), popularity=1, runtime=120, budget=15.5, revenue=30.5, tagline="Quête des six dofus",
        overwiew = "Deux cents ans ont passé depuis le grand déluge qui a mis fin à l'Âge des Dofus…",
        poster_path="", vote_count=50000, vote_average=4.253, id_directeur=1, id_collection=2, id_original_language=3
    )
    db.session.add(film)
    db.session.commit()

    assert directeur.films.count() == 1
    assert directeur.films.first().title == "Wakfu le film"
####<TEST-END>-----------------------------------

