# ///////////////////////////////////////
# /*								   */
# /*               Stats               */
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

def importCSV(file):
	data = []
	station_ids = []

	with open(file, 'rb') as csvfile:
		trips = csv.reader(csvfile)
		for station in trips:
			try:
				station_id = int(station[0])
			except:
				continue
			station_ids.append(station_id)
			del station[0]


			try:
				row = [float(i) for i in station]
			except:
				"Error! Be aware..."

			data.append(row)

	return data

def r_squared(x, y):
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	return r_value**2

files = ["raw", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]
data_in = []
data_out = []

startProgress("Processing data") # Start progress bar

count = 0
for file in files:
	data_in.append(importCSV("Data/"+file+"/"+file+"-bikes_in.csv"))
	data_out.append(importCSV("Data/"+file+"/"+file+"-bikes_out.csv"))
	
	count += 1
	percentage = (count/float(11))*100
	progress(percentage)

endProgress() # Finish progress bar

print r_squared(data_in[0][0], data_in[1][0])
