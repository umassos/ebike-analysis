import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import functions as f
import pickle
import glob
import sys

# load station data
stations = pd.read_csv("stations.csv")
lats = list(stations.get('latitude'))
longs = list(stations.get('longitude'))

names = []
towns = []
points = []
for index, row in stations.iterrows():
    names.append( row['name'] )
    towns.append( row["town"] )
    lat = lats[index]
    long = longs[index]
    points.append( (lat, long) )

# DATA_DIR = "/nfs/obelix/raid2/alechowicz/valleybike/*.csv"
# DATA_FILES = glob.glob(DATA_DIR)

# # load route data
# dfs = []
# for file in DATA_FILES:
#     print(file)
#     dfs.append(pd.read_csv(file))

# df = pd.concat(dfs)

# df["Date"] = pd.to_datetime(df["Date"])
# df.sort_values(by='Date')

print("Loading from pickle file!")
# pickle.dump( df, open( "/nfs/obelix/raid2/alechowicz/VB.pickle", "wb" ) )
df = pickle.load( open( "/nfs/obelix/raid2/alechowicz/VB.pickle", "rb" ) )

# locsDict = {}
# for index, row in df.iterrows():
#     if lat > 40 and long < -65:
#         try:
#             startLoc = f.closest_station(row['Latitude'], row['Longitude'], names, towns, points)
#             date = row["Date"]
#             if (startLoc, date) not in locsDict.keys():
#                 locsDict[(startLoc, date)] = 1
#             else:
#                 locsDict[(startLoc, date)] += 1
#             sys.stdout.write(".")
#         except:
#             sys.stdout.write("{}, {}".format(row['Latitude'], row['Longitude']))

# routesDict = {}

# for index, row in df.iterrows():
#     ID = row['Route ID']
#     if pd.isnull(row['Route ID']):
#         continue
#     if len(ID) < 10:
#         continue
#     location = (row['Latitude'], row['Longitude'])
#     if location[0] > 40 and location[1] < -65:
#         try:
#             time = row['Date']
#             if ID not in routesDict.keys():
#                 routesDict[ID] = {"locations": [location], "startTime": time, "endTime": time}
#             else:
#                 routesDict[ID]["locations"].append(location)
#                 routesDict[ID]["endTime"] = time
#             sys.stdout.write(".")
#         except:
#             sys.stdout.write("{}, {}".format(row['Latitude'], row['Longitude']))

# print("Dumping to pickle file!")
# pickle.dump( routesDict, open( "/nfs/obelix/raid2/alechowicz/routesDict.pickle", "wb" ) )
print("Loading from pickle file!")
routesDict = pickle.load( open( "/nfs/obelix/raid2/alechowicz/routesDict.pickle", "rb" ) )

durations = []
startLocations = []
endLocations = []
for ID in routesDict.keys():
    startTime = routesDict[ID]["startTime"]
    endTime = routesDict[ID]["endTime"]
    durations.append(endTime - startTime)
    lat, long = routesDict[ID]["locations"][0]
    try:
        startLocations.append(f.closest_station(lat, long, names, towns, points))
    except:
        startLocations.append("0")
    lat, long = routesDict[ID]["locations"][-1]
    try:
        endLocations.append(f.closest_station(lat, long, names, towns, points))
    except:
        endLocations.append("0")

# dates = [x[0] for x in locsDict.keys()]
# locs = [x[1] for x in locsDict.keys()]
# startLocsDict = {'date': dates, 'start_station': locs, 'num_trips': locsDict.values}
# startdf = pd.DataFrame(startLocsDict, columns=['date', 'start_station', 'num_trips'])
startTimes = [routesDict[ID]["startTime"] for ID in routesDict.keys()]

tripsDict = {'id': routesDict.keys(), 'start_station': startLocations, 'end_station': endLocations, 'start_time': startTimes, 'duration': durations}
tripdf = pd.DataFrame(tripsDict, columns=['id', 'start_station', 'end_station', 'start_time', 'duration'])
tripdf.to_csv('trips.csv')