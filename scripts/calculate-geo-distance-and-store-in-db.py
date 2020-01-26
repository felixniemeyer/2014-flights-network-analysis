import sqlite3
import geopy.distance
import sys

db_file = sys.argv[1]

print("usage {0} <db_file>".format(sys.argv[0]))
output = open("./temp_geo_distances.csv", "w")

db_conn = sqlite3.connect(db_file)
cursor = db_conn.cursor()

cursor.execute("""
SELECT 
	r.airline_id,
	r.source_airport_id, 
	r.destination_airport_id, 
	a1.latitude, 
	a1.longitude, 
	a2.latitude, 
	a2.longitude
FROM 
	routes as r, 
	airports as a1, 
	airports as a2
WHERE
	r.source_airport_id = a1.airport_id and
	r.destination_airport_id = a2.airport_id
""")

rows = cursor.fetchall()

update = 'UPDATE routes SET distance_km = '
where = ' WHERE airline_id = "{0}" AND source_airport_id = "{1}" AND destination_airport_id = "{2}"'
i = 0
for row in rows: 
	airline = row[0]
	source = row[1]
	destination = row[2]
	coordsA = (row[3], row[4])
	coordsB = (row[5], row[6])
	distance = geopy.distance.geodesic(coordsA, coordsB).km
	output.write(','.join([airline, source, destination, "{0:.3f}".format(distance)]) + '\n')
	sys.stdout.write('\r{0:.1f}%'.format(100 / len(rows) * i))
	i += 1

output.flush()

sys.stdout.write('\r100%  \n')
sys.stdout.flush()


