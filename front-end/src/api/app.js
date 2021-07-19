const { Pool, Client } = require("pg");
const bodyParser = require("body-parser");
var cors = require("cors");

const express = require("express");
const app = express();

let port = 3000;

// https://medium.com/zero-equals-false/using-cors-in-express-cac7e29b005b
// em produção devemos limitar somente para ambiente de desenvolvimento e para o domínio da aplicação.
app.use(cors());

const pool = new Pool({
    user: "postgres", // postgres marcelo
    host: "localhost",
    database: "covid", // covid - mauricio
    //password: 'zzdz0737', // postgres mauricio
    password: "!admpasswd@covid", // postgres marcelo WEpJqsYMnHWB //!admpasswd@covid
    port: 5432,
});

regions = {
    0: "Ignorado",
    1: "NULL",
    2: "ALTO URUGUAI CATARINENSE",
    3: "ALTO VALE DO ITAJAI",
    4: "ALTO VALE DO RIO DO PEIXE",
    5: "CARBONIFERA",
    6: "EXTREMO OESTE",
    7: "EXTREMO SUL CATARINENSE",
    8: "FOZ DO RIO ITAJAI",
    9: "GRANDE FLORIANOPOLIS",
    10: "LAGUNA",
    11: "MEDIO VALE DO ITAJAI",
    12: "MEIO OESTE",
    13: "NORDESTE",
    14: "OESTE",
    15: "PLANALTO NORTE",
    16: "SERRA CATARINENSE",
    17: "XANXERÊ",
};
regions_array = [
    "Ignorado",
    "ESTADO DE SC",
    "ALTO URUGUAI CATARINENSE",
    "ALTO VALE DO ITAJAI",
    "ALTO VALE DO RIO DO PEIXE",
    "CARBONIFERA",
    "EXTREMO OESTE",
    "EXTREMO SUL CATARINENSE",
    "FOZ DO RIO ITAJAI",
    "GRANDE FLORIANOPOLIS",
    "LAGUNA",
    "MEDIO VALE DO ITAJAI",
    "MEIO OESTE",
    "NORDESTE",
    "OESTE",
    "PLANALTO NORTE",
    "SERRA CATARINENSE",
    "XANXERÊ",
];
app.get("/", (req, res) => {
    res.send("Server up!");
});

