
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

/*---------------------*/
/* runway surface data */
/*---------------------*/

CREATE TABLE temp_runways (
	"runway_id" TEXT PRIMARY KEY, 
	"airport_ref" TEXT,
	"airport_ident" TEXT,
	"length_ft" TEXT,
	"width_ft" TEXT,
	"surface" TEXT,
	"lighted" TEXT,
	"closed" TEXT,
	"le_ident" TEXT,
	"le_latitude_deg" TEXT,
	"le_longitude_deg" TEXT,
	"le_elevation_ft" TEXT,
	"le_heading_degT" TEXT,
	"le_displaced_threshold_ft" TEXT,
	"he_ident" TEXT,
	"he_latitude_deg" TEXT,
	"he_longitude_deg" TEXT,
	"he_elevation_ft" TEXT,
	"he_heading_degT" TEXT,
	"he_displaced_threshold_ft" TEXT
); 

.mode csv temp_runways
.import data/ourairports.com/runways.csv temp_runways 
DELETE FROM temp_runways WHERE runway_id = 'id';

ALTER TABLE airports ADD COLUMN runway_surface REAL; 

CREATE TABLE temp_airport_runway_surfaces AS
SELECT 
	a.icao, 
	s.surface_area_ft2
FROM 
	airports as a, 
	(
		SELECT 
			UPPER(airport_ident) as icao, 
			SUM((cast(length_ft as integer) * cast(width_ft as integer))) as surface_area_ft2
		FROM 
			temp_runways
		WHERE 
			cast(length_ft as integer) > 20 * cast(width_ft as integer)
		GROUP BY airport_ident
	) as s
WHERE
	a.icao = s.icao
ORDER BY s.surface_area_ft2
;

UPDATE 
	airports as a
SET
	runway_surface = (
		SELECT
			surface_area_ft2
		FROM 
			temp_airport_runway_surfaces as s
		WHERE
			a.icao = s.icao
	)
;
	
DROP TABLE temp_airport_runway_surfaces; 

DROP TABLE temp_runways;

/*-----------*/
/* patronage */
/*-----------*/

CREATE TABLE temp_patronage (
	icao TEXT PRIMARY KEY, 
	patronage REAL
);

.mode csv temp_patronage
.import data/estimation_enriched_2014_patronage.csv temp_patronage

ALTER TABLE airports ADD COLUMN patronage REAL; 

UPDATE
	airports as a
SET 
	patronage = (
		SELECT
			patronage
		FROM 
			temp_patronage as p
		WHERE
			a.icao = p.icao
	)
; 

DROP TABLE temp_patronage;

CREATE TABLE patronage_lower_threshold AS
SELECT 
	avg( cast(patronage as REAL) ) 
FROM (
	SELECT 
		patronage
	FROM 
		airports 
	WHERE
		patronage <> '' AND
		patronage <> '0'
	ORDER BY patronage asc
	LIMIT (SELECT count(*) / 100 FROM airports) )
;

CREATE TABLE patronage_runway_surface_ratio AS 
SELECT 
	avg( cast(patronage as REAL) / cast(runway_surface as REAL) ) 
FROM 
	airports 
WHERE
	runway_surface <> '' AND
	patronage <> ''
;

UPDATE 
	airports as a
SET
	patronage = a.runway_surface * (
		SELECT * FROM patronage_runway_surface_ratio
	) 
WHERE
	patronage = '' AND
	runway_surface <> ''
;

DROP TABLE patronage_runway_surface_ratio;


UPDATE 
	airports as a
SET
	patronage = ( SELECT * FROM patronage_lower_threshold ) 
WHERE
	patronage = '' OR
	patronage < ( SELECT * FROM patronage_lower_threshold ) 
;

DROP TABLE patronage_lower_threshold;
