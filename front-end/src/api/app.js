const { Pool, Client } = require('pg')
const bodyParser = require('body-parser')
var cors = require('cors');

const express = require('express')
const app = express()

const env = 'dev' // prod || dev

let port = 0;


if (env == 'dev') {
    app.use(cors())
    port = 3000
} else if (env == 'prod') {
    // https://medium.com/zero-equals-false/using-cors-in-express-cac7e29b005b
    // em produção devemos limitar somente para ambiente de desenvolvimento e para o domínio da aplicação.
    app.use(cors())
    port = 80
} else {
    throw new Error("Wrong express server configuration");
}

const pool = new Pool({
    user: 'postgres', 
    host: 'localhost',
    database: 'dump', // covid - mauricio
    password: 'zzdz0737', // postgres mauricio
    port: 5432,
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

app.get('/api/casos-por-regiao/:id', (req, res) => {
    id = req.params.id;

    pool.query(
        `SELECT
            to_char(casos.data, 'DD/MM/YYYY') as data,
            sum(casos.casos) as casos_dia,
            sum(casos.obitos) as obitos_dias,
            sum(casos.casos_acumulados) as casos_acumulados,
            sum(casos.obitos_acumulados) as obitos_acumulados,
            replace(to_char(sum(casos.casos_mediaMovel), '99990d999999'), ',', '.') as casos_mediaMovel,
            replace(to_char(sum(casos.obitos_mediaMovel), '99990d999999'), ',', '.') as obitos_mediaMovel,
            to_char(avg(casos.casos_acumulados_100mil), '99990d999999') as casos_acumulados_100mil,
            to_char(avg(casos.obitos_acumulados_100mil), '99990d999999') as obitos_acumulados_100mil
        FROM regionais, casos
        WHERE casos.regional = regionais.id AND regionais.id = $1 group by regionais.regional_saude, casos.data ORDER BY casos.data`,
        [id],
        (err, rows) => {

            if (err) {
                console.log("Erro ao buscar por cidade: " + err)
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

                casos_acumulados = rows.rows.map(row => {
                    return row.casos_acumulados;
                })

                casos_media_movel = rows.rows.map(row => {
                    return row.casos_mediamovel;
                })

                obitos_media_movel = rows.rows.map(row => {
                    return row.obitos_mediamovel;
                })

                

            }

            res.send({region, datas, casos, casos_acumulados, casos_media_movel, obitos_media_movel, ocupacao_uti})
        })    
    })

app.listen(port, () => {
    console.log(`App running on port ${port}.`)
  })