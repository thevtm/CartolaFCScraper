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
console.log('Requisitando os arquivos...')

let requests_datetime = new Date();

let requests = Promise.join(
  rp(API_MERCADO_STATUS),
  rp(API_ATLETAS_MERCADO),
  rp(API_ATLETAS_PONTUADOS),
  rp(API_PARTIDAS),
  rp(API_CLUBES)
)

/* STORE FILES */
requests.spread(
  (mercadoStatus, atletasMercado, atletasPontuados, partidas, clubes) => {

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
        statement.run(requests_datetime.toISOString(), mercadoStatus,
          atletasMercado, atletasPontuados, partidas, clubes);
        statement.finalize();

        console.log('Dados armazenados no banco de dados com sucesso.')
      }
    )
  }
)