app.get("/api/casos-por-regiao/:id", (req, res) => {
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
        `, [id],
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar por região: " + err);
                return;
            }

            region = regions[id];

            if (typeof region === "undefined") {
                res.send("Região não reconhecida. Informe um ID válido.");
                return;
            }

            if (rows.rows.length > 0) {
                maxData = 0;
                rows.rows.forEach((item) => {
                    if (item.data > maxData) maxData = item.data;
                });
                datas = rows.rows.map((row) => {
                    return row.data;
                });

                casos = rows.rows.map((row) => {
                    return row.casos_dia;
                });

                casos_media_movel = rows.rows.map((row) => {
                    return row.casos_mediamovel;
                });

                obitos = rows.rows.map((row) => {
                    return row.obitos_dias;
                });

                obitos_media_movel = rows.rows.map((row) => {
                    return row.obitos_mediamovel;
                });

                casos_acumulados = rows.rows.map((row) => {
                    return row.casos_acumulados;
                });

                obitos_acumulados = rows.rows.map((row) => {
                    return row.obitos_acumulados;
                });
                incidencia = rows.rows.map((row) => {
                    return (row.casos_acumulados / row.populacao) * 1e5;
                });

                letalidade = rows.rows.map((row) => {
                    return row.letalidade;
                });
            }
            var d = new Date(maxData);
            var maiorData = ("0" + d.getDate()).slice(-2) + "/" + ("0" + (d.getMonth() + 1)).slice(-2) + "/" + d.getFullYear();

            res.send({
                region,
                maiorData,
                datas,
                casos,
                casos_media_movel,
                obitos,
                obitos_media_movel,
                casos_acumulados,
                obitos_acumulados,
                letalidade,
                incidencia,
            });
        },
    );
});

app.get("/api/casos-por-regiao/", (req, res) => {
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
                console.log("Erro ao buscar o casos por região: " + err);
                return;
            }

            result = rows.rows;
            regionais_casos_acumulados = [];
            regionais_obitos_acumulados = [];
            regionais_casos_mediamovel = [];
            regionais_obitos_mediamovel = [];
            regionais_incidencia = [];
            regionais_letalidade = [];
            maxData = 0;
            result.forEach((item) => {
                if (!regionais_casos_acumulados[item.id]) {
                    if (item.id == 1) {
                        regionais_casos_acumulados[item.id] = {
                            name: "Estado de SC",
                            mode: "lines",
                            type: "scatter",
                            x: [],
                            y: [],
                        };
                    } else {
                        regionais_casos_acumulados[item.id] = {
                            name: item.regional_saude,
                            mode: "lines",
                            type: "scatter",
                            visible: "legendonly",
                            x: [],
                            y: [],
                        };
                    }
                }
                if (!regionais_obitos_acumulados[item.id]) {
                    if (item.id == 1) {
                        regionais_obitos_acumulados[item.id] = {
                            name: "Estado de SC",
                            mode: "lines",
                            type: "scatter",
                            x: [],
                            y: [],
                        };
                    } else {
                        regionais_obitos_acumulados[item.id] = {
                            name: item.regional_saude,
                            mode: "lines",
                            type: "scatter",
                            visible: "legendonly",
                            x: [],
                            y: [],
                        };
                    }
                }
                // Casos média móvel
                if (!regionais_casos_mediamovel[item.id]) {
                    if (item.id == 1) {
                        regionais_casos_mediamovel[item.id] = {
                            name: "Estado de SC",
                            mode: "lines",
                            type: "scatter",
                            x: [],
                            y: [],
                        };
                    } else {
                        regionais_casos_mediamovel[item.id] = {
                            name: item.regional_saude,
                            mode: "lines",
                            type: "scatter",
                            visible: "legendonly",
                            x: [],
                            y: [],
                        };
                    }
                }

                // Óbitos média móvel
                if (!regionais_obitos_mediamovel[item.id]) {
                    if (item.id == 1) {
                        regionais_obitos_mediamovel[item.id] = {
                            name: "Estado de SC",
                            mode: "lines",
                            type: "scatter",
                            x: [],
                            y: [],
                        };
                    } else {
                        regionais_obitos_mediamovel[item.id] = {
                            name: item.regional_saude,
                            mode: "lines",
                            type: "scatter",
                            visible: "legendonly",
                            x: [],
                            y: [],
                        };
                    }
                }

                if (!regionais_incidencia[item.id]) {
                    if (item.id == 1) {
                        regionais_incidencia[item.id] = {
                            name: "Estado de SC",
                            mode: "lines",
                            type: "scatter",
                            x: [],
                            y: [],
                        };
                    } else {
                        regionais_incidencia[item.id] = {
                            name: item.regional_saude,
                            mode: "lines",
                            type: "scatter",
                            visible: "legendonly",
                            x: [],
                            y: [],
                        };
                    }
                }

                if (!regionais_letalidade[item.id]) {
                    if (item.id == 1) {
                        regionais_letalidade[item.id] = {
                            name: "Estado de SC",
                            mode: "lines",
                            type: "scatter",
                            x: [],
                            y: [],
                        };
                    } else {
                        regionais_letalidade[item.id] = {
                            name: item.regional_saude,
                            mode: "lines",
                            type: "scatter",
                            visible: "legendonly",
                            x: [],
                            y: [],
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
                regionais_incidencia[item.id].y.push(
                    (item.casos_acumulados / item.populacao) * 1e5,
                );

                regionais_letalidade[item.id].x.push(item.data);
                regionais_letalidade[item.id].y.push(item.letalidade);

                if (item.data > maxData) maxData = item.data;
            });
            var d = new Date(maxData);
            var maiorData = ("0" + d.getDate()).slice(-2) + "/" + ("0" + (d.getMonth() + 1)).slice(-2) + "/" + d.getFullYear();

            res.send({
                maiorData,
                regionais_casos_acumulados,
                regionais_obitos_acumulados,
                regionais_casos_mediamovel,
                regionais_obitos_mediamovel,
                regionais_incidencia,
                regionais_letalidade,
            });
        },
    );
});

app.get("/api/rt-por-regiao/:id", (req, res) => {
    id = req.params.id;

    pool.query(
        `SELECT RT_REGIONAL.DATA as data,
            RT_REGIONAL.VALOR_R as rt
        FROM REGIONAIS, RT_REGIONAL
        WHERE RT_REGIONAL.REGIONAL = REGIONAIS.ID
                AND RT_REGIONAL.REGIONAL = $1
        ORDER BY REGIONAIS.REGIONAL_SAUDE, RT_REGIONAL.DATA
            `, [id],
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o R(T) por região: " + err);
                return;
            }

            region = regions[id];

            if (typeof region === "undefined") {
                res.send("Região não reconhecida. Informe um ID válido.");
                return;
            }

            if (rows.rows.length > 0) {
                datas = rows.rows.map((row) => {
                    return row.data;
                });
                rt = rows.rows.map((row) => {
                    return row.rt;
                });
            }

            res.send({ region, datas, rt });
        },
    );
});

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

app.get("/api/rt-por-regiao/", (req, res) => {
    pool.query(
        `SELECT REGIONAIS.regional_saude, REGIONAIS.id, RT_REGIONAL.DATA as data,
            RT_REGIONAL.VALOR_R as rt
            FROM REGIONAIS, RT_REGIONAL
            WHERE RT_REGIONAL.REGIONAL = REGIONAIS.ID
            ORDER BY REGIONAIS.REGIONAL_SAUDE, RT_REGIONAL.DATA
            `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o valor de R(t) por região: " + err);
                return;
            }

            result = rows.rows;
            regionais = [];
            result.forEach((item) => {
                if (!regionais[item.id]) {
                    if (item.id == 1) {
                        regionais[item.id] = {
                            name: "Estado de SC",
                            mode: "lines",
                            type: "scatter",
                            x: [],
                            y: [],
                        };
                    } else {
                        regionais[item.id] = {
                            name: item.regional_saude,
                            mode: "lines",
                            type: "scatter",
                            visible: "legendonly",
                            x: [],
                            y: [],
                        };
                    }
                }
                regionais[item.id].x.push(item.data);
                regionais[item.id].y.push(item.rt);
            });

            // pool.query(
            //     `SELECT REGIONAIS.REGIONAL_SAUDE AS REGIONAL_SAUDE,
            //         RT_REGIONAL_PREDICTION.REGIONAL_SAUDE AS ID,
            //         RT_REGIONAL_PREDICTION.DATA AS DATA,
            //         RT_REGIONAL_PREDICTION.PRED AS RT,
            //         RT_REGIONAL_PREDICTION."pred_IC_95_inf",
            //         RT_REGIONAL_PREDICTION."pred_IC_95_sup"
            //     FROM REGIONAIS,
            //         RT_REGIONAL_PREDICTION
            //     WHERE RT_REGIONAL_PREDICTION.REGIONAL_SAUDE = REGIONAIS.ID`,
            //     (err, rows) => {
            //         if (err) {
            //             console.log("Erro ao buscar o valor da predição do R(t): " + err);
            //             res.send({ regionais });
            //         }

            //         result = rows.rows;
            //         result.forEach((item) => {
            //             var id = parseInt(item.id);
            //             if (!regionais[id + 20]) {
            //                 if (id == 1 + 20) {
            //                     regionais[id + 20] = {
            //                         name: "Estado de SC - Predição",
            //                         mode: "lines",
            //                         type: "scatter",
            //                         x: [],
            //                         y: [],
            //                     };
            //                 } else {
            //                     regionais[id + 20] = {
            //                         name: item.regional_saude + " - Predição",
            //                         mode: "lines",
            //                         type: "scatter",
            //                         visible: "legendonly",
            //                         x: [],
            //                         y: [],
            //                     };
            //                 }
            //             }
            //             regionais[id + 20].x.push(item.data);
            //             regionais[id + 20].y.push(item.rt);
            //         });

            //         res.send({ regionais });
            //     },
            // );
            res.send({ regionais });
        },
    );
});

