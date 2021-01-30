const { Pool, Client } = require('pg')
const bodyParser = require('body-parser')

const express = require('express')
const app = express()
const port = 3000

const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'covid',
    password: 'postgres',
    port: 5432,
})

app.get('/casos-por-regiao', (req, res) => {
    pool.query(`SELECT
                    casos.data as data,
                    sum(casos.casos) as casos_dia,
                    sum(casos.obitos) as obitos_dias,
                    sum(casos.casos_acumulados) as casos_acumulados,
                    sum(casos.obitos_acumulados) as obitos_acumulados,
                    to_char(sum(casos.casos_mediaMovel), '99990d999999') as casos_mediaMovel,
                    to_char(sum(casos.obitos_mediaMovel), '99990d999999') as obitos_mediaMovel,
                    to_char(avg(casos.casos_acumulados_100mil), '99990d999999') as casos_acumulados_100mil,
                    to_char(avg(casos.obitos_acumulados_100mil), '99990d999999') as obitos_acumulados_100mil
                FROM regionais, casos
                WHERE casos.regional = regionais.id AND  regionais.id = 4 group by regionais.regional_saude, casos.data ORDER BY casos.data`, 
                (err, rows) => {
        if (err) console.log("Erro ao buscar por cidade: " + err)

        if (rows) {
            res.send(rows.rows)
        } else {
            res.send("Problema ao consultar os dados.")
        }
    })
    
})

app.listen(port, () => {
    console.log(`App running on port ${port}.`)
  })