SELECT 
	source_airport
FROM 
	routes
WHERE 
	source_airport_id = "\N"

UNION 

SELECT 
	destination_airport	
FROM 
	routes
WHERE 
	destination_airport_id = "\N"
;
