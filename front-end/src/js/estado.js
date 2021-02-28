$(document).ready(() => {

    fetch(base_url + '/api/rt-por-regiao/').then(response => {
        return response.json()
    }).then(dados => {
        var dadosEstado = [];
        for(var regional in dados.regionais ){
            dadosEstado.push(dados.regionais[regional]);
          }
        var regionais_layout = {
            title: 'Dados das regiões',
        };

        var config = {responsive: true}
        // Não funciona!!!
        //Plotly.newPlot('rt-estado-graph', dadosEstado, regionais_layout, config);
  
        //Se for passado apena 1, funciona.
        Plotly.newPlot('rt-estado-graph', dadosEstado[1], regionais_layout, config);
    }).catch(err => console.error(err));
  
  
    fetch(base_url + '/api/dados-estado').then(response => {
        return response.json()
    }).then(dados => {
            /* Casos / Casos média móvel */
            var casos= {
              type: "scatter",
              mode: "lines",
              x: dados.datas,                
              y: dados.casos,
              line: {color: '#17BECF'},
              name: "Casos"
          }
    
          var casos_media_movel = {
              type: "scatter",
              mode: "lines",
              x: dados.datas,
              y: dados.casos_media_movel,
              line: {color: '#FF0000'},
              name: "Casos Média Móvel"
          }
          dados_casos = [casos, casos_media_movel]
    
          var mm_layout = {
              title: 'Casos X Casos Média Móvel',
          };
          
          var config = {responsive: true};
  
          Plotly.newPlot('casos-graph', dados_casos, mm_layout, config);
  
        /* Óbitos / Óbitos média móvel */
        var obitos = {
            type: "scatter",
            mode: "lines",
            x: dados.datas,                
            y: dados.obitos,
            line: {color: '#17BECF'},
            name: "Óbitos"
        }
  
        var obitos_media_movel = {
            type: "scatter",
            mode: "lines",
            x: dados.datas,
            y: dados.obitos_media_movel,
            line: {color: '#FF0000'},
            name: "Óbitos Média Móvel"
        }
        dados_obitos = [obitos, obitos_media_movel]
  
        var mm_layout = {
            title: 'Óbitos X Óbitos Média Móvel',
        };
        
        var config = {responsive: true};
  
        Plotly.newPlot('obitos-graph', dados_obitos, mm_layout, config);
  
        /* Ocupacao de Leitos */
        var ocupacao_leitos = [
            {
            x: ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
            y: [80, 97, 100],
            type: 'scatter'
            }
        ];
  
        var ol_layout = {
            title: 'Ocupação de Leitos (UTI) em porcentagem (%)',
        };
      
        var config = {responsive: true};
  
        Plotly.newPlot('leitos-graph', ocupacao_leitos, ol_layout, config);
  
  
        /* CASOS ACUMULADOS */
        var traco_casos = {
          x: dados.datas,
          y: dados.casos_acumulados_100mil,
          type: "bar",
          mode: "horizontal",
          name: 'Incidência acumulada por 100 mil habitantes',
          marker: {
              color: 'rgba(222,45,38,0.8)',
              opacity: 0.7
            }, 
          orientation: 'v'
            
        }
  
        data = [traco_casos]
  
        var layout = {
            title: 'Incidência acumulada por 100 mil habitantes',
            barmode: 'stack',
        };
  
        var config = {responsive: true};
        
        Plotly.newPlot('casos-acumulados', data, layout, config);
  
    }).catch(err => console.error(err));
  
  
   });