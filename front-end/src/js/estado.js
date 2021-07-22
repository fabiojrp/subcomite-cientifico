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


    fetch(base_url + "/api/vacinacao-por-regiao/")
        .then((response) => {
            return response.json();
        })
        .then((dados) => {
            //Limpa célculas vazias. 
            dadosRegionais = $.grep(dados.regionais, function (n) { return n == 0 || n });

            var mm_layout = {
                title: 'Vacinação 2ª Dose da População geral - fonte: <a href="https://www.coronavirus.sc.gov.br">Coronavírus SC</a>',
                showlegend: true,
                yaxis: {
                    tickformat: '.2%',
                }
            };

            var config = { responsive: true };

            Plotly.newPlot("vacina-graph", dadosRegionais, mm_layout, config);
        })
        .catch((err) => console.error(err));

    fetch(base_url + "/api/vacinacao-ms-por-regiao/")
        .then((response) => {
            return response.json();
        })
        .then((dados) => {
            //Limpa célculas vazias. 
            dadosRegionais = $.grep(dados.regionais, function (n) { return n == 0 || n });

            var mm_layout = {
                title: 'Vacinação 2ª Dose + Dose Única da População geral - fonte: <a href="https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao">OpenDatasus</a>',
                showlegend: true,
                yaxis: {
                    tickformat: '.2%',
                }

            };

            var config = { responsive: true };

            Plotly.newPlot("vacina-ms-graph", dadosRegionais, mm_layout, config);
        })
        .catch((err) => console.error(err));


    fetch(base_url + "/api/rt-por-regiao/")
        .then((response) => {
            return response.json();
        })
        .then((dados) => {
            //Limpa célculas vazias. 
            dadosRegionais = $.grep(dados.regionais, function (n) { return n == 0 || n });

            var mm_layout = {
                title: 'Taxa média de transmissibilidade (Rt) por região de SC <br> <a href="nota-explicativa.html#RT" id="RTreste"> Nota Explicativa</a>',
                showlegend: true,
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
            $("#dataAtualizacao").text(dados.maiorData);

            // Casos média Movel
            dadosRegionaisCasosMediaMovel = $.grep(dados.regionais_casos_mediamovel, function (n) { return n == 0 || n });
            var mm_layout = {
                title: 'Casos Média Móvel <br> <a href="nota-explicativa.html#mediaMovel"> Nota Explicativa</a>',
            };

            var config = { responsive: true };
            Plotly.newPlot("casos-graph", dadosRegionaisCasosMediaMovel, mm_layout, config);

            // Óbitos média Movel
            dadosRegionaisObitosMediaMovel = $.grep(dados.regionais_obitos_mediamovel, function (n) { return n == 0 || n });
            var mm_layout = {
                title: 'Óbitos Média Móvel <br> <a href="nota-explicativa.html#mediaMovel"> Nota Explicativa</a>',
            };

            var config = { responsive: true };
            Plotly.newPlot("obitos-graph", dadosRegionaisObitosMediaMovel, mm_layout, config);

            // Incidencia
            dadosRegionaisIncidencia = $.grep(dados.regionais_incidencia, function (n) { return n == 0 || n });
            var mm_layout = {
                title: 'Incidência acumulada de casos a cada 100 mil habitantes <br> <a href="nota-explicativa.html#incidencia"> Nota Explicativa</a>',
            };

            var config = { responsive: true };
            Plotly.newPlot("incidencia-graph", dadosRegionaisIncidencia, mm_layout, config);

            // Letalidade
            dadosRegionaisLetalidade = $.grep(dados.regionais_letalidade, function (n) { return n == 0 || n });
            var mm_layout = {
                title: 'Taxa de letalidade (em %) <br> <a href="nota-explicativa.html#letalidade"> Nota Explicativa</a>',
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
            ocupacao_leitos = $.grep(dados.regionais, function (n) { return n == 0 || n });

            var max = ocupacao_leitos[0].y.reduce(function(y) {
                return Math.max(y);
            });
            console.log(max);
            
            var mm_layout = {
                title: 'Taxa de ocupação de leitos UTI Adulto em relação ao MÁXIMO de leitos ativos (em %)  <br> <a href="nota-explicativa.html#leitos"> Nota Explicativa</a>',
                yaxis: {
                    tickformat: '.2%',
                },
                // annotations: [
                //     {
                //       y: max,
                //       yref: 'y',
                //       text: 'max=5',
                //       showarrow: true,
                //       font: {
                //         family: 'Courier New, monospace',
                //         size: 16,
                //         color: '#ffffff'
                //       },
                //       align: 'center',
                //       arrowhead: 2,
                //       arrowsize: 1,
                //       arrowwidth: 2,
                //       arrowcolor: '#636363',
                //       ax: 20,
                //       ay: -30,
                //       bordercolor: '#c7c7c7',
                //       borderwidth: 2,
                //       borderpad: 4,
                //       bgcolor: '#ff7f0e',
                //       opacity: 0.8
                //     }
                //   ]
                
            };
            
            var config = { responsive: true };

            Plotly.newPlot("leitos-graph", ocupacao_leitos, mm_layout, config);
        }).catch((err) => console.error(err));
});