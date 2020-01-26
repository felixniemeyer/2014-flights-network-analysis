#!/usr/bin/bash

echo "load and clean openflights data" 
sqlite3 db.db < ./load-openflights-data.sql 
sqlite3 db.db < ./clean-openflights-data.sql

echo "export airport list" 
sqlite3 db.db < ./list-airports.sql > ./airport-patronage/custom_airport_ids

pushd ./airport-patronage > /dev/null

node ./extract-yearly-patronage.js
node ./estimate-2014-patronage.js

popd > /dev/null

cp ./airport-patronage/estimated-2014-patronage.csv ./data/

echo "adding runway surface column"
sqlite3 db.db < ./queries/set-up-runway-surface.sql

echo "adding patronage column"
sqlite3 db.db < ./queries/set-up-patronage.sql

echo "removing duplicate routes (source, destination, airline)"
sqlite3 ./db.db < ./queries/remove-duplicate-connections-by-same-airline.sql

# let's better do this in a script...
# echo "calculating and adding routes distance" 
# python ./set-up-geo-distance-to-routes.py ./db.db

