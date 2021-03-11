$(document).ready(() => {
/*
  fetch(base_url + '/api/rt-estado/').then(response => {
    return response.json()
    }).then(dados => {
        // R(t) 
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
*/
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
        
        Plotly.newPlot("rt-graph", dadosRegionais, mm_layout, config);
    })
    .catch((err) => console.error(err));


  fetch(base_url + "/api/casos-por-regiao/")
    .then((response) => {
      return response.json();
    })
    .then((dados) => {
      var d = new Date(dados.maxData); 
      var datestring = ("0" + d.getDate()).slice(-2) + "/" + ("0"+(d.getMonth()+1)).slice(-2) + "/" + d.getFullYear();
      $("#dataAtualizacao").text(datestring);

      // Casos média Movel
      dadosRegionaisCasosMediaMovel = $.grep(dados.regionais_casos_mediamovel,function(n){ return n == 0 || n });
      var mm_layout = {
        title: "Casos Média Móvel",
      };
      
      var config = { responsive: true };
      Plotly.newPlot("casos-graph", dadosRegionaisCasosMediaMovel, mm_layout, config);

      // Óbitos média Movel
      dadosRegionaisObitosMediaMovel = $.grep(dados.regionais_obitos_mediamovel,function(n){ return n == 0 || n });
      var mm_layout = {
        title: "Óbitos Média Móvel",
      };
      
      var config = { responsive: true };
      Plotly.newPlot("obitos-graph", dadosRegionaisObitosMediaMovel, mm_layout, config);

      // Incidencia
      dadosRegionaisIncidencia = $.grep(dados.regionais_incidencia,function(n){ return n == 0 || n });
      var mm_layout = {
        title: "Incidência acumulada por 100 mil habitantes",
      };
      
      var config = { responsive: true };
      Plotly.newPlot("incidencia-graph", dadosRegionaisIncidencia, mm_layout, config);

      // Letalidade
      dadosRegionaisLetalidade = $.grep(dados.regionais_letalidade,function(n){ return n == 0 || n });
      var mm_layout = {
        title: "Óbitos / número de casos (em %)",
      };
      
      var config = { responsive: true };
      Plotly.newPlot("letalidade-graph", dadosRegionaisLetalidade, mm_layout, config);
      
    }).catch((err) => console.error(err));

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

      var config = { responsive: true};
      
      Plotly.newPlot("leitos-graph", ocupacao_leitos, mm_layout, config);
    }).catch((err) => console.error(err));
    
});
