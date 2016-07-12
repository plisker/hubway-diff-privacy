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
stationList = [""]
(stationList.append(i) for i in range(STATIONS))
row_counter = 0
number_of_trips = 0

def initialize_matrix():
	matrix = []
	for i in range(STATIONS):
		row = []
		for j in range(STATIONS):
			row.append(0)
		row.append(i)
		matrix.append(row)
	return matrix


def processData(file, inMatrix, outMatrix, raw, counter):
	with open(file, 'rb') as csvfile:
		number_of_trips = sum(1 for line in csvfile)
		csvfile.seek(0) # Go back to top of file for next loop

		trips = csv.reader(csvfile)
		for row in trips:
			if raw:
				try:
					start_station = int(row[5]) # Get start station ID number
					end_station = int(row[7]) # Get end station ID number

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

					start_time_string = row[3] # Get start date and time
					duration = timedelta(seconds=float(row[4]))
					start_datetime = datetime.strptime(start_time_string, " %d/%m/%Y %H:%M") # Convert date and time to datetime format
					end_datetime = start_datetime + duration # Convert date and time to datetime format
				except:
					continue # If error (e.g. if header row, or if some information is missing, go to next row)

			# Note: station 145 will be in index 145 (i.e., first row will be empty, since there is no station 0)
			# 1-indexing for future clarity
			if start_datetime.isoweekday() and end_datetime.isoweekday() in range(1, 6):
				outMatrix[start_station][end_station] += 1 # Increase counter to appropriate spot in tracking matrix
				inMatrix[end_station][start_station] += 1 # Increase counter to appropriate spot in tracking matrix

				start_date = str(datetime.strftime(start_datetime, "%x"))
				end_date = str(datetime.strftime(end_datetime, "%x"))


			# increase progress bar as appropriately
			counter += 1
			percentage = (counter/float(4*number_of_trips))*100
			progress(percentage)

def writeCSV(filename, inMatrix, outMatrix, rawIn, rawOut):
	a = np.matrix(inMatrix)
	b = np.matrix(outMatrix)

	c = np.matrix(rawIn)
	d = np.matrix(rawOut)

	e = c-a
	f = d-b

	in_data = e.tolist()
	out_data = f.tolist()

	i = 0
	for row in in_data:
		row.insert(0, i)
		del row[-1]
		i += 1

	i = 0
	for row in out_data:
		row.insert(0, i)
		del row[-1]
		i += 1

	in_data.insert(0, stationList)
	out_data.insert(0, stationList)

	with open('Data/diff-'+filename+'-bikes_in.csv', 'w') as cleaned_file:
	    a = csv.writer(cleaned_file, delimiter=',')
	    data = in_data
	    a.writerows(data)

	with open('Data/diff-'+filename+'-bikes_out.csv', 'w') as cleaned_file:
	    a = csv.writer(cleaned_file, delimiter=',')
	    data = out_data
	    a.writerows(data)

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

startProgress("Processing data") # Start progress bar

in_matrix_raw = initialize_matrix()
out_matrix_raw = initialize_matrix()

in_matrix_2 = initialize_matrix()
out_matrix_2 = initialize_matrix()

in_matrix_3 = initialize_matrix()
out_matrix_3 = initialize_matrix()

in_matrix_6 = initialize_matrix()
out_matrix_6 = initialize_matrix()

processData("Data/8-diffprivTest/0.2-hubway-synthetic-our.csv", in_matrix_2, out_matrix_2, False, row_counter)
processData("Data/8-diffprivTest/0.3-hubway-synthetic-our.csv", in_matrix_3, out_matrix_3, False, row_counter)
processData("Data/8-diffprivTest/0.6-hubway-synthetic-our.csv", in_matrix_6, out_matrix_6, False, row_counter)
processData("Data/hubway-original_post2012/trips_post2012_3iqr.csv", in_matrix_raw, out_matrix_raw, True, row_counter)

endProgress() # Finish progress bar

writeCSV("0.2", in_matrix_2, out_matrix_2, in_matrix_raw, out_matrix_raw)
writeCSV("0.3", in_matrix_3, out_matrix_3, in_matrix_raw, out_matrix_raw)
writeCSV("0.6", in_matrix_6, out_matrix_6, in_matrix_raw, out_matrix_raw)