app.get("/api/rt-estado/", (req, res) => {
    pool.query(
        `SELECT RT.DATA as data,
            RT.RT as rt
        FROM RT
        WHERE RT.REGIONAL = 1
        ORDER BY RT.DATA
            `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o R(T) do estado: " + err);
                return;
            }

            if (rows.rows.length > 0) {
                datas = rows.rows.map((row) => {
                    return row.data;
                });

                rt = rows.rows.map((row) => {
                    return row.rt;
                });
            }

            res.send({ datas, rt });
        },
    );
});

app.get("/api/leitos-por-regiao/:id", (req, res) => {
    id = req.params.id;
    pool.query(
        `SELECT REGIONAL_SAUDE, ID,
        LEITOS_OCUPADOS,
        LEITOS_ATIVOS_MAX,
        DATA
    FROM PUBLIC.VIEW_LEITOS_MAX
    WHERE ID = $1
            `, [id],
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o valor de leitos da região: " + err);
                return;
            }

            region = regions[id];
            if (typeof region === "undefined") {
                res.send("Região não reconhecida. Informe um ID válido.");
                return;
            }

            leitos_ocupados = {
                name: "Leitos Ocupados",
                type: "scatter",
                fill: 'tozeroy',
                opacity: 0.5,
                x: [],
                y: [],
            };
            leitos_disponiveis = {
                name: "Leitos Máximo",
                type: "scatter",
                fill: 'tonextx',
                opacity: 0.4,
                x: [],
                y: [],
            };

            result = rows.rows;
            result.forEach((item) => {
                leitos_ocupados.x.push(item.data);
                leitos_ocupados.y.push(item.leitos_ocupados);

                leitos_disponiveis.x.push(item.data);
                leitos_disponiveis.y.push(item.leitos_ativos_max);
            });

            res.send({ leitos_disponiveis, leitos_ocupados });
        },
    );
});

app.get("/api/leitos-por-regiao/", (req, res) => {
    pool.query(
        `SELECT REGIONAL_SAUDE, ID,
            LEITOS_OCUPADOS,
            LEITOS_ATIVOS_MAX,
            TO_CHAR(DATA,'YYYY-MM-DD') AS DATA
        FROM PUBLIC.VIEW_LEITOS_MAX
            `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o valor de leitos das regiões: " + err);
                return;
            }
            result = rows.rows;
            regionais = [];
            totalEstado = new Map();
            totalEstadoData = new Set();

            result.forEach((item) => {
                dataItem = item.data;
                if (!regionais[item.id]) {
                    regionais[item.id] = {
                        name: item.regional_saude,
                        mode: "lines",
                        type: "scatter",
                        visible: "legendonly",
                        x: [],
                        y: [],
                    };
                }
                regionais[item.id].x.push(item.data);
                regionais[item.id].y.push(
                    (item.leitos_ocupados / item.leitos_ativos_max),
                );

                totalEstadoData.add(dataItem)
                if (!totalEstado.has(dataItem)) {
                    totalEstado.set(dataItem, {
                        leitos_ocupados: 0,
                        leitos_ativos_max: 0,
                        data: item.data,
                    });
                }
                totalEstado.get(dataItem).leitos_ocupados += parseInt(item.leitos_ocupados);
                totalEstado.get(dataItem).leitos_ativos_max += parseInt(item.leitos_ativos_max);
            });

            regionais[0] = {
                name: "Estado de SC",
                mode: "lines",
                type: "scatter",
                x: [],
                y: [],
            };

            arrData = Array.from(totalEstadoData).sort();

            leitos_ativos_max_anterior =  totalEstado.get(arrData[0]).leitos_ativos_max 
            arrData.forEach(function (key) {
                // console.log(totalEstado.get(key).data);
                regionais[0].x.push(totalEstado.get(key).data);
                regionais[0].y.push((totalEstado.get(key).leitos_ocupados / totalEstado.get(key).leitos_ativos_max));
                // if (totalEstado.get(key).leitos_ativos_max != leitos_ativos_max_anterior){
                //     console.log("Mudança no dia " + key + ", era: " + leitos_ativos_max_anterior + ", passou:" + totalEstado.get(key).leitos_ativos_max); 
                //     // Alex: inserir as anotações das mudanças
                // }
                leitos_ativos_max_anterior = totalEstado.get(key).leitos_ativos_max;
            });

            res.send({ regionais });
        },
    );
});

// app.get("/api/leitos-por-regiao/:id", (req, res) => {
//     id = req.params.id;
//     pool.query(
//         `SELECT SUM(leitoscovid.LEITOS_OCUPADOS) AS LEITOS_OCUPADOS,
//                 SUM(leitoscovid.LEITOS_ATIVOS) AS LEITOS_ATIVOS,
//                 leitoscovid.ATUALIZACAO AS DATA
//             FROM leitoscovid
//             WHERE leitoscovid.INDEX_REGIONAL = $1
//             GROUP BY leitoscovid.ATUALIZACAO
//             ORDER BY leitoscovid.ATUALIZACAO
//             `, [id],
//         (err, rows) => {
//             if (err) {
//                 console.log("Erro ao buscar o valor de leitos da região: " + err);
//                 return;
//             }

//             region = regions[id];
//             if (typeof region === "undefined") {
//                 res.send("Região não reconhecida. Informe um ID válido.");
//                 return;
//             }

//             leitos_ocupados = {
//                 name: "Leitos Ocupados",
//                 type: "scatter",
//                 fill: 'tozeroy',
//                 opacity: 0.5,
//                 x: [],
//                 y: [],
//             };
//             leitos_disponiveis = {
//                 name: "Leitos Totais",
//                 type: "scatter",
//                 fill: 'tonextx',
//                 opacity: 0.4,
//                 x: [],
//                 y: [],
//             };

