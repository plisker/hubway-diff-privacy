# ///////////////////////////////////////
# /*								   */
# /*          Bikes In and Out         */
# /*            Paul Lisker            */
# /*           June-July 2016          */
# /*	   							   */
# ///////////////////////////////////////

import csv
import numpy as np
import sys

NUMBER_OF_STATIONS = 145

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

startProgress("Processing data")

def initializeMatrix(n):
	matrix = [ [ [] for i in range(n)] for j in range(n)]
	return matrix

duration = []
to_write = []
count = 0

a = initializeMatrix(NUMBER_OF_STATIONS+1)

with open('Data/hubway-original_post2012/trips_post2012.csv', 'rb') as original_file:
	number_of_trips = sum(1 for line in original_file)
	original_file.seek(0) # Go back to top of file for next loop

	stations = csv.reader(original_file)
	for row in stations:

		percentage = (count/(3*float(number_of_trips)))*100
		progress(percentage)

		try:
			start_station = int(row[5])
			end_station = int(row[7])
		except:
			count += 1
			continue

		trip_length = row[3]
		try:
			trip_length = int(trip_length)
		except:
			if trip_length is "\"duration\"": #I.e., ignore title row
				count += 1
				continue
			else:
				pass

		if trip_length <= 0:
			a[start_station][end_station].append(0)
		else:
			a[start_station][end_station].append(trip_length)

		count += 1

	# print(duration)
	original_file.seek(0) # Go back to top of file for next loop
	
	for i in range(NUMBER_OF_STATIONS+1):
		for j in range(NUMBER_OF_STATIONS+1):
			count += 1

			percentage = (count/(3*float(number_of_trips)))*100
			progress(percentage)

			b = np.array(a[i][j])

			if len(b) == 0:
				a[i][j] = (-1,-1)
				continue

			q75, q25 = np.percentile(b, [75 ,25]) # Calculate quartiles
			iqr = q75 - q25 # Calculate IQR

			# Calculate 3IQR
			lbound = q25 - (1.5*iqr) 
			ubound = q75 + (1.5*iqr)

			a[i][j] = (lbound, ubound)

	# Start writing the CSV without outliers
	stations = csv.reader(original_file)
	
	for row in stations: # Read each row of original file
		
		percentage = (count/(3*float(number_of_trips)))*100
		progress(percentage)

		temp = row

		try:
			start_station = int(row[5])
			end_station = int(row[7])
		except:
			count += 1
			continue

		if row[3] is "\"duration\"": # If header row, include
			to_write.append(temp)

		else:
			value = row[3] # Obtain duration value
			try:
				low, high = a[start_station][end_station]
			except:
				# For debugging...
				print(start_station)
				print(end_station)
				print(a[start_station][end_station])
				break
			
			try:
				value = int(value)
			except: # If non-numeric, replace with 0 and write row
				to_write.append(temp)			

			if value < low or value > high: # If value outside of bounds, discard
				pass
			else: # All other values are within bounds, so write row
				to_write.append(temp)

		count += 1


# Start writing the CSV without outliers
with open('Data/hubway-original_post2012/trips_post2012_3iqr.csv', 'w') as cleaned_file:
    a = csv.writer(cleaned_file, delimiter=',')
    data = to_write
    a.writerows(data)

endProgress()

with open('Data/hubway-original_post2012/trips_post2012_3iqr.csv', 'rb') as new_file:
	number_of_trips = sum(1 for line in new_file)

	print(number_of_trips)