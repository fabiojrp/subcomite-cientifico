const { Pool, Client } = require('pg')
const bodyParser = require('body-parser')
var cors = require('cors');

const express = require('express')
const app = express()

let port = 3000;

// https://medium.com/zero-equals-false/using-cors-in-express-cac7e29b005b
// em produção devemos limitar somente para ambiente de desenvolvimento e para o domínio da aplicação.
app.use(cors())

const pool = new Pool({
    user: 'postgres', // postgres marcelo
    host: 'localhost',
    database: 'covid', // covid - mauricio
    //password: 'postgres', // postgres mauricio
    password: '!admpasswd@covid', // postgres marcelo WEpJqsYMnHWB //!admpasswd@covid
    port: 5432
})

regions = {
    0: 'Ignorado',
    1: 'NULL',
    2: 'ALTO URUGUAI CATARINENSE',
    3: 'ALTO VALE DO ITAJAI',
    4: 'ALTO VALE DO RIO DO PEIXE',
    5: 'CARBONIFERA',
    6: 'EXTREMO OESTE',
    7: 'EXTREMO SUL CATARINENSE',
    8: 'FOZ DO RIO ITAJAI',
    9: 'GRANDE FLORIANOPOLIS',
    10: 'LAGUNA',
    11: 'MEDIO VALE DO ITAJAI',
    12: 'MEIO OESTE',
    13: 'NORDESTE',
    14: 'OESTE',
    15: 'PLANALTO NORTE',
    16: 'SERRA CATARINENSE',
    17: 'XANXERÊ'
}
html_regions = {
    0: 'Ignorado',
    1: 'NULL',
    2: 'ALTO URUGUAI CATARINENSE',
    3: 'ALTO VALE DO ITAJAI',
    4: 'ALTO VALE DO RIO DO PEIXE',
    5: 'carbonifera',
    6: 'EXTREMO OESTE',
    7: 'EXTREMO SUL CATARINENSE',
    8: 'FOZ DO RIO ITAJAI',
    9: 'GRANDE FLORIANOPOLIS',
    10: 'LAGUNA',
    11: 'MEDIO VALE DO ITAJAI',
    12: 'MEIO OESTE',
    13: 'NORDESTE',
    14: 'OESTE',
    15: 'PLANALTO NORTE',
    16: 'SERRA CATARINENSE',
    17: 'XANXERÊ'
}
app.get('/', (req, res) => {
    res.send("foi..");
});

app.get('/api/casos-por-regiao/:id', (req, res) => {
    id = req.params.id;

    pool.query(
        `SELECT CASOS.DATA,
        SUM(CASOS.CASOS) AS CASOS_DIA,
        SUM(CASOS.OBITOS) AS OBITOS_DIAS,
        SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL,
        SUM(CASOS.OBITOS_MEDIAMOVEL) AS OBITOS_MEDIAMOVEL,
        SUM(CASOS.CASOS_ACUMULADOS) AS CASOS_ACUMULADOS,
        SUM(CASOS.OBITOS_ACUMULADOS) AS OBITOS_ACUMULADOS,
        SUM(CASOS.POPULACAO) AS POPULACAO,
        CASE WHEN (SUM(CASOS.CASOS_ACUMULADOS) < 100) 
                THEN TO_CHAR(0,'99990d99')
                ELSE TO_CHAR((SUM(CASOS.OBITOS_ACUMULADOS)::real / SUM(CASOS.CASOS_ACUMULADOS)::real) * 100,'99990d99')
                END AS LETALIDADE
        FROM REGIONAIS, CASOS
        WHERE CASOS.REGIONAL = REGIONAIS.ID
            AND REGIONAIS.ID = $1
        GROUP BY REGIONAIS.REGIONAL_SAUDE, CASOS.DATA
        ORDER BY CASOS.DATA
        `,
        [id],
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar por região: " + err)
                return
            }

            region = regions[id]

            if (typeof (region) === 'undefined') {
                res.send("Região não reconhecida. Informe um ID válido.")
                return;
            }

            if (rows.rows.length > 0) {
                maxData = 0;
                rows.rows.forEach(item => {
                    if (item.data > maxData)
                        maxData = item.data;
                });
                datas = rows.rows.map(row => {
                    return row.data;
                })

                casos = rows.rows.map(row => {
                    return row.casos_dia;
                })

                casos_media_movel = rows.rows.map(row => {
                    return row.casos_mediamovel;
                })

                obitos = rows.rows.map(row => {
                    return row.obitos_dias;
                })

                obitos_media_movel = rows.rows.map(row => {
                    return row.obitos_mediamovel;
                })

                casos_acumulados = rows.rows.map(row => {
                    return row.casos_acumulados;
                })

                obitos_acumulados = rows.rows.map(row => {
                    return row.obitos_acumulados;
                })
                incidencia = rows.rows.map(row => {
                    return (row.casos_acumulados / row.populacao) * 1e5;
                })

                letalidade = rows.rows.map(row => {
                    return row.letalidade;
                })

            }

            res.send({
                region, maxData, datas, casos, casos_media_movel, obitos, obitos_media_movel,
                casos_acumulados, obitos_acumulados, letalidade, incidencia
            })
        })
})

