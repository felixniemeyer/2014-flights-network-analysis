const fs = require('fs') 
const rl = require('readline') 

const splitSet = require('./split-set.js')

const FROM_YEAR = 2011
const TO_YEAR = 2017
const YEARS = Array(TO_YEAR + 1 - FROM_YEAR).fill().map((v,i) => FROM_YEAR + i)

let ws = fs.createWriteStream('./yearly-patronages.csv')
ws.write(['icao'].concat(YEARS).join(",") + '\n')

let id_lookup = {
  by_iata: {},
  by_icao: {}
}

rl.createInterface({
  input: fs.createReadStream('./custom_airport_ids') 
})
  .on('line', line => { 
    let [id, iata, icao] = line.split("|")
    if(iata !== undefined && iata !== '\\N') {
      id_lookup.by_iata[iata] = id
    }
    if(icao !== undefined && icao !== '\\N') {
      id_lookup.by_iata[icao] = id
    }
  })
  .on('close', () => {
    run()
  })

function run() {
  let headerSkipped = false
  let airport_data = undefined
  let currentId = undefined
  rl.createInterface({
    input: fs.createReadStream('./wikidata-airport-patronage.csv') 
  })
    .on('line', line => {
      if(!headerSkipped) {
        headerSkipped = true
        return 
      }
      let [iata, icao, patronage, point_in_time] = line.split(",")
      patronage = parseInt(patronage) 
      let id = id_lookup.by_iata[iata] || id_lookup.by_icao[icao]
      if(id === '7266') {
        console.log('7266', iata, icao, patronage, point_in_time)
      }
      if(id !== undefined && patronage > 0) {
        if(id !== currentId) {
          if(airport_data !== undefined) {
            processAirport(currentId, airport_data, ws)          
          }
          currentId = id
          airport_data = {}
        } 
        [year, month] = parsePointInTime(point_in_time)     
        if(airport_data[year] === undefined) {
          airport_data[year] = {}
        }
        if(airport_data[year][month] === undefined) {
          airport_data[year][month] = []
        }
        airport_data[year][month].push(patronage)
      }
    })
    .on('close', () => {
      if(Object.keys(airport_data) > 0) {
        processAirport(currentId, airport_data, ws)
      }
      ws.end()
    })
}
        
function processAirport(id, airport_data, ws) {
  let yearly_patronages = chooseYearlyPatronages(airport_data)
  let patronage_columns = YEARS.map(year => yearly_patronages[year] || 'unavailable')
  ws.write([id].concat(patronage_columns).join(',') + '\n')
}
      
function parsePointInTime(point_in_time) {
  let components = point_in_time.split('-')
  let year = components[0]
  let month = components[1]
  let rest = components[2]
  if( rest !== '01T00:00:00Z') {
    console.error('point_in_time not the first of a month, ignoring', point_in_time)
    return [undefined, undefined]
  }
  return [year, month].map(n => parseInt(n))
}

function chooseYearlyPatronages(airport_data) {
  let results = {}
  for(year in airport_data) {
    if(Object.keys(airport_data[year]).length === 1) { // info only about one kind of month
      if(airport_data[year][1] !== undefined) { // info only in Januaries
        let yearly_patronages = airport_data[year][1]
        let avg_patr = yearly_patronages.reduce((a, b) => a + b) / yearly_patronages.length
        results[year] = parseInt(avg_patr) 
      } else { 
        // not sure how to interpret
      }
    } else { // there is data for various kind of months
      let allValues = []
      for(month in airport_data[year]) {
        for(patronage of airport_data[year][month]) {
          allValues.push(patronage) 
        }
      }
      let info = splitSet(allValues) 
      if( info.lower_mean * 6 < info.upper_mean ) { // assume we have monthly and yearly values
        results[year] = parseInt(info.upper_mean)
      } else { // assume we only have monthly data
        let avg_monthly_patronages = allValues.reduce((a,b) => a + b) / allValues.length
        results[year] = parseInt(avg_monthly_patronages * 12)
      }
    }
  }
  return results
}

