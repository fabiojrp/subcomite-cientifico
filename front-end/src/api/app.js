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

// app.get("/api/rt-predict-por-regiao/", (req, res) => {
//     pool.query(
//         `SELECT REGIONAIS.REGIONAL_SAUDE AS REGIONAL_SAUDE,
//                 REGIONAIS.ID,
//                 RT_REGIONAL.DATA AS DATA,
//                 RT_REGIONAL.VALOR_R AS RT,
//                 RT_REGIONAL.VALOR_R AS RT_PRED_INF,
//                 RT_REGIONAL.VALOR_R AS RT_PRED_SUP
//             FROM REGIONAIS, RT_REGIONAL
//             WHERE RT_REGIONAL.REGIONAL = REGIONAIS.ID 
//                 AND RT_REGIONAL.DATA >= (SELECT NOW() - INTERVAL '15 DAYS')
//             UNION
//             SELECT REGIONAIS.REGIONAL_SAUDE AS REGIONAL_SAUDE,
//                 RT_REGIONAL_PREDICTION.REGIONAL_SAUDE AS ID,
//                 RT_REGIONAL_PREDICTION.DATA AS DATA,
//                 RT_REGIONAL_PREDICTION.PRED AS RT,
//                 RT_REGIONAL_PREDICTION."pred_IC_95_inf" AS RT_PRED_INF,
//                 RT_REGIONAL_PREDICTION."pred_IC_95_sup" AS RT_PRED_SUP
//             FROM REGIONAIS,
//                 RT_REGIONAL_PREDICTION
//             WHERE RT_REGIONAL_PREDICTION.REGIONAL_SAUDE = REGIONAIS.ID
//             ORDER BY REGIONAL_SAUDE, DATA`,
//         (err, rows) => {
//             if (err) {
//                 console.log("Erro ao buscar o valor de R(t) por região: " + err);
//                 return;
//             }

//             regionais = [];
//             rt = rows.rows;
//             rt.forEach((item) => {
//                 if (!regionais[item.id]) {
//                     regionais[item.id] = [];
                    
//                     regionais[item.id].push({
//                         name: item.regional_saude,
//                         mode: "lines",
//                         type: "scatter",
//                         visible: "true",
//                         x: [],
//                         y: [],
//                     });
//                     regionais[item.id].push({
//                         name: 'IC inferior',
//                         x: [],
//                         y: [],
//                         showlegend: false,
//                         line: {'width': 0},
//                         mode: 'lines'
//                         // type: 'scatter'
//                     });

//                     regionais[item.id].push({
//                         name: 'IC superior',
//                         x: [],
//                         y: [],
//                         fillcolor:'rgba(68, 68, 68, 0.2)',
//                         fill: 'tonexty',
//                         showlegend: false,
//                         mode: 'lines',
//                         line: {'width': 0}
//                         // type: 'scatter'
//                     });

//                     // regionais[item.id].push({
//                     //     name: item.regional_saude + '_predict',
//                     //     x: [],
//                     //     y: [],
//                     //     mode: 'lines+markers',
//                     //     line: {'dash': 'dash', 'color': 'green'},
//                     //     type: 'scatter'
//                     // });

//                 }
//                 regionais[item.id][0].x.push(item.data);
//                 regionais[item.id][0].y.push(item.rt);
//                 regionais[item.id][1].x.push(item.data);
//                 regionais[item.id][1].y.push(item.rt_pred_inf);
//                 regionais[item.id][2].x.push(item.data);
//                 regionais[item.id][2].y.push(item.rt_pred_sup);
//             });
//             res.send({ regionais });
//         },
//     );
// });

// app.get("/api/rt-predict-por-regiao/:id", (req, res) => {
//     id = req.params.id;

//     pool.query(
//         `SELECT RT_REGIONAL.DATA AS DATA,
//                 RT_REGIONAL.VALOR_R AS RT,
//                 RT_REGIONAL.VALOR_R AS RT_PRED_INF,
//                 RT_REGIONAL.VALOR_R AS RT_PRED_SUP
//             FROM RT_REGIONAL
//             WHERE RT_REGIONAL.regional = $1
//                 AND RT_REGIONAL.DATA >= (SELECT NOW() - INTERVAL '30 DAYS')
//             UNION
//             SELECT RT_REGIONAL_PREDICTION.DATA AS DATA,
//                 RT_REGIONAL_PREDICTION.PRED AS RT,
//                 RT_REGIONAL_PREDICTION."pred_IC_95_inf" AS RT_PRED_INF,
//                 RT_REGIONAL_PREDICTION."pred_IC_95_sup" AS RT_PRED_SUP
//             FROM RT_REGIONAL_PREDICTION
//             WHERE RT_REGIONAL_PREDICTION.regional_saude = $1
//             ORDER BY DATA`, [id] ,
//         (err, rows) => {
//             region = regions[id];
//             if (typeof region === "undefined") {
//                 res.send("Região não reconhecida. Informe um ID válido.");
//                 return;
//             }

