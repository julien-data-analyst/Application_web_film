from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
import pytest
from modele_bdd import Collection, Film

# CRUD and relation testing for Collection

def test_create_read_collection(client: FlaskClient, collection: Collection, test_db: SQLAlchemy):
    """Test creating and retrieving a Collection using test_db."""

    test_db.session.add(collection)
    test_db.session.commit()

    retrieved_collection = test_db.session.get(Collection, 1)
    assert retrieved_collection is not None
    assert retrieved_collection.name == "Test collection"

def test_update_collection(client: FlaskClient, test_db: SQLAlchemy, collection: Collection):
    """Test updating a Collection name."""
    test_db.session.add(collection)
    test_db.session.commit()

    collection.name = "Updated Collection Name"
    test_db.session.commit()

    updated_collection = test_db.session.get(Collection, collection.id)
    assert updated_collection.name == "Updated Collection Name"

def test_delete_collection(client: FlaskClient, test_db: SQLAlchemy, collection: Collection):
    """Test deleting a Collection from the database."""
    test_db.session.add(collection)
    test_db.session.commit()

    test_db.session.delete(collection)
    test_db.session.commit()

    deleted_collection = test_db.session.get(Collection, collection.id)
    assert deleted_collection is None

def test_collection_with_films(client, test_db, collection, exemple_film):
    """Test that a Collection can contain multiple films using the fixture."""
    
    # Create scond movie
    film2 = Film(
        id=2,
        title="Film Two",
        release_date=exemple_film.release_date,  
        popularity=exemple_film.popularity,
        runtime=exemple_film.runtime,
        budget=exemple_film.budget,
        revenue=exemple_film.revenue,
        tagline="Second Film Tagline",
        overwiew="This is the second film in the collection.",
        poster_path=exemple_film.poster_path,
        vote_count=exemple_film.vote_count,
        vote_average=exemple_film.vote_average,
        id_directeur=exemple_film.id_directeur,
        id_collection=collection.id, 
        id_original_language=exemple_film.id_original_language
    )

    # First film also belongs to the collection
    exemple_film.id_collection = collection.id

    # Add films and collection to the db
    test_db.session.add_all([collection, exemple_film, film2])
    test_db.session.commit()

    # get collection from the database
    retrieved_collection = test_db.session.get(Collection, collection.id)

    # Assertions
    assert retrieved_collection is not None
    assert len(retrieved_collection.films.all()) == 2
    assert {film.title for film in retrieved_collection.films} == {"Wakfu le film", "Film Two"}