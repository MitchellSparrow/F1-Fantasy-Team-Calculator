

class Driver:

    def __init__(self, name, points, price, streak_quali, streak_race):
        self.name = name
        self.price = price
        self.points = points
        self.streak_quali = streak_quali
        self.streak_race = streak_race

    def __str__(self):
        return self.name
