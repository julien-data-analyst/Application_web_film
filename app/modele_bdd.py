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
                             backref='films')

    companies = db.relationship('Companie',
                             secondary="film_companies",
                             backref='films')
    
    acteurs = db.relationship('Acteur',
                             secondary="film_acteurs",
                             backref='films')
    
##############################
# ---- Pour la table Directeur ----
##############################
class Directeur(db.Model):
    __tablename__ = "directeurs"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(70), nullable=False)
    prenom = db.Column(db.String(70), nullable=False)

    # Création de la relation avec la clé étrangère (1-*)
    films = db.relationship('Film', backref = 'film',
    lazy = 'dynamic')

##############################
# ---- Pour la table Genre ----
##############################
class Genre(db.Model):
    __tablename__ = "genres"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(20), nullable=False)

##############################
# ---- Pour la table Collection ----
##############################
class Collection(db.Model):
    __tablename__="collections"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)

    # Création de la relation avec la clé étrangère (1-*)
    films = db.relationship('Film', backref = 'film',
    lazy = 'dynamic')

##############################
# ---- Pour la table Acteur ----
##############################
class Acteur(db.Model):
    __tablename__="acteurs"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(70), nullable=False)
    prenom = db.Column(db.String(70), nullable=False)


##############################
# ---- Pour la table Langage ----
##############################
class Langage(db.Model):
    __tablename__="langages"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True)
    langage = db.Column(db.String(50), nullable=False)


##############################
# ---- Pour la table Production_Company ----
##############################
class Companie(db.Model):
    __tablename__="companies"
    
    # Création des différentes colonnes
    # La clé primaire : id
    id = db.Column(db.Integer, primary_key=True)
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

# Pour Film et Companie
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

# Pour Film et Langage
film_langages = db.Table(
    'film_langages',

    db.Column('id_film', db.Integer,
              db.ForeignKey("films.id"), primary_key=True),
    
    db.Column('id_langage', db.Integer,
              db.ForeignKey('langages.id'), primary_key=True),
    
    db.Column('original', db.Boolean, nullable=False)
)