# ///////////////////////////////////////
# /*								   */
# /*                R^2                */
# /*            Paul Lisker            */
# /*           June-July 2016          */
# /*	   							   */
# ///////////////////////////////////////

import numpy as np
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy import stats
import sys
import copy

STATIONS = 145+1 # So as to 1-index
stationList = [""]
[stationList.append(i) for i in range(STATIONS)]
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


def processData(file, tripMatrix, raw, counter):
	with open(file, 'rb') as csvfile:
		number_of_trips = sum(1 for line in csvfile)
		csvfile.seek(0) # Go back to top of file for next loop

		trips = csv.reader(csvfile)
		for row in trips:
			if raw:
				try:
					start_station = int(row[0]) # Get start station ID number
					end_station = int(row[1]) # Get end station ID number

					start_time_string = row[2] # Get start date and time
					end_time_string = row[4] # Get end date and time
					start_datetime = datetime.strptime(start_time_string, " %Y-%m-%d %H:%M:%S") # Convert date and time to datetime format
					end_datetime = datetime.strptime(end_time_string, " %Y-%m-%d %H:%M:%S") # Convert date and time to datetime format
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
				tripMatrix[start_station][end_station] += 1 # Increase counter to appropriate spot in tracking matrix

			# increase progress bar as appropriately
			counter += 1
			percentage = (counter/float(11*number_of_trips))*100
			progress(percentage)

def divideEntries(numerator, denominator):
	a = initialize_matrix()

	for i in range(STATIONS):
		for j in range(STATIONS):
			denom = denominator[i][j]
			num = numerator[i][j]
			if denom != 0:
				a[i][j] = int((100*(num/float(denom))))

	return a

def matrixCSV(filename, tripMatrix, rawOut):

	tripMatrix_copy = copy.deepcopy(tripMatrix)


	a = np.matrix(tripMatrix_copy)
	b = np.matrix(rawOut)

	c = a-b # Out
	out_data = c.tolist()

	d = divideEntries(out_data, rawOut)

	i = 0
	for row in out_data:
		row.insert(0, i)
		del row[-1]
		i += 1

	i = 0
	for row in d:
		row.insert(0, i)
		del row[-1]
		i += 1

	i = 0
	for row in tripMatrix_copy:
		row.insert(0, i)
		del row[-1]
		i += 1

	out_data.insert(0, stationList)
	d.insert(0, stationList)
	tripMatrix_copy.insert(0, stationList)

	with open('Data/'+filename+'/'+filename+'-bikes_trip.csv', 'w') as cleaned_file:
	    a = csv.writer(cleaned_file, delimiter=',')
	    data = tripMatrix_copy
	    a.writerows(data)
	
	with open('Data/'+filename+'/diff-'+filename+'-bikes_trip.csv', 'w') as cleaned_file:
	    a = csv.writer(cleaned_file, delimiter=',')
	    data = out_data
	    a.writerows(data)

	with open('Data/'+filename+'/percent-diff-'+filename+'-bikes_trip.csv', 'w') as cleaned_file:
	    a = csv.writer(cleaned_file, delimiter=',')
	    data = d
	    a.writerows(data)

def arrayCSV(filename, array):
	with open('Data/'+filename+'/'+filename+'-bikes_trip.csv', 'w') as cleaned_file:
		a = csv.writer(cleaned_file, delimiter=',')
		data = array
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

out_matrix_raw = initialize_matrix()
out_matrix_1 = initialize_matrix()
out_matrix_2 = initialize_matrix()
out_matrix_3 = initialize_matrix()
out_matrix_4 = initialize_matrix()
out_matrix_5 = initialize_matrix()
out_matrix_6 = initialize_matrix()
out_matrix_7 = initialize_matrix()
out_matrix_8 = initialize_matrix()
out_matrix_9 = initialize_matrix()
out_matrix_10 = initialize_matrix()

processData("Data/hubway-syn-data/0.1-1-hubway-synthetic-our.data", out_matrix_1, False, row_counter)
processData("Data/hubway-syn-data/0.2-1-hubway-synthetic-our.data", out_matrix_2, False, row_counter)
processData("Data/hubway-syn-data/0.3-1-hubway-synthetic-our.data", out_matrix_3, False, row_counter)
processData("Data/hubway-syn-data/0.4-1-hubway-synthetic-our.data", out_matrix_4, False, row_counter)
processData("Data/hubway-syn-data/0.5-1-hubway-synthetic-our.data", out_matrix_5, False, row_counter)
processData("Data/hubway-syn-data/0.6-1-hubway-synthetic-our.data", out_matrix_6, False, row_counter)
processData("Data/hubway-syn-data/0.7-1-hubway-synthetic-our.data", out_matrix_7, False, row_counter)
processData("Data/hubway-syn-data/0.8-1-hubway-synthetic-our.data", out_matrix_8, False, row_counter)
processData("Data/hubway-syn-data/0.9-1-hubway-synthetic-our.data", out_matrix_9, False, row_counter)
processData("Data/hubway-syn-data/1.0-1-hubway-synthetic-our.data", out_matrix_10, False, row_counter)
processData("Data/hubway-syn-data/hubway-error-free.data", out_matrix_raw, True, row_counter)

endProgress() # Finish progress bar

matrixCSV("0.1", out_matrix_1, out_matrix_raw)
matrixCSV("0.2", out_matrix_2, out_matrix_raw)
matrixCSV("0.3", out_matrix_3, out_matrix_raw)
matrixCSV("0.4", out_matrix_4, out_matrix_raw)
matrixCSV("0.5", out_matrix_5, out_matrix_raw)
matrixCSV("0.6", out_matrix_6, out_matrix_raw)
matrixCSV("0.7", out_matrix_7, out_matrix_raw)
matrixCSV("0.8", out_matrix_8, out_matrix_raw)
matrixCSV("0.9", out_matrix_9, out_matrix_raw)
matrixCSV("1.0", out_matrix_10, out_matrix_raw)
arrayCSV("raw", out_matrix_raw)