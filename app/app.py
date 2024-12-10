#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024
# Sujet : création d'une application web (lanceur)
#################################################

# Chargement des librairies
import os
from config import app
from modele_bdd import db, Genre, Film, Directeur, Language, Company, Acteur, Collection, film_languages, film_genres, film_companies, film_directeurs

# Toutes les tables et relations
from requete_utl import inf_film_10, req_joint_par_crit, mise_forme_resultats_graph, \
                        films_par_genre, films_par_annee, films_par_langue, top_10_mieux_notes, \
                        top_10_plus_cher, top_10_plus_court, top_10_plus_deficit, top_10_plus_long, top_10_plus_populaires, \
                        top_10_plus_rentables, top_10_plus_votes, total_budget_recette, annee_plus_productive, max_films_genre, \
                        top_10_realisateur, rech_films, rech_genres

from formulaire_real import RealForm, TitGenForm
from sqlalchemy.sql import insert
import datetime
from flask import render_template, jsonify, flash, redirect, url_for, session
import pandas as pd
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# Attention : se placer dans le dossier app pour tester le programme
# Si base déjà créée : supprimer la base en question pour éviter le moindre problème dans la création de table si modif au niveau des colonnes/tables

@app.route('/inf', methods=["GET", "POST"])
def informations():

    # Application des différentes requêtes SQL pour récupérer les informations

    # ---- Les indicateurs ----
    annee_plus_prod = annee_plus_productive()
    total_budg_rec = total_budget_recette()
    genre_max = max_films_genre()
    
    # ---- Les top 10 ----
    r_top_10_mieux_notes = top_10_mieux_notes()
    r_top_10_plus_votes = top_10_plus_votes()
    r_top_10_plus_populaires = top_10_plus_populaires()
    r_top_10_plus_cher = top_10_plus_cher()
    r_top_10_plus_long = top_10_plus_long()
    r_top_10_plus_court = top_10_plus_court()
    r_top_10_plus_deficit = top_10_plus_deficit()
    r_top_10_plus_rentable = top_10_plus_rentables()
    r_top_10_real_film = top_10_realisateur()

    return render_template("page_test_req.html",
                           annee_plus_prod = annee_plus_prod,
                           total_budg_rec = total_budg_rec,
                           genre_max = genre_max,
                           r_top_10_mieux_notes =  r_top_10_mieux_notes,
                           r_top_10_plus_cher = r_top_10_plus_cher,
                           r_top_10_plus_court = r_top_10_plus_court,
                           r_top_10_plus_long = r_top_10_plus_long,
                           r_top_10_plus_deficit = r_top_10_plus_deficit,
                           r_top_10_plus_votes = r_top_10_plus_votes,
                           r_top_10_plus_populaires = r_top_10_plus_populaires,
                           r_top_10_plus_rentable = r_top_10_plus_rentable,
                           r_top_10_real_film = r_top_10_real_film # [(nom_directeur, prenom_directeur, effectif)]
                           )

#################################
# Création de la page du formulaire pour la recherche de réalisateur
#################################
@app.route('/rech_real', methods=["GET", "POST"])
def recherche_realisateur():
    # Pour le formulaire
    form = RealForm()

    # ---- Les top 10 ----
    r_top_10_mieux_notes = top_10_mieux_notes()
    r_top_10_plus_populaires = top_10_plus_populaires()
    r_top_10_real_film = top_10_realisateur()
    reals=[]

    if form.validate_on_submit():
        # Récupération de la recherche de l'utilisateur après validation de la demande
        nom_real = form.nom_real.data
        #print(nom_real)
        
        reals = rech_films(nom_real, Directeur, Directeur.nom)

        if reals == []:
            # Message d'attention à l'utilisateur sur la non trouvaille du nom
            flash("Nous n'avons pas pu trouvé de réalisateurs correspondant à votre recherche")

            # Retour du formulaire sans la possibilité de renvoyer les données envoyées
            return redirect(url_for('recherche_realisateur'))

        
    return render_template("realisateur.html",
                           form = form,
                           reals = reals,
                           r_top_10_mieux_notes =  r_top_10_mieux_notes,
                           r_top_10_plus_populaires = r_top_10_plus_populaires,
                           r_top_10_real_film = r_top_10_real_film)

