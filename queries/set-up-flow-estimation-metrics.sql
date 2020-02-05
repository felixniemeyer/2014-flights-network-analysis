DROP TABLE IF EXISTS temp_flow_estimation_metrics;

CREATE TABLE temp_flow_estimation_metrics (
	airport_id TEXT PRIMARY KEY, 
	flow_sum REAL, 
	flow_deviation REAL
);

.mode csv temp_flow_estimation_metrics 
.import ./temp_flow_estimation_metrics.csv temp_flow_estimation_metrics

ALTER TABLE airports ADD COLUMN flow_sum REAL; 
ALTER TABLE airports ADD COLUMN flow_deviation REAL; 

UPDATE 
	airports	
SET
	flow_sum = (
		SELECT 
			flow_sum 	
		FROM 
			temp_flow_estimation_metrics
		WHERE 
			airports.airport_id = temp_flow_estimation_metrics.airport_id
	),
	flow_deviation = (
		SELECT 
			flow_deviation	
		FROM 
			temp_flow_estimation_metrics
		WHERE 
			airports.airport_id = temp_flow_estimation_metrics.airport_id
	)
		
