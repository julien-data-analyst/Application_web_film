import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modele_bdd import db, Film, Acteur, film_acteurs

@pytest.fixture
def test_db():
    """Créer une base de données SQLite en mémoire pour les tests."""
    engine = create_engine("sqlite:///:memory:")
    db.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()

    yield session  
    session.close() 
def test_film_actor_relationship(test_db):
    """Vérifie que la relation entre un film et un acteur est bien enregistrée."""
    
    # Création d'un film
    film = Film(id=1, title="Inception", release_date="2010-07-16")
    test_db.add(film)
    
    # Création d'un acteur
    actor = Acteur(id=1, nom="DiCaprio", prenom="Leonardo")
    test_db.add(actor)
    
    # Liaison du film et de l'acteur dans la table d'association
    test_db.execute(film_acteurs.insert().values(id_film=film.id, id_acteur=actor.id))
    
    # Commit des changements
    test_db.commit()

    # Vérification que l'association existe
    result = test_db.execute(film_acteurs.select().where(film_acteurs.c.id_film == film.id)).fetchall()
    assert len(result) == 1
    assert result[0].id_acteur == actor.id
