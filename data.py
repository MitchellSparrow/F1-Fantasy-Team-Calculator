import requests
from pprint import pprint
from driver import Driver
from constructor import Constructor
from itertools import combinations, product
import pandas as pd


def get_f1_data(combined_cost_limit):

    URL = 'https://fantasy-api.formula1.com/partner_games/f1/players'

    result = requests.get(url=URL)

    data = result.json()
    players = data['players']

    # pprint(players)

    drivers = []
    constructors = []

    for player in players:
        # Check if the data entry is a driver or constructor
        if player['constructor_data'] == None:
            drivers.append(
                Driver(player['display_name'],
                       player['season_score'],
                       player['price'],
                       player['streak_events_progress']['top_ten_in_a_row_qualifying_progress'],
                       player['streak_events_progress']['top_ten_in_a_row_race_progress']))

        else:
            constructors.append(
                Constructor(player['display_name'],
                            player['season_score'],
                            player['price'],
                            player['streak_events_progress']['top_ten_in_a_row_qualifying_progress'],
                            player['streak_events_progress']['top_ten_in_a_row_race_progress']))

    driver_combinations = list(combinations(drivers, 5))
    driver_constructors = list(product(driver_combinations, constructors))

    df = pd.DataFrame(driver_constructors)
    df[['d1', 'd2', 'd3', 'd4', 'd5']] = pd.DataFrame(
        df[0].tolist(), index=df.index)

    # print(df)
    df.columns = ['All Drivers', 'Constructer', 'Driver 1',
                  'Driver 2', 'Driver 3', 'Driver 4', 'Driver 5']
    df = df.drop(columns=['All Drivers'])

    # print(df)

    costList = []
    pointsList = []
    ppmList = []
    streak_points = []
    turbo_driver = []
    turbo_points = []
    number_races_past = len(players[0]['season_prices'])

    # print(number_races_past)

    for index, row in df.iterrows():

        sumPoints = 0
        sumCost = 0
        streaks = 0
        bestTurbo = 0
        bestTurboName = ''

        for ind, column in enumerate(row):
            sumPoints += column.points
            sumCost += column.price
            #res = column.streak_race
            if ind == 0:
                if column.streak_quali == '2':
                    streaks += 5
                if column.streak_race == '2':
                    streaks += 10
            else:
                if column.streak_quali == '4':
                    streaks += 5
                if column.streak_race == '4':
                    streaks += 10
            if float(column.price) <= 20 and column.points > bestTurbo and ind != 0:
                bestTurbo = column.points
                bestTurboName = column.name

        costList.append(sumCost)
        pointsList.append(sumPoints)
        ppmList.append(sumPoints/sumCost)
        streak_points.append(streaks)
        turbo_driver.append(bestTurboName)
        turbo_points.append(bestTurbo)

    df["Turbo Driver"] = turbo_driver
    df["Turbo Points"] = turbo_points
    df["Turbo Points"] = df["Turbo Points"] / number_races_past
    df["Cost"] = costList
    df["Points"] = pointsList
    df["PPM"] = ppmList
    df["Streak Points"] = streak_points
    df["Predicted Points"] = df["Streak Points"] + \
        df["Points"] / number_races_past + df["Turbo Points"]

    # print(df)

    df = df.sort_values('Predicted Points', ascending=False)
    df = df.drop(df[df["Cost"] > combined_cost_limit].index)

    # print(df.head())
    return df
