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
        regionData.features[0].properties.rt = dados.rt;
        regionData.features[0].properties.media_movel = dados.media_movel;
        regionData.features[0].properties.ocupacao_leitos = dados.ocupacao_leitos;
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
      shadowUrl:"../css/images/marker-shadow.png",
      iconSize:[25,41],
      iconAnchor:[12,41]
    }
  });
  
  var iconIf = new iconBase({
    iconUrl:"../css/images/marker-icon.png",
  });

  var iconIfsc = new iconBase({
    iconUrl:"../css/images/marker-icon-ifsc.png",
    
  });

  var videira = L.marker([-27.026555588666362, -51.14521223224076], {icon: iconIf}).bindPopup(
    "IFC - Campus Videira",
  );
  var luzerna = L.marker([-27.132361991407368, -51.46302556370465], {icon: iconIf}).bindPopup(
    "IFC - Campus Luzerna",
  );
  var fraiburgo = L.marker([-27.030183953471692, -50.91809746417005], {icon: iconIf}).bindPopup(
    "IFC - Campus Fraiburgo",
  );
  var riodosul = L.marker([-27.21220797789442, -49.639967538355734], {icon: iconIf}).bindPopup(
    "IFC - Campus Rio do Sul - Unidade Urbana",
  );
  var riodosul2 = L.marker([-27.18469255860665, -49.66081786276957], {icon: iconIf}).bindPopup(
    "IFC - Campus Rio do Sul - Sede",
  );
  var riodosul3 = L.marker([-27.211806140692513, -49.65704082501049], {icon: iconIf}).bindPopup(
    "IFC - Campus Rio do Sul - Unidade Tecnológica",
  );
  var sombrio = L.marker([-29.101905323823694, -49.63864611448503], {icon: iconIf}).bindPopup(
    "IFC - Campus Sombrio",
  );
  var sao_francisco_do_sul = L.marker([ -26.21763874417492, -48.57035665361086,], {icon: iconIf}).bindPopup(
    "IFC - Campus São Francisco de Sul");
  var araquari = L.marker([-26.394781055206387, -48.73823989999723], {icon: iconIf}).bindPopup(
    "IFC - Campus Araquari",
  );
  var abelardo_luz = L.marker([ -26.586521596148813, -52.10501674417086], {icon: iconIf}).bindPopup(
    "IFC - Campus Abelardo Luz (Avançado)");
  var sao_bento_do_sul = L.marker([ -26.25027687276346, -49.35088784121336], {icon: iconIf}).bindPopup(
    "IFC - Campus São Bento do Sul");
  var santa_rosa_do_sul = L.marker([ -29.0954650121907, -49.81419731861792 ], {icon: iconIf}).bindPopup(
    "IFC - Campus Santa Rosa do Sul");
  var ibirama = L.marker([-27.04909677497824, -49.53896279407205], {icon: iconIf}).bindPopup(
    "IFC - Campus Ibirama",
  );
  var blumenau = L.marker([-26.881739150584163, -49.137095301484216], {icon: iconIf}).bindPopup(
    "IFC - Campus Blumenau",
  );
  var concordia = L.marker([-27.201912072094206, -52.08319161549669], {icon: iconIf}).bindPopup(
    "IFC - Campus Concórdia",
  );
  var blumenau2 = L.marker([-26.912126542043502, -49.0664407730001], {icon: iconIf}).bindPopup(
    "IFC - Reitoria",
  );
  var camboriu = L.marker([-27.015680100497377, -48.65878562611805], {icon: iconIf}).bindPopup(
    "IFC - Campus Camboriú",
  );
  var brusque = L.marker([-27.09941598304748, -48.92860645226999], {icon: iconIf}).bindPopup(
    "IFC - Campus Brusque",
  );

 //IFSC
  var ifscsaomigueloeste = L.marker([ -26.741901957217408, -53.52609855884629 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus São Miguel do Oeste",
  );
  var ifscsaocarlos = L.marker([ -27.091910843991037, -53.01319594534334 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus São Carlos",
  );
  var ifscsaolourenco = L.marker([ -26.34874569633562, -52.84645603757906 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus São Lourenço do Oeste",
  );
  var ifscchapeco = L.marker([ -27.13732883700056, -52.598267716505994 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Chapecó",
  );
  var ifscxanxere = L.marker([ -26.876463944597976, -52.41823904535004 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Xanxerê",
  );
  var ifsccacador = L.marker([ -26.77903961642183, -51.03877490302486 ], {icon: iconIfsc}).bindPopup(
    "IFSC -  Câmpus Caçador",
  );
  var ifsccanoinhas = L.marker([ -26.183083657376354, -50.367038060714734 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Canoinhas",
  );
  var ifsclages = L.marker([ -27.80497873077295, -50.337622747172794 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Lages",
  );
  var ifscurupema = L.marker([ -27.957562151114153, -49.87245555880857 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Urupema",
  );
  var ifscararangua = L.marker([ -28.94721817158039, -49.49345364713646 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Araranguá",
  );
  var ifsccriciuma = L.marker([ -28.678035700825063, -49.3314548434419 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Criciúma",
  );
  var ifsctubarao = L.marker([ -28.47414960790433, -49.025392745299946 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Tubarão",
  );
  var ifscgaropaba = L.marker([ -28.09864097503046, -48.67534507599955 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Garopaba",
  );
  var ifscgaspar = L.marker([ -26.90052577846774, -49.004026831857054 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Gaspar",
  );
  var ifscitajai = L.marker([ -26.93053145730176, -48.685177460692096 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Itajaí",
  );
  var ifscjoinvile = L.marker([ -26.278238302174334, -48.880652103040084 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Joinville",
  );
  var ifscjaraguadosul = L.marker([ -26.467905846640125, -49.11405536070609 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Jaraguá do Sul - Rau",
  );
  var ifscjaraguacentro = L.marker([ -26.476921205814246, -49.089831131870014 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Jaraguá do Sul - Centro",
  );
  var ifscpalhoca = L.marker([ -27.630125844831145, -48.68894680299862 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Palhoça - Bilíngue",
  );
  var ifscsaojose = L.marker([ -27.608215302586004, -48.63321567416328 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus São José",
  );
  var ifscreitoriafloripa = L.marker([ -27.599500291641426, -48.572364229983826 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Florianópolis - Continente e Reitoria",
  );
  var ifscflorianopolis = L.marker([ -27.59403720556465, -48.54317238950758 ], {icon: iconIfsc}).bindPopup(
    "IFSC - Câmpus Florianópolis",
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
  ]);

  var campusIFSC = L.layerGroup([
    ifscsaomigueloeste,
    ifscsaocarlos,
    ifscsaolourenco,
    ifscchapeco,
    ifscxanxere,
    ifsccacador,
    ifsccanoinhas,
    ifsclages,
    ifscurupema,
    ifscararangua,
    ifsccriciuma,
    ifsctubarao,
    ifscgaropaba,
    ifscgaspar,
    ifscitajai,
    ifscjoinvile,
    ifscjaraguadosul,
    ifscjaraguacentro,
    ifscpalhoca,
    ifscsaojose,
    ifscreitoriafloripa,
    ifscflorianopolis
  ]);

  //SELECT INSTITUTO
    var mapControlsContainer = document.getElementsByClassName("leaflet-top leaflet-right")[0];
    var SelectContainer = document.getElementById("SelectContainer");
    mapControlsContainer.appendChild(SelectContainer);
    $('.btnSelect').on('click', function() {
      document.querySelector('.modal-overlay')
        .classList
        .add('active');
    });  
    
    $('.IFSC').on('click', () => {
      campusIFSC.addTo(map);
      map.removeLayer(campusIFC);
      var tokensIfsc = campusIFSC;
      document.querySelector('.modal-overlay')
        .classList
        .remove('active');

      document.querySelector('.modal-overlay')
        .classList
        .add('off');
      
      document.querySelector('.selectIFSC')
        .classList
        .remove('none');

      //remover a imagem anterior
      const testIFC = document.querySelector('.selectIFC.none');
      if(!testIFC){
        document.querySelector('.selectIFC')
          .classList
          .add('none');
      }
    });

    $('.IFC').on('click', () => {
      campusIFC.addTo(map);
      map.removeLayer(campusIFSC);
      var tokensIfc = campusIFC;
      document.querySelector('.modal-overlay')
        .classList
        .remove('active');
      document.querySelector('.modal-overlay')
        .classList
        .add('off');
      document.querySelector('.selectIFC')
        .classList
        .remove('none');

      //remover a imagem anterior
      const testIFC = document.querySelector('.selectIFSC.none');
      if(!testIFC){
        document.querySelector('.selectIFSC')
          .classList
          .add('none');
      }
    });

  // control that shows state info on hover
  var info = L.control({ position: "topleft" });

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
  function getColor(d) {
    var fav = "#92efb6";
    var threeNfav = "#ff7979";
    var twoNfav = "#FA9600";
    var oneNfav = "#FAD700";

    if (typeof d == "object") {
      var levelRegion = 0;
      levelRegion += d.rt > 1 ? 1 : 0;
      levelRegion += d.media_movel > 15 ? 1 : 0;
      levelRegion += d.ocupacao_leitos > 60 ? 1 : 0;

      if (levelRegion == 3) return threeNfav;
      else if (levelRegion == 2) return twoNfav;
      else if (levelRegion == 1) return oneNfav;
      else fav;
    }
    switch (d) {
      case 3:
        return threeNfav;
      case 2:
        return twoNfav;
      case 1:
        return oneNfav;
      case 0:
        return fav;
      default:
        "transparent";
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

  var legend = L.control({ position: "bottomleft"});

  legend.onAdd = function (map) {
    var div = L.DomUtil.create("div", "map-info legend");
    labels = ['<h6><b>Condição de retorno das aulas</b><img class="close-map-info" src="img/close-icon.png" /></h6> '];
    labels.push(
      '<p><i style="background:' + getColor(0) + '"></i> (Favorável)</p>',
    );
    labels.push(
      '<p><i style="background:' +
      getColor(1) +
      '"></i> (1 Indicador não Favorável)</p>',
    );
    labels.push(
      '<p><i style="background:' +
      getColor(2) +
      '"></i> (2 Indicadores não Favoráveis)</p>',
    );
    labels.push(
      '<p><i style="background:' +
      getColor(3) +
      '"></i> (3 Indicadores não Favoráveis)</p>',
    );
    div.innerHTML = labels.join("");
    return div;
  };

  legend.addTo(map);

  var btnLegend = L.control({ position: "bottomleft"});
  btnLegend.onAdd = function (map) {
    var div = L.DomUtil.create("div", "btnLegend");
    div.innerHTML = '<h6><b>Legenda</b></h6><p><img src="img/legend.svg" /></p>'
    return div;
  }
  btnLegend.addTo(map)

  $('.map-info.legend').hide();


  $('.btnLegend').on('click', function() {
    $('.btnLegend').hide();
    $('.map-info.legend').show();
  })

  $('.close-map-info').on('click', function() {
    $('.btnLegend').show();
    $('.map-info.legend').hide();
  })

  // END LEAF

  
});
