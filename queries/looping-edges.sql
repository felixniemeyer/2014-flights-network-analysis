SELECT
	*
FROM 
	routes 
WHERE 
	destination_airport_id = source_airport_id and
	destination_airport = source_airport
