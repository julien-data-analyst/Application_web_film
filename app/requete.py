#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024
# Sujet : requête SQL pour les visualisations graphiques + indicateurs 
#################################################

from modele_bdd import db, Genre, Film, Directeur, Langage, film_langages, film_genres # Toutes les tables et relations
from sqlalchemy.sql import insert, func # Les fonctions utilisées pour gérer les group_by et les aggrégations
from config import app
import os 
import datetime

# Attention : se placer dans le dossier app pour tester le programme
# Si base déjà créée : supprimer la base en question pour éviter le moindre problème dans la création de table si modif au niveau des colonnes/tables

# ---- Test provisoire sur la création du BDD ----
db.init_app(app)

# ---- Création d'une fct utilitaire pour les informations de Film ----
def inf_film(col, cond, order_by="", calcule=False, limit=10):
    """
    Fonction : Récupérer des informations numériques (top 10) sur les Films (runtime, vote_count, budget, etc)
    Arguments :
    - col : colonne en question (objet Film) 
    - cond : condition à utiliser dans la requête (expression booléenne)
    - calcule : valeur booléenne s'il est calculé ou non (par défaut : False)
    - order_by : ordre croissant / décroissant (par défaut : croissant)
    - limit : nombre d'enregistrements à récupérer (par défaut : 10)
    Retour : 
    Résultat de la requête SQL (liste d'instance/de tuples)
    """

    if order_by=="" :
        order_by = col
    
    if calcule :
        result = (
                Film.query
                .add_columns(col)
                .order_by(order_by)
                .filter(cond)
                .limit(limit)
                .all()
        )
    else:
        result = (
                Film.query
                .order_by(order_by)
                .filter(cond)
                .limit(limit)
                .all()
        )
    
    return result

