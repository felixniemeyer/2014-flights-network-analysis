select 
	avg ( cast(length_ft as real) / cast(width_ft as real) ) as ratio
from 
	runways