app.get('/api/casos-por-regiao/', (req, res) => {
    pool.query(
        `SELECT REGIONAIS.ID,
                    REGIONAIS.REGIONAL_SAUDE,
                    CASOS.DATA,
                    SUM(CASOS.CASOS_ACUMULADOS) AS CASOS_ACUMULADOS,
                    SUM(CASOS.OBITOS_ACUMULADOS) AS OBITOS_ACUMULADOS,
                    SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL,
                    SUM(CASOS.OBITOS_MEDIAMOVEL) AS OBITOS_MEDIAMOVEL,
                    SUM(CASOS.POPULACAO) AS POPULACAO,
                    CASE WHEN (SUM(CASOS.CASOS_ACUMULADOS) < 100) 
                        THEN TO_CHAR(0,'99990d99')
                        ELSE TO_CHAR((SUM(CASOS.OBITOS_ACUMULADOS)::real / SUM(CASOS.CASOS_ACUMULADOS)::real) * 100,'99990d99')
                        END AS LETALIDADE
                FROM REGIONAIS, CASOS
                WHERE CASOS.REGIONAL = REGIONAIS.ID
                    AND REGIONAIS.ID <> 0
                GROUP BY REGIONAIS.ID, REGIONAIS.REGIONAL_SAUDE, CASOS.DATA
                ORDER BY REGIONAIS.ID, CASOS.DATA
            `,
        (err, rows) => {

            if (err) {
                console.log("Erro ao buscar o casos por região: " + err)
                return
            }

            result = rows.rows;
            regionais_casos_acumulados = [];
            regionais_obitos_acumulados = [];
            regionais_casos_mediamovel = [];
            regionais_obitos_mediamovel = [];
            regionais_incidencia = [];
            regionais_letalidade = [];
            maxData = 0;
            result.forEach(item => {
                if (!regionais_casos_acumulados[item.id]) {
                    if (item.id == 1) {
                        regionais_casos_acumulados[item.id] = {
                            "name": "Estado de SC",
                            "mode": "lines",
                            "type": "scatter",
                            "x": [],
                            "y": []
                        };
                    } else {
                        regionais_casos_acumulados[item.id] = {
                            "name": item.regional_saude,
                            "mode": "lines",
                            "type": "scatter",
                            "visible": "legendonly",
                            "x": [],
                            "y": []
                        };
                    }
                }
                if (!regionais_obitos_acumulados[item.id]) {
                    if (item.id == 1) {
                        regionais_obitos_acumulados[item.id] = {
                            "name": "Estado de SC",
                            "mode": "lines",
                            "type": "scatter",
                            "x": [],
                            "y": []
                        };
                    } else {
                        regionais_obitos_acumulados[item.id] = {
                            "name": item.regional_saude,
                            "mode": "lines",
                            "type": "scatter",
                            "visible": "legendonly",
                            "x": [],
                            "y": []
                        };
                    }
                }
                // Casos média móvel
                if (!regionais_casos_mediamovel[item.id]) {
                    if (item.id == 1) {
                        regionais_casos_mediamovel[item.id] = {
                            "name": "Estado de SC",
                            "mode": "lines",
                            "type": "scatter",
                            "x": [],
                            "y": []
                        };
                    } else {
                        regionais_casos_mediamovel[item.id] = {
                            "name": item.regional_saude,
                            "mode": "lines",
                            "type": "scatter",
                            "visible": "legendonly",
                            "x": [],
                            "y": []
                        };
                    }
                }


                // Óbitos média móvel
                if (!regionais_obitos_mediamovel[item.id]) {
                    if (item.id == 1) {
                        regionais_obitos_mediamovel[item.id] = {
                            "name": "Estado de SC",
                            "mode": "lines",
                            "type": "scatter",
                            "x": [],
                            "y": []
                        };
                    } else {
                        regionais_obitos_mediamovel[item.id] = {
                            "name": item.regional_saude,
                            "mode": "lines",
                            "type": "scatter",
                            "visible": "legendonly",
                            "x": [],
                            "y": []
                        };
                    }
                }

                if (!regionais_incidencia[item.id]) {
                    if (item.id == 1) {
                        regionais_incidencia[item.id] = {
                            "name": "Estado de SC",
                            "mode": "lines",
                            "type": "scatter",
                            "x": [],
                            "y": []
                        };
                    } else {
                        regionais_incidencia[item.id] = {
                            "name": item.regional_saude,
                            "mode": "lines",
                            "type": "scatter",
                            "visible": "legendonly",
                            "x": [],
                            "y": []
                        };
                    }
                }

                if (!regionais_letalidade[item.id]) {
                    if (item.id == 1) {
                        regionais_letalidade[item.id] = {
                            "name": "Estado de SC",
                            "mode": "lines",
                            "type": "scatter",
                            "x": [],
                            "y": []
                        };
                    } else {
                        regionais_letalidade[item.id] = {
                            "name": item.regional_saude,
                            "mode": "lines",
                            "type": "scatter",
                            "visible": "legendonly",
                            "x": [],
                            "y": []
                        };
                    }
                }

                regionais_casos_acumulados[item.id].x.push(item.data);
                regionais_casos_acumulados[item.id].y.push(item.casos_acumulados);

                regionais_obitos_acumulados[item.id].x.push(item.data);
                regionais_obitos_acumulados[item.id].y.push(item.obitos_acumulados);

                regionais_casos_mediamovel[item.id].x.push(item.data);
                regionais_casos_mediamovel[item.id].y.push(item.casos_mediamovel);

                regionais_obitos_mediamovel[item.id].x.push(item.data);
                regionais_obitos_mediamovel[item.id].y.push(item.obitos_mediamovel);

                regionais_incidencia[item.id].x.push(item.data);
                regionais_incidencia[item.id].y.push((item.casos_acumulados / item.populacao) * 1e5);

                regionais_letalidade[item.id].x.push(item.data);
                regionais_letalidade[item.id].y.push(item.letalidade);

                if (item.data > maxData)
                    maxData = item.data;
            });


            res.send({
                maxData, regionais_casos_acumulados, regionais_obitos_acumulados, regionais_casos_mediamovel,
                regionais_obitos_mediamovel, regionais_incidencia, regionais_letalidade
            })

        })
})

