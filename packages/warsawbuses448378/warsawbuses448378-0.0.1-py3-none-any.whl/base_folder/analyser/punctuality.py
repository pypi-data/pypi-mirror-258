import pandas as pd
import os
from analyser import distance2
import time


# This function uses geo data from buses and bus stops to determine if the bus is on the bus stop
# and if it is, it saves the data to a csv file
def punctuality_of_line(locations_file, line, km_threshold=0.10):
    point0 = time.time()
    locations = pd.read_csv('data\\' + locations_file)
    if not os.path.isfile('data\\schedules' + line + '.csv'):
        raise FileNotFoundError('File not found')
    schedules = pd.read_csv('data\\schedules' + line + '.csv')
    point1 = time.time()
    print("Time to read csv: ", point1 - point0)
    schedules = schedules.rename(columns={'szer_geo': 'szer_geo_stop', 'dl_geo': 'dl_geo_stop',
                                          'time': 'time_stop'})
    # narrow down locations to line
    locations = locations[locations['lines'] == line]
    locations = locations.rename(columns={'szer_geo': 'szer_geo_bus', 'dl_geo': 'dl_geo_bus',
                                          'time': 'time_bus'})
    locations['time_bus'] = pd.to_datetime(locations['time_bus']).dt.time

    # convert time_stop to time HH:MM:SS
    schedules['time_stop'] = pd.to_datetime(schedules['time_stop'], format='%H:%M:%S').dt.time

    # brigade to string
    schedules['brigade'] = schedules['brigade'].astype(str)
    locations['brigade'] = locations['brigade'].astype(str)

    # merge schedules and locations on brigade
    buses_on_stops = schedules.merge(locations, on='brigade')
    point2 = time.time()
    print("Time to merge: ", point2 - point1)
    mask = buses_on_stops.apply(lambda row: distance2(row['dl_geo_stop'] - row['dl_geo_bus'],
                                            row['szer_geo_stop'] - row['szer_geo_bus']) < km_threshold, axis=1)
    point3 = time.time()
    print("Time to calculate distance: ", point3 - point2)
    buses_on_stops = buses_on_stops[mask]

    # create a mask for time difference, chcec if time difference is less than an hour
    mask = buses_on_stops.apply(lambda row: abs(row['time_bus'].hour - row['time_stop'].hour) < 1, axis=1)
    buses_on_stops = buses_on_stops[mask]
    point4 = time.time()
    print("Time to calculate time difference: ", point4 - point3)

    # remove duplicate rows
    buses_on_stops = buses_on_stops.drop_duplicates()

    # remove rows with NaN values
    buses_on_stops = buses_on_stops.dropna()
    # save buses_on_stops to csv in data directory
    buses_on_stops.to_csv('data\\buses_on_stops' + line + '.csv', index=False)


# This function uses data from buses_on_stops to determine if the bus is late or early
def test_punctuality_of_line(line, threshold=3, output_file='buses_late_or_early.csv'):
    time0 = time.time()
    buses_on_stops = pd.read_csv('data\\buses_on_stops' + line + '.csv')
    time1 = time.time()
    print("Time to read csv: ", time1 - time0)
    # treshold is amount of minutes that bus can be late or early
    buses_on_stops['time_bus'] = pd.to_datetime(buses_on_stops['time_bus'], format='%H:%M:%S')
    buses_on_stops['time_stop'] = pd.to_datetime(buses_on_stops['time_stop'], format='%H:%M:%S')
    buses_on_stops['time_diff'] = buses_on_stops['time_bus'] - buses_on_stops['time_stop']
    buses_on_stops['is_late'] = buses_on_stops['time_diff'] > pd.Timedelta(0)
    buses_on_stops['is_early'] = buses_on_stops['time_diff'] < pd.Timedelta(0)
    buses_on_stops['time_diff'] = buses_on_stops['time_diff'].dt.total_seconds() / 60
    buses_on_stops['time_diff'] = buses_on_stops['time_diff'].abs()
    buses_on_stops = buses_on_stops[buses_on_stops['time_diff'] > threshold]
    # discard columns brigade, szer_geo_bus, dl_geo_bus, id_ulicy
    buses_on_stops = buses_on_stops.drop(columns=['brigade', 'szer_geo_bus', 'dl_geo_bus', 'id_ulicy'])
    # group by zespol and slupek and take mean of time_diff
    buses_on_stops = buses_on_stops.groupby(['zespol', 'slupek', 'szer_geo_stop',
                                             'dl_geo_stop', 'nazwa_zespolu']).agg({'time_diff': 'mean'}).reset_index()
    buses_on_stops.to_csv('data\\' + output_file, index=False)
    time2 = time.time()
    print("Time to finish: ", time2 - time1)


# punctuality_of_line('180')
# test_punctuality_of_line('180')