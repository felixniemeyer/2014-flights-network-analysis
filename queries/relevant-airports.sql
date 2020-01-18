SELECT p.airport_id, p.iata, p.icao, p.name FROM 
(
	SELECT source_airport_id as id FROM routes
	UNION 
	SELECT destination_airport_id as id FROM routes
) as ids,
airports as p
WHERE ids.id = p.airport_id

