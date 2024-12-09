#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024
# Sujet : création d'une application web (lanceur)
#################################################

# Chargement des librairies
import os
from config import app
from modele_bdd import db, Genre, Film, Directeur, Langage, film_langages, film_genres # Toutes les tables et relations
from requete_utl import inf_film_10, req_joint_par_crit, mise_forme_resultats_graph, \
                        films_par_genre, films_par_annee, films_par_langue, top_10_mieux_notes, \
                        top_10_plus_cher, top_10_plus_court, top_10_plus_deficit, top_10_plus_long, top_10_plus_populaires, \
                        top_10_plus_rentables, top_10_plus_votes, total_budget_recette, annee_plus_productive, max_films_genre, \
                        top_10_realisateur

from sqlalchemy.sql import insert
import datetime
from flask import render_template, jsonify

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

# Test de l'application
if __name__ == "__main__":
    # Exemple d'initialisation de la base de données
    with app.app_context():
        print("Initialisation de la base de données...")
        db.drop_all()  # Supprimer toutes les tables
        db.create_all()  # Créer toutes les tables
        print("Base de données initialisée.")

        # Ajout d'instances
        new_genre = Genre(genre="drama")
        new_genre_2 = Genre(genre="action")
        new_film = Film(title="Film", vote_count=15000,
                        vote_average = 10,
                        popularity = 0.5, 
                        release_date=datetime.datetime.now(),
                        runtime = 60,
                        budget = 200,
                        revenue = 100)
        
        new_film_2 = Film(title="Mastermind", vote_count=10000,
                        vote_average=20, 
                        release_date = datetime.datetime.now(),
                        budget = 70,
                        runtime = 120,
                        popularity= 0.7,
                        revenue = 100)
        new_film_3 = Film(title="Popularity", 
                        vote_count=0,
                        budget = 10,
                        revenue = 100,
                        popularity = 0.8,
                        runtime = 50)
        new_film_4 = Film(title="Popularity", vote_count=0, 
                        release_date = datetime.datetime.strptime("2023-03-14", "%Y-%m-%d"),
                        budget = 20,
                        revenue = 10)
        new_film_5 = Film(title="Popularity", 
                        vote_count=0, 
                        release_date = datetime.datetime.strptime("2023-03-14", "%Y-%m-%d"),
                        budget = 50,
                        revenue = 80)
        new_film_6 = Film(title="Popularity", vote_count=0, release_date = datetime.datetime.strptime("2023-03-14", "%Y-%m-%d"))
        new_langage = Langage(langage="French")
        new_langage_2 = Langage(langage="Allemand")
        new_langage_3 = Langage(langage="Espagnol")

        # Pour les directeurs
        new_dir = Directeur(nom="Dir", prenom='Dir')
        new_dir_2 = Directeur(nom="Dir2", prenom="Dir2")
        new_dir_3 = Directeur(nom="Dir3", prenom="Dir3")

        # Ajout du lien entre Genre et Film
        new_genre.films.extend([new_film])
        new_film.genres.extend([new_genre_2])

        new_dir.films.extend([new_film, new_film_2])
        new_dir_2.films.extend([new_film_3, new_film_4, new_film_5])
        new_dir_3.films.extend([new_film_6])

        db.session.add_all([new_langage, new_film, new_film_2, new_film_3,
                            new_langage_2, new_langage_3, 
                            new_genre, new_genre_2, new_dir,
                            new_film_4, new_film_5, new_film_6])
        db.session.commit()
        # Ajout du lien entre Film et langage (obligée car on ne peut pas rajouter d'attributs avec extend)
        db.session.execute(
        insert(film_langages).values(
            id_film=new_film.id,
            id_langage=new_langage.id,
            original=True  # Ajouter la valeur pour la colonne supplémentaire
        )
        )

        db.session.execute(
        insert(film_langages).values(
            id_film=new_film.id,
            id_langage=new_langage_2.id,
            original=False  # Ajouter la valeur pour la colonne supplémentaire
        )
        )

        db.session.execute(
        insert(film_langages).values(
            id_film=new_film.id,
            id_langage=new_langage_3.id,
            original=False  # Ajouter la valeur pour la colonne supplémentaire
        )
        )

        db.session.execute(
        insert(film_langages).values(
            id_film=new_film_2.id,
            id_langage=new_langage_2.id,
            original=True  # Ajouter la valeur pour la colonne supplémentaire
        )
        )

        db.session.execute(
        insert(film_langages).values(
            id_film=new_film_3.id,
            id_langage=new_langage_3.id,
            original=True  # Ajouter la valeur pour la colonne supplémentaire
        )
        )
    
        db.session.execute(
        insert(film_langages).values(
            id_film=new_film_3.id,
            id_langage=new_langage.id,
            original=True  # Ajouter la valeur pour la colonne supplémentaire
        )
        )
        db.session.commit()

        
        db.session.execute(
        insert(film_langages).values(
            id_film=new_film_2.id,
            id_langage=new_langage.id,
            original=True  # Ajouter la valeur pour la colonne supplémentaire
        )
        )
    # Lancer l'application Flask
    app.run(debug=True, port=5000)



#if not(os.path.exists("instance/films.db")):
#    with app.app_context():
#        db.drop_all()
#        db.create_all()
