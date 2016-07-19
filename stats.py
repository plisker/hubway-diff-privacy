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

for file in files:
	data_in.append(importCSV("Data/"+file+"/"+file+"-bikes_in.csv"))
	data_out.append(importCSV("Data/"+file+"/"+file+"-bikes_out.csv"))

results_in = []
results_out = []

for i in range(len(data_in)):
	
	r_values = []
	for j in range(len(data_in[0])):
		try:
			r_values.append(r_squared(data_in[0][j], data_in[i][j]))
		except:
			print "Row "+str(j)+" failed for epsilon of "+str(i)+"! Check why..."

	results_in.append(r_values)

for i in range(len(data_out)):
	
	r_values = []
	for j in range(len(data_out[0])):
		try:
			r_values.append(r_squared(data_out[0][j], data_out[i][j]))
		except:
			print "Row "+str(j)+" failed for epsilon of "+str(i)+"! Check why..."

	results_out.append(r_values)

# To see the r^2 values for all the stations for a specific file, add
# print(results_in[i][j]), where i represents the epsilon of the file multiplied by 10
# Optional, add the bracket with the j to see only the r^2 values of the station in the jth row

print ""
print "Epsilon 0.1, first in then out"
print results_in[1][0]
print results_out[1][0]
print ""

print "Epsilon 0.2, first in then out"
print results_in[2][0]
print results_out[2][0]
print ""

print "Epsilon 0.3, first in then out"
print results_in[3][0]
print results_out[3][0]
print ""

print "Epsilon 0.4, first in then out"
print results_in[4][0]
print results_out[4][0]
print ""

print "Epsilon 0.5, first in then out"
print results_in[5][0]
print results_out[5][0]
print ""

print "Epsilon 0.6, first in then out"
print results_in[6][0]
print results_out[6][0]
print ""

print "Epsilon 0.7, first in then out"
print results_in[7][0]
print results_out[7][0]
print ""

print "Epsilon 0.8, first in then out"
print results_in[8][0]
print results_out[8][0]
print ""

print "Epsilon 0.9, first in then out"
print results_in[9][0]
print results_out[9][0]
print ""

print "Epsilon 1.0, first in then out"
print results_in[10][0]
print results_out[10][0]
print ""