app.get('/api/rt-por-regiao/:id', (req, res) => {
    id = req.params.id;

    pool.query(
        `SELECT RT.DATA as data,
            RT.RT as rt
        FROM REGIONAIS, RT
        WHERE RT.REGIONAL = REGIONAIS.ID
                AND RT.REGIONAL = $1
        ORDER BY REGIONAIS.REGIONAL_SAUDE, RT.DATA
            `,
        [id],
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o R(T) por região: " + err)
                return
            }

            region = regions[id]

            if (typeof (region) === 'undefined') {
                res.send("Região não reconhecida. Informe um ID válido.")
                return;
            }

            if (rows.rows.length > 0) {
                datas = rows.rows.map(row => {
                    return row.data;
                })
                rt = rows.rows.map(row => {
                    return row.rt;
                })

            }

            res.send({ region, datas, rt })
        })
})

/*
app.get('/api/rt-por-regiao/', (req, res) => {  
    pool.query(
        `SELECT REGIONAIS.regional_saude, REGIONAIS.id, RT.DATA as data,
        RT.RT as rt
    FROM REGIONAIS, RT
    WHERE DATA BETWEEN
            (SELECT MAX(RT.DATA) AS MAX_DATA FROM RT) - interval '5 months' AND
            (SELECT MAX(RT.DATA) AS MAX_DATA FROM RT) - interval '1 day'
            AND RT.REGIONAL = REGIONAIS.ID
            AND REGIONAIS.ID <> 1
    ORDER BY REGIONAIS.REGIONAL_SAUDE, RT.DATA
        `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o R(T) por região: " + err)
                return
            }
            
            result = rows.rows;
            regionais = {};
            result.forEach(item => {
               const temp = {};
               if (!regionais[item.regional_saude]) {
                    regionais[item.regional_saude] = [{
                        "name":item.regional_saude,
                        "mode":"lines",
                        "type":"scatter",
                        "x" : [], 
                        "y": []
                    }];
                };
                regionais[item.regional_saude][0].x.push(item.data);
                regionais[item.regional_saude][0].y.push(item.rt);
                
            });
 
            res.send({regionais})
        })    
})
*/

