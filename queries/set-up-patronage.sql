/*-----------*/
/* patronage */
/*-----------*/

DROP TABLE IF EXISTS temp_patronage;
DROP TABLE IF EXISTS temp_default_patronage;
DROP TABLE IF EXISTS patronage_runway_surface_ratio;

CREATE TABLE temp_patronage (
	icao TEXT PRIMARY KEY, 
	patronage INT
);

.mode csv temp_patronage
.import data/estimation_enriched_2014_patronage.csv temp_patronage

ALTER TABLE airports ADD COLUMN patronage INT; 

UPDATE
	airports 
SET 
	patronage = (
		SELECT
			patronage
		FROM 
			temp_patronage as p
		WHERE
			airports.icao = p.icao
	)
; 

DROP TABLE temp_patronage;

DROP TABLE IF EXISTS temp_default_patronage;
CREATE TABLE temp_default_patronage AS
SELECT 
	avg( patronage )
FROM (
	SELECT 
		patronage
	FROM 
		airports 
	WHERE
		patronage is not null AND
		patronage > 0
	ORDER BY patronage asc
	LIMIT (SELECT count(*) / 100 FROM airports) )
;

SELECT count(*) || ' airports without patronage left' FROM airports WHERE patronage is null; 
