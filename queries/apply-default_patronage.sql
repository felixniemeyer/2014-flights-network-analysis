/* the necessary temporary table is created in the set-up-patronage.sql file. 
this split is necessary, so that we can run the estimation script in between */

UPDATE 
	airports 
SET
	patronage = ( SELECT * FROM temp_default_patronage ) 
WHERE
	patronage is null
;

DROP TABLE temp_default_patronage;

