


class Driver:
    '''A class for a Formula One driver'''
    def __init__(self, id, name, points, price, streak_quali, streak_race, imageUrl, teamName, wins, podiums, price_change, birthPlace, poles, fastestLaps, bestFinish, bestFinishCount):
        self.id = id
        self.name = name
        self.price = price
        self.points = points
        self.streak_quali = streak_quali
        self.streak_race = streak_race
        self.odds_value = 0
        self.odds = 'N/A'
        self.upcoming_odds = 'N/A'
        self.odds_rank = 0
        self.odds_value = 0
        self.upcoming_odds_rank = 0
        self.upcoming_odds_value = 0
        self.price_rank = 0
        self.avg_points = 0
        self.avg_points_rank = 0
        self.imageUrl = imageUrl
        self.team_name = teamName
        self.wins = wins
        self.podiums = podiums
        self.price_change_data = price_change
        self.place_of_birth = birthPlace
        self.poles = poles
        self.fastest_laps = fastestLaps
        self.best_finish = bestFinish
        self.best_finish_count = bestFinishCount
        

        
    def __str__(self):
        return self.name