#################################
# Création de la page du formulaire pour la recherche de films par genre/titre
#################################
@app.route('/rech_film', methods=["GET", "POST"])
def recherche():
    form = TitGenForm()
    result = []
    type_data = ""
    word_data = ""

    if form.validate_on_submit():

        type_data = form.type.data # "Genre" /ou/ "Titre"
        word_data = form.word.data # ZONE DE TEXTE
        
        if type_data == "Genre" :
            result = rech_genres(word_data)
            mess_inf = "Le genre que vous avez renseigné n'existe pas."

        else:
            result = rech_films(word_data, Film, Film.title)
            mess_inf = "Le titre que vous avez renseigné n'existe pas."

        if result == []:
            flash(mess_inf)
    
    return render_template('formulaire_films.html', 
                           form=form,
                           films_titre_genre = result,
                           type_data = type_data,
                           word_data = word_data)

# Création de la route pour afficher les films réalisés par le réalisateur/directeur
@app.route("/films_realisateur/<id_dir>")
def aff_film(id_dir):

    # Recherche SQL sur les films réalisés par ce directeur
    resultat = Directeur.query.filter(Directeur.id == id_dir).first()

    return render_template("realisateur_films.html",
                           films_real = resultat)

##################################
# Création des routes spécifiques pour la Data 
# JSON avec Fetch 
##################################

# Pour le nombre de films par genre
@app.route('/api/data/films_par_genre')
def get_data_genre():
    result = films_par_genre()

    return jsonify(result)

# Pour le nombre de films par langue
@app.route('/api/data/films_par_langue')
def get_data_langue():
    result = films_par_langue()

    return jsonify(result)

# Pour le nombre de films par année
@app.route('/api/data/films_par_annee')
def get_data_annee():
    result = films_par_annee()

    return jsonify(result)

#####################################
# Création des filtrages personnalisés
#####################################
def extract_year(date_year):
    date_year = str(date_year)
    year = date_year.split("-")[0]

    return year

#___________________________________________________________________ #
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
dataset = namespace["dataset"]
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


# Insert into the table Film and the related associated tables
with app.app_context():
    for index, row in dataset.iterrows():
        # Ensure all critical film attributes are valid
        orig_lang = Language.query.filter_by(language=row["original_language"]).first()
        direc = Directeur.query.filter_by(nom=row["lastname"], prenom=row["firstname"]).first()
        collec = Collection.query.filter_by(name=row["belongs_to_collection"]).first()

        if not orig_lang or not direc or not collec:
            continue
        
        # Initialize film object
        film = Film()
        
        film.id = row["id"]
        film.title = row["title"]
        film.release_date = row["release_date"]
        film.popularity = row["popularity"]
        film.runtime = row["runtime"]
        film.budget = row["budget_musd"] if not pd.isna(row["budget_musd"]) else 0
        film.revenue = row["revenue_musd"] if not pd.isna(row["revenue_musd"]) else 0
        film.tagline = row["tagline"] if not pd.isna(row["tagline"]) else None
        film.overview = row["overview"] if not pd.isna(row["overview"]) else None
        film.poster_path = row["poster"]
        film.vote_count = row["vote_count"]
        film.vote_average = row["vote_average"]
        film.id_original_language = orig_lang.id
        film.id_directeur = direc.id
        film.id_collection = collec.id

        # initialiser les clé étragères : film.fk = orig_lang.id    
        db.session.add(film)
        db.session.flush()
        print(f"Inserting data...")
        
        # Insert into association tables

        # Genres
        genres = row["genres"].split("|") if not pd.isna(row["genres"]) else []
        for genre_name in genres:
            genre = Genre.query.filter_by(genre=genre_name.strip()).first()
            if not genre:
                genre = Genre(genre=genre_name.strip())
                db.session.add(genre)
                db.session.flush()  # Generate genre ID
            db.session.execute(film_genres.insert().values(id_film=film.id, id_genres=genre.id))

        # Companies
        companies = row["production_companies"].split("|") if not pd.isna(row["production_companies"]) else []
        for company_name in companies:
            company = Company.query.filter_by(name=company_name.strip()).first()
            if not company:
                company = Company(name=company_name.strip())
                db.session.add(company)
                db.session.flush()  # Generate company ID
            db.session.execute(film_companies.insert().values(id_film=film.id, id_companies=company.id))

        if direc:
            db.session.execute(film_directeurs.insert().values(id_film=film.id, id_directeur=direc.id))

        # Spoken Languages
        spoken_languages = row["spoken_languages"].split("|") if not pd.isna(row["spoken_languages"]) else []
        for lang in spoken_languages:
            language = Language.query.filter_by(language=lang.strip()).first()
            if not language:
                language = Language(language=lang.strip())
                db.session.add(language)
                db.session.flush()  # Generate language ID
            db.session.execute(film_languages.insert().values(id_film=film.id, id_language=language.id))

    db.session.commit()
