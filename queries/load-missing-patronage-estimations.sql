DROP TABLE IF EXISTS temp_patronage_estimations;

CREATE TABLE temp_patronage_estimations (
	airport_id TEXT PRIMARY KEY, 
	patronage INT
);

.mode csv temp_patronage_estimations
.import ./temp_missing_patronages.csv temp_patronage_estimations

UPDATE
	airports
SET
	patronage = (
		SELECT 
			patronage
		FROM 
			temp_patronage_estimations
		WHERE
			airports.airport_id = temp_patronage_estimations.airport_id
	)
WHERE
	patronage is null
;

DROP TABLE temp_patronage_estimations;

SELECT count(*) || ' airports without patronage left' FROM airports WHERE patronage is null; 
