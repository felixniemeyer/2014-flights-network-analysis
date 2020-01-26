/*-----------*/
/* patronage */
/*-----------*/

DROP TABLE IF EXISTS temp_patronage;
DROP TABLE IF EXISTS patronage_lower_threshold;
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

CREATE TABLE patronage_lower_threshold AS
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

CREATE TABLE patronage_runway_surface_ratio AS 
SELECT 
	avg( cast(patronage as REAL) / cast(runway_surface as REAL) )
FROM 
	airports 
WHERE
	runway_surface is not null AND
	patronage is not null
;

UPDATE 
	airports 
SET
	patronage = cast( runway_surface * (
		SELECT * FROM patronage_runway_surface_ratio
	) as int)
WHERE
	patronage is null AND
	runway_surface is not null
;

DROP TABLE patronage_runway_surface_ratio;

UPDATE 
	airports 
SET
	patronage = ( SELECT * FROM patronage_lower_threshold ) 
WHERE
	patronage is null OR
	patronage < ( SELECT * FROM patronage_lower_threshold ) 
;

DROP TABLE patronage_lower_threshold;
