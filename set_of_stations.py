# ///////////////////////////////////////
# /*								   */
# /*          Bikes In and Out         */
# /*            Paul Lisker            */
# /*           June-July 2016          */
# /*	   							   */
# ///////////////////////////////////////

import csv

set_of_stations = []

with open('Data/hubway2/hubway_stations.csv', 'rb') as csvfile:
	stations = csv.reader(csvfile)
	for row in stations:
		try:
			station = int(row[0])
		except:
			continue # If error (e.g. if header row, or if some information is missing, go to next row)
		set_of_stations.append(station)

print(set(set_of_stations))
