# ///////////////////////////////////////
# /*                                   */
# /*               Stats               */
# /*            Paul Lisker            */
# /*           June-July 2016          */
# /*                                   */
# ///////////////////////////////////////

import numpy as np
import matplotlib.pyplot as plt
from trip_statistics import TripStatistics

# x_axis = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

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

def main():
	one = TripStatistics("0.1")
	print one.r_squared_in[0]
	one.plotAll()

main()