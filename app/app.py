#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024
# Sujet : création d'une application web (lanceur)
#################################################

# Chargement des librairies
import os
from config import app
from modele_bdd import db, Genre, Film, Directeur, Language, Company, Acteur, Collection, film_languages, film_genres # Toutes les tables et relations
from requete_utl import inf_film_10, req_joint_par_crit, mise_forme_resultats_graph, \
                        films_par_genre, films_par_annee, films_par_langue, top_10_mieux_notes, \
                        top_10_plus_cher, top_10_plus_court, top_10_plus_deficit, top_10_plus_long, top_10_plus_populaires, \
                        top_10_plus_rentables, top_10_plus_votes, total_budget_recette, annee_plus_productive, max_films_genre, \
                        top_10_realisateur, rech_films, rech_genres

from formulaire_real import RealForm, TitGenForm
from sqlalchemy.sql import insert
import datetime
from flask import render_template, jsonify, flash, redirect, url_for, session
from config import app
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# Attention : se placer dans le dossier app pour tester le programme
# Si base déjà créée : supprimer la base en question pour éviter le moindre problème dans la création de table si modif au niveau des colonnes/tables

# ---- Test provisoire sur la création du BDD ----
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

#___________________________________________________________________ #
# Chargement des données préparées.
def run_notebook(notebook_path, timeout=600):
    """
    Executes a Jupyter notebook and returns its namespace.
    
    :param notebook_path: Path to the Jupyter notebook file.
    :param timeout: Timeout in seconds for each cell execution.
    :return: A dictionary containing the global variables and functions from the notebook.
    """
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    # Configure the execution
    ep = ExecutePreprocessor(timeout=timeout, kernel_name='python3')

    # Create a namespace to capture global variables/functions
    namespace = {}

    # Execute the notebook
    try:
        ep.preprocess(notebook, {'metadata': {'path': './'}})
        # Extract all code cells and execute them in the namespace
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                exec(cell.source, namespace)
    except Exception as e:
        print(f"Error executing the notebook: {e}")

    return namespace

namespace = run_notebook("./explo.ipynb")

#_______________________ Access data __________________________________ #
film = namespace["film"]
genre = namespace["list_genre"]
collection = namespace["list_collection"]
languages = namespace["list_languages"]
production = namespace["list_production"]
actor = namespace["list_actors"]
director = namespace["list_directors"]
# --------------------------------------------------------------------- #

# Insert collection into the db
with app.app_context():
    for index, row in collection.iterrows():
        collection = Collection(name=row["belongs_to_collection"])
        db.session.add(collection)
    db.session.commit()
    print("Collections data inserted successfully!")

# Insert actors into the db
with app.app_context():
    for index, row in actor.iterrows():
        actor = Acteur(
            nom=row["lastname"], 
            prenom=row["firstname"], 
        )
        db.session.add(actor)
    db.session.commit()
    print("Actors successfully added.")


# Insert directors into the db 
with app.app_context():
    for index, row in director.iterrows():
        director = Directeur(nom=row["lastname"], prenom=row["firstname"])
        db.session.add(director)
    db.session.commit()
    print("Directors successfully added.")

    
# Insert genres into the db
with app.app_context():
    for index, row in genre.iterrows():
        genss = Genre(genre = row["genres"])
        db.session.add(genss)
    db.session.commit()
    print("Genre successfully added.")
    
# Insert production companies
with app.app_context():
    for index, row in production.iterrows():
        companyss = Company(name = row["production_companies"])
        db.session.add(companyss)
    db.session.commit()
    print("Companies added.") 
    
    
# Insert original languages
with app.app_context():
    for index, row in languages.iterrows():
        langss = Language(language = row["spoken_languages"])
        db.session.add(langss)
    db.session.commit()
    print("Languages added.") 
