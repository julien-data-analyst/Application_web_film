#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024 - 10/12/2024
# Sujet : création des tables pour la bdd
#################################################

# Chargement de la librairie
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#########################################
### Créer les colonnes des tables ####
########################################

##############################
# ---- Pour la table Film ----
##############################
class Film(db.Model):
    """
    Création de la table Film dans la BDD.
    Elle contient comme colonnes :
    - id : clé primaire permettant d'identifier la ligne en question
    - title : titre du film
    - release_date : date de sortie
    - popularity : l'indice de popularité [0, 1]
    - runtime : durée du film en minute
    - budget : budget du film en million de $
    - revenue : revenue du film en million de $
    - tagline : phrase clé (slogan) du film
    - overwiew : résumé du film
    - poster_path : url du poster du film
    - vote_count : nombre de personnes qui ont voté
    - vote_average : note moyenne des personnes qui ont voté
    
    Pour les relations étrangères (* à 1)
    - id_directeur : clé étrangère montrant le réalisateur/directeur qui a fait le film
    - id_collection : clé étrangère montrant s'il fait partie ou non d'une collection
    
    Pour les relations étrangères (* à *)
    - genres : permet de voir les genres associés au film en question
    - companies : permet de voir les companies de productions associées au film en question
    - acteurs : permet de voir les acteurs associés au film en question
    - langages : permet de voir les langues disponibles du film en question
    """
    __tablename__ = "films"  # Table name in SQLite

    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date)
    popularity = db.Column(db.Float)
    runtime = db.Column(db.Float)
    budget = db.Column(db.Float)    
    revenue = db.Column(db.Float)
    tagline = db.Column(db.Text)
    overwiew = db.Column(db.Text)
    poster_path = db.Column(db.Text)
    vote_count = db.Column(db.Integer, nullable=False)
    vote_average = db.Column(db.Float)

    # Création des clés étrangères
    id_directeur = db.Column(db.Integer, 
                             db.ForeignKey("directeurs.id"))

    id_collection = db.Column(db.Integer,
                              db.ForeignKey("collections.id"))
    
    id_original_language = db.Column(db.Integer,
                            db.ForeignKey("languages.id"))
    
    # Création des relations étrangères (*-*)
    genres = db.relationship('Genre',
                             secondary="film_genres",
                             backref='films',
                             lazy = "dynamic")

    companies = db.relationship('Company',
                             secondary="film_companies",
                             backref='films',
                             lazy = 'dynamic')
    
    directeurs = db.relationship('Directeur',
                             secondary="film_directeurs",
                             backref='directed_films',
                             lazy="dynamic")
    
    languages = db.relationship('Language',
                             secondary="film_languages",
                             backref='films',
                             lazy="dynamic")
    
##############################
# ---- Pour la table Directeur ----
##############################
class Directeur(db.Model):
    """
    Création de la table Film dans la BDD.
    Elle contient comme colonnes :
    - id : clé primaire permettant d'identifier la ligne en question
    - nom : nom du directeur
    - prenom : prénom du directeur
    """

    __tablename__ = "directeurs"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(70))
    prenom = db.Column(db.String(70))
    
    # Création de la relation avec la clé étrangère (1-*)
    films = db.relationship('Film', backref = 'directeur',
    lazy = 'dynamic') # Modif au niveau du backref car on ne peut pas mettre le même nom plusieurs fois

##############################
# ---- Pour la table Genre ----
##############################
class Genre(db.Model):
    """
    Création de la table Genre dans la BDD.
    Elle contient comme colonnes :
    - id : clé primaire permettant d'identifier la ligne en question
    - genre : le genre associé
    """
    __tablename__ = "genres"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre = db.Column(db.String(20), nullable=False)

##############################
# ---- Pour la table Collection ----
##############################
class Collection(db.Model):
    """
    Création de la table Collection dans la BDD.
    Elle contient comme colonnes :
    - id : clé primaire permettant d'identifier la ligne en question
    - name : nom de la collection 
    """
    __tablename__="collections"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    name = db.Column(db.String(90))

    # Création de la relation avec la clé étrangère (1-*)
    films = db.relationship('Film', backref = 'collection',
    lazy = 'dynamic') # Modif au niveau du backref car on ne peut pas mettre le même nom plusieurs fois

##############################
# ---- Pour la table Acteur ----
##############################
class Acteur(db.Model):
    """
    Création de la table Acteur dans la BDD.
    Elle contient comme colonnes :
    - id : clé primaire permettant d'identifier la ligne en question
    - nom : nom de l'acteur
    - prenom : prénom de l'acteur
    """
    __tablename__="acteurs"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(70))
    prenom = db.Column(db.String(70))


##############################
# ---- Pour la table Language ----
##############################
class Language(db.Model):
    """
    Création de la table Langage dans la BDD.
    Elle contient comme colonnes :
    - id : clé primaire permettant d'identifier la ligne en question
    - langage : la langue en question
    """
    __tablename__="languages"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    language = db.Column(db.String(50), nullable=False)

    # Création de la relation avec la clé étrangère (1-*)
    films_org = db.relationship('Film', backref = 'language_org',
    lazy = 'dynamic') # Modif au niveau du backref car on ne peut pas mettre le même nom plusieurs fois

##############################
# ---- Pour la table Production_Company ----
##############################
class Company(db.Model):
    """
    Création de la table Companie dans la BDD.
    Elle contient comme colonnes :
    - id : clé primaire permettant d'identifier la ligne en question
    - name : nom de la companie
    """
    __tablename__="companies"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    name = db.Column(db.String(150), nullable=False)


##############################
# ---- Création des tables d'associations (*-*) ----
##############################

# Pour Film et Genre
film_genres = db.Table(
    'film_genres',

    db.Column('id_film', db.Integer,
              db.ForeignKey("films.id"), primary_key=True),
    
    db.Column('id_genres', db.Integer,
              db.ForeignKey('genres.id'), primary_key=True)
)

# Pour Film et Company
film_companies = db.Table(
    'film_companies',

    db.Column('id_film', db.Integer,
              db.ForeignKey("films.id"), primary_key=True),
    
    db.Column('id_companies', db.Integer,
              db.ForeignKey('companies.id'), primary_key=True)
)

# Pour Film et Director
film_directeurs = db.Table(
    'film_directeurs',

    db.Column('id_film', db.Integer,
              db.ForeignKey("films.id"), primary_key=True),
    
    db.Column('id_directeur', db.Integer,
              db.ForeignKey('directeurs.id'), primary_key=True)
)

# Pour Film et Language
film_languages = db.Table(
    'film_languages',

    db.Column('id_film', db.Integer,
              db.ForeignKey("films.id"), primary_key=True),
    
    db.Column('id_language', db.Integer,
              db.ForeignKey('languages.id'), primary_key=True)
)
