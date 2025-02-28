#################################################
# Auteurs : Julien RENOULT
# Date : 28/02/2025
# Sujet : test d'un outil décsionnel (film)
#################################################

from modele_bdd import Film
from app import db

def test_crud_film(client, exemple_film):
    
    # Vérification de la non existence de la base de données
    assert Film.query.filter_by(title=exemple_film.title).first() is None

    # Persister dans la base de données
    db.session.add(exemple_film)
    db.session.commit()

    # Récupérer le film ajouté
    film = Film.query.filter_by(title=exemple_film.title).first()
    
    # Vérification qu'il existe après persistence
    assert film is not None

    # Modification dans la base de données
    film.title = "Wakfu et la quête des six dofus"
    db.session.commit()

    # Vérification que ça a bien été modifié dans la base de données
    assert film.title == "Wakfu et la quête des six dofus"

    # Suppression dans la base de données
    db.session.delete(film)
    db.session.commit()

    # Vérification que ça a bien été supprimé
    assert Film.query.filter_by(title=exemple_film.title).first() is None

#def test_relationship_film(client, exemple_film):
    
#    # Tester 