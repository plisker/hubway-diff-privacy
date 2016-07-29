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
from trip_statistics import TripStatistics
# import stats

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
	# syn2 = GraphTrips(synthetic_file="0.2")
	# syn3 = GraphTrips(synthetic_file="0.3")
	# syn4 = GraphTrips(synthetic_file="0.4")
	# syn5 = GraphTrips(synthetic_file="0.5")
	# syn6 = GraphTrips(synthetic_file="0.6")
	# syn7 = GraphTrips(synthetic_file="0.7")
	# syn8 = GraphTrips(synthetic_file="0.8")
	# syn9 = GraphTrips(synthetic_file="0.9")
	syn10 = GraphTrips(synthetic_file="1.0")

	raw = TripStatistics()
	stat1 = TripStatistics("0.1")
	stat2 = TripStatistics("0.2")
	stat3 = TripStatistics("0.3")
	stat4 = TripStatistics("0.4")
	stat5 = TripStatistics("0.5")
	stat6 = TripStatistics("0.6")
	stat7 = TripStatistics("0.7")
	stat8 = TripStatistics("0.8")
	stat9 = TripStatistics("0.9")
	stat10 = TripStatistics("1.0")
	
	a = [rawData, syn1, syn10]

	graphData(a, 14)
	graphData(a, 90)
	graphData(a, 40)
	graphData(a, 123)




main()