//             result = rows.rows;
//             result.forEach((item) => {
//                 leitos_ocupados.x.push(item.data);
//                 leitos_ocupados.y.push(item.leitos_ocupados);

//                 leitos_disponiveis.x.push(item.data);
//                 leitos_disponiveis.y.push(item.leitos_ativos);
//             });

//             res.send({ leitos_disponiveis, leitos_ocupados });
//         },
//     );
// });


// app.get("/api/leitos-por-regiao/", (req, res) => {
//     pool.query(
//         `SELECT REGIONAIS.REGIONAL_SAUDE,
//                 REGIONAIS.ID as ID,
//                 SUM(leitoscovid.LEITOS_ATIVOS) AS LEITOS_ATIVOS,
//                 SUM(leitoscovid.LEITOS_OCUPADOS) AS LEITOS_OCUPADOS,
//                 leitoscovid.ATUALIZACAO AS DATA
//             FROM REGIONAIS,
//             leitoscovid
//             WHERE leitoscovid.INDEX_REGIONAL = REGIONAIS.ID
//             GROUP BY REGIONAIS.ID,
//                 leitoscovid.ATUALIZACAO,
//                 REGIONAIS.REGIONAL_SAUDE
//             ORDER BY REGIONAIS.ID,
//                 leitoscovid.ATUALIZACAO
//             `,
//         (err, rows) => {
//             if (err) {
//                 console.log("Erro ao buscar o valor de leitos das regiões: " + err);
//                 return;
//             }
//             result = rows.rows;
//             regionais = [];
//             totalEstado = [];
//             result.forEach((item) => {
//                 if (!regionais[item.id]) {
//                     regionais[item.id] = {
//                         name: item.regional_saude,
//                         mode: "lines",
//                         type: "scatter",
//                         visible: "legendonly",
//                         x: [],
//                         y: [],
//                     };
//                 }
//                 regionais[item.id].x.push(item.data);
//                 regionais[item.id].y.push(
//                     (item.leitos_ocupados / item.leitos_ativos) * 100,
//                 );

//                 if (!totalEstado[item.data]) {
//                     totalEstado[item.data] = {
//                         leitos_ocupados: 0,
//                         leitos_ativos: 0,
//                         data: item.data,
//                     };
//                 }
//                 totalEstado[item.data].leitos_ocupados += parseInt(
//                     item.leitos_ocupados,
//                 );
//                 totalEstado[item.data].leitos_ativos += parseInt(item.leitos_ativos);
//             });

//             regionais[0] = {
//                 name: "Estado de SC",
//                 mode: "lines",
//                 type: "scatter",
//                 x: [],
//                 y: [],
//             };

//             for (var [key, item] of Object.entries(totalEstado)) {
//                 regionais[0].x.push(item.data);
//                 regionais[0].y.push((item.leitos_ocupados / item.leitos_ativos) * 100);
//             }

//             res.send({ regionais });
//         },
//     );
// });

app.get("/api/vacinacao-por-regiao/:id", (req, res) => {
    id = req.params.id;

    pool.query(
        `SELECT REGIONAIS.REGIONAL_SAUDE,
                REGIONAIS.ID AS ID,
                REGIONAIS.POPULACAO AS POPULACAO,
                SUM(VACINACAO_DIVE."D1") AS VACINACAO_D1,
                SUM(VACINACAO_DIVE."D2") AS VACINACAO_D2,
                VACINACAO_DIVE."Data" AS DATA
            FROM REGIONAIS,
                VACINACAO_DIVE
            WHERE VACINACAO_DIVE.REGIONAL = REGIONAIS.ID
                AND REGIONAIS.ID = $1
            GROUP BY REGIONAIS.ID,
                REGIONAIS.REGIONAL_SAUDE,
                VACINACAO_DIVE."Data"
            ORDER BY REGIONAIS.ID,
                VACINACAO_DIVE."Data"
            `, [id],
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar OS valores de vacinação por região: " + err);
                return;
            }

            region = regions[id];
            if (typeof region === "undefined") {
                res.send("Região não reconhecida. Informe um ID válido.");
                return;
            }

            vacinados_D1 = {
                name: "Vacinados 1ª Dose",
                type: "scatter",
                fill: 'tozeroy',
                fillcolor: 'rgba(247, 238, 197, 0.6)',
                x: [],
                y: [],
            };
            vacinados_D2 = {
                name: "Vacinados 2ª Dose",
                type: "scatter",
                fill: 'tonextx',
                fillcolor: 'rgba(168, 168, 255, 0.5)',
                x: [],
                y: [],
            };

            result = rows.rows;
            result.forEach((item) => {
                vacinados_D1.x.push(item.data);
                vacinados_D1.y.push((item.vacinacao_d1 / item.populacao));

                vacinados_D2.x.push(item.data);
                vacinados_D2.y.push((item.vacinacao_d2 / item.populacao));
            });

            res.send({ vacinados_D1, vacinados_D2 });
        },
    );
});


app.get("/api/vacinacao-ms-por-regiao/:id", (req, res) => {
    id = req.params.id;

    pool.query(
        `SELECT ID,
            REGIONAL_SAUDE,
            POPULACAO,
            DATA,
            D1 AS VACINACAO_D1,
            D2 AS VACINACAO_D2
        FROM VIEW_VACINACAO_MS_POR_REGIAO
        WHERE ID = $1
        ORDER BY REGIONAL_SAUDE,
            DATA
            `, [id],
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar OS valores de vacinação do MS por região: " + err);
                return;
            }

            region = regions[id];
            if (typeof region === "undefined") {
                res.send("Região não reconhecida. Informe um ID válido.");
                return;
            }

            vacinados_D1 = {
                name: "Vacinados 1ª Dose",
                type: "scatter",
                fill: 'tozeroy',
                fillcolor: 'rgba(247, 238, 197, 0.6)',
                x: [],
                y: [],
            };
            vacinados_D2 = {
                name: "Vacinados 2ª Dose",
                type: "scatter",
                fill: 'tonextx',
                fillcolor: 'rgba(168, 168, 255, 0.5)',
                x: [],
                y: [],
            };

            result = rows.rows;
            result.forEach((item) => {
                vacinados_D1.x.push(item.data);
                vacinados_D1.y.push((item.vacinacao_d1 / item.populacao));

                vacinados_D2.x.push(item.data);
                vacinados_D2.y.push((item.vacinacao_d2 / item.populacao));
            });

            res.send({ vacinados_D1, vacinados_D2 });
        },
    );
});



