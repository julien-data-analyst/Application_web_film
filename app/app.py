#################################################
# Auteurs : Julien RENOULT - Yop JUGUL DALYOP - Gabriel DURAND - Ryan DOBIGNY
# Date : 03/12/2024
# Sujet : création d'une application web (lanceur)
#################################################

# Chargement des librairies
import os
from modele_bdd import db, Collection, Film, Directeur, Genre, Acteur, Language, Company
from config import app
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# Attention : se placer dans le dossier app pour tester le programme
# Si base déjà créée : supprimer la base en question pour éviter le moindre problème dans la création de table si modif au niveau des colonnes/tables

# ---- Test provisoire sur la création du BDD ----
db.init_app(app)

if not(os.path.exists("instance/films.db")):
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

# Access data
film = namespace["film"]
genre = namespace["genre"]
collection = namespace["collection"]
original_language = namespace["original_language"]
spoken_languages = namespace["spoken_language"]
production = namespace["production"]
actor = namespace["actor"]
director = namespace["director"]

# ---------------------------------------------------- #

with app.app_context():
    for index, row in collection.iterrows():
        collection = Collection(id=row["id"], name=row["belongs_to_collection"])
        db.session.add(collection)
    db.session.commit()
    print("Collections data inserted successfully!")
    
with app.app_context():
    for index, row in actor.iterrows():
        actor = Acteur(id=row["id"], name=row["person"])
        db.session.add(actor)
    db.session.commit()
    print("Actors successfully added.")