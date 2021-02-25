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
    user: 'postgres', 
    host: 'localhost',
    database: 'dump', // covid - mauricio
    password: 'zzdz0737', // postgres mauricio
    port: 5432,
    multipleStatements: true
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

// app.get ('/api/indicadores/:id', (req, res) => {
//     id = req.params.id;
//     pool.query(
//         `SELECT RT.DATA as data,
//         RT.RT as rt
//         FROM REGIONAIS, RT
//         WHERE RT.REGIONAL = REGIONAIS.ID
//             AND RT.REGIONAL = $1
//         ORDER BY REGIONAIS.REGIONAL_SAUDE, RT.DATA`
//     ,
//     [id],
//     (err, rows) => {
//         if (err) {
//             console.log("Erro ao buscar o R(T) por região: " + err)
//             return
//         }

//         region = regions[id]

//         if (typeof(region) === 'undefined') {
//             res.send("Região não reconhecida. Informe um ID válido.")
//             return;
//         }

//         if (rows.rows.length > 0) {
//             datas = rows.rows.map(row => {
//                 return row.data;
//             })

//             rt = rows.rows.map(row => {
//                 return row.rt;
//             })

//         }
//         rtf = rt[rt.length - 1]
//         properties = {
            
//             "name": "Alto Uruguai Catarinense", 
//             "rt": Number(rtf),
//             "media_movel": '55%', 
//             "ocupacao_leitos": "120%",
//             "center" : [-27.142063934075992, -52.060554383313196],
//             "zoom" : 10,

//         }
//         res.send({properties})
//     }

//     ) })

app.get('/api/casos-por-regiao/:id', (req, res) => {
    id = req.params.id;

    pool.query(
        `SELECT CASOS.DATA,
        SUM(CASOS.CASOS) AS CASOS_DIA,
        SUM(CASOS.OBITOS) AS OBITOS_DIAS,
        SUM(CASOS.CASOS_MEDIAMOVEL) AS CASOS_MEDIAMOVEL,
        SUM(CASOS.OBITOS_MEDIAMOVEL) AS OBITOS_MEDIAMOVEL,
        SUM(CASOS.CASOS_ACUMULADOS_100mil) AS CASOS_ACUMULADOS_100mil
        FROM REGIONAIS, CASOS
        
        WHERE CASOS.REGIONAL = REGIONAIS.ID
        AND REGIONAIS.ID = $1
        GROUP BY REGIONAIS.REGIONAL_SAUDE, CASOS.DATA
        ORDER BY CASOS.DATA
        `,
        // WHERE CASOS.DATA BETWEEN 
        //     (SELECT MAX(CASOS.DATA) AS MAX_DATA FROM CASOS) - interval '15 days' AND
        //     (SELECT MAX(CASOS.DATA) AS MAX_DATA FROM CASOS)
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

                casos_acumulados_100mil = rows.rows.map(row => {
                    return row.casos_acumulados_100mil;
                })

            }

            res.send({region, datas, casos, casos_media_movel, obitos, obitos_media_movel, casos_acumulados_100mil})
        })    
    })

    app.get('/api/rt-por-regiao/:id', (req, res) => {
 
        id = req.params.id;
    
        // pool.query(
        //     `SELECT RT.DATA as data,
        //     RT.RT as rt
        // FROM REGIONAIS, RT
        // WHERE DATA BETWEEN
        //         (SELECT MAX(RT.DATA) AS MAX_DATA FROM RT) - interval '15 days' AND
        //         (SELECT MAX(RT.DATA) AS MAX_DATA FROM RT) - interval '1 day'
        //         AND RT.REGIONAL = REGIONAIS.ID
        //         AND RT.REGIONAL = $1
        // ORDER BY REGIONAIS.REGIONAL_SAUDE, RT.DATA
        //     `
            pool.query(
                `SELECT RT.DATA as data,
                RT.RT as rt
                FROM REGIONAIS, RT
                WHERE RT.REGIONAL = REGIONAIS.ID
                    AND RT.REGIONAL = $1
                ORDER BY REGIONAIS.REGIONAL_SAUDE, RT.DATA`
            ,
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

app.listen(port, () => {
    console.log(`App running on port ${port}.`)
})