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
row_counter = 0

duration = []

with open('Data/hubway-original_post2012/trips_post2012.csv', 'rb') as original_file:
	number_of_trips = sum(1 for line in original_file) # Calculated for progress bar
	original_file.seek(0) # Go back to top of file for next loop

	stations = csv.reader(original_file)
	for row in stations:
		trip_length = row[3]
		try:
			trip_length = int(trip_length)
		except:
			if trip_length is "\"duration\"": #I.e., ignore title row
				continue
			else:
				# duration.append(0)
				continue # If error (e.g. if some information is missing, append 0 and go to next row)

		if trip_length <= 0:
			1+1
			# duration.append(0) #Ignore values less than 0 and append as 0
		else:
			duration.append(trip_length) #Append all other values

		# More progress bar code
		row_counter += 0.5
		percentage = (row_counter/float(number_of_trips))*100
		progress(percentage)

	original_file.seek(0) # Go back to top of file for next loop
	
	a = np.array(duration) #Numpy array for statistics

	q75, q25 = np.percentile(a, [75 ,25]) # Calculate quartiles
	iqr = q75 - q25 # Calculate IQR

	# Calculate 3IQR
	lbound = q25 - (1.5*iqr) 
	ubound = q75 + (1.5*iqr)

	# Start writing the CSV without outliers
	with open('Data/hubway-original_post2012/trips_post2012_3iqr.csv', 'w') as cleaned_file:
		writer = csv.writer(cleaned_file, delimiter=',')
		stations = csv.reader(original_file)
		
		for row in stations: # Read each row of original file
			temp = row

			if row[3] is "\"duration\"": # If header row, include
				writer.writerow(temp)
			else:
				value = row[3] # Obtain duration value
				
				try:
					value = int(value)
				except: # If non-numeric, replace with 0 and write row
					temp[3] = 0
					# writer.writerow(temp)
				
				if value <= 0 and lbound <= 0: # If less than 0 and lower bound is <= 0, then the value becomes 0 (and thus above lower bound) and row written
					temp[3] = 0
					# writer.writerow(temp)
				elif value < lbound or value > ubound: # If value outside of bounds, discard
					row_counter += 0.5
					percentage = (row_counter/float(number_of_trips))*100
					progress(percentage)
					continue
				else: # All other values are within bounds, so write row
					writer.writerow(temp)
				
			# More progress bar code
			row_counter += 0.5
			percentage = (row_counter/float(number_of_trips))*100
			progress(percentage)

	endProgress()

	# Print some statistcs on original file
	print("q25: "+str(q25))
	print("q75: "+str(q75))
	print("iqr: "+str(iqr))
	print("lbound: "+str(lbound))
	print("ubound: "+str(ubound))
	print("min: "+str(min(duration)))
	print("max: "+str(max(duration)))

	# print(sorted(duration))


