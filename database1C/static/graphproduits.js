const ctx = document.getElementById('ChartProduits');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: liste_labels_produits,
    datasets: [{
      label: 'TOP 10 Ventes par Produits',
      data: liste_datas_produits,
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});
