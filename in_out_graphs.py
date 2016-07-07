# ///////////////////////////////////////
# /*								   */
# /*          Bikes In and Out         */
# /*            Paul Lisker            */
# /*           June-July 2016          */
# /*	   							   */
# ///////////////////////////////////////

import numpy as np
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import sys
import copy

STATIONS = 145+1 # So as to 1-index
HOURS = 24 # So as to have first number be the row index
SET_OF_STATIONS = set([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145])

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

def station_data(station_id, bikes_in, bikes_out):
	station_out = bikes_out[station_id]
	del station_out[-1]

	station_in = bikes_in[station_id]
	del station_in[-1]

	a = copy.deepcopy(station_in)
	b = copy.deepcopy(station_out)

	x = (a, b)

	station_out.append(station_id)
	station_in.append(station_id)

	return x

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

in_stations_represented = []
out_stations_represented = []

filename = ""

raw = True

while True:
	raw_or_synthetic = raw_input("Would you like to analyze the raw or synthetic data? Type 'r' or 's'. ")
	if raw_or_synthetic is "r":
		break
	elif raw_or_synthetic is "s":
		raw = False
		break
	else:
		print("Sorry, that is not an option. Please try again!")

file = ""

if raw:
	print("Raw data will be analyzed!")
	file = "Data/hubway-original_post2012/trips_post2012_3iqr.csv"
	filename = "raw"

while not raw:
	synthetic_file = raw_input("Which synthetic data would you like to analyze? 0.2, 0.3, or 0.6? ")
	if synthetic_file not in ["0.2", "0.3", "0.6"]:
		print("That is not an option. Please try again!")
	else:
		file = "Data/8-diffprivTest/"+synthetic_file+"-hubway-synthetic-our.csv"
		filename = synthetic_file+"_synthetic"
		break
startProgress("Processing data")

with open(file, 'rb') as csvfile:
	number_of_trips = sum(1 for line in csvfile)
	csvfile.seek(0) # Go back to top of file for next loop

	trips = csv.reader(csvfile)
	for row in trips:
		if raw:
			try:
				start_station = int(row[5]) # Get start station ID number
				end_station = int(row[7]) # Get end station ID number

				in_stations_represented.append(end_station)
				out_stations_represented.append(start_station)

				start_time_string = row[4] # Get start date and time
				end_time_string = row[6] # Get end date and time
				start_datetime = datetime.strptime(start_time_string, "%Y-%m-%d %H:%M:%S") # Convert date and time to datetime format
				end_datetime = datetime.strptime(end_time_string, "%m/%d/%Y %H:%M:%S") # Convert date and time to datetime format
			except:
				continue # If error (e.g. if header row, or if some information is missing, go to next row)
		
		elif not raw:
			try:
				start_station = int(row[1]) # Get start station ID number
				end_station = int(row[2]) # Get end station ID number

				in_stations_represented.append(end_station)
				out_stations_represented.append(start_station)

				start_time_string = row[3] # Get start date and time
				duration = timedelta(seconds=float(row[4]))
				start_datetime = datetime.strptime(start_time_string, " %d/%m/%Y %H:%M") # Convert date and time to datetime format
				end_datetime = start_datetime + duration # Convert date and time to datetime format
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

in_station_set = set(in_stations_represented)
out_station_set = set(out_stations_represented)

in_sets_missing = SET_OF_STATIONS - in_station_set
out_sets_missing = SET_OF_STATIONS - out_station_set

print("")
print("Let's start with some statistics:")
print("The number of trips is "+str(number_of_trips))
print("The number of days for which there are outbound trips are "+str(len(out_date_set)))
print("The number of days for which there are inbound trips are "+str(len(in_date_set)))
print("Outgoing stations not represented in the data are: ")
print(list(out_sets_missing))
print("Incoming stations not represented in the data are: ")
print(list(in_sets_missing))
print("")

in_data = []
out_data = []

for station in SET_OF_STATIONS:

	try:
		arrive, leave = station_data(station, in_matrix, out_matrix)
	except:
		print(station)
		continue

	arrive.insert(0, station)
	leave.insert(0, station)

	in_data.append(arrive)
	out_data.append(leave)

	print(in_data)
	print(out_data)

# Start writing the CSV without outliers
with open('Data/'+filename+'-bikes_in.csv', 'w') as cleaned_file:
    a = csv.writer(cleaned_file, delimiter=',')
    data = in_data
    a.writerows(data)

with open('Data/'+filename+'-bikes_out.csv', 'w') as cleaned_file:
    a = csv.writer(cleaned_file, delimiter=',')
    data = out_data
    a.writerows(data)

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