app.get("/api/vacinacao-por-regiao/", (req, res) => {
    pool.query(
        `SELECT REGIONAIS.REGIONAL_SAUDE,
                REGIONAIS.ID AS ID,
                REGIONAIS.POPULACAO AS POPULACAO,
                SUM(VACINACAO_DIVE."D1") AS VACINACAO_D1,
                SUM(VACINACAO_DIVE."D2") AS VACINACAO_D2,
                TO_CHAR(VACINACAO_DIVE."Data",'YYYY-MM-DD') AS DATA
            FROM REGIONAIS,
                VACINACAO_DIVE
            WHERE VACINACAO_DIVE.REGIONAL = REGIONAIS.ID
            GROUP BY REGIONAIS.ID,
                REGIONAIS.REGIONAL_SAUDE,
                VACINACAO_DIVE."Data"
            ORDER BY REGIONAIS.ID,
                VACINACAO_DIVE."Data"
            `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o valores de vacinação por região: " + err);
                return;
            }

            result = rows.rows;
            regionais = [];
            totalEstadoData = new Set();
            totalEstado = new Map();
            result.forEach((item) => {
                // dataItem = new Date(item.data);
                dataItem = item.data;
                // dataItem = dataItem.getFullYear() + "/" + ("0" + (dataItem.getMonth() + 1)).slice(-2) + "/" + ("0" + dataItem.getUTCDay()).slice(-2)
                // dataItem = parseInt(dataItem.getFullYear() + ("0" + (dataItem.getMonth() + 1)).slice(-2) + ("0" + dataItem.getUTCDay()).slice(-2));
                if (!regionais[item.id]) {
                    regionais[item.id] = {
                        name: item.regional_saude,
                        mode: "lines",
                        type: "scatter",
                        visible: "legendonly",
                        x: [],
                        y: [],
                    };
                }
                regionais[item.id].x.push(item.data);
                regionais[item.id].y.push(
                    (item.vacinacao_d2 / item.populacao),
                );
                totalEstadoData.add(dataItem)
                if (!totalEstado.has(dataItem)) {
                    totalEstado.set(dataItem, {
                        populacao: parseInt(item.populacao),
                        vacinacao_d1: 0,
                        vacinacao_d2: 0,
                        data: item.data,
                    });
                }

                totalEstado.get(dataItem).vacinacao_d1 += parseInt(item.vacinacao_d1);
                totalEstado.get(dataItem).vacinacao_d2 += parseInt(item.vacinacao_d2);
                totalEstado.get(dataItem).populacao += parseInt(item.populacao);
            });

            regionais[0] = {
                name: "Estado de SC",
                mode: "lines",
                type: "scatter",
                x: [],
                y: [],
            };


            arrData = Array.from(totalEstadoData).sort();

            arrData.forEach(function (key) {
                // console.log(totalEstado.get(key).data);
                regionais[0].x.push(totalEstado.get(key).data);
                regionais[0].y.push((totalEstado.get(key).vacinacao_d2 / totalEstado.get(key).populacao));
            });

            res.send({ regionais });
        },
    );
});

app.get("/api/vacinacao-ms-por-regiao/", (req, res) => {
    pool.query(
        `SELECT ID,
            REGIONAL_SAUDE,
            POPULACAO,
            DATA, D1,
            D2 AS DOSES_APLICADAS
        FROM VIEW_VACINACAO_MS_POR_REGIAO ORDER BY REGIONAL_SAUDE,DATA
            `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o valores de vacinação de MS por região: " + err);
                return;
            }

            result = rows.rows;
            var regionais = [];
            regionais[0] = {
                name: "Estado de SC",
                mode: "lines",
                type: "scatter",
                x: [],
                y: [],
            };

            totalEstadoData = new Set();
            totalEstado = new Map();
            result.forEach((item) => {
                // dataItem = new Date(item.data);
                // dataItem = dataItem.getFullYear() + "/" + ("0" + (dataItem.getMonth() + 1)).slice(-2) + "/" + ("0" + dataItem.getUTCDay()).slice(-2)
                dataItem = item.data;
                if (!regionais[item.id]) {
                    regionais[item.id] = {
                        name: item.regional_saude,
                        mode: "lines",
                        type: "scatter",
                        visible: "legendonly",
                        x: [],
                        y: [],
                    };
                }
                regionais[item.id].x.push(item.data);
                regionais[item.id].y.push(
                    (item.doses_aplicadas / item.populacao),
                );
            });

            pool.query(
                `SELECT 
                    T.DATA,
                    SUM(REGIONAIS.POPULACAO) AS POPULACAO,
                    SUM(T.D2) OVER (ORDER BY DATA ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS DOSES_APLICADAS
                FROM
                    (SELECT VACINA_DATAAPLICACAO AS DATA,
                            SUM(DOSES_APLICADAS) AS D2
                        FROM VACINACAO_MS
                        WHERE VACINA_DESCRICAO_DOSE != '1ª Dose'
                        GROUP BY VACINA_DATAAPLICACAO
                        ORDER BY VACINA_DATAAPLICACAO) AS T,
                    REGIONAIS
                WHERE REGIONAIS.ID = 1
                GROUP BY T.DATA, T.D2
                ORDER  BY DATA;
                    `,
                (err, rows) => {
                    if (err) {
                        console.log("Erro ao buscar o valores de vacinação do estado da tabela de MS: " + err);
                        return;
                    }

                    result = rows.rows;
                    result.forEach((item) => {
                        // dataItem = new Date(item.data);
                        // dataItem = dataItem.getFullYear() + "/" + ("0" + (dataItem.getMonth() + 1)).slice(-2) + "/" + ("0" + dataItem.getUTCDay()).slice(-2)
                        dataItem = item.data;

                        regionais[0].x.push(item.data);
                        regionais[0].y.push(
                            (item.doses_aplicadas / item.populacao),
                        );
                    });
                    res.send({ regionais });
                },
            );


        },
    );
});

