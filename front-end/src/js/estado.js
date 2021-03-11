$(document).ready(() => {

  fetch(base_url + '/api/rt-estado/').then(response => {
    return response.json()
    }).then(dados => {
        /* R(t) */
        var rt = [
            {
            x: dados.datas,
            y: dados.rt,
            type: 'scatter'
            }
        ];
        var rt_layout = {
            title: 'Taxa de Transmissibilidade R(t) no estado de SC',
        };

        var config = {responsive: true};

        Plotly.newPlot('rt-estado-graph', rt, rt_layout, config);
    }).catch(err => console.error(err));

 /*
  fetch(base_url + "/api/rt-por-regiao/")
    .then((response) => {
      return response.json();
    })
    .then((dados) => {
      var dadosEstado = [];
      for (var regional in dados.regionais) {
        dadosEstado.push(dados.regionais[regional]);
      }
      var regionais_layout = {
        title: "Taxa de Transmissibilidade R(t) por região de SC",
      };

      ind = dadosEstado.length
      var draw =[];
      for(i = 0; i < ind; i++){
        var obj = dadosEstado[i].reduce((obj, dado) => {
              obj["name"] = dado.name;
              obj["mode"] = dado.mode;
              obj["type"] = dado.type;
              obj["x"] = dado.x;
              obj["y"] = dado.y;

          draw[i] = obj; 
          return draw;
          }, {});
      }
      var config = { responsive: true };

      Plotly.newPlot(
        "rt-estado-regioes-graph",
        draw,
        regionais_layout,
        config
      );
    })
    .catch((err) => console.error(err));

    */

    fetch(base_url + "/api/rt-por-regiao/")
    .then((response) => {
      return response.json();
    })
    .then((dados) => {
        //Limpa célculas vazias. 
        dadosRegionais = $.grep(dados.regionais,function(n){ return n == 0 || n });
  
        var mm_layout = {
          title: "Taxa de Transmissibilidade R(t) por região de SC",
        };
  
        var config = { responsive: true };
        
        Plotly.newPlot("rt-estado-regioes-graph", dadosRegionais, mm_layout, config);
    })
    .catch((err) => console.error(err));


  fetch(base_url + "/api/casos-por-regiao/")
    .then((response) => {
      return response.json();
    })
    .then((dados) => {
      //Limpa célculas vazias. 
      // dadosRegionais = $.grep(dados.regionais_casos_acumulados,function(n){ return n == 0 || n });
      // var mm_layout = {
      //   title: "Casos acumulados",
      // };
      // var config = { responsive: true };
      // Plotly.newPlot("casos-graph", dadosRegionais, mm_layout, config);


      // //Limpa célculas vazias. 
      // dadosRegionaisObitos = $.grep(dados.regionais_obitos_acumulados,function(n){ return n == 0 || n });
      // var mm_layout = {
      //   title: "Óbitos acumulados",
      // };
      // var config = { responsive: true };
      // Plotly.newPlot("obitos-graph", dadosRegionaisObitos, mm_layout, config);

      //Limpa célculas vazias. 
      dadosRegionaisIncidencia = $.grep(dados.regionais_incidencia,function(n){ return n == 0 || n });
      var mm_layout = {
        title: "Incidência acumulada por 100 mil habitantes",
      };
      
      var config = { responsive: true };
      Plotly.newPlot("incidencia", dadosRegionaisIncidencia, mm_layout, config);
    })
    .catch((err) => console.error(err));

    fetch(base_url + "/api/leitos-por-regiao/")
    .then((response) => {
      return response.json();
    })
    .then((dados) => {
       /* Ocupacao de Leitos */
      //Limpa célculas vazias. 
      ocupacao_leitos = $.grep(dados.regionais,function(n){ return n == 0 || n });
  
      var mm_layout = {
        title: "Ocupação de Leitos (UTI) em porcentagem (%)",
      };

      var config = { responsive: true };
      
      Plotly.newPlot("leitos-graph", ocupacao_leitos, mm_layout, config);
    })
    .catch((err) => console.error(err));
    
});
