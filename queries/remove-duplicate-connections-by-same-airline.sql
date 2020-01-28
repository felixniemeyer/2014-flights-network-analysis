DELETE FROM routes 
WHERE rowid NOT IN (
	SELECT MIN(rowid)
	FROM routes
	GROUP BY airline_id, destination_airport_id, source_airport_id
)
