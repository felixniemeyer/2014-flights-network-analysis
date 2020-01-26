SELECT 
	avg( cast(patronage as REAL) / cast(runway_surface as REAL) ) 
FROM 
	airports 
WHERE
	runway_surface <> '' AND
	patronage <> ''
;
