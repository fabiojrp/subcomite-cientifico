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
                    result.forEach((item) => {
                        var id = parseInt(item.id);
                        if (!regionais[id + 20]) {
                            if (id == 1 + 20) {
                                regionais[id + 20] = {
                                    name: "Estado de SC - Predição",
                                    mode: "lines",
                                    type: "scatter",
                                    x: [],
                                    y: [],
                                };
                            } else {
                                regionais[id + 20] = {
                                    name: item.regional_saude + " - Predição",
                                    mode: "lines",
                                    type: "scatter",
                                    visible: "legendonly",
                                    x: [],
                                    y: [],
                                };
                            }
                        }
                        regionais[id + 20].x.push(item.data);
                        regionais[id + 20].y.push(item.rt);
                    });

                    res.send({ regionais });
                },
            );
            // res.send({ regionais });
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
        `SELECT SUM(leitoscovid.LEITOS_OCUPADOS) AS LEITOS_OCUPADOS,
                SUM(leitoscovid.LEITOS_ATIVOS) AS LEITOS_ATIVOS,
                leitoscovid.ATUALIZACAO AS DATA
            FROM leitoscovid
            WHERE leitoscovid.INDEX_REGIONAL = $1
            GROUP BY leitoscovid.ATUALIZACAO
            ORDER BY leitoscovid.ATUALIZACAO
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
                name: "Leitos Totais",
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
                leitos_disponiveis.y.push(item.leitos_ativos);
            });

            res.send({ leitos_disponiveis, leitos_ocupados });
        },
    );
});

app.get("/api/leitos-por-regiao/", (req, res) => {
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
                console.log("Erro ao buscar o valor de leitos das regiões: " + err);
                return;
            }
            result = rows.rows;
            regionais = [];
            totalEstado = [];
            result.forEach((item) => {
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
                    (item.leitos_ocupados / item.leitos_ativos) * 100,
                );

                if (!totalEstado[item.data]) {
                    totalEstado[item.data] = {
                        leitos_ocupados: 0,
                        leitos_ativos: 0,
                        data: item.data,
                    };
                }
                totalEstado[item.data].leitos_ocupados += parseInt(
                    item.leitos_ocupados,
                );
                totalEstado[item.data].leitos_ativos += parseInt(item.leitos_ativos);
            });

            regionais[0] = {
                name: "Estado de SC",
                mode: "lines",
                type: "scatter",
                x: [],
                y: [],
            };

            for (var [key, item] of Object.entries(totalEstado)) {
                regionais[0].x.push(item.data);
                regionais[0].y.push((item.leitos_ocupados / item.leitos_ativos) * 100);
            }

            res.send({ regionais });
        },
    );
});

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

            arrData.forEach(function(key) {
                // console.log(totalEstado.get(key).data);
                regionais[0].x.push(totalEstado.get(key).data);
                regionais[0].y.push((totalEstado.get(key).vacinacao_d2 / totalEstado.get(key).populacao));
            });

            // for (item of totalEstado.values()) {
            //     regionais[0].x.push(item.data);
            //     regionais[0].y.push((item.vacinacao_d2 / item.populacao));
            // }
            // travelMap = new Map(Object.entries(totalEstado.values()));


            // for (var [key, item] of Object.keys(totalEstado)) {
            //     regionais[0].x.push(item.data);
            //     regionais[0].y.push((item.vacinacao_d2 / item.populacao));
            // }
            // totalEstado.forEach((item) => {
            //     console.log(item.data);
            // });
            res.send({ regionais });
        },
    );
});

app.get("/api/vacinacao-ms-por-regiao/", (req, res) => {
    pool.query(
        `SELECT REGIONAIS.REGIONAL_SAUDE,
                REGIONAIS.ID AS ID,
                REGIONAIS.POPULACAO AS POPULACAO,
                SUM(VACINACAO_MS.DOSES_APLICADAS) AS DOSES_APLICADAS,
                VACINACAO_MS.VACINA_DATAAPLICACAO AS DATA
            FROM REGIONAIS,
                VACINACAO_MS
            WHERE VACINACAO_MS.REGIONAL = REGIONAIS.ID 
            AND VACINACAO_MS.VACINA_DESCRICAO_DOSE <> '1ª Dose'
            GROUP BY REGIONAIS.ID,
                REGIONAIS.REGIONAL_SAUDE,
                VACINACAO_MS.VACINA_DATAAPLICACAO
            ORDER BY REGIONAIS.ID,
                VACINACAO_MS.VACINA_DATAAPLICACAO
            `,
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar o valores de vacinação de MS por região: " + err);
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
                        transforms: [{
                            type: 'aggregate',
                            aggregations: [
                                { target: 'y', func: 'sum', enabled: true },
                            ]
                        }],
                        x: [],
                        y: [],
                    };
                }
                regionais[item.id].x.push(item.data);
                regionais[item.id].y.push(item.doses_aplicadas);

                totalEstadoData.add(dataItem);
                if (!totalEstado.has(dataItem)) {
                    totalEstado.set(dataItem, {
                        populacao: parseInt(item.populacao),
                        doses_aplicadas: 0,
                        data: item.data,
                    });
                }

                totalEstado.get(dataItem).doses_aplicadas += parseInt(item.doses_aplicadas);
                totalEstado.get(dataItem).populacao += parseInt(item.populacao);
            });

            regionais[0] = {
                name: "Estado de SC",
                mode: "lines",
                type: "scatter",
                transforms: [{
                    type: 'aggregate',
                    aggregations: [
                        { target: 'y', func: 'sum', enabled: true },
                    ]
                }],
                x: [],
                y: [],
            };

            arrData = Array.from(totalEstadoData).sort();

            arrData.forEach(function(key) {
                // console.log(totalEstado.get(key).data);
                regionais[0].x.push(totalEstado.get(key).data);
                regionais[0].y.push(totalEstado.get(key).doses_aplicadas);
            });

            // for (item of totalEstado.values()) {
            //     regionais[0].x.push(item.data);
            //     regionais[0].y.push((item.vacinacao_d2 / item.populacao));
            // }
            // travelMap = new Map(Object.entries(totalEstado.values()));


            // for (var [key, item] of Object.keys(totalEstado)) {
            //     regionais[0].x.push(item.data);
            //     regionais[0].y.push((item.vacinacao_d2 / item.populacao));
            // }
            // totalEstado.forEach((item) => {
            //     console.log(item.data);
            // });
            res.send({ regionais });
        },
    );
});


app.get("/api/dados-estado/", (req, res) => {
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

                    /*
                            15 - Verde
                            12 >= e 15 = Amarelo
                            9 >= e 11 = laranja
                            9 < Vermelho

                    */

                    leitos = result[i].leitos_ocupados * 100;

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
            `, [id],
        (err, rows) => {
            if (err) {
                console.log("Erro ao buscar os dados do estado: " + err);
                return;
            }

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
                    regionais = regionais.filter(function(el) {
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


app.listen(port, () => {
    console.log(`App running on port ${port}.`);
});


// SELECT REGIONAIS.REGIONAL_SAUDE,
// 	REGIONAIS.ID AS ID,
// 	SUM(VACINACAO_DIVE."D1") AS DOSE1,
// 	VACINACAO_DIVE."Data" AS DATA
// FROM REGIONAIS,
// 	VACINACAO_DIVE
// WHERE VACINACAO_DIVE.REGIONAL = REGIONAIS.ID
// GROUP BY REGIONAIS.ID,
// 	VACINACAO_DIVE."Data",
// 	REGIONAIS.REGIONAL_SAUDE
// ORDER BY REGIONAIS.ID

// select  index_regional, sum(leitos_ativos), atualizacao
// from public.leitosgeraiscovid group by index_regional, atualizacao, index_regional
// order by index_regional, atualizacao

// SELECT *
//     FROM t1 WHERE(id, rev) IN
//         (SELECT id, MAX(rev)
//   FROM t1
//   GROUP BY id
//         )

// SELECT INDEX_REGIONAL,
//     MAX(LEITOS_ATIVOS_TOTAL)
// FROM
//     (SELECT INDEX_REGIONAL,
//         SUM(LEITOS_ATIVOS) AS LEITOS_ATIVOS_TOTAL
// 					FROM PUBLIC.LEITOSGERAISCOVID
// 					GROUP BY INDEX_REGIONAL,
//         ATUALIZACAO,
//         INDEX_REGIONAL
// 					ORDER BY INDEX_REGIONAL,
//         ATUALIZACAO) SUBTABLE
// GROUP BY SUBTABLE.INDEX_REGIONAL