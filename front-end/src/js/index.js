$(document).ready(() => {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  region = urlParams.get("region");

  var width = document.documentElement.clientWidth;
  var map;

  function teste() {
    if (width > 1024) {
      return [-27.587776543236944, -51.151320339703375];
    } else {
      return [-30.916065412264867, -50.64844684943738];
    }
  }
  if (region == null) {
    $.ajax({
      type: "GET",
      url: base_url + "/api/dados-estado/",
      async: false,
      success: function (data) {
        stateData = get_pontuacao_regionais(data.stateData);
      },
      error: function (result) {
        console.log("Erro");
      },
    });
    map = L.map("map", {
      zoomControl: false,
      center: teste(),
      //  [-27.587776543236944, -51.151320339703375],
      zoom: 8,
    });
    L.geoJson(stateData).addTo(map);
  } else {
    $.ajax({
      type: "GET",
      url: base_url + '/api/dados-regiao/' + id,
      async: false,
      success: function (dados) {
        regionData.features[0].properties.media_movel = dados.media_movel;
        regionData.features[0].properties.rt = dados.rt;    
        regionData.features[0].properties.leitos_geral_max = dados.leitos_geral_max;
        regionData.features[0].properties.leitos_covid_max = dados.leitos_covid_max;
        regionData.features[0].properties.incidencia = dados.incidencia;
        regionData.features[0].properties.letalidade = dados.letalidade;
        regionData.features[0].properties.vacinacao_dive = dados.vacinacao_dive;
        regionData.features[0].properties.vacinacao_ms = dados.vacinacao_ms;
        regionData.features[0].properties.vacinacao_pontos = dados.vacinacao_pontos;
        regionData.features[0].properties.incidencia_sc = dados.incidencia_sc;
        regionData.features[0].properties.letalidade_sc = dados.letalidade_sc;
        regionData.features[0].properties.pontuacao = dados.pontuacao;
        regionData.features[0].properties.fase_atual = dados.fase_atual;
      },
      error: function (result) {
        console.log("Erro");
      },
    });

    map = L.map("map", {
      zoomControl: false,
      center: regionData.features[0].properties.center,
      zoom: regionData.features[0].properties.zoom,
    });

    L.geoJson(regionData).addTo(map);
  }
  if (width < 1024) {
    map.setZoom(6);
    map.panTo(new L.LatLng(-227.587776543236944, -51.151320339703375));
    document.querySelector("#map").classList.add("mobile");
  }
  window.addEventListener("resize", function (event) {
    var width = document.documentElement.clientWidth;
    if (width < 1200) {
      // set the zoom level to 10
      map.setZoom(7);
    } else if (width < 787) {
      // set the zoom level to 8
      map.setZoom(5);
    } else {
      map.setZoom(8);
    }
  });

  L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  mapboxAccessToken =
    "pk.eyJ1IjoibWFuZmUiLCJhIjoiY2tranBsdWlxMG01OTJ3cW55YjhudW01cSJ9.quumn6h49KGEftd4odva2A";

  L.tileLayer(
    "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=" +
    mapboxAccessToken,
    {
      id: "mapbox/light-v10",
      attribution: "Subcomitê Ciêntifico",
      tileSize: 512,
      zoomOffset: -1,
    },
  ).addTo(map);

  var iconBase = L.Icon.extend({
    options: {
      shadowUrl: "../css/images/marker-shadow.png",
      iconSize: [25, 41],
      iconAnchor: [12, 41]
    }
  });

  var iconIf = new iconBase({
    iconUrl: "../css/images/marker-icon.png",
  });

  var videira = L.marker([-27.026555588666362, -51.14521223224076], { icon: iconIf }).bindPopup(
    "IFC - Campus Videira",
  );
  var luzerna = L.marker([-27.132361991407368, -51.46302556370465], { icon: iconIf }).bindPopup(
    "IFC - Campus Luzerna",
  );
  var fraiburgo = L.marker([-27.030183953471692, -50.91809746417005], { icon: iconIf }).bindPopup(
    "IFC - Campus Fraiburgo",
  );
  var riodosul = L.marker([-27.21220797789442, -49.639967538355734], { icon: iconIf }).bindPopup(
    "IFC - Campus Rio do Sul - Unidade Urbana",
  );
  var riodosul2 = L.marker([-27.18469255860665, -49.66081786276957], { icon: iconIf }).bindPopup(
    "IFC - Campus Rio do Sul - Sede",
  );
  var riodosul3 = L.marker([-27.211806140692513, -49.65704082501049], { icon: iconIf }).bindPopup(
    "IFC - Campus Rio do Sul - Unidade Tecnológica",
  );
  var sombrio = L.marker([-29.101905323823694, -49.63864611448503], { icon: iconIf }).bindPopup(
    "IFC - Campus Sombrio",
  );
  var sao_francisco_do_sul = L.marker([-26.21763874417492, -48.57035665361086,], { icon: iconIf }).bindPopup(
    "IFC - Campus São Francisco de Sul");
  var araquari = L.marker([-26.394781055206387, -48.73823989999723], { icon: iconIf }).bindPopup(
    "IFC - Campus Araquari",
  );
  var abelardo_luz = L.marker([-26.586521596148813, -52.10501674417086], { icon: iconIf }).bindPopup(
    "IFC - Campus Abelardo Luz (Avançado)");
  var sao_bento_do_sul = L.marker([-26.25027687276346, -49.35088784121336], { icon: iconIf }).bindPopup(
    "IFC - Campus São Bento do Sul");
  var santa_rosa_do_sul = L.marker([-29.0954650121907, -49.81419731861792], { icon: iconIf }).bindPopup(
    "IFC - Campus Santa Rosa do Sul");
  var ibirama = L.marker([-27.04909677497824, -49.53896279407205], { icon: iconIf }).bindPopup(
    "IFC - Campus Ibirama",
  );
  var blumenau = L.marker([-26.881739150584163, -49.137095301484216], { icon: iconIf }).bindPopup(
    "IFC - Campus Blumenau",
  );
  var concordia = L.marker([-27.201912072094206, -52.08319161549669], { icon: iconIf }).bindPopup(
    "IFC - Campus Concórdia",
  );
  var blumenau2 = L.marker([-26.912126542043502, -49.0664407730001], { icon: iconIf }).bindPopup(
    "IFC - Reitoria",
  );
  var camboriu = L.marker([-27.015680100497377, -48.65878562611805], { icon: iconIf }).bindPopup(
    "IFC - Campus Camboriú",
  );
  var brusque = L.marker([-27.09941598304748, -48.92860645226999], { icon: iconIf }).bindPopup(
    "IFC - Campus Brusque",
  );

  var campusIFC = L.layerGroup([
    videira,
    luzerna,
    fraiburgo,
    riodosul,
    riodosul2,
    riodosul3,
    sombrio,
    sao_francisco_do_sul,
    abelardo_luz,
    sao_bento_do_sul,
    santa_rosa_do_sul,
    araquari,
    ibirama,
    blumenau,
    concordia,
    blumenau2,
    camboriu,
    brusque,
  ]).addTo(map);

  // control that shows state info on hover
  var info = L.control({ position: "bottomleft" });

  info.onAdd = function (map) {
    this._div = L.DomUtil.create("div", "map-info");
    this.update();
    return this._div;
  };

  //Todo: formatar os números!
  info.update = function (props) {
    this._div.innerHTML =
      "" +
      (props
        ? "<h4><b>Regional:</b> " + props.name + "</h4>" + 
        "<p>Taxa de Transmissibilidade: " + props.rt + "<span>("+ props.pontos_rt +" / 5 Pontos)</span></p>"+
        "<p>Média Móvel: " + props.media_movel.toFixed(2) + "%" + "<span>("+ props.pontos_media_movel +" / 5 Pontos)</span></p>"+
        "<p>Ocupação de Leitos UTI Adulto Geral: " + props.leitos_geral_max.toFixed(2) + "% ou " + 
        "<p>Ocupação de Leitos UTI Adulto COVID: " + props.leitos_covid_max.toFixed(2) + "%" +"<span>("+ props.pontos_leitos_max+" / 5 Pontos)</span></p>"+
        "<p> Casos acumulados por 100 mil hab: " + props.incidencia.toFixed(2) + "<span class='float_right'>("+ props.pontos_incidencia +" / 2 Pontos)</span></p>"+
        "<p> Taxa de letalidade: " +  props.letalidade.toFixed(2) + "%" + "<span>("+ props.pontos_letalidade +" / 2 Pontos)</span></p>"+
        "<p> Percentual de vacinação DIVE: " + props.vacinacao_dive.toFixed(2) + "% ou" + 
        "<p> Percentual de vacinação OpenDataSus: " + props.vacinacao_ms.toFixed(2) + "%   <span>("+ props.pontos_vacinacao +" / 3 Pontos)</span></p>"+
        "<p> Fase Atual: " + props.fase_atual + '</p>'+
        '<p><a href="' + props.path + '?region=1">Saiba mais sobre essa região</a></p>'
        : "<h4>Dados</h4><p>Clique nas regiões da saúde para saber mais.</p>");
  };

  if (regionData === null) {
    info.addTo(map);
  }

  function get_pontuacao_regionais(dados){
    for (var i = 0; i < dados.features.length; i++) {
      dados.features[i].properties.pontos_rt = (dados.features[i].properties['rt'] <= 1 ? 5 : 0);
      dados.features[i].properties.pontos_media_movel = (dados.features[i].properties.media_movel < 15 ? 5 : 0);
      dados.features[i].properties.pontos_leitos_max = (dados.features[i].properties.leitos_geral_max <= 60 || dados.features[i].properties.leitos_covid_max <= 60 ? 5 : 0);
      dados.features[i].properties.pontos_incidencia = (dados.features[i].properties.incidencia <= dados.features[i].properties.incidencia_sc ? 2 : 0);
      dados.features[i].properties.pontos_letalidade = (dados.features[i].properties.letalidade <= dados.features[i].properties.letalidade_sc ? 2 : 0);
      dados.features[i].properties.pontos_vacinacao = dados.features[i].properties.vacinacao_pontos; 
    }
    return dados.features;
  };

  function getColor(d) {
    var fav = "#92efb6";
    var red = "#ff7979";
    var orange = "#FA9600";
    var yellow = "#FAD700";

    if (typeof d == "object") {
      if (!(d.pontuacao)) return "transparent";

      var levelRegion = d.pontuacao;
      // levelRegion += d.rt <= 1 ? 5 : 0;
      // levelRegion += d.media_movel < 15 ? 5 : 0;
      // levelRegion += d.ocupacao_leitos <= 60 ? 5 : 0;
      // levelRegion += d.incidencia <= d.incidencia_sc ? 2 : 0;
      // levelRegion += d.letalidade <= d.letalidade_sc ? 2 : 0;
      // levelRegion += d.vacinacao >= 20 ? 3 : 0; 

      if (levelRegion < 0) return "transparent";
       
      if (levelRegion >= 15) {
        // ↓↓↓ teste ocupacao > 80 = amarelo ↓↓↓
        if (d.leitos_geral_max > 80 || d.leitos_covid_max > 80) {
          return yellow;  
        } else return fav;
      } 

      else if (levelRegion >= 11 && levelRegion < 15) return yellow;

      else if (levelRegion >= 6 && levelRegion < 11) return orange;
      
      else return red;
    }

    else {
      if (d < 0) return "transparent";

      if ( d >= 15 ) return fav;

      else if ( d >= 11 && d < 15 ) return yellow;

      else if ( d >= 6 && d < 11 ) return orange;

      else return red;
    }
  };

  function style(feature) {
    return {
      weight: 2,
      opacity: 1,
      color: "white",
      dashArray: "3",
      fillOpacity: 0.5,
      fillColor: getColor(feature.properties.child ? -1 : feature.properties),
    };
  };

  function highlightFeature(e) {
    geojson.resetStyle();
    var layer = e.target;

    layer.setStyle({
      weight: 5,
      color: "#666",
      dashArray: "",
      fillOpacity: 0.7,
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
      layer.bringToFront();
    }

    info.update(layer.feature.properties);
  };

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
      onEachFeature: onEachFeature,
    }).addTo(map);
  } else {
    geojson = L.geoJson(stateData, {
      style: style,
      onEachFeature: onEachFeature,
    }).addTo(map);
  }

  map.attributionControl.addAttribution(
    'Dados do Covid &copy; <a href="https://covid.saude.gov.br/">Ministério da Saúde</a>',
  );
  map.attributionControl.addAttribution(
    'Dados de UTI &copy; <a href="https://www.ciasc.sc.gov.br/">CIASC</a>',
  );

  var legend = L.control({ position: "topleft" });

  legend.onAdd = function (map) {
    var div = L.DomUtil.create("div", "map-info legend");
    labels = ['<h6><b>Condição de retorno das aulas</b><img class="close-map-info" src="img/close-icon.png" /></h6> '];
    labels.push(
      '<p><i style="background:' + getColor(16) + '"></i> (Maior ou igual a 15 pontos)</p>',
    );
    labels.push(
      '<p><i style="background:' +
      getColor(13) +
      '"></i> (11 a 14 pontos)</p>',
    );
    labels.push(
      '<p><i style="background:' +
      getColor(8) +
      '"></i> (6 a 10 pontos)</p>',
    );
    labels.push(
      '<p><i style="background:' +
      getColor(4) +
      '"></i> (Menor ou igual a 5 pontos)</p>',
    );
    div.innerHTML = labels.join("");
    return div;
  };

  legend.addTo(map);

  var btnLegend = L.control({ position: "topleft" });
  btnLegend.onAdd = function (map) {
    var div = L.DomUtil.create("div", "btnLegend");
    div.innerHTML = '<h6><b>Legenda</b></h6><p><img src="img/legend.svg" /></p>'
    return div;
  }
  btnLegend.addTo(map)

  $('.map-info.legend').hide();


  $('.btnLegend').on('click', function () {
    $('.btnLegend').hide();
    $('.map-info.legend').show();
  })

  $('.close-map-info').on('click', function () {
    $('.btnLegend').show();
    $('.map-info.legend').hide();
  })

  // END LEAF
  L.control.BigImage({ position: 'topright' }).addTo(map);

});
