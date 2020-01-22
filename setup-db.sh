#!/usr/bin/bash

echo "load and clean openflights data" 
sqlite3 db.db < ./load-openflights-data.sql 
sqlite3 db.db < ./clean-openflights-data.sql

echo "export airport list" 
sqlite3 db.db < ./list-airports.sql > ./airport-patronage/custom_airport_ids

echo "lalala"  
pushd ./airport-patronage

node ./extract-yearly-patronage.js
node ./estimate-2014-patronage.js

popd

cp ./airport-patronage/estimated-2014-patronage.csv ./data/

echo "adding runway surface column"
sqlite3 db.db < ./add-runway-surface.sql

echo "adding patronage column"
sqlite3 db.db < ./add-patronage.sql