//             if (err) {
//                 console.log("Erro ao buscar o valor de R(t) por região: " + err);
//                 return;
//             }
            
//             regional = {
//                 name: "RT + predição",
//                 x: [],
//                 y: [],
//                 mode: 'lines',
//                 line: {'color': 'red'},
//                 type: 'scatter'
//             };

//             regional_inferior = {
//                 name: 'IC inferior',
//                 x: [],
//                 y: [],
//                 showlegend: false,
//                 line: {'width': 0},
//                 mode: 'lines'
//                 // type: 'scatter'
//             };

//             regional_superior = {
//                 name: 'IC superior',
//                 x: [],
//                 y: [],
//                 fillcolor:'rgba(68, 68, 68, 0.2)',
//                 fill: 'tonexty',
//                 showlegend: false,
//                 mode: 'lines',
//                 line: {'width': 0}
//                 // type: 'scatter'
//             };
//             rt = rows.rows;
//             count = 0;
//             rt.forEach((item) => {
//                 regional.x.push(item.data);
//                 regional.y.push(item.rt);

//                 if (count >= rt.length - 5){
//                     regional_inferior.x.push(item.data);
//                     regional_inferior.y.push(item.rt_pred_inf);
//                     regional_superior.x.push(item.data);
//                     regional_superior.y.push(item.rt_pred_sup);
//                 }
//                 count++;
//             });
//             res.send({ regional, regional_inferior, regional_superior });
//         },
//     );
// });


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

