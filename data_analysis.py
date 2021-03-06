# ///////////////////////////////////////
# /*                                   */
# /*           Data Analysis           */
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

class GraphTrips(object):
	def __init__(self, raw=True, filename="raw", file="Data/hubway-syn-data/hubway-error-free.data", synthetic_file="0.0"):
		super(GraphTrips, self).__init__()
		self.STATIONS = 145+1 # So as to 1-index
		self.HOURS = 24 # So as to have first number be the row index
		self.SET_OF_STATIONS = set([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145])
		self.x_axis_hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
		self.raw = raw
		self.number_of_trips = 0
		self.in_data = [["",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]
		self.out_data = [["",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]
		self.filename = filename
		self.file = file
		self.synthetic_file = synthetic_file
		self.analysis()

	def initialize_full_matrix(self):
		matrix = []
		for i in range(self.STATIONS):
			row = []
			for j in range(self.HOURS):
				row.append(0)
			row.append(i) # Each row will have 24 numbers, 0-indexed: 0-23 are hours, and 24th number is station ID
			matrix.append(row)
		return matrix

	def initialize_small_matrix(self):
		matrix = [0 for i in range(self.HOURS)]
		return matrix

	def average_matrix(self, matrix, denominator):
		for i in range(self.STATIONS):
			for j in range(self.HOURS):
					matrix[i][j] = (matrix[i][j])/float(denominator)

	def average_matrix_small(self, matrix, denominator):
		for i in range(self.HOURS):
				matrix[i] = (matrix[i])/float(denominator)

	def analysis(self):
		self.in_matrix = self.initialize_full_matrix()
		self.out_matrix = self.initialize_full_matrix()
		self.in_matrix_small = self.initialize_small_matrix()
		self.out_matrix_small = self.initialize_small_matrix()
		self.in_stations_represented = []
		self.out_stations_represented = []
		self.in_dates = []
		self.out_dates = []


		if self.synthetic_file not in ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]:
			self.user_input()
		else:
			if self.synthetic_file in ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]:
				self.file = "Data/hubway-syn-data/"+self.synthetic_file+"-1-hubway-synthetic-our.data"
				self.filename = self.synthetic_file
				self.raw = False

		if self.raw:
			self.startProgress("Processing raw data")
		else:
			self.startProgress("Processing "+self.synthetic_file+" synthetic data")

		row_counter = 0
		with open(self.file, 'rb') as csvfile:
				self.number_of_trips = sum(1 for line in csvfile)
				csvfile.seek(0) # Go back to top of file for next loop

				trips = csv.reader(csvfile)
				for row in trips:
					if self.raw:
						try:
							start_station = int(row[0]) # Get start station ID number
							end_station = int(row[1]) # Get end station ID number

							self.in_stations_represented.append(end_station)
							self.out_stations_represented.append(start_station)

							start_time_string = row[2] # Get start date and time
							end_time_string = row[4] # Get end date and time
							
							start_datetime = datetime.strptime(start_time_string, " %Y-%m-%d %H:%M:%S") # Convert date and time to datetime format
							end_datetime = datetime.strptime(end_time_string, " %Y-%m-%d %H:%M:%S") # Convert date and time to datetime format
						except:
							continue # If error (e.g. if header row, or if some information is missing, go to next row)
					
					elif not self.raw:
						try:
							start_station = int(row[1]) # Get start station ID number
							end_station = int(row[2]) # Get end station ID number

							self.in_stations_represented.append(end_station)
							self.out_stations_represented.append(start_station)

							start_time_string = row[3] # Get start date and time
							duration = timedelta(seconds=float(row[4]))
							start_datetime = datetime.strptime(start_time_string, " %d/%m/%Y %H:%M") # Convert date and time to datetime format
							end_datetime = start_datetime + duration # Convert date and time to datetime format
						except:
							continue # If error (e.g. if header row, or if some information is missing, go to next row)

					# Note: station 145 will be in index 145 (i.e., first row will be empty, since there is no station 0)
					# 1-indexing for future clarity
					if start_datetime.isoweekday() and end_datetime.isoweekday() in range(1, 6):
						self.out_matrix[start_station][start_datetime.hour] += 1 # Increase counter to appropriate spot in tracking matrix
						self.in_matrix[end_station][end_datetime.hour] += 1 # Increase counter to appropriate spot in tracking matrix

						self.out_matrix_small[start_datetime.hour] += 1
						self.in_matrix_small[end_datetime.hour] += 1

						start_date = str(datetime.strftime(start_datetime, "%x"))
						end_date = str(datetime.strftime(end_datetime, "%x"))

						self.out_dates.append(start_date)
						self.in_dates.append(end_date)

					# increase progress bar as appropriately
					row_counter += 1
					percentage = (row_counter/float(self.number_of_trips))*100
					self.progress(percentage)

		self.in_date_set = set(self.in_dates) # Create set to get number of unique dates for the sake of creating averages
		self.out_date_set = set(self.out_dates)

		self.average_matrix(self.in_matrix, len(self.in_date_set))
		self.average_matrix(self.out_matrix, len(self.out_date_set))

		self.average_matrix_small(self.in_matrix_small, len(self.in_date_set))
		self.average_matrix_small(self.out_matrix_small, len(self.out_date_set))

		self.in_station_set = set(self.in_stations_represented)
		self.out_station_set = set(self.out_stations_represented)

		self.in_sets_missing = self.SET_OF_STATIONS - self.in_station_set
		self.out_sets_missing = self.SET_OF_STATIONS - self.out_station_set

		self.output_csv()

		self.endProgress()

	# Used to set "file", "filename", and maybe "synthetic_file" via terminal
	def user_input(self):
		while True:
			raw_or_synthetic = raw_input("Would you like to analyze the raw or synthetic data? Type 'r' or 's'. ")
			if raw_or_synthetic is "r":
				break
			elif raw_or_synthetic is "s":
				self.raw = False
				break
			else:
				print("Sorry, that is not an option. Please try again!")
		
		if self.raw:
			print("Raw data will be analyzed!")
			self.file = "Data/hubway-syn-data/hubway-error-free.data"
			self.filename = "raw"

		while not self.raw:
			self.synthetic_file = raw_input("Which synthetic data would you like to analyze? 0.1, 0.2, 0.3, ... 0.8, 0.9, 1.0? ")
			if self.synthetic_file not in ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]:
				print("That is not an option. Please try again!")
			else:
				self.file = "Data/hubway-syn-data/"+self.synthetic_file+"-1-hubway-synthetic-our.data"
				self.filename = self.synthetic_file
				break

	def user_plot(self):
		self.continue_running = True
		while self.continue_running:
			try:
				station = input("What station do you want to plot? ")
				self.plot_station(station)
			except:
				print("That isn't a valid number. Please try again!")
				continue
			test = self.plot_again()
			if test is 0:
				continue
			else:
				break

	def output_csv(self):
		for station in self.SET_OF_STATIONS:
				try:
					arrive, leave = self.station_data(station)
				except:
					print(station)
					continue

				arrive.insert(0, station)
				leave.insert(0, station)

				self.in_data.append(arrive)
				self.out_data.append(leave)

		# Write CSV per station
		with open('Data/'+self.filename+'/'+self.filename+'-bikes_in.csv', 'w') as cleaned_file:
			a = csv.writer(cleaned_file, delimiter=',')
			data = self.in_data
			a.writerows(data)

		with open('Data/'+self.filename+'/'+self.filename+'-bikes_out.csv', 'w') as cleaned_file:
			a = csv.writer(cleaned_file, delimiter=',')
			data = self.out_data
			a.writerows(data)

		# Write CSV for generali
		with open('Data/'+self.filename+'/'+self.filename+'-total-bikes_in.csv', 'w') as cleaned_file:
			a = csv.writer(cleaned_file, delimiter=',')
			data = self.in_matrix_small
			a.writerow(data)

		with open('Data/'+self.filename+'/'+self.filename+'-total-bikes_out.csv', 'w') as cleaned_file:
			a = csv.writer(cleaned_file, delimiter=',')
			data = self.out_matrix_small
			a.writerow(data)

	def station_data(self, station_id):
		station_out = self.out_matrix[station_id]
		station_in = self.in_matrix[station_id]

		a = copy.deepcopy(station_in)
		b = copy.deepcopy(station_out)

		del a[-1]
		del b[-1]

		x = (a, b)

		return x
		
	def plot_station(self, station_id):
		station_in, station_out = self.station_data(station_id)

		print("Bikes out: ", station_out)
		plt.plot(self.x_axis_hours, station_out, label="Out")

		print("Bikes in: ", station_in)
		plt.plot(self.x_axis_hours, station_in, label="In")

		plt.xlabel('Hour of Day')
		plt.ylabel('Number of trips') 
		plt.legend()

		if self.raw:
			plt.title("Number of Trips per Hour: Raw Data, Station "+str(station_id))
		else:
			plt.title("Number of Trips per Hour: Epsilon "+str(self.synthetic_file)+", Station "+str(station_id))
		plt.grid(True)

		plt.show()

	def plot_again(self):
		proceed = raw_input("Would you like to plot another station? y/n ")
		if proceed is "y":
			return 0
		elif proceed is "n":
			return 1
		else:
			print("Sorry, didn't catch that. Let's try again.")
			plot_again()

	def statistics(self):
		print("")
		print("Some descriptory statistics:")
		if self.raw:
			print("Data analyzed: raw data")
		else:
			print("Data analyzed: "+self.synthetic_file+" synthetic data")
		print("The number of trips is "+str(self.number_of_trips))
		print("The number of days for which there are outbound trips are "+str(len(self.out_date_set)))
		print("The number of days for which there are inbound trips are "+str(len(self.in_date_set)))
		print("Outgoing stations not represented in the data are: ")
		print(list(self.out_sets_missing))
		print("Incoming stations not represented in the data are: ")
		print(list(self.in_sets_missing))
		print("")

	# Progress bar with credit to http://stackoverflow.com/a/6169274 #
	def startProgress(self, title):
		global progress_x
		sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
		sys.stdout.flush()
		progress_x = 0

	def progress(self, x):
		global progress_x
		x = int(x * 40 // 100)
		sys.stdout.write("#" * (x - progress_x))
		sys.stdout.flush()
		progress_x = x

	def endProgress(self):
		sys.stdout.write("#" * (40 - progress_x) + "]\n")
		sys.stdout.flush()


		