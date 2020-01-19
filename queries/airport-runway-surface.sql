SELECT 
	a.name,
	a.icao, 
	s.surface_area_ft2
FROM 
	airports as a, 
	(
		SELECT 
			UPPER(airport_ident) as icao, 
			SUM((cast(length_ft as integer) * cast(width_ft as integer))) as surface_area_ft2
		FROM 
			runways
		WHERE 
/*
			surface = 'ASPH-P' or
			surface = 'TURF-P' or
			surface = 'S' or
			surface = 'C' or
			surface = 'Asphalt' or
			surface = 'ASPH-F' or
			surface = 'CONC-G' or
			surface = 'GRAVEL' or
			surface = 'Turf' or
			surface = 'GRVL' or
			surface = 'GVL' or
			surface = 'PEM' or
			surface = 'ASPH/ CONC' or
			surface = 'N' or
			surface = 'X' or
			surface = 'G' or
			surface = 'DIRT' or
			surface = 'TURF-F' or
			surface = 'ASPH-G' or
			surface = 'TURF-G' or
			surface = 'ASPH' or
			surface = 'GRE' or
			surface = 'CON' or
			surface = 'CONC' or
			surface = 'TURF' or
			surface = 'ASP' 
*/
			cast(length_ft as integer) > 20 * cast(width_ft as integer) /* this is for excluding "strange" runways like water surface runways */

		GROUP BY airport_ident
	) as s
WHERE
	a.icao = s.icao
ORDER BY s.surface_area_ft2
;