app.get('/api/rt-por-regiao/', (req, res) => {
    pool.query(
        `SELECT REGIONAIS.regional_saude, REGIONAIS.id, RT.DATA as data,
                RT.RT as rt
            FROM REGIONAIS, RT
            WHERE RT.REGIONAL = REGIONAIS.ID
            ORDER BY REGIONAIS.REGIONAL_SAUDE, RT.DATA
            `,
        (err, rows) => {

            if (err) {
                console.log("Erro ao buscar o valor de R(t) por região: " + err)
                return
            }

            result = rows.rows;
            regionais = [];
            result.forEach(item => {
                if (!regionais[item.id]) {
                    if (item.id == 1) {
                        regionais[item.id] = {
                            "name": "Estado de SC",
                            "mode": "lines",
                            "type": "scatter",
                            "x": [],
                            "y": []
                        };

                    } else {
                        regionais[item.id] = {
                            "name": item.regional_saude,
                            "mode": "lines",
                            "type": "scatter",
                            "visible": "legendonly",
                            "x": [],
                            "y": []
                        };
                    }
                };
                regionais[item.id].x.push(item.data);
                regionais[item.id].y.push(item.rt);

            });

            res.send({ regionais })

        })
})


app.get('/api/rt-estado/', (req, res) => {
    pool.query(
        `SELECT RT.DATA as data,
            RT.RT as rt
        FROM RT
        WHERE RT.REGIONAL = 1
        ORDER BY RT.DATA
            `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o R(T) por região: " + err)
                return
            }

            if (rows.rows.length > 0) {
                datas = rows.rows.map(row => {
                    return row.data;
                })

                rt = rows.rows.map(row => {
                    return row.rt;
                })
            }

            res.send({ datas, rt })
        })
})

app.get('/api/leitos-por-regiao/:id', (req, res) => {
    id = req.params.id;
    pool.query(
        `SELECT SUM(leitoscovid.LEITOS_OCUPADOS) AS LEITOS_OCUPADOS,
                SUM(leitoscovid.LEITOS_DISPONIVEIS) AS LEITOS_DISPONIVEIS,
                leitoscovid.ATUALIZACAO AS DATA
            FROM leitoscovid
            WHERE leitoscovid.INDEX_REGIONAL = $1
            GROUP BY leitoscovid.ATUALIZACAO
            ORDER BY leitoscovid.ATUALIZACAO
            `,
        [id],
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o valor de leitos da região: " + err)
                return
            }

            region = regions[id]
            if (typeof (region) === 'undefined') {
                res.send("Região não reconhecida. Informe um ID válido.")
                return;
            }

            leitos_ocupados = {
                "name": "Leitos Ocupados",
                "type": "bar",
                "opacity": 0.5,
                "x": [],
                "y": []
            };
            leitos_disponiveis = {
                "name": "Leitos Disponíveis",
                "type": "bar",
                "opacity": 0.4,
                "x": [],
                "y": []
            };

            result = rows.rows;
            result.forEach(item => {
                leitos_ocupados.x.push(item.data);
                leitos_ocupados.y.push(item.leitos_ocupados);

                leitos_disponiveis.x.push(item.data);
                leitos_disponiveis.y.push(item.leitos_disponiveis);
            });

            res.send({ leitos_disponiveis, leitos_ocupados })
        })
})

app.get('/api/leitos-por-regiao/', (req, res) => {
    pool.query(
        `SELECT REGIONAIS.REGIONAL_SAUDE,
                REGIONAIS.ID as ID,
                SUM(leitoscovid.LEITOS_ATIVOS) AS LEITOS_ATIVOS,
                SUM(leitoscovid.LEITOS_OCUPADOS) AS LEITOS_OCUPADOS,
                leitoscovid.ATUALIZACAO AS DATA
            FROM REGIONAIS,
            leitoscovid
            WHERE leitoscovid.INDEX_REGIONAL = REGIONAIS.ID
            GROUP BY REGIONAIS.ID,
                leitoscovid.ATUALIZACAO,
                REGIONAIS.REGIONAL_SAUDE
            ORDER BY REGIONAIS.ID,
                leitoscovid.ATUALIZACAO
            `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o valor de leitos das regiões: " + err)
                return
            }
            result = rows.rows;
            regionais = [];
            totalEstado = [];
            result.forEach(item => {
                if (!regionais[item.id]) {
                    regionais[item.id] = {
                        "name": item.regional_saude,
                        "mode": "lines",
                        "type": "scatter",
                        "visible": "legendonly",
                        "x": [],
                        "y": []
                    };
                };
                regionais[item.id].x.push(item.data);
                regionais[item.id].y.push((item.leitos_ocupados / item.leitos_ativos) * 100);

                if (!totalEstado[item.data]) {
                    totalEstado[item.data] = {
                        "leitos_ocupados": 0,
                        "leitos_ativos": 0,
                        "data": item.data

                    };
                }
                totalEstado[item.data].leitos_ocupados += parseInt(item.leitos_ocupados);
                totalEstado[item.data].leitos_ativos += parseInt(item.leitos_ativos);

            });

            regionais[0] = {
                "name": "Estado de SC",
                "mode": "lines",
                "type": "scatter",
                "x": [],
                "y": []
            };

            for (var [key, item] of Object.entries(totalEstado)) {
                regionais[0].x.push(item.data);
                regionais[0].y.push((item.leitos_ocupados / item.leitos_ativos) * 100);
            }


            res.send({ regionais })
        })
})