app.get("/api/dados-estado/", (req, res) => {
    pool.query(
        `SELECT VIEW_RT.REGIONAL_SAUDE AS REGIONAIS,
            VIEW_RT.ID AS ID, 
            (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS VARIACAO,
            VIEW_RT.DATA AS RT_DATA,
            VIEW_RT.RT AS RT_VALOR,
            VIEW_RT.poligono AS POLIGONO,
            VIEW_RT.url AS url,
            (VIEW_LEITOS_MAX.LEITOS_OCUPADOS:: NUMERIC / VIEW_LEITOS_MAX.LEITOS_ATIVOS_MAX:: NUMERIC) LEITOS_OCUPADOS,
            VIEW_LEITOS_MAX.DATA AS LEITOS_DATA, 
            VIEW_CASOS_ATUAL.DATA AS DATA_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR.DATA AS DATA_CASOS_ANTERIOR,
            VIEW_INCIDENCIA.INCIDENCIA,
            TABELA_ESTADO.INCIDENCIA AS INCIDENCIA_SC,
            VIEW_INCIDENCIA.LETALIDADE,
            TABELA_ESTADO.LETALIDADE AS LETALIDADE_SC,
            view_vacinacao.vacinacao_d2 / view_vacinacao.populacao AS D2_DIVE,
            (VIEW_VACINACAO_MS_POR_REGIAO.D2 / VIEW_VACINACAO_MS_POR_REGIAO.POPULACAO) AS D2_MS
        FROM VIEW_RT,
            VIEW_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR,
            VIEW_LEITOS_MAX,
            VIEW_INCIDENCIA,
            view_vacinacao,
            VIEW_VACINACAO_MS_POR_REGIAO,
            (SELECT VIEW_INCIDENCIA.LETALIDADE, VIEW_INCIDENCIA.INCIDENCIA
                FROM VIEW_INCIDENCIA
                WHERE VIEW_INCIDENCIA.ID  = 1) as TABELA_ESTADO
        WHERE VIEW_RT.ID = VIEW_CASOS_ATUAL.ID
            AND VIEW_RT.ID = VIEW_CASOS_ANTERIOR.ID
            AND VIEW_RT.ID = VIEW_LEITOS_MAX.ID
            AND VIEW_RT.ID = VIEW_INCIDENCIA.ID
            AND VIEW_RT.ID = VIEW_VACINACAO_MS_POR_REGIAO.ID
            AND VIEW_RT.ID = view_vacinacao.ID	
            AND VIEW_LEITOS_MAX.DATA = (SELECT MAX(DATA) FROM VIEW_LEITOS_MAX)
            AND VIEW_VACINACAO_MS_POR_REGIAO.DATA = (SELECT MAX(DATA) FROM VIEW_VACINACAO_MS_POR_REGIAO)
            `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados do estado: " + err);
                return;
            }

            stateData = {
                type: "FeatureCollection",
                features: [],
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
                    incidencia = result[i].incidencia;
                    letalidade  = result[i].letalidade;
                    vacinacao = result[i].d2_populacao * 100;
                    

                    stateData.features.push({
                        type: "Feature",
                        regional_id: result[i].id,
                        properties: {
                            name: result[i].regionais,
                            rt: Number(result[i].rt_valor),
                            media_movel: mediamovel,
                            // result[i].variacao,
                            // "ocupacao_leitos": leitos.toFixed(0) + "%",
                            ocupacao_leitos: leitos,
                            incidencia:incidencia,
                            letalidade:letalidade,
                            vacinacao: vacinacao,
                            
                            path: result[i].url,
                        },
                        geometry: result[i].poligono,
                    });
                }
            }

            res.send({ stateData });
        },
    );
});

app.get("/api/dados-regiao/:id", (req, res) => {
    id = req.params.id;
    pool.query(
        `SELECT DISTINCT
            VIEW_RT.RT AS RT_VALOR,
            1 - (VIEW_LEITOS.LEITOS_ATIVOS - VIEW_LEITOS.LEITOS_OCUPADOS)/VIEW_LEITOS.LEITOS_ATIVOS :: NUMERIC LEITOS_OCUPADOS,
            (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS VARIACAO,
            VIEW_INCIDENCIA.LETALIDADE,
            VIEW_INCIDENCIA.INCIDENCIA,
            VACINACAO.D2_POPULACAO
            
        FROM VIEW_RT,
            VIEW_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR,
            VIEW_LEITOS,
            VIEW_INCIDENCIA,
            (SELECT ID, (D2 / POPULACAO) AS D2_POPULACAO FROM VIEW_VACINACAO_MS_POR_REGIAO WHERE DATA = (SELECT MAX(DATA) FROM VIEW_VACINACAO_MS_POR_REGIAO) ) AS VACINACAO

        WHERE VIEW_RT.ID = VIEW_CASOS_ATUAL.ID
                    AND VIEW_RT.ID = VIEW_CASOS_ANTERIOR.ID
                    AND VIEW_RT.ID = VIEW_LEITOS.ID
                    AND VIEW_RT.ID = VIEW_INCIDENCIA.ID
                    AND VIEW_RT.ID = VACINACAO.ID
                    AND VIEW_RT.ID = $1
            `, [id],

        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados do estado: " + err);
                return;
            }

            console.log(rows.rows);

            if (rows.rows.length > 0) {
                result = rows.rows;
                mediamovel = result[0].variacao * 100;
                leitos = result[0].leitos_ocupados * 100;
                

                dados = {
                    rt: (result[0].rt_valor * 1).toFixed(2),
                    media_movel: mediamovel.toFixed(2),
                    ocupacao_leitos: leitos.toFixed(2),
                };

                res.send(dados);
            }
        },
    );
});


