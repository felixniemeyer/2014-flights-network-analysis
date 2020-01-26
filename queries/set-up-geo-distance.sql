/*--------------*/
/* geo_distance */
/*--------------*/

DROP TABLE IF EXISTS temp_geo_distances;

CREATE TABLE temp_geo_distances (
	airline_id TEXT, 
	source_airport_id TEXT, 
	destination_airport_id TEXT, 
	geo_distance REAL
);
CREATE INDEX temp_index ON temp_geo_distances (airline_id, source_airport_id, destination_airport_id);

.mode csv temp_geo_distances
.import ./temp_geo_distances.csv temp_geo_distances

ALTER TABLE routes ADD COLUMN geo_distance REAL;

UPDATE 
	routes
SET 
	geo_distance = (
		SELECT 
			geo_distance
		FROM 
			temp_geo_distances
		WHERE
			temp_geo_distances.airline_id = routes.airline_id and
			temp_geo_distances.source_airport_id = routes.source_airport_id and
			temp_geo_distances.destination_airport_id = routes.destination_airport_id
	)
;

DROP INDEX temp_index;

DROP TABLE temp_geo_distances;
