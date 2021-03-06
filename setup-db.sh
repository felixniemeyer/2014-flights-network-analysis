#/usr/bin/bash

printf "\nusage: $0 [<db-file>]>\n"
printf "make sure you have the following files in place:\n"
printf "./data/{airports.dat,airlines.dat,routes.dat}\n"
printf "./data/ourairports.com/runways.csv\n"
printf "./airport-patronage/wikidata-airport-patronage.csv\n\n"

DB_FILE=${1:-./db.db}

printf "loading and cleaning openflights data...\n" 
sqlite3 "$DB_FILE" < ./queries/load-openflights-data.sql 
sqlite3 "$DB_FILE" < ./queries/clean-openflights-data.sql

printf "exporting airport list...\n" 
sqlite3 "$DB_FILE" < ./queries/list-airports.sql > ./airport-patronage/custom_airport_ids

printf "extracting patronage from wikidata download...\n"
pushd ./airport-patronage > /dev/null
node ./extract-yearly-patronage.js
node ./estimate-2014-patronage.js
popd > /dev/null
cp ./airport-patronage/estimated-2014-patronage.csv ./data/

printf "adding patronage column...\n"
sqlite3 "$DB_FILE" < ./queries/set-up-patronage.sql

printf "estimating missing patronage...\n"
python ./scripts/estimate-missing-patronages.py "$DB_FILE" ./temp_missing_patronages.csv

printf "loading missing patronage estimations...\n"
sqlite3 "$DB_FILE" < ./queries/load-missing-patronage-estimations.sql
rm ./temp_missing_patronages.csv

printf "remove those disconnected airports and their routes...\n"
sqlite3 "$DB_FILE" < ./queries/remove_disconnected_subgraphs_without_patronage_data.sql

printf "removing duplicate routes (source, destination, airline)...\n"
sqlite3 "$DB_FILE" < ./queries/remove-duplicate-connections-by-same-airline.sql

printf "calculating geographic distance...\n" 
python ./scripts/calculate-geo-distance.py "$DB_FILE"

printf "adding geo_distance column...\n"
sqlite3 "$DB_FILE" < ./queries/set-up-geo-distance.sql
rm ./temp_geo_distances.csv

printf "estimating edge flows"
python ./scripts/estimate-passenger-flows.py write_csv "$DB_FILE"

printf "adding passenger flows"
sqlite3 "$DB_FILE" < ./queries/set-up-passenger-flows.sql
sqlite3 "$DB_FILE" < ./queries/set-up-flow-estimation-metrics.sql
rm ./temp_passenger_flows.csv
rm ./temp_flow_estimation_metrics.csv

printf "\ndone, enjoy.\n\n" 

