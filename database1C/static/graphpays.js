const ctx = document.getElementById('ChartPays');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: liste_labels_pays,
    datasets: [{
      label: 'TOP 10 Ventes par Pays',
      data: liste_datas_pays,
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