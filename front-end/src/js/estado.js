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
      dadosRegionais = $.grep(dados.regionais_casos_acumulados,function(n){ return n == 0 || n });
      
      var mm_layout = {
        title: "Casos X Casos Média Móvel",
      };

      var config = { responsive: true };
      
      Plotly.newPlot("casos-graph", dadosRegionais, mm_layout, config);


      //Limpa célculas vazias. 
      dadosRegionaisObitos = $.grep(dados.regionais_obitos_acumulados,function(n){ return n == 0 || n });

      var mm_layout = {
        title: "Óbitos acumulados",
      };

      var config = { responsive: true };
      
      Plotly.newPlot("obitos-graph", dadosRegionaisObitos, mm_layout, config);

      /* CASOS ACUMULADOS */
      var traco_casos = {
        x: dados.datas,
        y: dados.casos_acumulados_100mil,
        type: "bar",
        mode: "horizontal",
        name: "Incidência acumulada por 100 mil habitantes",
        marker: {
          color: "rgba(222,45,38,0.8)",
          opacity: 0.7,
        },
        orientation: "v",
      };

      data = [traco_casos];

      var layout = {
        title: "Incidência acumulada por 100 mil habitantes",
        barmode: "stack",
      };

      var config = { responsive: true };

      Plotly.newPlot("casos-acumulados", data, layout, config);
    })
    .catch((err) => console.error(err));

    fetch(base_url + "/api/leitos-por-regiao/")
    .then((response) => {
      return response.json();
    })
    .then((dados) => {
         /* Ocupacao de Leitos */
      var ocupacao_leitos = [
        {
          x: [
            "2013-10-04 22:23:00",
            "2013-11-04 22:23:00",
            "2013-12-04 22:23:00",
          ],
          y: [80, 97, 100],
          type: "scatter",
        },
      ];

      var ol_layout = {
        title: "Ocupação de Leitos (UTI) em porcentagem (%)",
      };

      var config = { responsive: true };

      Plotly.newPlot("leitos-graph", ocupacao_leitos, ol_layout, config);
    })
    .catch((err) => console.error(err));
    
});
