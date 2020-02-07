/* the necessary temporary table is created in the set-up-patronage.sql file. 
this split is necessary, so that we can run the estimation script in between */

DROP TABLE IF EXISTS temp_isolated_airports_without_patronage_data;
CREATE TABLE temp_isolated_airports_without_patronage_data AS 
SELECT
	airport_id
FROM 
	airports
WHERE 
	patronage is null
;

DELETE FROM 
	routes
WHERE 
	source_airport_id in temp_isolated_airports_without_patronage_data or
	destination_airport_id in temp_isolated_airports_without_patronage_data
;

DELETE FROM 
	airports
WHERE 
	patronage is null
;

DROP TABLE temp_isolated_airports_without_patronage_data;