// app.get("/api/leitos-atuais/", (req, res) => {
//     pool.query(
//         `SELECT REGIONAIS.REGIONAL_SAUDE as regional,
//           VIEW_LEITOS.LEITOS_ATIVOS as ativos,
//           VIEW_LEITOS.LEITOS_OCUPADOS as ocupados,
//           VIEW_LEITOS.MAX_DATA as data
//         FROM VIEW_LEITOS,
//           REGIONAIS
//         WHERE VIEW_LEITOS.ID = REGIONAIS.ID
//         ORDER BY REGIONAIS.REGIONAL_SAUDE`,
//         (err, rows) => {
//             if (err) {
//                 console.log("Erro ao buscar o valor de leitos das regiões: " + err);
//                 return;
//             }
//             result = rows.rows;
//             regionais = [];
//             result.forEach((item) => {
//                 item.percentual = ((item.ocupados / item.ativos) * 100).toFixed(2);
//                 regionais.push(item)
//             });

//             var json2csv = require('json2csv').parse;
//             var data = json2csv(regionais);

//             res.attachment('leitos.csv');
//             res.status(200).send(data);


//         },
//     );
// });



app.get("/api/dados-extrato/", (req, res) => {
    pool.query(
        `SELECT VIEW_RT.REGIONAL_SAUDE AS REGIONAIS,
        VIEW_RT.data AS DATA,
        1 - (VIEW_LEITOS.LEITOS_ATIVOS - VIEW_LEITOS.LEITOS_OCUPADOS) / VIEW_LEITOS.LEITOS_ATIVOS :: NUMERIC LEITOS_OCUPADOS,
        (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS MEDIA_MOVEL
    FROM VIEW_RT,
        VIEW_CASOS_ATUAL,
        VIEW_CASOS_ANTERIOR,
        VIEW_LEITOS
    WHERE VIEW_RT.ID = VIEW_CASOS_ATUAL.ID
                    AND VIEW_RT.ID = VIEW_CASOS_ANTERIOR.ID
                    AND VIEW_RT.ID = VIEW_LEITOS.ID
    ORDER BY REGIONAIS`,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados de extrato das regiões: " + err);
                return;
            }
            result = rows.rows;
            regionais = [];
            result.forEach((item) => {
                item.leitos_ocupados = (item.leitos_ocupados * 100).toFixed(2).replace(".", ",");
                item.media_movel = (item.media_movel * 100).toFixed(2).replace(".", ",");
                regionais.push(item)
            });

            var json2csv = require('json2csv').parse;
            var data = json2csv(regionais);

            res.attachment('extrato.csv');
            res.status(200).send(data);


        },
    );
});

// Variação Média Móvel,
// Ocupação Leito UTI,
// Taxa de Transmissibilidade,
// Taxa de Letalidade,
// Casos confirmados por 100 mil hab.
// Fila de espera - Leitos UTI

app.get("/api/dados-boletim/", (req, res) => {
    pool.query(
        `SELECT VIEW_RT.ID AS ID,
            VIEW_RT.REGIONAL_SAUDE AS REGIONAL,
            VIEW_RT.DATA AS DATA,
            (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS VAR_MEDIA_MOVEL,
            VIEW_RT.RT AS RT,
            VIEW_INCIDENCIA.LETALIDADE,
            VIEW_INCIDENCIA.INCIDENCIA
        FROM VIEW_RT,
            VIEW_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR,
            VIEW_INCIDENCIA
        WHERE VIEW_RT.ID = VIEW_CASOS_ATUAL.ID
            AND VIEW_RT.ID = VIEW_CASOS_ANTERIOR.ID
            AND VIEW_RT.ID = VIEW_INCIDENCIA.ID
        ORDER BY VIEW_RT.ID`,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados de extrato das regiões: " + err);
                return;
            }

            pool.query(
                `SELECT VIEW_LEITOS.ID AS ID,
                        VIEW_LEITOS.MAX_DATA AS DATA,
                        VIEW_LEITOS.LEITOS_ATIVOS LEITOS_ATIVOS,
                        VIEW_LEITOS.LEITOS_OCUPADOS AS LEITOS_OCUPADOS,
                        VIEW_VACINACAO.VACINACAO_D1,
                        VIEW_VACINACAO.VACINACAO_D2,
                        VIEW_VACINACAO.POPULACAO
                    FROM VIEW_RT,
                        VIEW_LEITOS,
                        VIEW_VACINACAO
                    WHERE VIEW_RT.ID = VIEW_LEITOS.ID
                        AND VIEW_RT.ID = VIEW_VACINACAO.ID
                    ORDER BY ID`,
                (err2, rows2) => {
                    if (err2) {
                        console.log("Erro ao buscar os dados de leitos das regiões: " + err);
                        return;
                    }

                    totalEstado = {
                        leitos_ocupados: 0,
                        leitos_ativos: 0,
                        populacao: 0,
                        vacinacao_d1: 0,
                        vacinacao_d2: 0,
                    }
                    result = rows.rows;
                    result_Leitos = rows2.rows;
                    regionais = [];
                    result.forEach((item) => {
                        item.var_media_movel = (item.var_media_movel * 100).toFixed(2).replace(".", ",");
                        // item.leitos_ocupados = (item.leitos_ocupados * 100).toFixed(2).replace(".", ",");
                        item.rt = (item.rt).replace(".", ",");
                        item.letalidade = (item.letalidade).toFixed(2).replace(".", ",");
                        item.incidencia = (item.incidencia).toFixed(2).replace(".", ",");
                        regionais[item.id] = item;

                    });

                    result_Leitos.forEach((item) => {
                        regionais[item.id].ocupacao_leitos = ((item.leitos_ocupados / item.leitos_ativos) * 100).toFixed(2).replace(".", ",");
                        regionais[item.id].vacinacao_d1 = ((item.vacinacao_d1 / item.populacao) * 100).toFixed(4).replace(".", ",");
                        regionais[item.id].vacinacao_d2 = ((item.vacinacao_d2 / item.populacao) * 100).toFixed(4).replace(".", ",");

                        totalEstado.leitos_ocupados += parseInt(item.leitos_ocupados);
                        totalEstado.leitos_ativos += parseInt(item.leitos_ativos);

                        totalEstado.populacao += parseInt(item.populacao);
                        totalEstado.vacinacao_d1 += parseInt(item.vacinacao_d1);
                        totalEstado.vacinacao_d2 += parseInt(item.vacinacao_d2);
                    });
                    regionais[1].ocupacao_leitos = ((totalEstado.leitos_ocupados / totalEstado.leitos_ativos) * 100).toFixed(2).replace(".", ",");
                    regionais[1].vacinacao_d1 = ((totalEstado.vacinacao_d1 / totalEstado.populacao) * 100).toFixed(4).replace(".", ",");
                    regionais[1].vacinacao_d2 = ((totalEstado.vacinacao_d2 / totalEstado.populacao) * 100).toFixed(4).replace(".", ",");
                    regionais[1].regional = "Estado de SC";
                    regionais = regionais.filter(function (el) {
                        return el != null;
                    });
                    var json2csv = require('json2csv').parse;
                    var data = json2csv(regionais);

                    res.attachment('boletim.csv');
                    res.status(200).send(data);
                },
            );
        });
});

