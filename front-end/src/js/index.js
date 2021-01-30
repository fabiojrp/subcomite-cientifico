$(document).ready(() => {

  

  var map = L.map('map').setView([-27.587776543236944, -51.151320339703375], 8);
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  mapboxAccessToken = 'pk.eyJ1IjoibWFuZmUiLCJhIjoiY2tranBsdWlxMG01OTJ3cW55YjhudW01cSJ9.quumn6h49KGEftd4odva2A';

  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    id: 'mapbox/light-v10',
    attribution: "blabla",
    tileSize: 512,
    zoomOffset: -1
  }).addTo(map);

  L.geoJson(regionData).addTo(map);




  


  google.load("visualization", "1", { packages: ["corechart", "line"] });
  google.setOnLoadCallback(grafico);
  function grafico() {
    var json_text = $.ajax({
      method: "post",
      url: "new.php",
      dataType: "json",
      async: false,
    }).responseText;
    var dados = new google.visualization.DataTable(json_text);

    var options = {
      title: "Casos Confirmados",
      colors: ["#1C1C61", "#5f0404"],
      titlePosition: "center",
      hAxis: {
        title: "Meses",
        titleTextStyle: { color: "#5f0404" },
        baselineColor: "#000",
        format: "MM/yy",
        gridlines: { count: 20 },
      },
      backgroundColor: { strokeWidth: 1, fill: "#F0F0F0" },
      dataOpacity: 3,
    };

    var chart = new google.visualization.LineChart(
      document.getElementById("chart_casos_confirmados")
    );
    chart.draw(dados, options);
  }

  google.load("visualization", "1", { packages: ["corechart"] });
  google.setOnLoadCallback(drawChart2);
  function drawChart2() {
    var data = google.visualization.arrayToDataTable([
      ["Meses", "Casos Confirmados", "Casos Ativos"],
      ["Mar/20", 1000, 400],
      ["Abr/20", 1200, 300],
      ["Mai/20", 1400, 450],
      ["Jun/20", 1600, 410],
      ["Jul/20", 1800, 420],
      ["Ago/20", 2000, 860],
      ["Set/20", 2200, 1020],
      ["Out/20", 2400, 540],
      ["Nov/20", 2600, 300],
      ["Dez/20", 2800, 200],
      ["Jan/21", 3000, 800],
    ]);

    var options = {
      title: "Taxa de Letalidade",
      colors: ["#3232AD", "#5f0404"],
      hAxis: { title: "Meses", titleTextStyle: { color: "#333" } },
      vAxis: { minValue: 0 },
    };

    var chart = new google.visualization.AreaChart(
      document.getElementById("chart_taxa_letalidade")
    );
    chart.draw(data, options);
  }

  google.charts.load("current", { packages: ["corechart"] });
  google.charts.setOnLoadCallback(drawChart3);

  function drawChart3() {
    // Some raw data (not necessarily accurate)
    var data = google.visualization.arrayToDataTable([
      ["Meses", "Casos Confirmados", "Casos Ativos"],
      ["Mar/20", 1000, 400],
      ["Abr/20", 1200, 300],
      ["Mai/20", 1400, 450],
      ["Jun/20", 1600, 410],
      ["Jul/20", 1800, 420],
      ["Ago/20", 2000, 860],
      ["Set/20", 2200, 1020],
      ["Out/20", 2400, 540],
      ["Nov/20", 2600, 300],
      ["Dez/20", 2800, 200],
      ["Jan/21", 3000, 800],
    ]);

    var options = {
      title: "Média Móvel de Casos",
      vAxis: { title: "Quantidade de casos" },
      hAxis: { title: "Meses" },
      colors: ["#3232AD", "#5f0404"],
      seriesType: "bars",
      backgroundColor: { strokeWidth: 1, fill: "#F0F0F0" },
      series: { 1: { type: "line" } },
    };

    var chart = new google.visualization.ComboChart(
      document.getElementById("chart_media_movel")
    );
    chart.draw(data, options);
  }
  google.charts.load("current", { packages: ["corechart", "line"] });
  google.charts.setOnLoadCallback(drawChart4);

  function drawChart4() {
    var data = new google.visualization.DataTable();
    data.addColumn("number", "X");
    data.addColumn("number", "Casos");
    data.addColumn("number", "Ativos");

    data.addRows([
      [0, 0, 0],
      [5, 1000, 400],
      [10, 2000, 800],
      [15, 2300, 550],
      [20, 3000, 600],
      [25, 2000, 500],
      [30, 1000, 600],
      [35, 6300, 1550],
      [40, 5000, 2000],
      [45, 8000, 4200],
      [50, 1000, 800],
      [55, 300, 550],
    ]);
    var options = {
      title: "Taxa de transmissibilidade R(t)",
      hAxis: {
        title: "",
      },
      vAxis: {
        title: "Quantidade de Casos",
      },
      colors: ["#3232AD", "#5f0404"],
      series: {
        0: {
          lineWidth: 6,
          lineDashStyle: [1, 1, 1],
        },
      },
    };

    var chart = new google.visualization.LineChart(
      document.getElementById("chart_rt")
    );
    chart.draw(data, options);
  }
  google.charts.load("current", { packages: ["corechart", "bar"] });
  google.charts.setOnLoadCallback(drawChart5);

  function drawChart5() {
    var data = google.visualization.arrayToDataTable([
      ["Meses", "Leitos "],
      ["Mar/20", 0],
      ["Abr/20", 30],
      ["Mai/20", 40],
      ["Jun/20", 60],
      ["Jul/20", 80],
      ["Ago/20", 90],
      ["Set/20", 90],
      ["Out/20", 60],
      ["Nov/20", 90],
      ["Dez/20", 90],
      ["Jan/21", 95],
    ]);

    var options = {
      title: "Taxa de ocupação de UTI",
      hAxis: {
        title: "%",
        minValue: 0,
      },
      vAxis: {
        title: "Meses",
      },
    };

    var chart = new google.visualization.BarChart(
      document.getElementById("chart_ocup_uti")
    );
    chart.draw(data, options);
  }

  $(window).resize(function () {
    grafico();
    drawChart2();
    drawChart3();
    drawChart4();
    drawChart5();
  });
});
