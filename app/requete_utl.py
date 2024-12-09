#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 08/12/2024
# Sujet : requête SQL pour les visualisations graphiques + indicateurs + formulaire
#################################################

# ---- Chargement des librairies ----
from modele_bdd import db, Genre, Film, Directeur, Langage, film_langages, film_genres # Toutes les tables et relations
from sqlalchemy.sql import insert, func # Les fonctions utilisées pour gérer les group_by et les aggrégations
from sqlalchemy.sql.expression import ColumnElement
from config import app

# ---- Test provisoire sur la création du BDD ----
db.init_app(app)

# ---- Création de plusieurs fct utilitaires pour les informations de Film et la mise en forme des résultats ----
def inf_film_10(col, cond, order_by="", calcule=False, limit=10):
    """
    Fonction : Récupérer des informations numériques (top 10) sur les Films (runtime, vote_count, budget, etc)
    Arguments :
    - col : colonne en question (objet Film) 
    - cond : condition à utiliser dans la requête (expression booléenne)
    - calcule : valeur booléenne s'il est calculé ou non (par défaut : "" donc croissant = 'col')
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

def mise_forme_resultats_graph(donnees, empl_mod = 0, empl_chiffre = 1):
        """
        Fonction : Mettre en forme les résultats poru les visualisations graphiques (ChartJS) avec JSON (jsonify)
        
        Arguments :
        - donnees : Liste de tuple dont le premier emplacement représente la modalité et le deuxième la valeur
        - empl_mod : l'emplacement dans le tuple où on peut trouver la modalité (par défaut : 0)
        - empl_chiffre : l'emplacement dans le tuple où on peut trouver l'effectif (par défaut : 1)

        Retour :
        - dictionnaire de liste {"mod" : [...], "eff" : [...]}
        """

        if type(donnees) != list :
            raise TypeError("L'argument 'donnees' n'est pas une liste")
        
        if any([type(tupl)==tuple for tupl in donnees]) :
            raise TypeError("L'argument 'donnees' ne doit posséder que des tuples")
        
        dict_donn = {
            "mod" : [],
            "eff" : []
        }
        
        for tupl in donnees:
            dict_donn["mod"].append(tupl[empl_mod])
            dict_donn["eff"].append(tupl[empl_chiffre])
        
        return dict_donn

def req_joint_par_crit(table, col, jointure, col_table, add_filter=False, filter=None, group_by=None,
                       limit=0, col_film=None, col_cal=None, order_by=None):
    """
     Fonction : Permet de faire les différentes requêtes SQL nécessitant des jointures ou des opérations complexes
     
     Arguments :
     - table : la table en question avec la relation * à * avec le Film
     - col : la colonne pour le résultat
     - jointure : la table d'association entre les deux tables (table d'association : db.Table)
     si jointure est égale à False, alors il n'y a pas de jointure à faire (colonne existante dans film)
     - col_table : la colonne pour joindre la table d'association 
     - filter : La condition de filtrage ave la méthode filter (par défaut : rien)
     - group_by : la colonne de groupage (par défaut : col)
     - order_by : colonne pour l'ordre croissante ou décroissante (par défaut : -col_cal)
     - limit : le nombre d'observations limitées (par défaut : 0, on prend toutes les observations)
     - col_film : la colonne pour joindre le film (par défaut : jointure.c.id_film)
     - col_cal : colonne calculée (utilisation de la fonction "func" de SQLAlchemy) (par défaut : func.count(col))
     - add_filter : valeur booléenne disant si on doit ajouter un filtre à notre requête SQL
     - filter : filtrage SQL à faire
     ça peut concerner aussi une colonne numérique dans la table Film.

     
     Retour :
     Résultat de la requête SQL (Liste de tuples ou d'un tuple selon la limit)

    """
    # Utilisation de la fonction count par défaut
    if col_cal == None :
          col_cal = func.count(col)

    # Création du début de la requête
    query_sql = db.session.query(col, col_cal)

    # Vérifions la présence de jointure
    if jointure != False:
        if col_film == None:
         col_film = jointure.c.id_film
         query_sql = (
             query_sql
             .join(jointure, table.id == col_table) # Jointure avec la table d'association
             .join(Film, Film.id == col_film)
             )

    # Faisons le filter (pas obligatoire)
    if add_filter :
        query_sql = (
            query_sql
            .filter(filter)
        )

    # Faisons le group_by + order_by
    if not(isinstance(group_by, ColumnElement)) : # Si ce n'est pas une instance de colonne
        group_by = col
    
    if not(isinstance(order_by, ColumnElement)) : # Si ce n'est pas une instance de colonne
        order_by = -col_cal

    query_sql = (
                 query_sql
                 .group_by(group_by)
                 .order_by(order_by)
                 )
    
    # Faisons le cas de limit
    if limit > 0 :
        query_sql = (
            query_sql
            .limit(limit)
        )
    
    return query_sql.all()

####################################################
# PARTIE : REQUÊTE SQL POUR LES VISUELS ET INDICATEURS
####################################################

####################################################
# SECTION 1 : Répartition des films selon différents critères
####################################################

###########################
# Nombre de films par genre 
###########################
def films_par_genre():
    """
    Fonction : requête SQL pour récupérer le nombre de films par genre avec mise en forme des résultats
    Retour : Dictionnaire de liste ({"mod" : [...], "eff" : [...]})
    """

    # Application de la requête SQL
    result_f_par_g = req_joint_par_crit(Genre, # Table en question 
                                        Genre.genre, # Colonne concernée
                                       film_genres, # Table d'association
                                       film_genres.c.id_genres) # Colonne de la table d'association
    
    # Mise en forme des résultats
    result_f_par_g = mise_forme_resultats_graph(result_f_par_g)

    return result_f_par_g


###########################
# Nombre de films par langue (20 premiers) 
########################### 
def films_par_langue():
    """
    Fonction : requête SQL pour récupérer le nombre de films par langue avec mise en forme des résultats
    Retour : Dictionnaire de liste ({"mod" : [...], "eff" : [...]})
    """

    # Application de la requête SQL
    result_f_par_l = req_joint_par_crit(
        Langage, Langage.langage, 
        film_langages, film_langages.c.id_langage,
        limit=20
    )

    # Application de la mise en forme
    result_f_par_l = mise_forme_resultats_graph(
        result_f_par_l
    )

    return result_f_par_l

###########################
# Nombre de films par année (20 dernières années)
###########################
def films_par_annee():

    # Création de la variable d'année
    date_year = func.extract("year", Film.release_date)

    # Application de la requête SQL
    result_f_par_a = req_joint_par_crit(
        Film, date_year, False, "",
        group_by=date_year,
        order_by=-date_year,
        add_filter=True,
        filter=date_year != None,
        limit=20
    )
    
    # Mise en forme des résultats sous dictionnaire
    result_f_par_a = mise_forme_resultats_graph(result_f_par_a)

    return result_f_par_a

###########################
# L'année la plus productive
###########################

def annee_plus_productive():
    # Création de la variable d'année
    date_year = func.extract("year", Film.release_date)

    # Requête pour trouver l'année la plus productive
    result_max_ann = req_joint_par_crit(
        Film, date_year, False, "",
        group_by=date_year,
        add_filter=True,
        filter=date_year != None,
        limit=1
    )

    return result_max_ann[0]

############################
# Genre contenant le plus de film
############################
def max_films_genre():
    """
    Fonction : requête SQL pour récupérer le nombre de films par genre avec mise en forme des résultats
    Retour : Dictionnaire de liste ({"mod" : [...], "eff" : [...]})
    """

    # Application de la requête SQL
    result_f_par_g = req_joint_par_crit(Genre, # Table en question 
                                        Genre.genre, # Colonne concernée
                                       film_genres, # Table d'association
                                       film_genres.c.id_genres, # Colonne de la table d'association
                                       limit=1
                                       ) 

    return result_f_par_g[0]

####################################################
# SECTION 2 : Statistiques financières
####################################################

####################################################
# Total des recettes et budgets cumulés ############
####################################################
def total_budget_recette():

    # Création des colonnes calculées
    somme_budget = func.sum(Film.budget)
    somme_revenue = func.sum(Film.revenue)

    total_budget_recette = (Film.query
                            .add_columns(somme_budget, somme_revenue)
                            .first()[1:]
                            )
    
    return total_budget_recette

####################################################
# Liste des dix films les plus chères ############
####################################################
def top_10_plus_cher():

    # Application de la requête SQL
    result_f_plus_cher = inf_film_10(col=Film.budget, cond=Film.budget != None, order_by=Film.budget.desc())
    
    return result_f_plus_cher

####################################################
# Liste des dix films les plus rentables ############
####################################################
def top_10_plus_rentables():

    # Création de la colonne calculée
    ratio = Film.revenue / Film.budget

    # Application de la requête SQL
    result_f_plus_rent = inf_film_10(col=ratio, cond=ratio>=1, order_by=-ratio, calcule=True)

    return result_f_plus_rent

####################################################
# Liste des dix films les plus déficitaire ############
####################################################
def top_10_plus_deficit():

    # Création de la colonne calculée
    deficit = Film.revenue - Film.budget

    # Application de la requête SQL
    result_f_plus_def = inf_film_10(col=deficit, cond=deficit <= 0, calcule=True)

    return result_f_plus_def


####################################################
# SECTION 3 : Statistiques sur les votes
####################################################

# Les dix films les mieux notés (vote_average)
# Pour récupérer le directeur : result_f_n[0].directeur
def top_10_mieux_notes():

    # Application de la requête SQL
    result_f_n = inf_film_10(col=Film.vote_average, cond=Film.vote_average != None, 
                          order_by=Film.vote_average.desc())

    return result_f_n

# Les dix films les plus votés (vote_count)
def top_10_plus_votes():

    # Application de la requête SQL
    result_f_c = inf_film_10(col=Film.vote_count, cond=Film.vote_count > 0, 
                          order_by=Film.vote_count.desc())
    
    return result_f_c

# Les dix films les plus populaires (popularity)
def top_10_plus_populaires():
    
    # Application de la requête SQL
    result_f_p =  inf_film_10(col=Film.popularity, cond=Film.popularity != None, 
                          order_by=Film.popularity.desc())
    
    return result_f_p

####################################################
# SECTION 4 : Statistiques sur les durées
####################################################

# Les dix films les plus longues
def top_10_plus_long():

    # Application de la requête SQL
    result_f_plus_long = inf_film_10(col=Film.runtime, cond=Film.runtime != None, 
                          order_by=Film.runtime.desc())
    
    return result_f_plus_long

# Les dix films les plus courtes
def top_10_plus_court():

    # Application de la requête SQL
    result_f_plus_court = inf_film_10(col=Film.runtime, cond=Film.runtime != None, 
                          order_by=Film.runtime)
    
    return result_f_plus_court

####################################################
# POUR LES PAGES : REALISATEURS / ACTEURS 
####################################################
# Les 10 réalisateurs ayant réalisé le plus de films
def top_10_realisateur():
    # Création de la colonne calculé
    cpt_film = func.count(Film.id)

    # Application de la requête SQL
    result_f_r = (
        db.session.query(Directeur.nom, Directeur.prenom, cpt_film)
        .join(Film, Directeur.id == Film.id_directeur) # Jointure avec la table Film
        .group_by(Directeur.id) # Grouper par directeur
        .order_by(-cpt_film) # Ordre décroissant
        .limit(10)
        .all()
    )

    return result_f_r

if __name__=="__main__":
    with app.app_context() :

        # Test pour la première section
        print("Le nombre de films par genre : \n"+str(films_par_genre()) + "\n")
        print("Le nombre de films par langue : \n"+str(films_par_langue()) + "\n")
        print("Le nombre de films par année : \n"+str(films_par_annee()) + "\n")
        print("Le genre qui apparaît le plus : " + str(max_films_genre())) # Le premier de notre première requête
        print("L'année la plus productive : " + str(annee_plus_productive())) # L'année la plus productive

        # Test pour la deuixème section
        print("Le total des budgets et des recettes cumulés : \n"+str(total_budget_recette())+"\n")
        print("Les dix films les plus chères : \n"+str(top_10_plus_cher())+"\n") # Les instances des films
        print("Les dix films les plus rentables : \n"+str(top_10_plus_rentables())+"\n") # Les instances des films
        print("Les dix films les plus déficitaires : \n"+str(top_10_plus_deficit())+"\n") # Les instances des films

        # Test pour la troisième section
        print("Les dix films les mieux notés : "+ str(top_10_mieux_notes())) # Instances de films
        print("Les dix films les plus votés : "+ str(top_10_plus_votes())) # Instances de films
        print("Les dix films les plus populaires : "+ str(top_10_plus_populaires())) # Instances de films

        # Test pour la quatrième section
        print("Les dix films les plus longues : "+ str(top_10_plus_long())) # Instances de films
        print("Les dix films les plus courtes : "+ str(top_10_plus_court())) # Instances de films

        # Test pour la partie Page/Réalisateur
        print("Les dix réalisateurs qui ont réalisé le plus de film : "+str(top_10_realisateur()))
        
        # Pour récupérer les réalisateurs des 10 films les mieux notés / les plus populaires
        liste_real_not = []
        for film in top_10_mieux_notes():
            liste_real_not.append(film.directeur)

        liste_real_pop = []
        for film in top_10_plus_populaires():
            liste_real_pop.append(film.directeur)

        print("Les réalisateurs des 10 films les mieux notés : "+str(liste_real_not))
        print("Les réalisateurs des 10 films les plus populaires : "+str(liste_real_pop))