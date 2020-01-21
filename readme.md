## Setup

### Get data 
#### get the following files from openflights.org
- airports.dat
- routes.dat
- airlines.dat

place them in ```./data```

#### get runway data from ourairports.com
put it in ```./data/ourairports.com/runways.csv```

#### get patronage data from wikidata
use the script from this repository
[https://github.com/felixniemeyer/airport-patronage-collector]

put the .csv with estimation enriched year-2014-values into 
```./data/estimation_enriched_2014_patronage.csv```

### Set up the sqlite database
```sqlite3 db.db < setup-sqlite.sqlite```


