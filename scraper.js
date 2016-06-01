var async = require('asyncawait/async');
var await = require('asyncawait/await');
let Promise = require("bluebird");
let rp = require('request-promise');
let sqlite3 = require("sqlite3").verbose();

/* CONSTANTS */

const API_MERCADO_STATUS = 'https://api.cartolafc.globo.com/mercado/status'
const API_ATLETAS_MERCADO = 'https://api.cartolafc.globo.com/atletas/mercado'
const API_ATLETAS_PONTUADOS = 'https://api.cartolafc.globo.com/atletas/pontuados'
const API_PARTIDAS = 'https://api.cartolafc.globo.com/partidas'
const API_CLUBES = 'https://api.cartolafc.globo.com/clubes'


/* REQUEST FILES */

let requests_datetime = new Date();

async (function () {
  console.log('Requisitando os arquivos...')

  console.log('Requisitando API_MERCADO_STATUS...')
  let mercado_status = await (rp(API_MERCADO_STATUS))

  console.log('Requisitando API_ATLETAS_MERCADO...')
  let atletas_mercado = await (rp(API_ATLETAS_MERCADO))

  console.log('Requisitando API_PARTIDAS...')
  let partidas = await (rp(API_PARTIDAS))

  console.log('Requisitando API_CLUBES...')
  let clubes = await (rp(API_CLUBES))

  // Parciais nem sempre estão disponiveis
  let atletas_pontuados
  try {
    console.log('Requisitando API_ATLETAS_PONTUADOS...')
    atletas_pontuados = await (rp(API_ATLETAS_PONTUADOS))
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