app.get("/api/rt-predicao", (req, res) => {
            pool.query(
                `SELECT REGIONAIS.REGIONAL_SAUDE AS REGIONAL_SAUDE,
                    RT_REGIONAL_PREDICTION.REGIONAL_SAUDE AS ID,
                    RT_REGIONAL_PREDICTION.DATA AS DATA,
                    RT_REGIONAL_PREDICTION.PRED AS RT,
                    RT_REGIONAL_PREDICTION."pred_IC_95_inf",
                    RT_REGIONAL_PREDICTION."pred_IC_95_sup"
                FROM REGIONAIS,
                    RT_REGIONAL_PREDICTION
                WHERE RT_REGIONAL_PREDICTION.REGIONAL_SAUDE = REGIONAIS.ID`,
                (err, rows) => {
                    if (err) {
                        console.log("Erro ao buscar o valor da predição do R(t): " + err);
                        res.send({ regionais });
                    }

                    result = rows.rows;
                    regionais = [];
                    result.forEach((item) => {
                        var id = parseInt(item.id);
                        if (!regionais[id]) {
                            if (id == 1) {
                                regionais[id] = {
                                    name: "Estado de SC - Predição",
                                    mode: "lines",
                                    type: "scatter",
                                    x: [],
                                    y: [],
                                };
                            } else {
                                regionais[id] = {
                                    name: item.regional_saude + " - Predição",
                                    mode: "lines",
                                    type: "scatter",
                                    visible: "legendonly",
                                    x: [],
                                    y: [],
                                };
                            }
                        }
                        regionais[id].x.push(item.data);
                        regionais[id].y.push(item.rt);
                    });

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
            TO_CHAR(DATA,'YYYY-MM-DD HH:MI') AS DATA
        FROM VIEW_LEITOS_MAX
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

app.get("/api/leitos-covid-por-regiao/:id", (req, res) => {
    id = req.params.id;
    pool.query(
        `SELECT REGIONAL_SAUDE, ID,
            LEITOS_OCUPADOS,
            LEITOS_ATIVOS_MAX,
            DATA
        FROM PUBLIC.VIEW_LEITOS_COVID_MAX
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

app.get("/api/leitos-covid-por-regiao/", (req, res) => {
    pool.query(
        `SELECT REGIONAL_SAUDE, ID,
            LEITOS_OCUPADOS,
            LEITOS_ATIVOS_MAX,
            TO_CHAR(DATA,'YYYY-MM-DD HH:MI') AS DATA
        FROM VIEW_LEITOS_COVID_MAX
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

// app.get("/api/leitos-covid-por-regiao/:id", (req, res) => {
//     id = req.params.id; // Verificar query
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


// app.get("/api/leitos-covid-por-regiao/", (req, res) => {
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
                        populacao: 0,
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
                        WHERE VACINA_DESCRICAO_DOSE != '1ª Dose'
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
        `SELECT ID, REGIONAL, DATA,
            VAR_MEDIA_MOVEL, RT,
            POLIGONO, URL,
            LETALIDADE, INCIDENCIA,
            LEITOS_COVID_MAX, LEITOS_GERAL_MAX,
            LETALIDADE_SC, INCIDENCIA_SC,
            VACINACAO_D2_DIVE, VACINACAO_D2_MS,
            FASE_ANTERIOR AS FASE, DATA_MUDANCA_FASE, PONTUACAO
        FROM "avaliacaoRegionaisDiario"
        WHERE ID <> 1
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

            var vacinacao_fase = { "1": {descricao: ">= 20%", f: function(x) {return x > 0.2;}},
                "2": {descricao: ">= 20%", f: function(x) {return x >= 0.3;}},
                "3.1": {descricao: ">= 30%", f: function(x) {return x >= 0.4;}},
                "3.2": {descricao: ">= 40%", f: function(x) {return x >= 0.5;}},
                "3.3": {descricao: ">= 50%", f: function(x) {return x >= 0.75;}},
                "4": {descricao: ">= 75%",  f: function(x) {return x >= 1;}}
}

            if (rows.rows.length > 0) {
                result = rows.rows;
                for (var i = 0; i < result.length; i++) {
                    mediamovel = result[i].var_media_movel * 100;
                    // leitos = result[i].leitos_geral_max * 100;
                    incidencia = result[i].incidencia;
                    letalidade  = result[i].letalidade;
                    leitos_geral_max = result[i].leitos_geral_max * 100;
                    leitos_covid_max = result[i].leitos_covid_max * 100;

                    stateData.features.push({
                        type: "Feature",
                        regional_id: result[i].id,
                        properties: {
                            name: result[i].regional,
                            rt: Number(result[i].rt),
                            media_movel: mediamovel,
                            leitos_geral_max: leitos_geral_max,
                            leitos_covid_max: leitos_covid_max,
                            incidencia: incidencia,
                            incidencia_sc: result[i].incidencia_sc,
                            letalidade: letalidade,
                            letalidade_sc: result[i].letalidade_sc,
                            vacinacao_dive: result[i].vacinacao_d2_dive * 100,
                            vacinacao_ms: result[i].vacinacao_d2_ms * 100,
                            vacinacao_pontos: vacinacao_fase[result[i].fase].f(result[i].vacinacao_d2_dive) || vacinacao_fase[result[0].fase].f(result[0].vacinacao_d2_ms) ? 3: 0,
                            path: result[i].url,
                            fase_atual: result[i].fase,
                            pontuacao: result[i].pontuacao
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
        `SELECT ID, REGIONAL, DATA,
            VAR_MEDIA_MOVEL, RT,
            LETALIDADE, INCIDENCIA,
            LEITOS_COVID_MAX, LEITOS_GERAL_MAX,
            LETALIDADE_SC, INCIDENCIA_SC,
            VACINACAO_D2_DIVE, VACINACAO_D2_MS,
            FASE_ANTERIOR AS FASE, DATA_MUDANCA_FASE, PONTUACAO
        FROM "avaliacaoRegionaisDiario" 
        WHERE ID = $1
            `, [id],

        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados do estado: " + err);
                return;
            }

           // console.log(rows.rows);

            if (rows.rows.length > 0) {
                result = rows.rows;
                mediamovel = result[0].var_media_movel * 100;
                leitos_geral_max = result[0].leitos_geral_max * 100;
                leitos_covid_max = result[0].leitos_covid_max * 100;

                dados = {
                    rt: (result[0].rt * 1).toFixed(2),
                    media_movel: mediamovel.toFixed(2),
                    vacinacao: result[0].vacinacao_d2_dive * 100,
                    leitos_geral_max: leitos_geral_max,
                    leitos_covid_max: leitos_covid_max,
                    incidencia: result[0].incidencia.toFixed(2),
                    incidencia_sc: result[0].incidencia_sc.toFixed(2),
                    letalidade: result[0].letalidade.toFixed(2),
                    letalidade_sc: result[0].letalidade_sc.toFixed(2),
                    pontuacao: result[0].pontuacao,
                };

                res.send(dados);
            }
        },
    );
});


app.get("/api/fases-regiao/:id", (req, res) => {
    id = req.params.id;
    pool.query(
        `SELECT DATA_MUDANCA_FASE,
            FASE_ANTERIOR,
            FASE_CALCULADA
        FROM PUBLIC."avaliacaoRegionais"
        WHERE ID = $1
            AND FASE_ANTERIOR <> FASE_CALCULADA
            order by DATA`, [id],

        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar as fases da região: " + err);
                return;
            }
            result = rows.rows;
            var count = 0;
            var fases = [];
            fases[count] = {
                x: [result[0].data_mudanca_fase], 
                y: ["Fase " + result[0].fase_calculada], 
                name: "Fase " + result[0].fase_calculada,
                title: "teste 1",
                type: 'scatter',
                mode: "lines",
                opacity: 0.4,
                line: {
                  width: 30,
                }
            };

            for (count++; count < result.length; count++) {
                fases[count-1].x.push(result[count].data_mudanca_fase)
                fases[count-1].y.push("Fase " + result[count].fase_anterior)

                fases[count] = {
                    x: [result[count].data_mudanca_fase], 
                    y: ["Fase " + result[count].fase_calculada], 
                    name: "Fase " + result[count].fase_calculada,
                    type: 'scatter',
                    mode: "lines",
                    opacity: 0.4,
                    line: {
                      width: 30
                    }
                };
            }

            var tzoffset = (new Date()).getTimezoneOffset() * 60000
            var localISOTime = (new Date(Date.now() - tzoffset)).toISOString().slice(0, -1);
            fases[count-1].x.push(localISOTime)
            fases[count-1].y.push("Fase " + result[count-1].fase_calculada)

            res.send(fases);
        }
    );
});


app.get("/api/fases-regiao-detalhado/:id", (req, res) => {
    id = req.params.id;
    pool.query(
        `SELECT REGIONAL, DATA,
            VAR_MEDIA_MOVEL, RT,
            LEITOS_COVID_MAX, LEITOS_GERAL_MAX,
            INCIDENCIA, INCIDENCIA_SC,
            LETALIDADE, LETALIDADE_SC,
            VACINACAO_D2_DIVE, VACINACAO_D2_MS,
            FASE_ANTERIOR, DATA_MUDANCA_FASE,
            PONTUACAO, FASE_CALCULADA
        FROM "avaliacaoRegionais" 
        WHERE DATA = (SELECT MAX(DATA) FROM "avaliacaoRegionais" )
        AND ID = $1`, [id],

        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar as fases da região: " + err);
                return;
            }
            vacinacao_fase = { "1": {descricao: ">= 20%", f: function(x) {return x > 0.2;}},
                                "2": {descricao: ">= 20%", f: function(x) {return x >= 0.3;}},
                                "3.1": {descricao: ">= 30%", f: function(x) {return x >= 0.4;}},
                                "3.2": {descricao: ">= 40%", f: function(x) {return x >= 0.5;}},
                                "3.3": {descricao: ">= 50%", f: function(x) {return x >= 0.75;}},
                                "4": {descricao: ">= 75%",  f: function(x) {return x >= 1;}}
            }

            result = rows.rows;
            var d = result[0].data
            var dataBoletim = ("0" + d.getDate()).slice(-2) + "/" + ("0" + (d.getMonth() + 1)).slice(-2) + "/" + d.getFullYear();
            indicadores = { cabecalho: 
                            {   Regional: result[0].regional,
                                Data: dataBoletim,
                                Fase_anterior: result[0].fase_anterior,
                                Data_mudanca_fase: result[0].data_mudanca_fase,
                                Pontuacao: result[0].pontuacao,
                                Fase_calculada: result[0].fase_calculada
                            },
                            linhas:
                            [
                                [{
                                    campo: "Variação da média móvel",
                                    texto: "5 pontos se for menor ou igual a 15%",
                                    valor: (result[0].var_media_movel*100).toFixed(2) +'%',
                                    cor: result[0].var_media_movel <= 0.15? "green-fase-fundo" : "red-fase-fundo",
                                    cor_text: result[0].var_media_movel <= 0.15? "" : "red-fase"
                                   
                                },
                                {
                                    campo: "Taxa de transmissibilidade",
                                    texto: "5 pontos se o valor for menor ou igual a 1.0",
                                    valor: result[0].rt.toFixed(2),
                                    cor: result[0].rt < 1.00? "green-fase-fundo" : "red-fase-fundo",
                                    cor_text: result[0].rt < 1.00? "" : "red-text"                                   
                                },
                                {
                                    campo: "Leitos UTI Adulto",
                                    texto: "5 pontos caso a ocupação de Leitos UTI Adulto COVID ou Leitos UTI Adulto GERAL for menor do que 60% em relação a quantidade máxima de leitos disponíveis ",
                                    valor: "<p>Leitos UTI Adulto COVID/Máximo = " + (result[0].leitos_covid_max*100).toFixed(2) +'%'+ "</p>" + 
                                        "<p>Leitos UTI Adulto GERAL/Máximo = " + (result[0].leitos_geral_max*100).toFixed(2) +'%' + "</p>",
                                    cor: (result[0].leitos_covid_max < 0.6) || (result[0].leitos_geral_max < 0.6)  ? "green-fase-fundo" : "red-fase-fundo",
                                    cor_text: (result[0].leitos_covid_max < 0.6) || (result[0].leitos_geral_max < 0.6)  ? "" : "red-fase"

                                }],
                                [{
                                    campo: "Incidencia",
                                    texto: "2 pontos se incidência da região for menor ou igual que a referência do Estado",
                                    valor: "<p>Incidência da Região = " + (result[0].incidencia).toFixed(2) + "</p>" + 
                                    "<p>Incidência do Estado = " + (result[0].incidencia_sc).toFixed(2)  + "</p>",
                                    cor: result[0].incidencia <= result[0].incidencia_sc ? "green-fase-fundo" : "red-fase-fundo",
                                    cor_text: result[0].incidencia <= result[0].incidencia_sc ? "" : "red-fase"

                                },
                                {
                                    campo: "Letalidade",
                                    texto: "2 pontos se letalidade da região for menor ou igual que a referência do Estado",
                                    valor: "<p>Letalidade da Região = " + (result[0].letalidade).toFixed(2) + "</p>" + 
                                    "<p>Letalidade do Estado = " + (result[0].letalidade_sc).toFixed(2)  + "</p>",
                                    cor: result[0].letalidade <= result[0].letalidade_sc ? "green-fase-fundo" : "red-fase-fundo",
                                    cor_text: result[0].letalidade <= result[0].letalidade_sc ? "" : "red-fase",
                                },
                                {
                                    campo: "Vacinação",
                                    texto: "3 pontos conforme a fase da região.<br>O Campus está na fase " + result[0].fase_anterior + ", para pontuar na próxima fase a vacinação precisar que um dos indicadores seja " + vacinacao_fase[result[0].fase_anterior].descricao,
                                    valor: "<p>Vacinação - DIVE = " + (result[0].vacinacao_d2_dive*100).toFixed(2) + "</p>" + 
                                    "<p>Vacinação - OpenDataSus  = " + (result[0].vacinacao_d2_ms*100).toFixed(2)  + "</p>",
                                    cor: vacinacao_fase[result[0].fase_calculada].f(result[0].vacinacao_d2_dive) || vacinacao_fase[result[0].fase_calculada].f(result[0].vacinacao_d2_ms) ? "green-fase-fundo" : "red-fase-fundo",
                                    cor_text: vacinacao_fase[result[0].fase_calculada].f(result[0].vacinacao_d2_dive) || vacinacao_fase[result[0].fase_calculada].f(result[0].vacinacao_d2_ms) ? "": "red-fase"  
                                }],
                            ]


            }

            // result.forEach((item) => {

            // });

            res.send(indicadores);
        }
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

// app.get("/api/dados-boletim/", (req, res) => {
//     pool.query(
//         `SELECT VIEW_RT.ID AS ID,
//             VIEW_RT.REGIONAL_SAUDE AS REGIONAL,
//             VIEW_RT.DATA AS DATA,
//             (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS VAR_MEDIA_MOVEL,
//             VIEW_RT.RT AS RT,
//             VIEW_INCIDENCIA.LETALIDADE,
//             VIEW_INCIDENCIA.INCIDENCIA
//         FROM VIEW_RT,
//             VIEW_CASOS_ATUAL,
//             VIEW_CASOS_ANTERIOR,
//             VIEW_INCIDENCIA
//         WHERE VIEW_RT.ID = VIEW_CASOS_ATUAL.ID
//             AND VIEW_RT.ID = VIEW_CASOS_ANTERIOR.ID
//             AND VIEW_RT.ID = VIEW_INCIDENCIA.ID
//         ORDER BY VIEW_RT.ID`,
//         (err, rows) => {
//             if (err) {
//                 console.log("Erro ao buscar os dados de extrato das regiões: " + err);
//                 return;
//             }

//             pool.query(
//                 `SELECT VIEW_LEITOS_MAX.ID AS ID,
//                         VIEW_LEITOS_MAX.DATA AS DATA,
//                         VIEW_LEITOS_MAX.LEITOS_ATIVOS_MAX LEITOS_ATIVOS,
//                         VIEW_LEITOS_MAX.LEITOS_OCUPADOS AS LEITOS_OCUPADOS,
//                         VIEW_VACINACAO.VACINACAO_D1,
//                         VIEW_VACINACAO.VACINACAO_D2,
//                         VIEW_VACINACAO.POPULACAO
//                     FROM VIEW_RT,
//                         VIEW_LEITOS_MAX,
//                         VIEW_VACINACAO
//                     WHERE VIEW_RT.ID = VIEW_LEITOS_MAX.ID
//                         AND VIEW_RT.ID = VIEW_VACINACAO.ID
//                         AND VIEW_LEITOS_MAX.DATA = (SELECT MAX(DATA) FROM VIEW_LEITOS_MAX)
//                     ORDER BY ID`,
//                 (err2, rows2) => {
//                     if (err2) {
//                         console.log("Erro ao buscar os dados de leitos das regiões: " + err);
//                         return;
//                     }

//                     totalEstado = {
//                         leitos_ocupados: 0,
//                         leitos_ativos: 0,
//                         populacao: 0,
//                         vacinacao_d1: 0,
//                         vacinacao_d2: 0,
//                     }
//                     result = rows.rows;
//                     result_Leitos = rows2.rows;
//                     regionais = [];
//                     result.forEach((item) => {
//                         item.var_media_movel = (item.var_media_movel * 100).toFixed(2).replace(".", ",");
//                         // item.leitos_ocupados = (item.leitos_ocupados * 100).toFixed(2).replace(".", ",");
//                         item.rt = (item.rt).replace(".", ",");
//                         item.letalidade = (item.letalidade).toFixed(2).replace(".", ",");
//                         item.incidencia = (item.incidencia).toFixed(2).replace(".", ",");
//                         regionais[item.id] = item;

//                     });

//                     result_Leitos.forEach((item) => {
//                         regionais[item.id].ocupacao_leitos = ((item.leitos_ocupados / item.leitos_ativos) * 100).toFixed(2).replace(".", ",");
//                         regionais[item.id].vacinacao_d1 = ((item.vacinacao_d1 / item.populacao) * 100).toFixed(4).replace(".", ",");
//                         regionais[item.id].vacinacao_d2 = ((item.vacinacao_d2 / item.populacao) * 100).toFixed(4).replace(".", ",");

//                         //totalEstado.leitos_ocupados += parseInt(item.leitos_ocupados);
//                         //totalEstado.leitos_ativos += parseInt(item.leitos_ativos);

//                         totalEstado.populacao += parseInt(item.populacao);
//                         totalEstado.vacinacao_d1 += parseInt(item.vacinacao_d1);
//                         totalEstado.vacinacao_d2 += parseInt(item.vacinacao_d2);
//                     });
//                     //regionais[1].ocupacao_leitos = ((totalEstado.leitos_ocupados / totalEstado.leitos_ativos) * 100).toFixed(2).replace(".", ",");
//                     regionais[1].ocupacao_leitos = "-";
//                     regionais[1].vacinacao_d1 = ((totalEstado.vacinacao_d1 / totalEstado.populacao) * 100).toFixed(4).replace(".", ",");
//                     regionais[1].vacinacao_d2 = ((totalEstado.vacinacao_d2 / totalEstado.populacao) * 100).toFixed(4).replace(".", ",");
//                     regionais[1].regional = "Estado de SC";
//                     regionais = regionais.filter(function (el) {
//                         return el != null;
//                     });
//                     var json2csv = require('json2csv').parse;
//                     var data = json2csv(regionais);

//                     res.attachment('boletim.csv');
//                     res.status(200).send(data);
//                 },
//             );
//         });
// });


app.get("/api/dados-boletim/", (req, res) => {
        pool.query(
            `SELECT ID, REGIONAL, DATA,
                    VAR_MEDIA_MOVEL, RT,
                    LEITOS_COVID_MAX, LEITOS_GERAL_MAX,
                    INCIDENCIA, INCIDENCIA_SC,
                    LETALIDADE, LETALIDADE_SC,
                    VACINACAO_D2_DIVE, VACINACAO_D2_MS,
                    FASE_ANTERIOR, DATA_MUDANCA_FASE,
                    PONTUACAO, FASE_CALCULADA
            FROM "avaliacaoRegionais" 
            WHERE DATA = (SELECT MAX(DATA) FROM "avaliacaoRegionais" )`,
            (err, rows) => {
                if (err) {
                    console.log("Erro ao buscar os dados de extrato das regiões: " + err);
                    return;
                }
    
                var json2csv = require('json2csv').parse;
                var data = json2csv(rows.rows);

                var d = rows.rows[0]['data']
                var dataBoletim = ("0" + d.getDate()).slice(-2) + "_" + ("0" + (d.getMonth() + 1)).slice(-2) + "_" + d.getFullYear();
                res.attachment('boletim_'+ dataBoletim + '.csv');
                res.status(200).send(data);
                });
    });

app.get("/api/dados-boletim-diario/", (req, res) => {
        pool.query(
            `SELECT ID, REGIONAL, DATA,
                    VAR_MEDIA_MOVEL, RT,
                    LETALIDADE, INCIDENCIA,
                    LEITOS_COVID_MAX, LEITOS_GERAL_MAX,
                    LETALIDADE_SC, INCIDENCIA_SC,
                    VACINACAO_D2_DIVE, VACINACAO_D2_MS,
                    FASE_ANTERIOR AS FASE, DATA_MUDANCA_FASE, PONTUACAO
                FROM "avaliacaoRegionaisDiario" `,
            (err, rows) => {
                if (err) {
                    console.log("Erro ao buscar os dados de extrato das regiões: " + err);
                    return;
                }
    
                var json2csv = require('json2csv').parse;
                var data = json2csv(rows.rows);

                var d = rows.rows[0]['data']
                var dataBoletim = ("0" + d.getDate()).slice(-2) + "_" + ("0" + (d.getMonth() + 1)).slice(-2) + "_" + d.getFullYear();
                res.attachment('boletim_'+ dataBoletim + '.csv');
                res.status(200).send(data);
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

app.get("/api/dados-vacinacao/", (req, res) => {
    pool.query(
        `SELECT MUNICIPIOS.MUNICIPIO_CORRIGIDO,
            REGIONAIS.REGIONAL_SAUDE,
            SUM(VACINACAO_DIVE."D1") AS VACINACAO_D1,
            SUM(VACINACAO_DIVE."D2") AS VACINACAO_D2,
            VACINACAO_DIVE."Data" AS DATA
        FROM MUNICIPIOS,
            REGIONAIS,
            VACINACAO_DIVE
        WHERE VACINACAO_DIVE."Municipio" = MUNICIPIOS.COD_MUNICIPIO
            AND REGIONAIS.ID = MUNICIPIOS.REGIONAL_SAUDE
            AND VACINACAO_DIVE."Data" BETWEEN
                (SELECT MAX(VACINACAO_DIVE."Data")
                    FROM VACINACAO_DIVE) - interval '14 day' AND
                (SELECT MAX(VACINACAO_DIVE."Data")
                    FROM VACINACAO_DIVE)
        GROUP BY MUNICIPIOS.MUNICIPIO_CORRIGIDO,
            MUNICIPIOS.MUNICIPIO_CIASC,
            VACINACAO_DIVE."Data",
            REGIONAIS.REGIONAL_SAUDE
        ORDER BY MUNICIPIOS.MUNICIPIO_CIASC,
            VACINACAO_DIVE."Data"`,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados de leitos das regiões: " + err);
                return;
            }

            var json2csv = require('json2csv').parse;
            var data = json2csv(rows.rows, { expandArrayObjects: true });

            res.attachment('dados-vacinacao.csv');
            res.status(200).send(data);
        },
    );
});

app.get("/api/leitos_max", (req, res) => {
    pool.query(
        `SELECT REGIONAIS.REGIONAL_SAUDE,				
        TO_CHAR(TBL.DATA, 'YYYY-MM-DD HH:MI:SS') AS DATA,			
        TBL.LEITOS_OCUPADOS,			
        TBL.LEITOS_ATIVOS,			
        MAX(TBL.LEITOS_ATIVOS) OVER (PARTITION BY TBL.ID  ORDER BY DATA) AS LEITOS_ATIVOS_MAX			
    FROM				
        (SELECT LEITOSGERAISCOVID.INDEX_REGIONAL AS ID,			
                SUM(LEITOSGERAISCOVID.LEITOS_OCUPADOS) AS LEITOS_OCUPADOS,	
                SUM(LEITOSGERAISCOVID.LEITOS_ATIVOS) AS LEITOS_ATIVOS,	
                (LEITOSGERAISCOVID.ATUALIZACAO) AS DATA	
            FROM LEITOSGERAISCOVID		
            GROUP BY LEITOSGERAISCOVID.INDEX_REGIONAL,		
                LEITOSGERAISCOVID.ATUALIZACAO	
            ORDER BY LEITOSGERAISCOVID.INDEX_REGIONAL,		
                LEITOSGERAISCOVID.ATUALIZACAO) AS TBL,	
        REGIONAIS			
    WHERE TBL.ID = REGIONAIS.ID				
        AND TBL.DATA > '2021-06-11'			
    ORDER BY TBL.ID,				
        TBL.DATA`,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados de leitos das regiões: " + err);
                return;
            }

            var json2csv = require('json2csv').parse;
            var data = json2csv(rows.rows, { expandArrayObjects: true });

            res.attachment('leitos_max.csv');
            res.status(200).send(data);
        },
    );
});

app.get("/api/leitos_ativos", (req, res) => {
    pool.query(
        `SELECT REGIONAIS.REGIONAL_SAUDE,		
        SUM(LEITOSCOVID.LEITOS_ATIVOS) AS LEITOS_ATIVOS,	
        SUM(LEITOSCOVID.LEITOS_OCUPADOS) AS LEITOS_OCUPADOS,	
        TO_CHAR(LEITOSCOVID.ATUALIZACAO, 'YYYY-MM-DD HH:MI:SS') AS DATA	
    FROM REGIONAIS,		
        LEITOSCOVID	
    WHERE LEITOSCOVID.INDEX_REGIONAL = REGIONAIS.ID		
        AND LEITOSCOVID.ATUALIZACAO > '2021-03-19'	
    GROUP BY LEITOSCOVID.ATUALIZACAO,		
        REGIONAIS.REGIONAL_SAUDE	
    ORDER BY REGIONAIS.REGIONAL_SAUDE,		
        LEITOSCOVID.ATUALIZACAO`,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados de leitos das regiões: " + err);
                return;
            }

            var json2csv = require('json2csv').parse;
            var data = json2csv(rows.rows, { expandArrayObjects: true });

            res.attachment('leitos_ativos.csv');
            res.status(200).send(data);
        },
    );
});

app.get("/api/media-movel/", (req, res) => {
    pool.query(
        `SELECT REGIONAIS.ID,
            CASE WHEN REGIONAIS.ID=1 THEN 'Estado de Santa Catarina' ELSE REGIONAIS.REGIONAL_SAUDE END,
            CASOS.DATA,
            SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL,
            SUM(CASOS.OBITOS_MEDIAMOVEL) AS OBITOS_MEDIAMOVEL,
            SUM(CASOS.POPULACAO) AS POPULACAO
        FROM REGIONAIS, CASOS
        WHERE CASOS.REGIONAL = REGIONAIS.ID
            AND REGIONAIS.ID <> 0
        GROUP BY REGIONAIS.ID, REGIONAIS.REGIONAL_SAUDE, CASOS.DATA
        ORDER BY REGIONAIS.ID, CASOS.DATA`,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados da média movel: " + err);
                return;
            }

            var json2csv = require('json2csv').parse;
            var data = json2csv(rows.rows, { expandArrayObjects: true });

            res.attachment('dados_media_movel.csv');
            res.status(200).send(data);
        },
    );
});

app.listen(port, () => {
    console.log(`App running on port ${port}.`);
});