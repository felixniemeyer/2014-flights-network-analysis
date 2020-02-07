## Setup

### Get data 
#### get the following files from openflights.org
- airports.dat
- routes.dat
- airlines.dat

place them in ```./data```

#### get patronage data from wikidata
Go to [https://query.wikidata.org] and execute the query from ```./airport-patronage/sparql-queries/get-all-airports-with-patronage-values.sparql```
Click on "Download", "CSV File" and save it as ```./airport-patronage/wikidata-airport-patronage.csv```

### Set up the sqlite database
run ```./setup-db.sh```

