import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import functions as f
import pickle
import glob
import sys
from pytz import timezone
import pytz
et = timezone('US/Eastern')
from collections import Counter
 
def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]


# load station data
stations = pd.read_csv("stations.csv")
lats = list(stations.get('latitude'))
longs = list(stations.get('longitude'))

stationMapping = {}
for index, row in stations.iterrows():
    stationMapping[row['name']] = row['town']


# DATA_DIR = "/nfs/obelix/raid2/alechowicz/ValleyUsers/*.csv"
# DATA_FILES = glob.glob(DATA_DIR)
# # DATA_FILES = ["/nfs/obelix/raid2/alechowicz/ValleyBike/VB_Routes_Data_2018_11_08.csv"]

# # load user data
# dfs = []
# for file in DATA_FILES:
#    print(file)
#    df = pd.read_csv(file)
#    dfs.append(df)

# df = pd.concat(dfs)
# df = df.dropna(axis=1, how='all')
# print(len(df))

# df["Unlock"] = pd.to_datetime(df['UnlockDate'] + ' ' + df['UnlockTime'])
# df["Lock"] = pd.to_datetime(df['LockDate'] + ' ' + df['LockTime'])

# print("Dumping to pickle file!")
# pickle.dump( df, open( "/nfs/obelix/raid2/alechowicz/VU.pickle", "wb" ) )
print("Loading from pickle file!")
df = pickle.load( open( "/nfs/obelix/raid2/alechowicz/VU.pickle", "rb" ) )

# usersDict = {}

# for index, row in df.iterrows():
#     name = (row['fName'], row['lName'])
#     if pd.isnull(row['fName']):
#         continue
#     trip = {'unlock': row['Unlock'], 'lock': row['Lock'], 'dist': row['Distance'], 'duration': row['Duration'], 'cost': row['Costs'], 'startstation': row['StartStation'], 'endstation': row['EndStation']}
#     try:
#         if name not in usersDict.keys():
#             usersDict[name] = [trip]
#         else:
#             usersDict[name].append(trip)
#         sys.stdout.write(".")
#     except:
#         sys.stdout.write("{}".format(name))

# print("Dumping to pickle file!")
# pickle.dump( usersDict, open( "/nfs/obelix/raid2/alechowicz/usersDict.pickle", "wb" ) )

print("Loading from pickle file!")
usersDict = pickle.load( open( "/nfs/obelix/raid2/alechowicz/usersDict.pickle", "rb" ) )

trips = []
tripValues = []
activations = []
user_actives = []
top_stations = []
top_towns = []
avg_durations = []
avg_distances = []
for name in usersDict.keys():
    listStations = [x['startstation'] for x in usersDict[name]]
    mostCommonStation = most_frequent(listStations).replace('/','-')

    if mostCommonStation not in stationMapping.keys():
        # print(mostCommonStation)
        continue

    tripValues.append(usersDict[name])
    
    trips.append( len(usersDict[name]) )

    listTimes = [x['unlock'].replace(tzinfo=pytz.utc).astimezone(et) for x in usersDict[name]]
    activations.append(listTimes)
    active = (min(listTimes).strftime("%m-%d-%Y"), max(listTimes).strftime("%m-%d-%Y"))
    user_actives.append(active)

    top_stations.append(mostCommonStation)
    top_towns.append(stationMapping[mostCommonStation])

    durations = [x['duration'] for x in usersDict[name]]
    distances = [x['dist'] for x in usersDict[name]]
    avg_durations.append(sum(durations)/len(durations))
    avg_distances.append(sum(distances)/len(distances))

for name in usersDict.keys():
    for trip in usersDict[name]:
        trip['unlock'] = trip['unlock'].strftime("%m-%d-%y %H:%M:%S")
        trip['lock'] = trip['lock'].strftime("%m-%d-%y %H:%M:%S")

# names = [str(x[0]) + ' ' + str(x[1]) for x in usersDict.keys()]
# locs = [x[1] for x in locsDict.keys()]
# startLocsDict = {'date': dates, 'start_station': locs, 'num_trips': locsDict.values}
# startdf = pd.DataFrame(startLocsDict, columns=['date', 'start_station', 'num_trips'])

dfDict = {'num_trips': trips, 'active': user_actives, 'top_station': top_stations, 'top_town': top_towns, 'avg_duration': avg_durations, 'avg_distance': avg_distances, 'trips': tripValues}
userdf = pd.DataFrame(dfDict, columns=['num_trips', 'active', 'top_station', 'avg_duration', 'avg_distance', 'trips'])
userdf.to_csv('users.csv')