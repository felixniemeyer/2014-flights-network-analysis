/* take the avg of the 1% with the smalles patronage as lower threshold */ 

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
