const { Pool, Client } = require('pg')

const express = require('express')
const app = express()
const port = 3000

const pool = new Pool()

app.get('/casos-confirmados', (req, res) => {
    pool.query('SELECT count(*) as total FROM casos;', (err, rows) => {
        if (err) console.log("Erro ao buscar por cidade: " + err)

        if (rows) {
            res.send(row)
        } else {
            res.send("Problema ao consultar os dados.")
        }
    })
    
})
