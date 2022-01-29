

class Constructor:
    def __init__(self, id, name, points, price, streak_quali, streak_race):
        self.id = id
        self.name = name
        self.price = price
        self.points = points
        self.streak_quali = streak_quali
        self.streak_race = streak_race
        self.odds_value = 0
        self.odds = 'N/A'
        self.odds_rank = 0
        self.price_rank = 0
        self.avg_points = 0
        self.avg_points_rank = 0

    def __str__(self):
        return self.name
