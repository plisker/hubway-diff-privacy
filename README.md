# Hubway-DP
Code to assess the utility of differential privacy when applied to Hubway Visualization Contest data

The visualization referred to in this repository is the one seen here: http://zsobhani.github.io/hubway-team-viz/

** raw-in_out_graphs.py **
This code will be run on the raw data and will prompt the user for a station to analyze. It will then plot the average number of bikes coming in and out of the determined station on a weekday.

** synthetic-in_out_graphs.py **
This code will prompt to user to choose a synthetic dataset (either 0.2, 0.3, or 0.6), and will otherwise run identically to raw-in_out_graphs.py.

** set_of_stations.py **
This code reads the CSV file with the list of stations and prints the set of stations. Used to hardcode the set into the previous two codes.

TODO: Merge the first two files into one code, since they run identically besides what file is being read.