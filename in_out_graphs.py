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

def plot(x, y, data_titles, station_id, direction):
	titles = ", "
	titles = titles.join(data_titles)

	counter = 0
	for row in y:
		plt.plot(x, row, label=data_titles[counter])
		counter += 1

	plt.xlabel('Hour of Day')
	plt.ylabel('Number of trips')
	plt.legend(loc='upper right')
	if direction:
		plt.title("Number of Trips per Hour, Bikes In: {"+titles+"}, Station "+str(station_id))
	else:
		plt.title("Number of Trips per Hour, Bikes Out:  {"+titles+"}, Station "+str(station_id))
	plt.grid(True)

	plt.show()

def graphData(data, station_id):
	bikes_in = []
	bikes_out = []
	x = data[0].x_axis_hours
	data_titles = []

	for row in data:
		station_in, station_out = row.station_data(station_id)
		bikes_in.append(station_in)
		bikes_out.append(station_out)

		data_titles.append(row.filename)

	plot(x, bikes_in, data_titles, station_id, True)
	plot(x, bikes_out, data_titles, station_id, False)

def graphGeneral(data):
	bikes_in = []
	bikes_out = []
	x = data[0].x_axis_hours
	data_titles = []

	for row in data:
		station_in, station_out = row.station_data(station_id)
		bikes_in.append(station_in)
		bikes_out.append(station_out)

		data_titles.append(row.filename)

	plot(x, bikes_in, data_titles, station_id, True)
	plot(x, bikes_out, data_titles, station_id, False)

def main():
	rawData = GraphTrips()
	syn1 = GraphTrips(synthetic_file="0.1")
	syn2 = GraphTrips(synthetic_file="0.2")
	syn3 = GraphTrips(synthetic_file="0.3")
	syn4 = GraphTrips(synthetic_file="0.4")
	syn5 = GraphTrips(synthetic_file="0.5")
	syn6 = GraphTrips(synthetic_file="0.6")
	syn7 = GraphTrips(synthetic_file="0.7")
	syn8 = GraphTrips(synthetic_file="0.8")
	syn9 = GraphTrips(synthetic_file="0.9")
	syn10 = GraphTrips(synthetic_file="1.0")
	
	# a = [rawData, syn1, syn10]

	# graphData(a, 14)


main()




