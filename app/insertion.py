#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024 - 14/12/2024
# Sujet : insertion des données dans le BDD après préparation
#################################################

# Chargement des librairies
import pandas as pd
import os
from tqdm import tqdm
import explo as ex

# Initialiser la BDD (si lancé ici)
if __name__=="__main__":
    from config import app
    from modele_bdd import db
    from sqlalchemy import insert
    db.init_app(app)

def creation_insertion_bdd(inst_app, inst_db):

    """
    Fonction : permet d'insérer les données dans notre BDD avec nos DataFrames préparés (expo.py)

    Arguments :  
    - inst_app : instance de l'application lancé par Flask(__name__)
    - inst_db : instance de connexion à la BDD SQLite

    Retour : 
    Insertion des données dans le BDD SQLite.
    """
    
    # Importation des différentes classes BDD
    from modele_bdd import Genre, Film, Directeur, Language, Company, Acteur, Collection, film_languages, film_genres, film_companies, film_acteurs

    # Création des BDD
    print("Création de la BDD SQLite films.db :")
    with inst_app.app_context():
            inst_db.drop_all()
            inst_db.create_all()
    print("Création réussie")

    # Insert collection into the db
    print("Insertion dans la table Collection :")
    with tqdm(total=ex.list_collection.shape[0]) as bar:
        with inst_app.app_context():
                for index, row in ex.list_collection.iterrows():
                    collection = Collection(name=row["belongs_to_collection"], id=row["id_cle"])
                    inst_db.session.add(collection)

                    # Avancement de la barre de progression
                    bar.update(1)

                inst_db.session.commit()
    print("Collections data inserted successfully!")

    # Insert actors into the db
    print("Insertion dans la table Acteur :")
    with tqdm(total=ex.list_actors.shape[0]) as bar:
        with inst_app.app_context():
            for index, row in ex.list_actors.iterrows():

                actor = Acteur(
                    nom=row["lastname"], 
                    prenom=row["firstname"], 
                    id=row["id_cle"]
                )
                inst_db.session.add(actor)
                
                # Avancement de la barre de progression
                bar.update(1)

            inst_db.session.commit()
    print("Actors successfully added.")


    # Insert directors into the db 
    print("Insertion dans la table Directeur :")
    with tqdm(total=ex.list_directors.shape[0]) as bar:
        with inst_app.app_context():
                for index, row in ex.list_directors.iterrows():

                    director = Directeur(nom=row["lastname"], 
                                        prenom=row["firstname"],
                                        id=row["id_cle"])
                    inst_db.session.add(director)

                    # Avancement de la barre de progression
                    bar.update(1)

                inst_db.session.commit()
    print("Directors successfully added.")

            
    # Insert genres into the db
    print("Insertion dans la table Genre :")
    with tqdm(total=ex.list_genre.shape[0]) as bar:
        with inst_app.app_context():
                
                for index, row in ex.list_genre.iterrows():
                    genss = Genre(genre = row["genres"],
                                id=row["id_cle"])
                    inst_db.session.add(genss)

                    # Avancement de la barre de progression
                    bar.update(1)

                inst_db.session.commit()
    print("Genre successfully added.")
            
    # Insert production companies
    print("Insertion dans la table Company :")
    with tqdm(total=ex.list_production.shape[0]) as bar:
        with inst_app.app_context():
                for index, row in ex.list_production.iterrows():
                    companyss = Company(name = row["production_companies"],
                                        id=row["id_cle"])
                    inst_db.session.add(companyss)

                    # Avancement de la barre de progression
                    bar.update(1)

                inst_db.session.commit()
    print("Companies added.") 
            
            
    # Insert languages
    print("Insertion dans la table Language :")
    with tqdm(total=ex.list_languages.shape[0]) as bar:
        with inst_app.app_context():
                for index, row in ex.list_languages.iterrows():
                    langss = Language(language = row["language"],
                                    id=row["id_cle"])
                    inst_db.session.add(langss)

                    # Avancement de la barre de progression
                    bar.update(1)

                inst_db.session.commit()
    print("Languages added.") 

    # Insert Films
    print("Insertion dans la table Film :")
    with tqdm(total=ex.dataset.shape[0]) as bar:
        with inst_app.app_context():
            for index, row in ex.dataset.iterrows():
                    film_data = Film()
                    film_data.id = row["id"]
                    film_data.title = row["title"]
                    film_data.release_date = row["release_date"] if not pd.isna(row["release_date"]) else None
                    film_data.popularity = row["popularity"]
                    film_data.runtime = row["runtime"]
                    film_data.budget = row["budget_musd"] if not pd.isna(row["budget_musd"]) else 0
                    film_data.revenue = row["revenue_musd"] if not pd.isna(row["revenue_musd"]) else 0
                    film_data.tagline = row["tagline"] if not pd.isna(row["tagline"]) else None
                    film_data.overwiew = row["overview"] if not pd.isna(row["overview"]) else None
                    film_data.poster_path = row["poster"]
                    film_data.vote_count = row["vote_count"]
                    film_data.vote_average = row["vote_average"]
                    film_data.id_original_language = row["id_cle"]
                    film_data.id_directeur = row['id_cle_dir']
                    film_data.id_collection = row["id_cle_coll"]


                    # initialiser les clé étragères : film.fk = orig_lang.id    
                    inst_db.session.add(film_data)
                    bar.update(1)

            inst_db.session.commit()
    print("Films successfully added.")

    # Insertion des tables d'associations
    # Pour la table film_genres
    print("Insertion dans la table film_genre :")
    with tqdm(total=ex.genre.shape[0]) as bar:
        with inst_app.app_context():
            for index, row in ex.genre.iterrows():
                inst_db.session.execute(film_genres.insert().values(id_film=row["id"], id_genres=row["id_cle"]))
                bar.update(1)
            inst_db.session.commit()
    print("Films and Genre successfully added.")

    # Pour la table film_companies
    print("Insertion dans la table film_companies :")
    with tqdm(total=ex.production.shape[0]) as bar:
        with inst_app.app_context():
            for index, row in ex.production.iterrows():
                inst_db.session.execute(film_companies.insert().values(id_film=row["id"], id_companies=row["id_cle"]))
                bar.update(1)
            inst_db.session.commit()
    print("Films and Company successfully added.")

    # Pour la table film_languages
    print("Insertion dans la table film_languages :")
    with tqdm(total=ex.liste_df_language[1].shape[0]) as bar:
        with inst_app.app_context():
            for index, row in ex.liste_df_language[1].iterrows():
                inst_db.session.execute(film_languages.insert().values(id_film=row["id"], id_language=row["id_cle"]))
                bar.update(1)
            inst_db.session.commit()
    print("Films and Language successfully added.")

    # Pour la table film_acteurs
    print("Insertion dans la table film_acteurs :")
    with tqdm(total=ex.actor.shape[0]) as bar:
        with inst_app.app_context():
            for index, row in ex.actor.iterrows():
                inst_db.session.execute(film_acteurs.insert().values(id_film=row["id"], id_acteur=row["id_cle"]))
                bar.update(1)
            inst_db.session.commit()
    print("Films and Actors successfully added.")

# Si lancé dans l'emplacement de ce fichier
if __name__=="__main__":
    creation_insertion_bdd(app, db)