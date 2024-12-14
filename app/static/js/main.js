document.addEventListener("DOMContentLoaded", function () {
  // Variable globale pour stocker les graphiques créés
  const charts = {};

  // Fonction générique pour récupérer les données depuis une API
  async function fetchData(apiEndpoint) {
    try {
      const response = await fetch(apiEndpoint);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return { labels: data.mod, valeurs: data.eff };
    } catch (error) {
      console.error(`Erreur lors de la récupération des données depuis ${apiEndpoint}:`, error);
      return { labels: [], valeurs: [] };
    }
  }

  // Fonction générique pour créer un graphique
  async function createChart(chartId, apiEndpoint, chartLabel) {
    const chartElement = document.getElementById(chartId);

    if (!chartElement) {
      console.error(`Impossible de trouver l'élément avec l'ID '${chartId}'.`);
      return;
    }

    const { labels, valeurs } = await fetchData(apiEndpoint);

    if (labels.length === 0 || valeurs.length === 0) {
      console.warn(`Aucune donnée disponible pour le graphique '${chartId}'.`);
      return;
    }

    // Vérifie si un graphique existe déjà pour ce canvas et le détruit
    if (charts[chartId]) {
      charts[chartId].destroy();
    }

    // Création et stockage du nouveau graphique
    charts[chartId] = new Chart(chartElement, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [
          {
            label: chartLabel,
            data: valeurs,
            borderWidth: 1,
            backgroundColor: [
              '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
              '#FF9F40', '#66FF66', '#FF66B2', '#6699FF', '#CCCC00',
              '#FF9900', '#FF3300', '#33CC33', '#33CCCC', '#3366FF',
              '#6600CC', '#9900FF', '#CC0066', '#00CCCC', '#0099CC'
          ]
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          tooltip: {
            enabled: true
          }
        }
      }
    });
  }

  // Création des trois graphiques
  createChart('myChart', '/api/data/films_par_genre', 'Nombre de Films par Genre');
  createChart('myChart2', '/api/data/films_par_langue', 'Nombre de Films par Langue');
  createChart('myChart3', '/api/data/films_par_annee', 'Nombre de Films par Année');
});






















