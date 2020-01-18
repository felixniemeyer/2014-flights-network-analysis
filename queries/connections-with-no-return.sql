SELECT count(*) FROM routes; 

SELECT 
	count(*)
FROM
	routes as r1, 
	routes as r2
WHERE
	r1.airline_id = r2.airline_id and
	r1.source_airport_id = r2.destination_airport_id and
	r1.destination_airport_id = r2.source_airport_id;

SELECT 
	count(*) 
FROM 
(
	SELECT 
		*
	FROM 
		routes

	EXCEPT 

	SELECT 
		r1.*
	FROM
		routes as r1, 
		routes as r2
	WHERE
		r1.source_airport_id = r2.destination_airport_id and
		r1.destination_airport_id = r2.source_airport_id	
)
;
