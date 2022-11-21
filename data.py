import requests
from driver import Driver
from constructor import Constructor
from bet import Bet
from news import Article
from itertools import combinations, product
import pandas as pd
from encryption import decode
import json
import re


def get_drivers_and_consturctors():
    '''Function to get all of the driver and constructor data from the
    F1 Fantasy Game API, and decode the values'''

    # Define the API endpoint of the F1 Fantasy Game
    URL = 'https://fantasy-api.formula1.com/f1/2022/players'

    try:
        # Get the json information from the API
        result = requests.get(url=URL)

        data = result.json()
        players = data['players']
        players_updated = []

        # Remove players which have not yet been confirmed
        # This often happens at the beginning of the season when 
        # contracts have not yet been signed
        for player in players:
            if player["last_name"] != "TBC":
                players_updated.append(player)

        # Lets define some variables that will hold our data
        players = players_updated
        drivers, constructors, = [], []
        
        # Loop through the json data, decode values which need to be decoded
        # and then append the result to drivers or constructors depending on 
        # the type of "player" 
        [(drivers.append(
                    Driver(player['id'],
                        player['first_name'] + " " + player['last_name'],
                        float(decode(player['season_score'])),
                        float(decode(player['price'])),
                        int(json.loads(decode(player['streak_events_progress']))['top_ten_in_a_row_qualifying_progress']),
                        int(json.loads(decode(player['streak_events_progress']))['top_ten_in_a_row_race_progress']),
                        player['profile_image']['url'],
                        player['team_abbreviation'],
                        player['driver_data']['wins'],
                        player['driver_data']['podiums'],
                        json.loads(decode(player['season_prices'])),
                        player['driver_data']['place_of_birth'],
                        player['driver_data']['poles'],
                        player['driver_data']['fastest_laps'],
                        player['driver_data']['best_finish'],
                        player['driver_data']['best_finish_count'],
                        
                        )) if player['position_abbreviation'] == "DR" else constructors.append(
                    Constructor(player['id'],
                                player['first_name'],
                                 float(decode(player['season_score'])),
                                 float(decode(player['price'])),
                                 int(json.loads(decode(player['streak_events_progress']))['top_ten_in_a_row_qualifying_progress']),
                                 int(json.loads(decode(player['streak_events_progress']))['top_ten_in_a_row_race_progress']),
                                ))) for player in players]
        

        # Lets put in a fail safe for the beginning of the season where
        # the number of races that have past must be 1 so that we do not 
        # divide by 0 
        if drivers[0].price_change_data == None:
            print("Beginning of the season")
            number_races = 1
        else:
            number_races = len(drivers[0].price_change_data)

    # If the above process fails, print the error and return empty values
    # so that the website can at least render 
    except Exception as e:
        print("Failed")
        print(e)
        drivers = []
        constructors = []
        number_races = 0

    # Return the results
    return [drivers, constructors, number_races]



def get_betting_data():
    '''Function to get the betting data from our API'''

    # Define our endpoint 
    URL = "https://formulaoneapi.herokuapp.com/bets"

    result = requests.get(url=URL)

    data = result.json()
    drivers = data['drivers_championship']
    constructors = data['constructors_championship']
    upcoming_gp_drivers = data['upcoming_grand_prix_drivers']['driver_odds']
    upcoming_gp_name = data['upcoming_grand_prix_drivers']['name']

    driver_bet, constructor_bets, upcoming_driver_bet = [], [], []

    for driver in drivers:
        try:
            driver_bet.append(Bet(driver['name'],driver['odds']))
        except:
            print("Something else went wrong with driver championship bets")
            continue

    for constructor in constructors:
        try:
            constructor_bets.append(Bet(constructor['name'],constructor['odds']))
        except:
            print("Something else went wrong with constructor bets")
            continue

    for driver in upcoming_gp_drivers:
        try:
            upcoming_driver_bet.append(Bet(driver['name'],driver['odds']))
        except:
            print("Something else went wrong with upcoming driver bets")
            continue

    return [driver_bet, constructor_bets, upcoming_driver_bet, upcoming_gp_name]

def get_news():
    '''Function to get the news data from our API'''
    # Define our API endpoint for news
    URL = "https://formulaoneapi.herokuapp.com/news"
    result = requests.get(url=URL)

    data = result.json()
    articles = []
    [(articles.append(Article(article['title'],article['url'],article['source']))) for article in data]

    return articles

def get_f1_data(combined_cost_limit, selected_drivers, selected_constructors, include_streak):

    drivers, constructors, costList, pointsList, ppmList, streak_points, turbo_driver, turbo_points = [], [], [], [], [], [], [], []

    [all_drivers, all_constructors, number_races_past] = get_drivers_and_consturctors()

    [drivers.append(d) if int(d.id) in selected_drivers else [] for d in all_drivers]
    [constructors.append(c) if int(c.id) in selected_constructors else [] for c in all_constructors]
    

    driver_combinations = list(combinations(drivers, 5))
    driver_constructors = list(product(driver_combinations, constructors))

    df = pd.DataFrame(driver_constructors)
    df[['d1', 'd2', 'd3', 'd4', 'd5']] = pd.DataFrame(
        df[0].tolist(), index=df.index)

    df.columns = ['All Drivers', 'Constructer', 'Driver 1',
                  'Driver 2', 'Driver 3', 'Driver 4', 'Driver 5']
    df = df.drop(columns=['All Drivers'])

    for index, row in df.iterrows():

        sumPoints, sumCost, streaks, bestTurbo = 0, 0, 0, 0
        bestTurboName = ''

        for ind, column in enumerate(row):
            sumPoints += column.points
            sumCost += column.price

            if ind == 0:
                if column.streak_quali == 2:
                    streaks += 5
                if column.streak_race == 2:
                    streaks += 10
            else:
                if column.streak_quali == 4:
                    streaks += 5
                if column.streak_race == 4:
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
    if include_streak:
        df["Streak Points"] = streak_points
        df["Predicted Points"] = df["Streak Points"] + \
            df["Points"] / number_races_past + df["Turbo Points"]
    else:
        df["Predicted Points"] = df["Points"] / number_races_past + df["Turbo Points"]

    df = df.sort_values('Predicted Points', ascending=False)
    df = df.drop(df[df["Cost"] > combined_cost_limit].index)

    return [df, drivers, constructors]
