/*-------------------------*/
/* import openflights data */
/*-------------------------*/

DROP TABLE IF EXISTS routes; 
DROP TABLE IF EXISTS airlines; 
DROP TABLE IF EXISTS airports; 
DROP TABLE IF EXISTS runways; 

CREATE TABLE routes(
	"airline"  TEXT,
	"airline_id"  TEXT,
	"source_airport" TEXT,
	"source_airport_id" TEXT,
	"destination_airport" TEXT,
	"destination_airport_id" TEXT,
	"codeshare" TEXT,
	"stops" TEXT,
	"equipment" TEXT
);

.mode csv routes
.import data/routes.dat routes

CREATE TABLE airports (
	"airport_id" TEXT PRIMARY KEY,
	"name" TEXT,
	"city" TEXT,
	"country" TEXT,
	"iata" TEXT,
	"icao" TEXT,
	"latitude" TEXT,
	"longitude" TEXT,
	"altitude" TEXT,
	"timezone" TEXT,
	"dst" TEXT,
	"tz_database_time_zone" TEXT,
	"type" TEXT,
	"source" TEXT
);

.mode csv airports
.import data/airports.dat airports

CREATE TABLE airlines ( 
	"airline_id" TEXT PRIMARY KEY,
	"name" TEXT,
	"alias" TEXT,
	"iata" TEXT,
	"icao" TEXT,
	"callsign" TEXT,
	"country" TEXT,
	"active" TEXT
);

.mode csv airlines
.import data/airlines.dat airlines

