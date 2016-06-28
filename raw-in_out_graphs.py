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
import sys

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
	print("Bikes out: ", station_out)
	plt.plot(hours_axis, station_out)
	station_out.append(station_id)

	station_in = bikes_in[station_id]
	del station_in[-1]
	print("Bikes in: ", station_in)
	plt.plot(hours_axis, station_in)
	station_in.append(station_id)
	plt.show()

def plot_again():
	proceed = raw_input("Would you like to plot another station? y/n ")
	if proceed is "y":
		return 0
	elif proceed is "n":
		return 1
	else:
		print("Sorry, didn't catch that. Let's try again.")
		plot_again()

# Progress bar with credit to http://stackoverflow.com/a/6169274 #
def startProgress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def endProgress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()

row_counter = 0
number_of_trips = 0

in_matrix = initialize_matrix()
out_matrix = initialize_matrix()
in_dates = []
out_dates = []

startProgress("Processing data")

with open('Data/hubway2/hubway_trips.csv', 'rb') as csvfile:
	number_of_trips = sum(1 for line in csvfile)
	csvfile.seek(0) # Go back to top of file for next loop

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
		if start_datetime.isoweekday() and end_datetime.isoweekday() in range(1, 6):
			out_matrix[start_station][start_datetime.hour] += 1 # Increase counter to appropriate spot in tracking matrix
			in_matrix[end_station][end_datetime.hour] += 1 # Increase counter to appropriate spot in tracking matrix

			start_date = str(datetime.strftime(start_datetime, "%x"))
			end_date = str(datetime.strftime(end_datetime, "%x"))

			out_dates.append(start_date)
			in_dates.append(end_date)

		# increase progress bar as appropriately
		row_counter += 1
		percentage = (row_counter/float(number_of_trips))*100
		progress(percentage)


in_date_set = set(in_dates) # Create set to get number of unique dates for the sake of creating averages
out_date_set = set(out_dates)

average_matrix(in_matrix, len(in_date_set))
average_matrix(out_matrix, len(out_date_set))

endProgress() # Finish progress bar

continue_running = True
while continue_running:
	try:
		station = input("What station do you want to plot? ")
		plot_station(station, in_matrix, out_matrix)
	except:
		print("That isn't a valid number. Please try again!")
		continue
	test = plot_again()
	if test is 0:
		continue
	else:
		break
		

