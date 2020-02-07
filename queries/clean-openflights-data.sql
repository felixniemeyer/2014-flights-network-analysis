/* delete routes with unknown airlines */ 
DELETE FROM 
	routes
WHERE
	airline_id = '\N'
;

/* delte airlines with no routes */ 
DROP TABLE IF EXISTS temp_airline_ids_with_no_routes;
CREATE TABLE temp_airline_ids_with_no_routes (
	airline_id TEXT PRIMARY KEY
);
INSERT INTO temp_airline_ids_with_no_routes SELECT airline_id FROM (
	SELECT 
		airline_id
	FROM 
		airlines
	EXCEPT
	SELECT 
		airline_id
	FROM 
		routes
);

DELETE FROM
	airlines
WHERE 
	EXISTS ( 
		SELECT
			1
		FROM
			temp_airline_ids_with_no_routes 
		WHERE 
			airlines.airline_id = temp_airline_ids_with_no_routes.airline_id
	) 
;

DROP TABLE temp_airline_ids_with_no_routes; 
		

/* delete routes that do not use an airport_id and use an iata, that does not appear in the airports table */ 
DROP TABLE IF EXISTS temp_iata_codes_without_id;
CREATE TABLE temp_iata_codes_without_id AS
SELECT 
	iata
FROM 
	(
		SELECT destination_airport as iata FROM routes WHERE destination_airport_id = '\N'
		UNION
		SELECT source_airport as iata FROM routes WHERE source_airport_id = '\N'
	)
EXCEPT 
SELECT 
	iata 
FROM 
	airports
;

DELETE FROM 
	routes
WHERE
	EXISTS ( 
		SELECT 1 
		FROM 
			temp_iata_codes_without_id 
		WHERE 
			iata = routes.destination_airport OR
			iata = routes.source_airport
	) 
;

DROP TABLE temp_iata_codes_without_id;

/* fill in airport_id in route entries, where iata code is present but no airport_id */ 
UPDATE 
	routes 
SET
	source_airport_id = (
		SELECT 1
			airport_id
		FROM 
			airports 
		WHERE
			iata = routes.source_airport
	)
WHERE
	source_airport_id = '\N'
;


UPDATE 
	routes 
SET
	destination_airport_id = (
		SELECT 1
			airport_id
		FROM 
			airports 
		WHERE
			iata = routes.destination_airport
	)
WHERE
	destination_airport_id = '\N'
;

/* delete routes with non-existing airports */ 
DROP TABLE IF EXISTS temp_airport_ids_from_routes_without_airport_row;
CREATE TABLE temp_airport_ids_from_routes_without_airport_row AS
SELECT 
	id
FROM 
	(
		SELECT destination_airport_id as id FROM routes 
		UNION
		SELECT source_airport_id as id FROM routes 
	)
EXCEPT 
SELECT 
	airport_id
FROM airports
;

DELETE FROM 
	routes
WHERE
	EXISTS ( 
		SELECT 1 
		FROM 
			temp_airport_ids_from_routes_without_airport_row
		WHERE 
			id = routes.destination_airport_id OR
			id = routes.source_airport_id
	) 
;
DROP TABLE temp_airport_ids_from_routes_without_airport_row;

/* delete airports with non-existing routes */ 
DROP TABLE IF EXISTS temp_airport_ids_without_routes;
CREATE TABLE temp_airport_ids_without_routes AS
SELECT 
	airport_id as id
FROM 
	airports
EXCEPT
SELECT 
	* 
FROM 
	(
		SELECT source_airport_id id FROM routes
		UNION 
		SELECT destination_airport_id as id FROM routes
	)
;

DELETE FROM 
	airports
WHERE
	EXISTS (
		SELECT 1 
			airport_id
		FROM 
			temp_airport_ids_without_routes	
		WHERE
			airports.airport_id = temp_airport_ids_without_routes.id
	)
;

DROP TABLE temp_airport_ids_without_routes;

SELECT count(*) || ' airports' FROM airports;
SELECT count(*) || ' routes' FROM routes; 
SELECT count(*) || ' airlines' FROM airlines; 