# ---- Préparation des différentes requêtes SQL ----
# cmd.produits.extend(prod_sel) # Ajout des produits sélecitonnées (liste des classes)
with app.app_context():

    db.drop_all()
    db.create_all()

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
    new_dir = Directeur(nom="Dir", prenom='Dir')

    # Ajout du lien entre Genre et Film
    new_genre.films.extend([new_film])
    new_film.genres.extend([new_genre_2])

    db.session.add_all([new_langage, new_film, new_film_2, new_film_3,
                        new_langage_2, new_langage_3, 
                        new_genre, new_genre_2, new_dir,
                        new_film_4, new_film_5, new_film_6])
    db.session.commit()

    # Ajout du lien entre Film et langage (obligée car on ne peut pas rajouter d'attributs)
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

    ####################################################
    # PARTIE : REQUÊTE SQL POUR LES VISUELS ET INDICATEURS
    ####################################################

    ####################################################
    # SECTION 1 : Répartition des films selon différents critères
    ####################################################

    # Création des variables pour le comptage et l'extraction de dates
    cpt_film = func.count(Film.id)
    date_year = func.extract("year", Film.release_date)

    ###########################
    # Nombre de films par genre 
    ###########################
    result_f_par_g = (
            db.session.query(Genre.genre, cpt_film) # Sélection des colonnes
            .join(film_genres, Genre.id == film_genres.c.id_genres)  # Utilisation de la table d'association
            .join(Film, Film.id == film_genres.c.id_film)  # Jointure avec Film
            .group_by(Genre.genre)
            .order_by(cpt_film.desc())
            .all()
    )

    print("Le nombre de films par genre : \n"+str(result_f_par_g) + "\n")
    ############################
    ############################

    ###########################
    # Nombre de films par langue (20 premiers) 
    ########################### 
    result_f_par_l = (
        db.session.query(Langage.langage, cpt_film) # Sélection des colonnes + colonne calculée
            .join(film_langages, Langage.id == film_langages.c.id_langage)  # Utilisation de la table d'association
            .join(Film, Film.id == film_langages.c.id_film)  # Jointure avec Film
            .group_by(Langage.langage) # grouper par langage
            .order_by(cpt_film.desc()) # ordonner par le nombre de films
            .limit(20) # Limiter à 20 langues
            .all() # Récupération de toutes les 20 lignes
    )
    print("Le nombre de films par langue : \n"+str(result_f_par_l) + "\n")
    ##########################
    ##########################

    ###########################
    # Nombre de films par année (20 dernières années)
    ###########################
    result_f_par_a = (
        db.session.query(date_year, cpt_film).group_by(date_year)
        .filter(date_year != None)
        .order_by(date_year.desc())
        .limit(20)
        .all()
    )
    print("Le nombre de films par année : \n"+str(result_f_par_a) + "\n")
    ###########################
    ###########################

    ###########################
    # Chercher le genre le plus associé au film + l'année la plus productive
    ###########################
    max_genre = result_f_par_l[0]
    print("Le genre qui apparaît le plus : " + str(max_genre[0])) # Le premier de notre première requête

    # Requête pour trouver l'année la plus productive
    result_max_ann = (
        Film.query
        .group_by(Film.release_date)
        .add_columns(date_year,
                    cpt_film) # 2ème et 3ème colonne (Année et total)
        .order_by(cpt_film.desc())
        .limit(1)
        .all()
    )
    max_annee = result_max_ann[0][1]
    print("L'année la plus productive : " + str(max_annee)) # L'année la plus productive
    ###########################
    ###########################

    ####################################################
    # SECTION 2 : Statistiques financières
    ####################################################

    # Définition des variables calculées
    somme_budget = func.sum(Film.budget)
    somme_revenue = func.sum(Film.revenue)
    ratio = Film.revenue / Film.budget
    deficit = Film.revenue - Film.budget

    ####################################################
    # Total des recettes et budgets cumulés ############
    ####################################################
    total_budget_recette = (Film.query
                            .add_columns(somme_budget, somme_revenue)
                            .first()
                            )
    print("Le total des budgets et des recettes cumulés : \n"+str(total_budget_recette)+"\n")
    ###################################################
    ###################################################

    ####################################################
    # Liste des dix films ############
    ####################################################

    # Les plus chères ##################
    result_f_plus_cher = inf_film(col=Film.budget, cond=Film.budget != None, order_by=Film.budget.desc())
    print("Les dix films les plus chères : \n"+str(result_f_plus_cher)+"\n") # Les instances des films

    # Les plus rentables (ratio recettes/budget)
    result_f_plus_rent = inf_film(col=ratio, cond=ratio>=1, order_by=-ratio, calcule=True)
    print("Les dix films les plus rentables : \n"+str(result_f_plus_rent)+"\n") # Les instances des films + le ratio recette/budget >= 1

    # Les plus décifitaires (recettes - budget)
    result_f_plus_def = inf_film(col=deficit, cond=deficit <= 0, calcule=True)
    print("Les dix films les plus déficitaires : \n"+str(result_f_plus_def)+"\n") # Les instances des films + le déficit
    ###################################################
    ###################################################

    ####################################################
    # SECTION 3 : Statistiques sur les votes
    ####################################################
    # Les dix films les mieux notés (vote_average)
    result_f_n = inf_film(col=Film.vote_average, cond=Film.vote_average != None, 
                          order_by=Film.vote_average.desc())
    print("Les dix films les mieux notés : "+ str(result_f_n)) # Instances de films

    # Les dix films les plus votés (vote_count)
    result_f_c = inf_film(col=Film.vote_count, cond=Film.vote_count > 0, 
                          order_by=Film.vote_count.desc())
    print("Les dix films les plus votés : "+ str(result_f_c)) # Instances de films

    # Les dix films les plus populaires (popularity)
    result_f_p =  inf_film(col=Film.popularity, cond=Film.popularity != None, 
                          order_by=Film.popularity.desc())
    print("Les dix films les plus populaires : "+ str(result_f_p)) # Instances de films

    ####################################################
    ####################################################

    ####################################################
    # SECTION 4 : Statistiques sur les durées
    ####################################################
    # Les dix films les plus longs
    result_f_plus_long = inf_film(col=Film.runtime, cond=Film.runtime != None, 
                          order_by=Film.runtime.desc())
    print("Les dix films les plus longues : "+ str(result_f_plus_long)) # Instances de films

    # Les dix films les plus courts
    result_f_plus_court = inf_film(col=Film.runtime, cond=Film.runtime != None, 
                          order_by=Film.runtime)
    print("Les dix films les plus courtes : "+ str(result_f_plus_court)) # Instances de films

    ####################################################
    ####################################################


    ####################################################
    # FIN DE LA PARTIE DES REQUÊTES SQL 
    ####################################################

    ####################################################
    # PARTIE FORMATTAGE DES RÉSULTATS POUR LES VISUELS GRAPHIQUES (CHARTJS) { "mod" : [...], ""}
    ####################################################

    # Dans cette partie, je vais mettre en forme mes réponses pour qu'il puisse être récupérée par l'application et le javascript (render_templates, jsonify)

    ####################################################
    ####################################################
    #print(Genre.query.first().films)

    #print(Directeur.query.first().films)


