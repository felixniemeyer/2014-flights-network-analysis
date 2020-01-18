SELECT 
	airport_ids.airport_id,
	COUNT(airport_ids.airport_id) as degree
	
FROM 

	(
		SELECT source_airport_id as airport_id FROM routes
		UNION
		SELECT destination_airport_id as airport_id FROM routes
	) as airport_ids,
	routes as r

WHERE
	r.source_airport_id = airport_ids.airport_id or
	r.destination_airport_id = airport_ids.airport_id
	
GROUP BY (airport_ids.airport_id)
ORDER BY degree
;
