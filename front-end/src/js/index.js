$(document).ready(() => {



    var map = L.map('map', { 
        zoomControl: false,
        center: [-27.587776543236944, -51.151320339703375], 
        zoom: 8
    });

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    mapboxAccessToken = 'pk.eyJ1IjoibWFuZmUiLCJhIjoiY2tranBsdWlxMG01OTJ3cW55YjhudW01cSJ9.quumn6h49KGEftd4odva2A';

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
        id: 'mapbox/light-v10',
        attribution: "Subcomitê Ciêntifico",
        tileSize: 512,
        zoomOffset: -1
    }).addTo(map);

    L.geoJson(regionData).addTo(map);

    var videira = L.marker([-27.026555588666362, -51.14521223224076]).bindPopup('IFC - Campus Videira');
    var luzerna = L.marker([-27.132361991407368, -51.46302556370465]).bindPopup('IFC - Campus Luzerna');
    var fraiburgo = L.marker([-27.030183953471692, -50.91809746417005]).bindPopup('IFC - Campus Fraiburgo');
    var riodosul = L.marker([-27.21220797789442, -49.639967538355734]).bindPopup('IFC - Campus Rio do Sul - Unidade Urbana');
    var riodosul2 = L.marker([-27.18469255860665, -49.66081786276957]).bindPopup('IFC - Campus Rio do Sul - Sede');
    var riodosul3 = L.marker([-27.211806140692513, -49.65704082501049]).bindPopup('IFC - Campus Rio do Sul - Unidade Tecnológica');
    var sombrio = L.marker([-29.101905323823694, -49.63864611448503]).bindPopup('IFC - Campus Sombrio');
    var sao_francisco_do_sul = L.marker([-26.21763874417492, -48.57035665361086]).bindPopup('IFC - Campus São Francisco de Sul');
    var araquari = L.marker([-26.394781055206387, -48.73823989999723]).bindPopup('IFC - Campus Araquari');
    var abelardo_luz = L.marker([-26.586521596148813, -52.10501674417086]).bindPopup('IFC - Campus Abelardo Luz (Avançado)');
    var sao_bento_do_sul = L.marker([-26.21763874417492, -48.57035665361086]).bindPopup('IFC - Campus São Bento do Sul');
    var santa_rosa_do_sul = L.marker([-29.0954650121907, -49.81419731861792]).bindPopup('IFC - Campus Santa Rosa do Sul');
    var ibirama = L.marker([-27.04909677497824, -49.53896279407205]).bindPopup('IFC - Campus Ibirama');
    var blumenau = L.marker([-26.881739150584163, -49.137095301484216]).bindPopup('IFC - Campus Blumenau');
    var concordia = L.marker([-27.201912072094206, -52.08319161549669]).bindPopup('IFC - Campus Concórdia');
    var blumenau2 = L.marker([-26.912126542043502, -49.0664407730001]).bindPopup('IFC - Reitoria');
    var camboriu = L.marker([-27.015680100497377, -48.65878562611805]).bindPopup('IFC - Campus Camboriú');
    var brusque = L.marker([-27.09941598304748, -48.92860645226999]).bindPopup('IFC - Campus Brusque');

    
    var campus = L.layerGroup(
        [
            videira, luzerna, fraiburgo, riodosul, riodosul2, 
            riodosul3, sombrio, sao_francisco_do_sul, abelardo_luz, sao_bento_do_sul,
            santa_rosa_do_sul, araquari, ibirama, blumenau, concordia, blumenau2, camboriu, brusque
        ]).addTo(map);

	// control that shows state info on hover
	var info = L.control({position: 'topleft'});

	info.onAdd = function (map) {
		this._div = L.DomUtil.create('div', 'map-info');
		this.update();
		return this._div;
	};

	info.update = function (props) {
        this._div.innerHTML = '' +  
          (props ? '<h4><b>Regional:</b> ' + props.name + '</h4><p>Taxa de Transmissibilidade: ' + props.rt + '</p><p>Média Móvel: ' + props.media_movel + '</p><p>Ocupação de Leitos: ' + props.ocupacao_leitos +'</p><p><a href="#">Saiba mais sobre essa região</a></p>' : '<h4>Dados</h4><p>Clique nas regiões da saúde para saber mais.</p>');
	};

	info.addTo(map);


	// get color depending on rt value
	function getColor(d) {
		return d >= 1 ? '#ff7979' : '#f9ca24';
	}

	function style(feature) {
		return {
			weight: 2,
			opacity: 1,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.5,
			fillColor: getColor(feature.properties.rt)
		};
	}

	function highlightFeature(e) {
        geojson.resetStyle();
		var layer = e.target;

		layer.setStyle({
			weight: 5,
			color: '#666',
			dashArray: '',
			fillOpacity: 0.7
		});

		if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
			layer.bringToFront();
		}

		info.update(layer.feature.properties);
	}

	var geojson;

	function resetHighlight(e) {
		geojson.resetStyle(e.target);
		info.update();
	}

	function onEachFeature(feature, layer) {
		layer.on({
            click: highlightFeature,            
		});
	}

	geojson = L.geoJson(regionData, {
		style: style,
		onEachFeature: onEachFeature
	}).addTo(map);

	map.attributionControl.addAttribution('Dados do Covid &copy; <a href="https://www.ciasc.sc.gov.br/">CIASC</a>');


	var legend = L.control({position: 'bottomleft'});

	legend.onAdd = function (map) {

		var div = L.DomUtil.create('div', 'map-info legend'),
			grades = [0, 1],
			labels = ["<b>R(t) - Taxa de Transmissibilidade</b> </br>"],
			from, to;

		for (var i = 0; i < grades.length; i++) {
			from = grades[i];
			to = grades[i + 1];

			labels.push(
				'<i style="background:' + getColor(from + 1) + '"></i> ' +
				from + (to ? '&ndash;' + to : '+'));
		}

		div.innerHTML = labels.join('<br>');
		return div;
	};

	legend.addTo(map);



    // END LEAF


    /* 
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
    */
});
