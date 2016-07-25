# ///////////////////////////////////////
# /*                                   */
# /*          Trip Statistics          */
# /*            Paul Lisker            */
# /*           June-July 2016          */
# /*                                   */
# ///////////////////////////////////////

import numpy as np
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy import stats
import sys
import copy


class TripStatistics(object):
	def __init__(self, file="raw"):
		super(TripStatistics, self).__init__()
		self.file = file
		self.data_in = self.importCSV("Data/"+self.file+"/"+self.file+"-bikes_in.csv")
		self.data_out = self.importCSV("Data/"+self.file+"/"+self.file+"-bikes_out.csv")
		self.data_in_original = self.importCSV("Data/raw/raw-bikes_in.csv")
		self.data_out_original = self.importCSV("Data/raw/raw-bikes_out.csv")
		self.r_squared_in = []
		self.r_squared_out = []
		self.analyzeTrips()

	def importCSV(self, file):
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

	def r_squared(self, x, y):
		slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
		return r_value**2

	def analyzeTrips(self):
		temp_in = []
		temp_out = []

		for i in range(len(self.data_in_original)):
			try:
				temp_in.append(self.r_squared(self.data_in_original[i], self.data_in[i]))
			except:
				print "First loop: Row "+str(i)+" failed for epsilon of "+self.file+"! Check why..."

		for i in range(len(self.data_out_original)):
			try:
				temp_out.append(self.r_squared(self.data_out_original[i], self.data_out[i]))
			except:
				print "Second loop: Row "+str(i)+" failed for epsilon of "+self.file+"! Check why..."

		self.r_squared_in = temp_in
		self.r_squared_out = temp_out

	def plotStation(self, station_id, data):
		plt.plot(station_id, data[station_id], '.')

	def plotAll(self):
		for i in range(len(self.r_squared_in)):
			self.plotStation(i, self.r_squared_in)

		plt.xlabel('Stations')
		plt.ylabel('R^2')
		plt.title("R^2 vs Station: Arriving Trips")
		plt.axis([0, 150, 0, 1.1])
		plt.show()

		for i in range(len(self.r_squared_out)):
			self.plotStation(i, self.r_squared_out)

		plt.xlabel('Stations')
		plt.ylabel('R^2')
		plt.title("R^2 vs Station: Arriving Trips")
		plt.axis([0, 150, 0, 1.1])
		plt.show()









