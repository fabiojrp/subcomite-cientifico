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
        stateData = data.stateData;
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
        regionData.features[0].properties.ocupacao_leitos = dados.ocupacao_leitos;
        regionData.features[0].properties.incidencia = dados.incidencia;
        regionData.features[0].properties.letalidade = dados.letalidade;
        regionData.features[0].properties.vacinacao = dados.vacinacao;
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
        ? "<h4><b>Regional:</b> " +
        props.name +
        "</h4><p>Taxa de Transmissibilidade: " +
        props.rt +
        "</p><p>Média Móvel: " +
        props.media_movel.toFixed(2) +
        "%" +
        "</p><p>Ocupação de Leitos Covid Adulto: " +
        props.ocupacao_leitos.toFixed(2) +
        "%" +
        "</p><p> Casos acumulados por 100 mil hab: " +
        props.incidencia.toFixed(2) +
        "</p><p> Taxa de letalidade: " +
        props.letalidade.toFixed(2) + "%" +
        "</p><p> Percentual de vacinação: " +
        props.vacinacao.toFixed(2) + "%" +
        '</p><p><a href="' +
        props.path +
        '?region=1">Saiba mais sobre essa região</a></p>'
        : "<h4>Dados</h4><p>Clique nas regiões da saúde para saber mais.</p>");
  };

  if (regionData === null) {
    info.addTo(map);
  }

  // TODO: Fazer a cor verde:
  // RT: < 1
  // Média Móvel < 15%
  // UTI < 60%
  // get color depending on rt value

  /*
        >= 15 - Verde
        12 >= e 15 = Amarelo
        9 >= e 11 = laranja
        9 < Vermelho

        Média = 5 pontos 
        R(t) = 5 pontos
        Leitos móvel = 5 pontos
        Casos acum. = 2 pontos
        Letalidade = 2 pontos
        Vacinação (D2) = 3 pontos
                    */
  function getColor(d) {
    var fav = "#92efb6";
    var red = "#ff7979";
    var orange = "#FA9600";
    var yellow = "#FAD700";

    if (typeof d == "object") {
      if (!(d.rt)) return "transparent";

      var levelRegion = 0;
      levelRegion += d.rt < 1 ? 5 : 0;
      levelRegion += d.media_movel < 15 ? 5 : 0;
      levelRegion += d.ocupacao_leitos < 60 ? 5 : 0;

      if (levelRegion >= 15) return fav;
      else if (levelRegion >= 12 && levelRegion < 15) return yellow;
      else if (levelRegion >= 9 && levelRegion <= 11) return orange;
      else return red;
    }
    // switch (d) {
    //   case d >= 15:
    //     return fav;
    //   case d >= 12 && d < 15:
    //     return yellow;
    //   case d >= 9 && d <= 11:
    //     return orange;
    //   default:
    //     return red;
    // }
    else {
      if ( d >= 15 ) return fav;
      else if ( d >= 12 && d < 15 ) return yellow;
      else if ( d >= 9 && d <= 11 ) return orange;
      else return red;
    }
  }

  function style(feature) {
    return {
      weight: 2,
      opacity: 1,
      color: "white",
      dashArray: "3",
      fillOpacity: 0.5,
      fillColor: getColor(feature.properties.child ? -1 : feature.properties),
    };
  }

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
      '<p><i style="background:' + getColor(16) + '"></i> (Favorável)</p>',
    );
    labels.push(
      '<p><i style="background:' +
      getColor(12) +
      '"></i> (Entre 12 e 14 pontos)</p>',
    );
    labels.push(
      '<p><i style="background:' +
      getColor(10) +
      '"></i> (Entre 9 e 11 pontos)</p>',
    );
    labels.push(
      '<p><i style="background:' +
      getColor(6) +
      '"></i> (Abaixo de 8 pontos)</p>',
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
