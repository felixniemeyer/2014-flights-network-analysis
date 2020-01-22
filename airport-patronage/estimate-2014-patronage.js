const fs = require('fs') 
const rl = require('readline') 

let header = true
let column_names = []
let patronage_sum = []
let complete_row_count = 0

const source_file = './yearly-patronages.csv'
const out_file = './estimated-2014-patronage.csv'

rl.createInterface({ input: fs.createReadStream(source_file) })
  .on('line', line => {
    let row = line.split(',')
    if(header) {
      header = false
      column_names = row
      console.log('header', column_names)
      return 
    }
    let complete = true
    for(let i = 1; i < column_names.length; i++) {
      if(row[i] === 'unavailable') {
        complete = false
        break
      }
    }
    if(complete) {
      complete_row_count++
      for(let i = 1; i < column_names.length; i++) {
        let patronage = parseInt(row[i])
        patronage_sum[i] = patronage_sum[i] + patronage || patronage
      }
    }
  })
  .on('close', () => {
    let patronage_avg = patronage_sum.map(sum => sum / complete_row_count)
    let i_2014 = column_names.indexOf('2014')
    let predict_from_other_year_factor = patronage_avg.map(avg => patronage_avg[i_2014] / avg)
    console.log('predicting based on other years with factors', predict_from_other_year_factor)
    header = true
    ws = fs.createWriteStream(out_file) 
    rl.createInterface({ input: fs.createReadStream(source_file) })
      .on('line', line => {
        let row = line.split(',')
        if(header) {
          header = false
          return 
        }
        if(row[0] == 'KFOE') {
          console.log('nan for row', row)
        }
        if(row[i_2014] === 'unavailable') {
          let other_years = 0
          let other_year_predictions = 0
          for(let i = 1; i < column_names.length; i++) {
            if(row[i] !== 'unavailable') {
              other_years++
              other_year_predictions += row[i] * predict_from_other_year_factor[i]
            }
          }
          row[i_2014] = parseInt(other_year_predictions / other_years)
        }
        ws.write(`${row[0]},${row[i_2014]}\n`)
      })
      .on('end', () => {
        ws.end()
      })
  })
    