app.get("/api/dados-rt/", (req, res) => {
    pool.query(
        `SELECT REGIONAIS.regional_saude, REGIONAIS.id AS ID, RT_REGIONAL.DATA as data,
            RT_REGIONAL.VALOR_R as rt
        FROM REGIONAIS, RT_REGIONAL
        WHERE RT_REGIONAL.REGIONAL = REGIONAIS.ID
        ORDER BY REGIONAIS.REGIONAL_SAUDE, RT_REGIONAL.DATA`,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados de leitos das regiões: " + err);
                return;
            }

            result = rows.rows;
            regionais = [];
            result.forEach((item) => {
                var dataItem = ("0" + item.data.getDate()).slice(-2) + "/" + ("0" + (item.data.getMonth() + 1)).slice(-2) + "/" + item.data.getFullYear();
                if (!regionais[dataItem]) {
                    regionais[dataItem] = new Array(18);
                }
                if (item.rt) {
                    regionais[dataItem][regions_array[item.id]] = (item.rt).replace(".", ",");
                }
            });

            dadosRegionais = []
            for (var data in regionais) {
                var value = regionais[data];
                value.unshift(data);
                dadosRegionais.push(value);
            }

            // regionais[1].ocupacao_leitos = ((totalEstado.leitos_ocupados / totalEstado.leitos_ativos) * 100).toFixed(2).replace(".", ",");
            // regionais[1].regional = "Estado de SC";
            //  regionais = regionais.filter(function (el) {
            //      return el != null;
            //  });

            var json2csv = require('json2csv').parse;
            var data = json2csv(dadosRegionais, { expandArrayObjects: true });

            res.attachment('dados_rt.csv');
            res.status(200).send(data);
        },
    );
});

app.get("/api/vacinacao-dive/", (req, res) => {
    pool.query(
        `SELECT
            ID,
            REGIONAL_SAUDE,
            POPULACAO,
            VACINACAO_D1 as D1,
            VACINACAO_D2 AS D2_UNICA,
            DATA AS DATA_ATUALIZACAO
            
        FROM VIEW_VACINACAO`,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados de vacinação DIVE das regiões: " + err);
                return;
            }
            result = rows.rows;
            dados = [];
            result.forEach((item) => {
                item.percentual_d1 = (item.d1 / item.populacao * 100).toFixed(2).replace(".", ",");
                item.percentual_d2 = (item.d2_unica / item.populacao * 100).toFixed(2).replace(".", ",");

                var data = new Date(item.data_atualizacao);
                var formatedDate = ("0" + data.getDate()).slice(-2) + "-" + ("0" + (data.getMonth() + 1)).slice(-2) + "-" + data.getFullYear();
                item.data_atualizacao = formatedDate;

                dados.push(item);
            });

            var json2csv = require('json2csv').parse;
            var data = json2csv(dados);

            res.attachment('vacinacao_dive.csv');
            res.status(200).send(data);
        });
});

app.get("/api/vacinacao-ms/", (req, res) => {
    pool.query(
        `SELECT 
            
            ID,
            REGIONAL_SAUDE,
            POPULACAO,
            D1,
            D2 AS D2_UNICA,
            DATA AS DATA_ATUALIZACAO

        FROM VIEW_VACINACAO_MS_POR_REGIAO
            WHERE DATA = (SELECT MAX(DATA)::DATE FROM VIEW_VACINACAO_MS_POR_REGIAO);
        `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados de vacinação MS das regiões: " + err);
                return;
            }
            result = rows.rows;
            dados = [];
            result.forEach((item) => {
                item.percentual_d1 = (item.d1 / item.populacao * 100).toFixed(2).replace(".", ",");
                item.percentual_d2 = (item.d2_unica / item.populacao * 100).toFixed(2).replace(".", ",");
                
                var data = new Date(item.data_atualizacao);
                var formatedDate = ("0" + data.getDate()).slice(-2) + "-" + ("0" + (data.getMonth() + 1)).slice(-2) + "-" + data.getFullYear();
                item.data_atualizacao = formatedDate;

                dados.push(item);
            });

            var json2csv = require('json2csv').parse;
            var data = json2csv(dados);

            res.attachment('vacinacao_ms.csv');
            res.status(200).send(data);
        });
});

app.listen(port, () => {
    console.log(`App running on port ${port}.`);
});
