#####################-
# Auteur : # Auteurs : Gabriel DURAND - Ryan DOBIGNY - Julien RENOULT - Yop JUGUL DALYOP 
# Promo : BUT SD3 
# Sujet : Test d'application 
# Création des fixtures
#####################-

import pytest
from app import app, db
import datetime
from modele_bdd import Film, Language, Collection, \
    Acteur , Directeur, Company, Genre #import to instantiate the Collection


@pytest.fixture
def test_db():
    """Provide a clean database session for each test without requiring app import."""
    with app.app_context():  # Ensure we are in a Flask app context
        db.create_all()  # Create tables in the test database
        yield db  # Provide the db session to tests
        db.session.remove()
        db.drop_all()  # Clean up after tests



@pytest.fixture
def client():
     """
     Fonction : permet de créer un client TEST pour l'application Flask.
     """
     # Activer le mode TESTING DE FLASK
     # C'est pas Flask qui gère les tests
     app.config["TESTING"] = True

     # Définir le chemin vers la base de données
     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
     # :memory: créée temporairement la base de données
     # pas obligatoire avec TESTING = True

     # Contexte d'application
     with app.app_context():
         # Créer toutes les bases de données
         # Obligé car la base de données sera supprimée après le test
         db.create_all()

         # Utilisation de yield (exécuter le test avant de supprimer la base de données et nettoyer après le test)
         yield app.test_client()

         # Enlever la session actuelle après que le test soit finie
         db.session.remove()

         # Nettoyer la session (supprimer BDD)
         db.drop_all()

@pytest.fixture
def exemple_film():
    """
    Fonction : permet de créer une instance de film
    """
    # Création d'une instance de film 
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
        id_collection=1,
        id_original_language=3
    )
    return film

@pytest.fixture 
def exemple_langue():
    """
    Fonction : création d'une instance de langue
    """
    lang = Language(
        id=3,
        langage = "Français")
    
    return lang

@pytest.fixture
def exemple_genre():
    """
    Fonction : création d'une instance de genre
    """
    genre = Genre(
        id=1,
        genre="Action"
    )

@pytest.fixture
def exemple_company():
    """
    Fonction : création d'une instance de Company
    """

    comp = Company(id=1,
                   name="Ankama Animations")
    
    return comp

@pytest.fixture
def collection():
    """
    Fixture for collection. 
    A collection has an id and a name.
    """
    collection = Collection(id=1, name="Test collection")
    return collection





@pytest.fixture
def acteur():
    """
    Fixture for Acteur. 
    A Acteur has an id and a name and a prenom.
    """
    acteur = Acteur(id=1, nom="Todd",prenom ='Jean')
    return  acteur 

@pytest.fixture
def directeur():
    """
    Fixture for Acteur. 
    A Acteur has an id and a name and a prenom.
    """
    directeur = Directeur(id=1, nom="Inthekitchen",prenom ='Bryan')
    return  directeur 


