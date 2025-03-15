from flask import jsonify

import pytest
from config import app
from modele_bdd import db, Acteur

@app.route('/acteur', methods=["GET"])
def liste_acteurs():
    """
    Retourne la liste des acteurs présents dans la BDD au format JSON.
    """
    from modele_bdd import Acteur  # Assure-toi que le modèle Acteur est importé
    acteurs = Acteur.query.all()
    acteurs_list = [{"id": a.id, "nom": a.nom, "prenom": a.prenom} for a in acteurs]
    return jsonify(acteurs_list)






@pytest.fixture
def client():
    """
    Fixture qui configure l'application Flask en mode test, 
    utilise une base de données SQLite en mémoire et initialise quelques acteurs.
    """
    app.config["TESTING"] = True
    # Utiliser une base en mémoire pour isoler le test
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Insertion de quelques acteurs pour le test
            acteur1 = Acteur(id=1, nom="Doe", prenom="John")
            acteur2 = Acteur(id=2, nom="Smith", prenom="Anna")
            db.session.add_all([acteur1, acteur2])
            db.session.commit()
        yield client
        # Nettoyage après le test
        with app.app_context():
            db.drop_all()

def test_liste_acteurs(client):
    """
    Teste la route /acteur pour vérifier qu'elle retourne bien la liste des acteurs.
    """
    response = client.get("/acteur")
    assert response.status_code == 200
    data = response.get_json()
    # Vérifie que la réponse est une liste
    assert isinstance(data, list)
    # Vérifie que les acteurs insérés apparaissent dans la réponse
    assert any(acteur["nom"] == "Doe" for acteur in data)
    assert any(acteur["nom"] == "Smith" for acteur in data)
