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

def printStatistics(data):
	print("")
	print("Let's start with some statistics:")
	print("The number of trips is "+str(data.number_of_trips))
	print("The number of days for which there are outbound trips are "+str(len(data.out_date_set)))
	print("The number of days for which there are inbound trips are "+str(len(data.in_date_set)))
	print("Outgoing stations not represented in the data are: ")
	print(list(data.out_sets_missing))
	print("Incoming stations not represented in the data are: ")
	print(list(data.in_sets_missing))
	print("")

def main():

	analyzeData = GraphTrips()

	analyzeData.user_input()
	analyzeData.analysis()
	
	# printStatistics(analyzeData)

	in_data = [["",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]
	out_data = [["",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]

	for station in analyzeData.SET_OF_STATIONS:
		try:
			arrive, leave = analyzeData.station_data(station, analyzeData.in_matrix, analyzeData.out_matrix)
		except:
			print(station)
			continue

		arrive.insert(0, station)
		leave.insert(0, station)

		in_data.append(arrive)
		out_data.append(leave)

	# Start writing the CSV without outliers
	with open('Data/'+analyzeData.filename+'/'+analyzeData.filename+'-bikes_in.csv', 'w') as cleaned_file:
	    a = csv.writer(cleaned_file, delimiter=',')
	    data = in_data
	    a.writerows(data)

	with open('Data/'+analyzeData.filename+'/'+analyzeData.filename+'-bikes_out.csv', 'w') as cleaned_file:
	    a = csv.writer(cleaned_file, delimiter=',')
	    data = out_data
	    a.writerows(data)

	continue_running = True
	while continue_running:
		try:
			station = input("What station do you want to plot? ")
			analyzeData.plot_station(station, analyzeData.in_matrix, analyzeData.out_matrix)
		except:
			print("That isn't a valid number. Please try again!")
			continue
		test = analyzeData.plot_again()
		if test is 0:
			continue
		else:
			break

main()
