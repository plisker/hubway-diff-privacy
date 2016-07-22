# ///////////////////////////////////////
# /*                                   */
# /*          Bikes In and Out         */
# /*            Paul Lisker            */
# /*           June-July 2016          */
# /*                                   */
# ///////////////////////////////////////

import numpy as np
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import sys
import copy
from data_analysis import GraphTrips

def main():
	rawData = GraphTrips()
	syn1 = GraphTrips(synthetic_file="1.0")

	rawData.analysis()
	syn1.analysis()
	
	rawData.statistics()
	syn1.statistics()

	in_data = [["",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]
	out_data = [["",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]

	for station in rawData.SET_OF_STATIONS:
		try:
			arrive, leave = rawData.station_data(station, rawData.in_matrix, rawData.out_matrix)
		except:
			print(station)
			continue

		arrive.insert(0, station)
		leave.insert(0, station)

		in_data.append(arrive)
		out_data.append(leave)

	# Start writing the CSV without outliers
	with open('Data/'+rawData.filename+'/'+rawData.filename+'-bikes_in.csv', 'w') as cleaned_file:
	    a = csv.writer(cleaned_file, delimiter=',')
	    data = in_data
	    a.writerows(data)

	with open('Data/'+rawData.filename+'/'+rawData.filename+'-bikes_out.csv', 'w') as cleaned_file:
	    a = csv.writer(cleaned_file, delimiter=',')
	    data = out_data
	    a.writerows(data)

main()
