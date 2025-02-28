#################################################
# Auteurs : Julien RENOULT
# Date : 28/02/2025
# Sujet : test d'un outil décsionnel (film)
#################################################

from modele_bdd import Film
from app import db

def test_crud_film(client, exemple_film):
    """
    Fonction : Test d'intégration sur les opérations CRUD (Create, Read, Update et Delete)

    Arguments :
    - client : l'instance client pour interagir avec l'application web et la BDD SQLite
    - exemple_film : exemple d'instance de film

    """
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

def test_relationship_film(client, exemple_film, 
                           acteur, directeur,
                           exemple_langue,
                           collection, exemple_genre,
                           exemple_company):
    """
    Fonction : Test d'intégration sur les relations entre les différentes tables

    Arguments : 
    - client : l'instance client pour interagir avec l'application web et la BDD SQLite
    - exemple_film : exemple d'instance de film
    - acteur : exemple d'instance d'acteur
    - directeur : exemple d'instance de directeur
    - exemple_langue : exemple d'instance de langue
    - collection : exemple d'instance de collection
    - exemple_genre : exemple d'instance de genre
    - exemple_company : exemple d'instance d'un studio de production
    
    """

    # Tester les relations entre films et les autres tables
    # 1ère étape : Insertion dans la Base de données avec la relation
    # Ajout des instances 
    db.session.add(exemple_film)
    db.session.add(acteur)
    db.session.add(exemple_langue)
    db.session.add(exemple_company)
    db.session.add(exemple_genre)
    db.session.add(directeur)
    db.session.add(collection)
    db.session.commit() 

    # Ajout des relations * à * (ceux de 1 à * sont déjà insérés avec les id)
    exemple_film.acteurs.append(acteur)
    exemple_film.companies.append(exemple_company)
    exemple_film.genres.append(exemple_genre)
    exemple_film.languages.append(exemple_langue)
    db.session.commit()

    # Test des relations entre le film et les différentes tables
    assert len(exemple_film.acteurs) > 0
    assert exemple_film.acteurs[0].name == "Todd" and \
    exemple_film.acteurs[0].prenom == "Jean"

    assert len(exemple_film.companies) > 0
    assert exemple_film.companies[0].name == "Ankama Animations"
    




