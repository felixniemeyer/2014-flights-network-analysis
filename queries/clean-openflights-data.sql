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

/* delete routes that include airports about which no data is present */ 
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

/* fill in airport_id, where iata code is present but no airport_id */ 

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

DROP TABLE temp_airport_ids_without_routes

