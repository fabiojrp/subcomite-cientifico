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
    //user: 'postgres', 
    user: 'covid', // postgres marcelo
    host: 'localhost',
    database: 'covid', // covid - mauricio
    //password: 'postgres', // postgres mauricio
    password: 'WEpJqsYMnHWB', // postgres marcelo
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
        SUM(CASOS.OBITOS_MEDIAMOVEL) AS OBITOS_MEDIAMOVEL
        FROM REGIONAIS, CASOS
        WHERE CASOS.DATA BETWEEN 
            (SELECT MAX(CASOS.DATA) AS MAX_DATA FROM CASOS) - interval '5 months' AND
            (SELECT MAX(CASOS.DATA) AS MAX_DATA FROM CASOS) - interval '1 day'
        AND CASOS.REGIONAL = REGIONAIS.ID
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

            if (typeof(region) === 'undefined') {
                res.send("Região não reconhecida. Informe um ID válido.")
                return;
            }

            if (rows.rows.length > 0) {
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

            }

            res.send({region, datas, casos, casos_media_movel, obitos, obitos_media_movel})
        })    
    })

    app.get('/api/rt-por-regiao/:id', (req, res) => {
        id = req.params.id;
    
        pool.query(
            `SELECT RT.DATA as data,
            RT.RT as rt
        FROM REGIONAIS, RT
        WHERE DATA BETWEEN
                (SELECT MAX(RT.DATA) AS MAX_DATA FROM RT) - interval '5 months' AND
                (SELECT MAX(RT.DATA) AS MAX_DATA FROM RT) - interval '1 day'
                AND RT.REGIONAL = REGIONAIS.ID
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
    
                if (typeof(region) === 'undefined') {
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
    
                res.send({region, datas, rt})
            })    
    })

    app.get('/api/dados-estado/', (req, res) => {
        /*
        "name": "Extremo Sul Catarinense", 
        "rt": 1, 
        "media_movel": '15%', 
        "ocupacao_leitos": "90%",
        "path": "extremo-sul.html"
        */
        pool.query(
            `SELECT VIEW_RT.REGIONAL_SAUDE AS REGIONAIS,
            VIEW_RT.DATA AS RT_DATA,
            VIEW_RT.RT AS RT_VALOR,
            1 - (VIEW_LEITOS.LEITOS_ATIVOS - VIEW_LEITOS.LEITOS_OCUPADOS)/VIEW_LEITOS.LEITOS_ATIVOS :: NUMERIC AS LEITOS_OCUPADOS,
            VIEW_LEITOS.MAX_DATA AS LEITOS_DATA,
            VIEW_CASOS_ATUAL.DATA AS DATA_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR.DATA AS DATA_CASOS_ANTERIOR,
            (VIEW_CASOS_ATUAL.CASOS_MEDIAMOVEL - VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL) / VIEW_CASOS_ANTERIOR.CASOS_MEDIAMOVEL AS VARIACAO
        FROM VIEW_RT,
            VIEW_CASOS_ATUAL,
            VIEW_CASOS_ANTERIOR,
            VIEW_LEITOS
        WHERE VIEW_RT.REGIONAL_SAUDE = VIEW_CASOS_ATUAL.REGIONAL_SAUDE
                        AND VIEW_RT.REGIONAL_SAUDE = VIEW_CASOS_ANTERIOR.REGIONAL_SAUDE
                        AND VIEW_RT.REGIONAL_SAUDE = VIEW_LEITOS.REGIONAL_SAUDE
            `,
            (err, rows) => {
                if (err) {
                    console.log("Erro ao buscar os dados por região: " + err)
                    return
                }
        
                if (rows.rows.length > 0) {
                    regionais = rows.rows.map(row => {
                        return row.regionais;
                    })
                    rt_data = rows.rows.map(row => {
                        return row.rt_data;
                    })
                    rt_valor = rows.rows.map(row => {
                        return row.rt_valor;
                    })
                    leitos_ocupados = rows.rows.map(row => {
                        return row.leitos_ocupados;
                    })
                    leitos_data = rows.rows.map(row => {
                        return row.leitos_data;
                    })
                    data_casos_atuais = rows.rows.map(row => {
                        return row.data_casos_atual;
                    })
                    data_casos_anterior = rows.rows.map(row => {
                        return row.data_casos_anterior;
                    })
                    variacao = rows.rows.map(row => {
                        return row.variacao;
                    })
                }
    
                res.send({regionais, rt_data, rt_valor, leitos_ocupados, leitos_data, data_casos_atuais, data_casos_anterior, variacao})
            })    
    })



app.listen(port, () => {
    console.log(`App running on port ${port}.`)
})