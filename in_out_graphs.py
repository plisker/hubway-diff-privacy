# ///////////////////////////////////////
# /*								   */
# /*          Bikes In and Out         */
# /*            Paul Lisker            */
# /*           June-July 2016          */
# /*	   							   */
# ///////////////////////////////////////

import numpy as np
import csv
from datetime import datetime
import matplotlib.pyplot as plt

STATIONS = 145+1 # So as to 1-index
HOURS = 24 # So as to have first number be the row index


def initialize_matrix():
	matrix = []
	for i in range(STATIONS):
		row = []
		for j in range(HOURS):
			row.append(0)
		row.append(i) # Each row will have 24 numbers, 0-indexed: 0-23 are hours, and 24th number is station ID
		matrix.append(row)
	return matrix

def average_matrix(matrix, denominator):
	for i in range(STATIONS):
		for j in range(HOURS):
				matrix[i][j] = (matrix[i][j])/float(denominator)

def plot_station(station_id, bikes_in, bikes_out):
	hours_axis = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

	station_out = bikes_out[station_id]
	del station_out[-1]
	print(station_out)
	plt.plot(hours_axis, station_out)

	station_in = bikes_in[station_id]
	del station_in[-1]
	print(station_in)
	plt.plot(hours_axis, station_in)
	plt.show()

in_matrix = initialize_matrix()
out_matrix = initialize_matrix()
in_dates = []
out_dates = []

with open('../hubway2/hubway_trips.csv', 'rb') as csvfile:
	trips = csv.reader(csvfile)
	for row in trips:
		try:
			start_station = int(row[5]) # Get start station ID number
			end_station = int(row[7]) # Get end station ID number
			start_time_string = row[4] # Get start date and time
			end_time_string = row[6] # Get end date and time
			start_datetime = datetime.strptime(start_time_string, "%m/%d/%Y %H:%M:%S") # Convert date and time to datetime format
			end_datetime = datetime.strptime(end_time_string, "%m/%d/%Y %H:%M:%S") # Convert date and time to datetime format
		except:
			continue # If error (e.g. if header row, or if some information is missing, go to next row)

		# Note: station 145 will be in index 145 (i.e., first row will be empty, since there is no station 0)
		# 1-indexing for future clarity

		out_matrix[start_station][start_datetime.hour] += 1 # Increase counter to appropriate spot in tracking matrix
		in_matrix[end_station][end_datetime.hour] += 1 # Increase counter to appropriate spot in tracking matrix

		start_date = datetime.strftime(start_datetime, "%x")
		end_date = datetime.strftime(end_datetime, "%x")

		out_dates.append(start_date)
		in_dates.append(end_date)

in_date_set = set(in_dates)
out_date_set = set(out_dates)

# TODO: DELETE the /4
average_matrix(in_matrix, len(in_date_set)/4)
average_matrix(out_matrix, len(out_date_set)/4)

print(len(in_date_set))
print(len(out_date_set))

plot_station(38, in_matrix, out_matrix)


