from flask.testing import FlaskClient
from modele_bdd import Collection

def test_film_attributes(exemple_film):
    """Test that the Film instance has correct attributes."""
    assert exemple_film.title == "Wakfu le film"
    assert exemple_film.release_date.year == 2012
    assert exemple_film.budget == 15.5
    assert exemple_film.id_collection == 2


def test_collection_json_avec_films(client: FlaskClient):
    pass