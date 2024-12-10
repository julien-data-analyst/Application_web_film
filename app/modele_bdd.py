# Import the necessary libraries
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#########################################
### Define the database models ###
########################################

##############################
# ---- Film Table ----
##############################
class Film(db.Model):
    __tablename__ = "films"  # Table name in SQLite

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
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

    # Foreign keys
    id_directeur = db.Column(db.Integer, db.ForeignKey("directeurs.id"))
    id_collection = db.Column(db.Integer, db.ForeignKey("collections.id"))

    # Relationships
    genres = db.relationship(
        'Genre', secondary="film_genres", backref="films"
    )
    companies = db.relationship(
        'Company', secondary="film_companies", backref="films"
    )
    acteurs = db.relationship(
        'Acteur', secondary="film_acteurs", backref="films"
    )

    # Define the relationship to the Collection model
    collection = db.relationship("Collection", back_populates="films")


##############################
# ---- Directeur Table ----
##############################
class Directeur(db.Model):
    __tablename__ = "directeurs"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    nom = db.Column(db.String(70), nullable=False)
    prenom = db.Column(db.String(70), nullable=False)

    # Relationship to Film
    films = db.relationship("Film", backref="directeur", lazy="dynamic")


##############################
# ---- Genre Table ----
##############################
class Genre(db.Model):
    __tablename__ = "genres"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    genre = db.Column(db.String(20), nullable=False)


##############################
# ---- Collection Table ----
##############################
class Collection(db.Model):
    __tablename__ = "collections"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    name = db.Column(db.String(90), nullable=False)

    # Relationship to Film
    films = db.relationship("Film", back_populates="collection", lazy="dynamic")


##############################
# ---- Acteur Table ----
##############################
class Acteur(db.Model):
    __tablename__ = "acteurs"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    nom = db.Column(db.String(70), nullable=False)
    prenom = db.Column(db.String(70), nullable=False)


##############################
# ---- Language Table ----
##############################
class Language(db.Model):
    __tablename__ = "languages"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    language = db.Column(db.String(50), nullable=False)


##############################
# ---- Production Company Table ----
##############################
class Company(db.Model):
    __tablename__ = "companies"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    name = db.Column(db.String(150), nullable=False)


##############################
# ---- Association Tables ----
##############################

# Association table for Film and Genre
film_genres = db.Table(
    'film_genres',
    db.Column('id_film', db.Integer, db.ForeignKey("films.id"), primary_key=True),
    db.Column('id_genres', db.Integer, db.ForeignKey("genres.id"), primary_key=True)
)

# Association table for Film and Company
film_companies = db.Table(
    'film_companies',
    db.Column('id_film', db.Integer, db.ForeignKey("films.id"), primary_key=True),
    db.Column('id_companies', db.Integer, db.ForeignKey("companies.id"), primary_key=True)
)

# Association table for Film and Acteur
film_acteurs = db.Table(
    'film_acteurs',
    db.Column('id_film', db.Integer, db.ForeignKey("films.id"), primary_key=True),
    db.Column('id_acteur', db.Integer, db.ForeignKey("acteurs.id"), primary_key=True)
)

# Association table for Film and Language
film_languages = db.Table(
    'film_languages',
    db.Column('id_film', db.Integer, db.ForeignKey("films.id"), primary_key=True),
    db.Column('id_language', db.Integer, db.ForeignKey("languages.id"), primary_key=True),
    db.Column('original', db.Boolean, nullable=False)
)
