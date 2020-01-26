/*---------------------*/
/* runway surface data */
/*---------------------*/

CREATE TABLE temp_runways (
	"runway_id" TEXT PRIMARY KEY, 
	"airport_ref" TEXT,
	"airport_ident" TEXT,
	"length_ft" TEXT,
	"width_ft" TEXT,
	"surface" TEXT,
	"lighted" TEXT,
	"closed" TEXT,
	"le_ident" TEXT,
	"le_latitude_deg" TEXT,
	"le_longitude_deg" TEXT,
	"le_elevation_ft" TEXT,
	"le_heading_degT" TEXT,
	"le_displaced_threshold_ft" TEXT,
	"he_ident" TEXT,
	"he_latitude_deg" TEXT,
	"he_longitude_deg" TEXT,
	"he_elevation_ft" TEXT,
	"he_heading_degT" TEXT,
	"he_displaced_threshold_ft" TEXT
); 

.mode csv temp_runways
.import data/ourairports.com/runways.csv temp_runways 
DELETE FROM temp_runways WHERE runway_id = 'id';

ALTER TABLE airports ADD COLUMN runway_surface INT; 

CREATE TABLE temp_airport_runway_surfaces AS
SELECT 
	a.icao, 
	s.surface_area_ft2
FROM 
	airports as a, 
	(
		SELECT 
			UPPER(airport_ident) as icao, 
			SUM((cast(length_ft as INT) * cast(width_ft as INT))) as surface_area_ft2
		FROM 
			temp_runways
		WHERE 
			cast(length_ft as INT) > 20 * cast(width_ft as INT)
		GROUP BY airport_ident
	) as s
WHERE
	a.icao = s.icao
ORDER BY s.surface_area_ft2
;

UPDATE 
	airports 
SET
	runway_surface = (
		SELECT
			surface_area_ft2
		FROM 
			temp_airport_runway_surfaces as s
		WHERE
			airports.icao = s.icao
	)
;
	
DROP TABLE temp_airport_runway_surfaces; 

DROP TABLE temp_runways;
