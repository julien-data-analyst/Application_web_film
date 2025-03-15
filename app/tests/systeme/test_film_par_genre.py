# By: Dalyop Yop
# BUT 3 SD VCOD 
import pytest
from app import app, db
import datetime
from modele_bdd import Film,  Genre



def test_films_par_genre(client, exemples_films, exemple_genre):
    """
    Test that the films are properly displayed for a specific genre.
    """

    # Add genre to the database
    db.session.add(exemple_genre)
    db.session.commit()

    # Add the genre to each film and commit
    for film in exemples_films:
        # Associate the genre with the film through the association table
        film.genres.append(exemple_genre)
        db.session.add(film)  # Explicitly add the film to the session

    db.session.commit()  # Ensure changes are saved to the database

    # Request the API for films filtered by genre
    genre_id = exemple_genre.id
    rep = client.get(f"/api/data/films_par_genre?genre={genre_id}")

    # Verify response status
    assert rep.status_code == 200

    # Parse the JSON response
    response_data = rep.json

    # Ensure the response contains either 'mod' or 'eff'
    assert isinstance(response_data, dict), f"Expected response_data to be a dictionary, but got {type(response_data)}"
    assert 'mod' in response_data or 'eff' in response_data, "Response does not contain expected keys ('mod' or 'eff')"

    # Extract films data from the correct key (either 'mod' or 'eff')
    films_data = response_data.get('mod', []) or response_data.get('eff', [])

    # Check if films_data is a list
    assert isinstance(films_data, list), f"Expected films_data to be a list, but got {type(films_data)}"

    # Create a list of film titles from the response (assuming they are just strings)
    film_titles_from_response = [film.strip() for film in films_data]

    # Ensure no films from other genres appear (if any other genres exist)
    other_genre_films = Film.query.filter(Film.genres.any(Genre.id != exemple_genre.id)).all()

    # Ensure that no films from other genres appear in the genre list
    for other_film in other_genre_films:
        assert other_film.title.strip() not in film_titles_from_response, f"Film '{other_film.title}' appeared in the '{exemple_genre.genre}' genre!"
