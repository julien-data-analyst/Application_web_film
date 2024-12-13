

/* Création de la fonction récupérant les données nécessaires */

 async function donnees_films_par_genre() {
    var response = await fetch("/api/data/films_par_genre"); /* Chercher les données JSON sur l'adresse correspondante */
    var data = await response.json(); /* Transformation en variable manipulable */

    /* Création des deux listes */
    var label = data.mod
    var valeur = data.eff

    /* Vérification du succès de l'opération */
    console.log(label)
    console.log(valeur)

    /* Création du visuel graphique avec ChartJS */
    /* À VOIR PLUS TARD */
}

donnees_films_par_genre()

async function donnees_films_par_annee() {
    var response = await fetch("/api/data/films_par_annee"); /* Chercher les données JSON sur l'adresse correspondante */
    var data = await response.json(); /* Transformation en variable manipulable */

    /* Création des deux listes */
    var label = data.mod
    var valeur = data.eff

    /* Vérification du succès de l'opération */
    console.log(label)
    console.log(valeur)

    /* Création du visuel graphique avec ChartJS */
    /* À VOIR PLUS TARD */
}

donnees_films_par_annee()

async function donnees_films_par_langue() {
    var response = await fetch("/api/data/films_par_langue"); /* Chercher les données JSON sur l'adresse correspondante */
    var data = await response.json(); /* Transformation en variable manipulable */

    /* Création des deux listes */
    var label = data.mod
    var valeur = data.eff

    /* Vérification du succès de l'opération */
    console.log(label)
    console.log(valeur)

    /* Création du visuel graphique avec ChartJS */
    /* À VOIR PLUS TARD */
}

donnees_films_par_langue()




