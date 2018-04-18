'use strict'

const fetch = require("node-fetch")
const Database = require("better-sqlite3")

async function main() {

  /* 1. Requisição dos arquivos */

  console.info('Requisitando os arquivos...')

  let requests_datetime = new Date()

  const API_MERCADO_STATUS = 'https://api.cartolafc.globo.com/mercado/status'
  const API_ATLETAS_MERCADO = 'https://api.cartolafc.globo.com/atletas/mercado'
  const API_ATLETAS_PONTUADOS = 'https://api.cartolafc.globo.com/atletas/pontuados'
  const API_PARTIDAS = 'https://api.cartolafc.globo.com/partidas'
  const API_CLUBES = 'https://api.cartolafc.globo.com/clubes'

  const fetchOptions = {
    method: 'GET',
    headers: {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }
  }

  console.info('Requisitando API_MERCADO_STATUS...')
  const mercado_status = await fetch(API_MERCADO_STATUS, fetchOptions).then((res) => res.text())
  console.info('API_MERCADO_STATUS obtido com sucesso.')

  console.info('Requisitando API_ATLETAS_MERCADO...')
  const atletas_mercado = await fetch(API_ATLETAS_MERCADO, fetchOptions).then((res) => res.text())
  console.info('API_ATLETAS_MERCADO obtido com sucesso.')

  console.info('Requisitando API_PARTIDAS...')
  const partidas = await fetch(API_PARTIDAS, fetchOptions).then((res) => res.text())
  console.info('API_PARTIDAS obtido com sucesso.')

  console.info('Requisitando API_CLUBES...')
  const clubes = await fetch(API_CLUBES, fetchOptions).then((res) => res.text())
  console.info('API_CLUBES obtido com sucesso.')

  // Parciais nem sempre estão disponiveis
  console.info('Requisitando API_ATLETAS_PONTUADOS...')
  const atletas_pontuados = await fetch(API_ATLETAS_PONTUADOS).then((res) => res.text())
  console.info('API_ATLETAS_PONTUADOS obtido com sucesso.')

  console.info('Arquivos requisitados com sucesso.')

  /* 2. Armazena arquivos no DB */

  console.info('Armazenando dados no banco de dados...')

  const dbFilename = 'data.sqlite'
  const db = new Database(dbFilename);

  // Cria tabela se não existir
  db.prepare(`
    CREATE TABLE IF NOT EXISTS data
    (
      DataHora TEXT,
      API_MERCADO_STATUS TEXT,
      API_ATLETAS_MERCADO TEXT,
      API_ATLETAS_PONTUADOS TEXT,
      API_PARTIDAS TEXT,
      API_CLUBES TEXT
    )
  `)
    .run();

  // Insere dados
  db.prepare("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)")
    .run(requests_datetime.toISOString(), mercado_status, atletas_mercado,
      atletas_pontuados, partidas, clubes)

  db.close()

  console.info('Dados armazenados no banco de dados com sucesso.')
}

main()
