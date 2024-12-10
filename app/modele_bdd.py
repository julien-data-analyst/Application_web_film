#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024
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
    __tablename__= "films" # Nom de la table dans la BDD SQLite

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
    
    # Création des relations étrangères (*-*)
    genres = db.relationship('Genre',
                             secondary="film_genres",
                             backref='films',
                             lazy = "dynamic")

    companies = db.relationship('Company',
                             secondary="film_companies",
                             backref='films',
                             lazy = 'dynamic')
    
    acteurs = db.relationship('Acteur',
                             secondary="film_acteurs",
                             backref='films',
                             lazy="dynamic")
    
    languages = db.relationship('Language',
                             secondary="film_languages",
                             backref='films',
                             lazy="dynamic")
    
##############################
# ---- Pour la table Directeur ----
##############################
class Directeur(db.Model):
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
    __tablename__ = "genres"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre = db.Column(db.String(20), nullable=False)

##############################
# ---- Pour la table Collection ----
##############################
class Collection(db.Model):
    __tablename__="collections"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(90), nullable=False)

    # Création de la relation avec la clé étrangère (1-*)
    films = db.relationship('Film', backref = 'collection',
    lazy = 'dynamic') # Modif au niveau du backref car on ne peut pas mettre le même nom plusieurs fois

##############################
# ---- Pour la table Acteur ----
##############################
class Acteur(db.Model):
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
    __tablename__="languages"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    language = db.Column(db.String(50), nullable=False)


##############################
# ---- Pour la table Production_Company ----
##############################
class Company(db.Model):
    __tablename__="companies"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))


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

# Pour Film et Acteur
film_acteurs = db.Table(
    'film_acteurs',

    db.Column('id_film', db.Integer,
              db.ForeignKey("films.id"), primary_key=True),
    
    db.Column('id_acteur', db.Integer,
              db.ForeignKey('acteurs.id'), primary_key=True)
)

# Pour Film et Language
film_languages = db.Table(
    'film_languages',

    db.Column('id_film', db.Integer,
              db.ForeignKey("films.id"), primary_key=True),
    
    db.Column('id_language', db.Integer,
              db.ForeignKey('languages.id'), primary_key=True),
    
    db.Column('original', db.Boolean, nullable=False)
)