'use strict'

let async = require('asyncawait/async')
let await = require('asyncawait/await')
let Promise = require('bluebird')
let request = require('request')
let rp = require('request-promise')
let sqlite3 = require("sqlite3").verbose()

/* CONSTANTS */

const API_MERCADO_STATUS = 'https://api.cartolafc.globo.com/mercado/status'
const API_ATLETAS_MERCADO = 'https://api.cartolafc.globo.com/atletas/mercado'
const API_ATLETAS_PONTUADOS = 'https://api.cartolafc.globo.com/atletas/pontuados'
const API_PARTIDAS = 'https://api.cartolafc.globo.com/partidas'
const API_CLUBES = 'https://api.cartolafc.globo.com/clubes'

const headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
}

/* REQUEST FILES */

let requests_datetime = new Date();

async (function () {
  console.log('Requisitando os arquivos...')

  console.log('Requisitando API_MERCADO_STATUS...')
  let mercado_status = await (rp({ uri: API_MERCADO_STATUS, headers: headers }))

  console.log('Requisitando API_ATLETAS_MERCADO...')
  let atletas_mercado = await (rp({ uri: API_ATLETAS_MERCADO, headers: headers }))

  console.log('Requisitando API_PARTIDAS...')
  let partidas = await (rp({ uri: API_PARTIDAS, headers: headers }))

  console.log('Requisitando API_CLUBES...')
  let clubes = await (rp({ uri: API_CLUBES, headers: headers }))

  // Parciais nem sempre estão disponiveis
  let atletas_pontuados
  try {
    console.log('Requisitando API_ATLETAS_PONTUADOS...')
    atletas_pontuados = await (rp({ uri: API_ATLETAS_PONTUADOS, headers: headers }))
  } catch (e) {
    atletas_pontuados = null
  }

  console.log('Arquivos requisitados com sucesso.')

  // Open a database handle
  let db = new sqlite3.Database("data.sqlite");
  db.serialize(
    () => {

      console.log('Armazenando dados no banco de dados...')

      // Create new table
      db.run(`CREATE TABLE IF NOT EXISTS data
        (
          DataHora TEXT,
          API_MERCADO_STATUS TEXT,
          API_ATLETAS_MERCADO TEXT,
          API_ATLETAS_PONTUADOS TEXT,
          API_PARTIDAS TEXT,
          API_CLUBES TEXT
        )`);

      // Insert a new record
      let statement = db.prepare("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)");
      statement.run(requests_datetime.toISOString(), mercado_status,
        atletas_mercado, atletas_pontuados, partidas, clubes);
      statement.finalize();

      console.log('Dados armazenados no banco de dados com sucesso.')
    }
  )
})()
