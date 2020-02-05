DROP TABLE IF EXISTS temp_passenger_flows;

CREATE TABLE temp_passenger_flows (
	airline_id TEXT, 
	source_airport_id TEXT, 
	destination_airport_id TEXT, 
	passenger_flow REAL
);
CREATE INDEX temp_index ON temp_passenger_flows (airline_id, source_airport_id, destination_airport_id);

.mode csv temp_passenger_flows
.import ./temp_passenger_flows.csv temp_passenger_flows

ALTER TABLE routes ADD COLUMN passenger_flow REAL;

UPDATE 
	routes
SET 
	passenger_flow = (
		SELECT 
			passenger_flow
		FROM 
			temp_passenger_flows
		WHERE
			temp_passenger_flows.airline_id = routes.airline_id and
			temp_passenger_flows.source_airport_id = routes.source_airport_id and
			temp_passenger_flows.destination_airport_id = routes.destination_airport_id
	)
;

DROP INDEX temp_index;

DROP TABLE temp_passenger_flows;