app.get('/api/dados-estado/', (req, res) => {

    pool.query(
        `SELECT VIEW_RT.REGIONAL_SAUDE AS REGIONAIS,
            VIEW_RT.ID AS ID,
            VIEW_RT.DATA AS RT_DATA,
            VIEW_RT.RT AS RT_VALOR,
            VIEW_RT.poligono AS POLIGONO,
            VIEW_RT.url AS url,
            1 - (VIEW_LEITOS.LEITOS_ATIVOS - VIEW_LEITOS.LEITOS_OCUPADOS)/VIEW_LEITOS.LEITOS_ATIVOS :: NUMERIC LEITOS_OCUPADOS,
            VIEW_LEITOS.MAX_DATA AS LEITOS_DATA,
            VIEW_CASOS_ATUAL.DATA AS DATA_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR.DATA AS DATA_CASOS_ANTERIOR,
            (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS VARIACAO
        FROM VIEW_RT,
            VIEW_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR,
            VIEW_LEITOS
        WHERE VIEW_RT.ID = VIEW_CASOS_ATUAL.ID
                        AND VIEW_RT.ID = VIEW_CASOS_ANTERIOR.ID
                        AND VIEW_RT.ID = VIEW_LEITOS.ID
            `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados do estado: " + err)
                return
            }

            stateData = {
                "type": "FeatureCollection",
                "features": []
            };

            if (rows.rows.length > 0) {
                result = rows.rows;
                for (var i = 0; i < result.length; i++) {
                    mediamovel = result[i].variacao * 100;
                    /*mediamovel = mediamovel.toFixed(0);
                    if (mediamovel > 15){
                       mediamovel += "%";
                       mediamovel += " (EM ALTA)"
                    } else if((mediamovel <= 15) && (mediamovel >= -15)) {
                       mediamovel += "%";
                       mediamovel += " (ESTÁVEL)" 
                    } else if (mediamovel < -15){
                       mediamovel += "%";
                       mediamovel += " (QUEDA)" 
                    }*/

                    leitos = result[i].leitos_ocupados * 100;

                    stateData.features.push(
                        {
                            "type": "Feature",
                            "regional_id": result[i].id,
                            "properties": {
                                "name": result[i].regionais,
                                "rt": Number(result[i].rt_valor),
                                "media_movel": mediamovel,
                                // result[i].variacao,

                                // "ocupacao_leitos": leitos.toFixed(0) + "%",
                                "ocupacao_leitos": leitos,
                                "path": result[i].url
                            },
                            "geometry": result[i].poligono
                        }
                    );
                }
            }

            res.send({ stateData })
        })
})

app.get('/api/dados-regiao/:id', (req, res) => {
    id = req.params.id;
    pool.query(
        `SELECT  VIEW_RT.RT AS RT_VALOR,
            1 - (VIEW_LEITOS.LEITOS_ATIVOS - VIEW_LEITOS.LEITOS_OCUPADOS)/VIEW_LEITOS.LEITOS_ATIVOS :: NUMERIC LEITOS_OCUPADOS,
            (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS VARIACAO
        FROM VIEW_RT,
            VIEW_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR,
            VIEW_LEITOS
        WHERE VIEW_RT.ID = VIEW_CASOS_ATUAL.ID
                        AND VIEW_RT.ID = VIEW_CASOS_ANTERIOR.ID
                        AND VIEW_RT.ID = VIEW_LEITOS.ID
						AND VIEW_RT.ID = $1
            `,
        [id],
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados do estado: " + err)
                return
            }

            if (rows.rows.length > 0) {
                result = rows.rows;
                mediamovel = result[0].variacao * 100;
                leitos = result[0].leitos_ocupados * 100;

                dados = {
                    "rt": (result[0].rt_valor * 1).toFixed(2),
                    "media_movel": mediamovel.toFixed(2),
                    "ocupacao_leitos": leitos.toFixed(2)
                };

                res.send(dados)
            }
        })
})

app.listen(port, () => {
    console.log(`App running on port ${port}.`)
})