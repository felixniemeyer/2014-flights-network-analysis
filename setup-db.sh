#/usr/bin/bash

printf "\nusage: $0 <db-file(optional)>\n"
printf "make sure you have the following files in place:\n"
printf "./data/{airports.dat,airlines.dat,routes.dat}\n"
printf "./airport-patronage/wikidata-airport-patronage.csv\n\n"

DB_FILE=${1:-./db.db}

printf "loading and cleaning openflights data...\n" 
sqlite3 "$DB_FILE" < ./queries/load-openflights-data.sql 
sqlite3 "$DB_FILE" < ./queries/clean-openflights-data.sql

printf "exporting airport list...\n" 
sqlite3 "$DB_FILE" < ./queries/list-airports.sql > ./airport-patronage/custom_airport_ids

printf "adding runway surface column\n"
sqlite3 "$DB_FILE" < ./queries/set-up-runway-surface.sql

printf "extracting patronage from wikidata download...\n"
pushd ./airport-patronage > /dev/null
node ./extract-yearly-patronage.js
node ./estimate-2014-patronage.js
popd > /dev/null
cp ./airport-patronage/estimated-2014-patronage.csv ./data/

printf "adding patronage column...\n"
sqlite3 "$DB_FILE" < ./queries/set-up-patronage.sql

printf "removing duplicate routes (source, destination, airline)...\n"
sqlite3 "$DB_FILE" < ./queries/remove-duplicate-connections-by-same-airline.sql

printf "calculating geographic distance...\n" 
python ./scripts/calculate-geo-distance-and-store-in-db.py "$DB_FILE"

printf "adding geo_distance column...\n"
sqlite3 "$DB_FILE" < ./queries/set-up-geo-distance.sql
rm ./temp_geo_distances.csv

printf "\ndone, enjoy.\n\n" 
