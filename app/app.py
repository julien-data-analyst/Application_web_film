#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024
# Sujet : création d'une application web (lanceur)
#################################################

# Chargement des librairies
import os
from config import app
from modele_bdd import db, Genre, Film, Directeur
# Toutes les requêtes SQL nécessaires
from requete_utl import films_par_genre, films_par_annee, films_par_langue, top_10_mieux_notes, \
                        top_10_plus_cher, top_10_plus_court, top_10_plus_deficit, top_10_plus_long, top_10_plus_populaires, \
                        top_10_plus_rentables, top_10_plus_votes, total_budget_recette, annee_plus_productive, max_films_genre, \
                        top_10_realisateur, rech_films
# Importation des formulaires
from formulaires import RealForm, TitGenForm
from flask import render_template, jsonify, flash, redirect, url_for
import pandas as pd

# Attention : se placer dans le dossier app pour lancer l'application
# si base déjà créé et que vous voulez relancer la création et l'insertion de la BDD, supprimer le fichier BDD

@app.route('/film', methods=["GET", "POST"])
def film():
    """
    Fonction : représente la page de film où on va retrouver les différents indicateurs/visuels sur les films
    Retour : page web contenant toutes les informations à propos des films
    """

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

    return render_template("film.html",
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
                           r_top_10_plus_rentable = r_top_10_plus_rentable
                           )


@app.route('/',methods = ['GET', 'POST'])
def index():
    """
    Fonction : représente la page d'index où on présente le projet, l'environnement technique et l'équipe.
    Retour : page web sur la présentation du projet
    """
    return render_template('index.html')

#################################
# Création de la page du formulaire pour la recherche de réalisateur
#################################
@app.route('/acteur_réa', methods=["GET", "POST"])
def acteur_réa():
    """
    Fonction : représente la page des réalisateurs
    Retour : page web contenant toutes les informations à propos des films
    """
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
            return redirect(url_for('acteur_réa'))

        
    return render_template("Acteurs_Réalisateurs.html",
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
    """
    Fonction : représente le formulaire de recherche de film par genre/titre
    Retour : page web contenant le formulaire en question
    """
    form = TitGenForm()
    result = []
    type_data = ""
    word_data = ""

    if form.validate_on_submit():

        type_data = form.type.data # "Genre" /ou/ "Titre"
        word_data = form.word.data # ZONE DE TEXTE
        
        if type_data == "Genre" :
            result = rech_films(word_data, Film, Genre.genre)
            mess_inf = "Le genre que vous avez renseigné n'existe pas."

        else:
            result = rech_films(word_data, Film, Film.title)
            mess_inf = "Le titre que vous avez renseigné n'existe pas."

        if result == []:
            flash(mess_inf)
            return redirect('formulaire_films.html')
        else :
            return render_template("resultat_recherche.html",
                        films_titre_genre = result,
                        type_data = type_data,
                        word_data = word_data)

    
    return render_template('formulaire_films.html', 
                           form=form,
                           films_titre_genre = result,
                           type_data = type_data,
                           word_data = word_data)



# Création de la route pour afficher les films réalisés par le réalisateur/directeur
@app.route("/films_realisateur/<id_dir>")
def aff_film(id_dir):
    """
    Fonction : représente la page de résultat sur les films réalisés par un directeur

    Argument :
    - id_dir : id du directeur à rechercher

    Retour : page web contenant tous les films réalisés par le directeur choisi (id_dir)
    """
    # Recherche SQL sur les films réalisés par ce directeur
    resultat = Directeur.query.filter(Directeur.id == id_dir).first()

    return render_template("realisateur_films.html",
                           films_real = resultat)

##################################
# Création des routes spécifiques pour la Data 
# JSON avec Fetch 
# Commentaire : facilite la tâche pour la création de visuels graphiques avec ChartJS (main.js)
##################################

# Pour le nombre de films par genre
@app.route('/api/data/films_par_genre')
def get_data_genre():
    """
    Fonction : permet d'avoir les données JSON concernant le nombre de films par genre
    Retour : résultat JSON de la requête SQL
    """
    result = films_par_genre()

    return jsonify(result)

# Pour le nombre de films par langue
@app.route('/api/data/films_par_langue')
def get_data_langue():
    """
    Fonction : permet d'avoir les données JSON concernant le nombre de films par langue (20 premières)
    Retour : résultat JSON de la requête SQL
    """
    result = films_par_langue()

    return jsonify(result)

# Pour le nombre de films par année
@app.route('/api/data/films_par_annee')
def get_data_annee():
    """
    Fonction : permet d'avoir les données JSON concernant le nombre de films par années (20 dernières années)
    Retour : résultat JSON de la requête SQL
    """
    result = films_par_annee()

    return jsonify(result)

#####################################
# Création des filtrages personnalisés
#####################################
def extract_year(date_year):
    """
    Fonction : filtrage permettant de récupérer l'année d'une date au format (yyyy-mm-dd)
    Retour : retourne l'année correspondante
    """
    date_year = str(date_year)
    year = date_year.split("-")[0]

    return year

# Enregistrer le filtre
app.jinja_env.filters['extract_year'] = extract_year

def conversion_heure_min(minutes):
    """
    Fonction :  filtrage permettant les minutes en heures.
    Retour : chaîne de caractère représentant l'heure et minute (00h00)
    """

    # Initialisation
    minutes = int(minutes)
    heure = 0

    # Ajouter une heure si notre valeur dépasse les 60 minutes
    while minutes >= 60:
            minutes = minutes - 60
            heure += 1

    # Retourner la chaîne 
    if minutes < 10:
        return str(heure) + "h0" + str(minutes)
    else:
        return str(heure) + "h" + str(minutes)

# Enregistrer le filtre
app.jinja_env.filters['conv_heure_min'] = conversion_heure_min

#############################
# Partie insertion des données
#############################

# Si base pas créé, il le crée avec ses insertions de données
if not(os.path.exists("instance/films.db")):

    # Importation des DataFrames préparés
    import insertion as i_n

    # Pour plus de détails, voir le script dans insertion_new
    i_n.creation_insertion_bdd(app, db)


# Lancement de l'application
app.run(debug=True)