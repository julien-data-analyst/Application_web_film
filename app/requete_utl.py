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
import os 
import datetime

# ---- Test provisoire sur la création du BDD ----
db.init_app(app)

# ---- Création de plusieurs fct utilitaires pour les informations de Film et la mise en forme des résultats ----
def inf_film(col, cond, order_by="", calcule=False, limit=10):
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
    if not(isinstance(group_by, ColumnElement)) : # Si ce n'est pas une instance de colonne élément
        group_by = col
    
    if not(isinstance(order_by, ColumnElement)) : # Si ce n'est pas une instance de colonne élément
        order_by = -col_cal

    print(order_by)
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
