SELECT 
	surface, 
	c
FROM 
	(
		SELECT 
			surface, 
			count(surface) as c
		FROM 
			runways 
		GROUP BY 
			surface
	)
ORDER BY c

