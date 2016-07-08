# Hubway-DP
Code to assess the utility of differential privacy when applied to Hubway Visualization Contest data

The visualization referred to in this repository is the one seen here: http://zsobhani.github.io/hubway-team-viz/

** in_out_graphs.py **
This code will prompt the user to determine whether raw data or synthetic data should be analyzed. If synthetic, the user will be prompted to choose between the available files. Then, the script will run on the selected dataset, provide some statistics, and will prompt the user for a station to analyze. It will then plot the average number of bikes coming in and out of the determined station on a weekday.

Furthermore, it will output the bikes coming in/out data into a CSV file for future analysis.

** set_of_stations.py **
This code reads the CSV file with the list of stations and prints the list of the set of stations. Used to hardcode the set into the previous two codes.

** remove_outlier.py **
This file takes in the trips_post2012.csv file and outputs a clean dataset with outliers removed, where outliers are removed via the following procedure, as described by Harichandan Roy:
  - Replace all negative duration values, if any, to zero. --probably, we should have removed (or reversed the sign) them rather than updating to zero.
  - Replace all non-numeric values, if any, to zero.  --probably, we should have removed them rather than updating to zero.
  - Make matrix [|stations| x |stations|] data structure and fill up with corresponding duration values. (Paul comment: in other words, each cell in the matrix consists of a trip from row station to column station.)
  - Apply 3IQR to each cell of the matrix. 3IQR approach left us entries having value in the range of [Q1 - 1.5(IQR), Q3 + 1.5(IQR)] where IQR = Q3 - Q1.