# ///////////////////////////////////////
# /*                                   */
# /*               Stats               */
# /*            Paul Lisker            */
# /*           June-July 2016          */
# /*                                   */
# ///////////////////////////////////////

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from trip_statistics import TripStatistics

x_axis = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# for i in range(len(results_in[i])):
# 	to_plot = []
# 	for j in range(10):
# 		x = float(j+1)/10
# 		to_plot.append(resultsi_in[j+1][i])
# 	plt.scatter(x_axis, to_plot)

# 	m, b = np.polyfit(x_axis, to_plot, 1)

# 	new_y = [m*t+b for t in x_axis]

# 	plt.plot(x_axis, to_plot, '.')
# 	plt.plot(x_axis, new_y, '-')

# plt.xlabel('Epsilon Value')
# plt.ylabel('R^2')
# plt.title("R^2 vs Epsilon Values per Station: Arriving Trips")
# plt.axis([0, 1.1, 0, 1.1])
# plt.show()

# i=0
# j=0
# for i in range(len(results_out[i])):
# 	to_plot = []
# 	for j in range(10):
# 		x = float(j+1)/10
# 		to_plot.append(results_out[j+1][i])
# 	plt.scatter(x_axis, to_plot)

# 	m, b = np.polyfit(x_axis, to_plot, 1)

# 	new_y = [m*t+b for t in x_axis]

# 	plt.plot(x_axis, to_plot, '.')
# 	plt.plot(x_axis, new_y, '-')

# plt.xlabel('Epsilon Value')
# plt.ylabel('R^2')
# plt.title("R^2 vs Epsilon Values per Station: Outgoing Trips")
# plt.axis([0, 1.1, 0, 1.1])
# plt.show()

def graph_r_squared(epsilons):
	data_in = []
	data_out = []

	for element in epsilons:
		data_in.append(element.r_squared_in_all)

	for element in epsilons:
		data_out.append(element.r_squared_out_all)

	print data_in
	print data_out

	plt.plot(x_axis, data_in, '-', label="Incoming")
	plt.plot(x_axis, data_out, '-', label="Outoing")

	plt.xlabel('Epsilon Value')
	plt.ylabel('R^2')
	plt.title("R^2 vs Epsilon Values")
	plt.axis([0.0, 1.1, 0.7, 1.1])
	plt.legend(loc='best')
	plt.show()

def r_squared(x, y):
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	return r_value**2


def main():
	raw = TripStatistics()
	stat1 = TripStatistics("0.1")
	stat2 = TripStatistics("0.2")
	stat3 = TripStatistics("0.3")
	stat4 = TripStatistics("0.4")
	stat5 = TripStatistics("0.5")
	stat6 = TripStatistics("0.6")
	stat7 = TripStatistics("0.7")
	stat8 = TripStatistics("0.8")
	stat9 = TripStatistics("0.9")
	stat10 = TripStatistics("1.0")

	data = [stat1, stat2, stat3, stat4, stat5, stat6, stat7, stat8, stat9, stat10]

	graph_r_squared(data)

main()



