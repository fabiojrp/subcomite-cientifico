$(document).ready(() => {

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    region = urlParams.get('region');
    
    var width = document.documentElement.clientWidth;
    var map;

    function teste() {
        if (width > 1024) {
            return [-27.587776543236944, -51.151320339703375]
        }else {
            return [-30.916065412264867, -50.64844684943738]
        }
    }
    if (region == null) {
        map = L.map('map', { 
            zoomControl: false,
             center: teste(),
            //  [-27.587776543236944, -51.151320339703375], 
            zoom: 8,
        });
        // $.ajax({
        //     type: 'GET',
        //     url: base_url + '/api/properties/' + 5,
        //     success: function(data) {
        //         dat = data.properties
        //         var dat2 = JSON.stringify(dat) + ",";      
        //         console.log(dat2) 
        //         return stateData.features[2].properties = dat2;
                 
        //    }
        //  }),
        //  ttt = {"name":"CARBONIFERA","rt":0.99,"media_movel":"55%","ocupacao_leitos":"99%","path":"carbonifera.html"}
        L.geoJson(stateData).addTo(map);
    } else {
        map = L.map('map', { 
            zoomControl: false,
            center: regionData.features[0].properties.center, 
            zoom: regionData.features[0].properties.zoom
        });
        
        L.geoJson(regionData).addTo(map);
    }
    if (width < 1024) {
        map.setZoom(6);
        map.panTo(new L.LatLng(-227.587776543236944, -51.151320339703375));
        document.querySelector('#map')
        .classList
        .add('mobile');
    }
    window.addEventListener('resize', function(event){
        var width = document.documentElement.clientWidth;
        if (width < 1200) {
            // set the zoom level to 10
            map.setZoom(7);
        }else if (width < 787) {
            // set the zoom level to 8
            map.setZoom(5);
        }else{
            map.setZoom(8);
        }
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
    var sao_bento_do_sul = L.marker([-26.25027687276346, -49.35088784121336]).bindPopup('IFC - Campus São Bento do Sul');
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
          (props ? '<h4><b>Regional:</b> ' + props.name + '</h4><p>Taxa de Transmissibilidade: ' + props.rt + '</p><p>Média Móvel: ' + props.media_movel + '</p><p>Ocupação de Leitos: ' + props.ocupacao_leitos +'</p><p><a href="'+ props.path + '?region=1">Saiba mais sobre essa região</a></p>' : '<h4>Dados</h4><p>Clique nas regiões da saúde para saber mais.</p>');
    };
    
    if (regionData === null) {
        info.addTo(map);
    }

	

    // TODO: Fazer a cor verde:
    // RT: < 1
    // Média Móvel < 15%
    // UTI < 60%
	// get color depending on rt value
	function getColor(d) {
        return d >= 1 ? '#ff7979' :
               d < 1 && d >= 0 ? '#f9ca24' : "transparent";
	}

	function style(feature) {
		return {
			weight: 2,
			opacity: 1,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.5,
			fillColor:  getColor(feature.properties.child ? -1 : feature.properties.rt)
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

    if (regionData !== null) {
        geojson = L.geoJson(regionData, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);

    } else {
        geojson = L.geoJson(stateData, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);
    }

	

	map.attributionControl.addAttribution('Dados do Covid &copy; <a href="https://covid.saude.gov.br/">Ministério da Saúde</a>');
    map.attributionControl.addAttribution('Dados de UTI &copy; <a href="https://www.ciasc.sc.gov.br/">CIASC</a>');


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
				'<i style="background:' + getColor(from) + '"></i> ' +
				from + (to ? '&ndash;' + to + '(Surto Controlado)<br />' : '+  (Transmissão Comunitária)'));
		}

		div.innerHTML = labels.join('<br>');
		return div;
	};

	legend.addTo(map);

    // END LEAF


});
