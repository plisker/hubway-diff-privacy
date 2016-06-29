# Hubway-DP
Code to assess the utility of differential privacy when applied to Hubway Visualization Contest data

The visualization referred to in this repository is the one seen here: http://zsobhani.github.io/hubway-team-viz/

** in_out_graphs.py **
This code will prompt the user to determine whehter raw data or synthetic data should be analyzed. If synthetic, the user will be prompted to choose between the available files. Then, the script will run on the selected dataset, provide some statistics, and will prompt the user for a station to analyze. It will then plot the average number of bikes coming in and out of the determined station on a weekday.

** set_of_stations.py **
This code reads the CSV file with the list of stations and prints the set of stations. Used to hardcode the set into the previous two codes.