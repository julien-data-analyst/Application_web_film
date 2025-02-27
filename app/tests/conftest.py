#####################-
# Auteur : # Auteurs : Gabriel DURAND - Ryan DOBIGNY - Julien RENOULT - Yop JUGUL DALYOP 
# Promo : BUT SD3 
# Sujet : Test d'application 
# Création des fixtures
#####################-

import pytest
from app import app, db
from modele_bdd import Film 
from modele_bdd import Collection #import to instantiate the Collection

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
def collection():
    """
    Fixture for collection. 
    A collection has an id and a name.
    """
    collection = Collection(id=1, name="Test collection")
    return collection