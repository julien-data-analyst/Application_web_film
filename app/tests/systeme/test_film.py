#################################################
# Auteurs : Julien RENOULT
# Date : 11/03/2025
# Sujet : test d'un outil décsionnel (film)
#################################################

from app import db
from bs4 import BeautifulSoup # Pour trouver les données facilement
import re

def test_top_10_films_plus_chers(client, exemples_films, exemple_genre):
    """
    Fonction : permet de tester si on détecte bien les dix films les plus chers dans le bon ordre

    Arguments :
    - client : TEST client de l'application Flask
    - exemples_films : liste d'instances de films
    """

    # Ajouter les dix films dans notre base de données tests + le genre
    db.session.add(exemple_genre)
    db.session.commit()
    for film in exemples_films:
        db.session.add(film)
        exemple_genre.films.append(film)
    db.session.commit()

    # Exécutons l'url permettant d'obtenir la page web contenant ces différents top 10
    rep = client.get("/film")
    html_page = rep.data.decode("utf-8")

    # Vérifions le statut de la réponse
    assert rep.status_code == 200

    # Vérifions le contenu de la réponse pour le top 10 des films les plus chers
    
    # Parser le HTML avec BeautifulSoup
    soup = BeautifulSoup(html_page, "html.parser")

    # Regardons la liste des films
    films = soup.select("ul li.list-unstyled")
    films_budgets = []
    for element in films:
        text = element.get_text(strip=True)  # Récupérer le texte brut de l'élément li

        # L'expression ci-dessous permet de regarder si on trouve le titre et le budget dans notre texte
        film_budget = re.search(r'Titre : (.*?) \| Budget : ([\d]+) M \$', text)

        # S'il n'est pas None
        if film_budget:
            # Ajoutons le titre et le budget dans la liste
            print(film_budget.groups())
            titre, budget = film_budget.groups()
            films_budgets.append((titre, int(budget)))

    # Vérifier que les films sont bien triés du plus cher au moins cher
    films_budgets_triees = sorted(films_budgets, key=lambda x: x[1], reverse=True)

    assert films_budgets == films_budgets_triees, "Les films ne sont pas triés correctement par budget !"

def test_top_10_films_plus_rentables(client, exemples_films, exemple_genre):
    """
    Fonction : permet de tester si on détecte bien les dix films les plus rentable dans le bon ordre

    Arguments :
    - client : TEST client de l'application Flask
    - exemples_films : liste d'instances de films
    """

    # Ajouter les dix films dans notre base de données tests + le genre
    db.session.add(exemple_genre)
    db.session.commit()
    for film in exemples_films:
        db.session.add(film)
        exemple_genre.films.append(film)
    db.session.commit()

    # Exécutons l'url permettant d'obtenir la page web contenant ces différents top 10
    rep = client.get("/film")
    html_page = rep.data.decode("utf-8")

    # Vérifions le statut de la réponse
    assert rep.status_code == 200

    # Vérifions le contenu de la réponse pour le top 10 des films les plus chers
    
    # Parser le HTML avec BeautifulSoup
    soup = BeautifulSoup(html_page, "html.parser")

    # Regardons la liste des films
    films = soup.select("ul li.list-unstyled")
    films_ratio = []
    for element in films:
        text = element.get_text(strip=True)  # Récupérer le texte brut de l'élément li

        # L'expression ci-dessous permet de regarder si on trouve le titre et le ratio dans notre texte
        film_ratio = re.search(r'Titre : (.*?) \| Ratio revenue/budget : ([\d]+) M \$', text)

        # S'il n'est pas None
        if film_ratio:
            # Ajoutons le titre et le budget dans la liste
            print(film_ratio.groups())
            titre, budget = film_ratio.groups()
            films_ratio.append((titre, int(budget)))

    # Vérifier que les films sont bien triés du plus cher au moins cher
    films_ratio_triees = sorted(films_ratio, key=lambda x: x[1], reverse=True)

    assert films_ratio == films_ratio_triees, "Les films ne sont pas triés correctement par ratio !"    

def test_films_max_genre(client, exemples_films, exemple_genre):
    """
    Fonction : permet de tester si on détecte bien le genre le plus répandue parmi les films

    Arguments :
    - client : TEST client de l'application Flask
    - exemples_films : liste d'instances de films
    - exemple_genre : instance de genre
    """

    # Ajouter les dix films + le genre
    db.session.add(exemple_genre)
    db.session.commit()
    for film in exemples_films:
        db.session.add(film)
        exemple_genre.films.append(film)
    db.session.commit()

    # Exécutons l'url permettant d'obtenir la page web contenant ces différents top 10
    rep = client.get("/film")
    html_page = rep.data.decode("utf-8")

    # Vérifions le statut de la réponse
    assert rep.status_code == 200

    # Regardons le contenu concerné par le genre le plus répandu
    soup = BeautifulSoup(html_page, "html.parser")
    elements_h3 = soup.select("h3.title_kpi") # Récupérer tous les éléments qui sont la balise h3
    elements_h4 = soup.select("h4.kpi")

    # Vérifier si le genre en question est bien dans cette liste et qu'on a le bon nombre pour ce genre
    assert elements_h3[0].get_text(strip=True) == "Action"
    assert elements_h4[0].get_text(strip=True) == str(len(list(exemple_genre.films))) + " films"