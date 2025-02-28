#################################################
# Auteurs : Julien RENOULT
# Date : 27/02/2025
# Sujet : test d'un outil décsionnel (film)
#################################################

import pytest
from modele_bdd import Film

import datetime

# Test de la table Film #########################
def test_attribut_film():
    """
    Fonction : test de la saisie d'instance du film
    """

    film = Film(
        id=1,
        title="Wakfu le film",
        release_date=datetime.datetime(2012, 2, 14),
        popularity=1,
        runtime=120,
        budget=15.5,
        revenue=30.5,
        tagline="Quête des six dofus",
        overwiew = """Deux cents ans ont passé depuis le grand déluge qui a mis fin à l'Âge des Dofus et transformé 
        les continents de l'époque en archipels. Les eaux montent, la nature devient folle. 
        Des choses se sont passées, d'autres se sont terminés, 
        mais le Wakfu, l'énergie primordiale créatrice du monde 
        est fortement perturbée par un être mystérieux. Sur une petite île au large de la nation d'Amakna, se trouve un petit village perdu dans la forêt : Emelka. 
        Dans ce petit village, démarrent les épopées d'un jeune garçon du nom de Yugo, qui vient de découvrir ses pouvoirs, mais aussi ses origines""",
        poster_path="http://image.tmdb.org/t/p/w185//ojDg0PGvs6R9xYFodRct2kdI6wC.jpg",
        vote_count=50000,
        vote_average=4.253,
        id_directeur=1,
        id_collection=2,
        id_original_language=3
    )


    # Les tests au niveau des attributs associés
    ################
    assert film.title == "Wakfu le film"
    assert film.id == 1
    assert film.release_date == datetime.datetime(2012, 2, 14)
    assert film.popularity == 1
    assert film.runtime == 120
    assert film.budget == 15.5
    assert film.tagline == "Quête des six dofus"
    assert film.id_directeur == 1
    assert film.id_collection == 2
    assert film.id_original_language == 3
    assert film.overwiew == """Deux cents ans ont passé depuis le grand déluge qui a mis fin à l'Âge des Dofus et transformé 
        les continents de l'époque en archipels. Les eaux montent, la nature devient folle. 
        Des choses se sont passées, d'autres se sont terminés, 
        mais le Wakfu, l'énergie primordiale créatrice du monde 
        est fortement perturbée par un être mystérieux. Sur une petite île au large de la nation d'Amakna, se trouve un petit village perdu dans la forêt : Emelka. 
        Dans ce petit village, démarrent les épopées d'un jeune garçon du nom de Yugo, qui vient de découvrir ses pouvoirs, mais aussi ses origines"""
    assert film.poster_path == "http://image.tmdb.org/t/p/w185//ojDg0PGvs6R9xYFodRct2kdI6wC.jpg"
    assert film.vote_average == 4.253
    assert film.vote_count == 50000
    ################

    # Les tests au niveau des relations (* à *, 1 à *)
    #################
    assert film.companies.all() == []
    assert film.genres.all() == []
    assert film.languages.all() == []
    assert film.acteurs.all() == []
    assert film.collection == None
    assert film.directeur == None
    assert film.language_org == None
    #################
#################################################
