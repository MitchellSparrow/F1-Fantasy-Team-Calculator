from distutils.log import debug
from os import name
from re import T
from flask import Flask, render_template,request, send_from_directory
import pandas as pd
from data import get_betting_data, get_f1_data, get_drivers_and_consturctors, get_news
from difflib import SequenceMatcher

app = Flask(__name__, static_folder='static', static_url_path='')

SEASON_END = False
FIRST_RACE = False

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@app.route("/")
def home():
    if SEASON_END:
        return render_template("season_end.html", name="Fantasy Analysis Coming Soon!")
    return render_template("home.html", name="Fantasy F1 Analysis Home")

@app.route("/team_suggestions/")
def fantasy_suggestions():
    if SEASON_END:
        return render_template("season_end.html", name="Fantasy Analysis Coming Soon!")
    elif FIRST_RACE:
        return render_template("fantasy_suggestions_beg.html", name="Fantasy F1 Team Suggestions")

    res = get_drivers_and_consturctors()
    drivers = res[0]
    constructors = res[1]
    x = pd.DataFrame()
    return render_template("fantasy_suggestions.html", name="Fantasy F1 Team Suggestions", driver_list = [ob.__dict__ for ob in drivers], constructor_list = [ob.__dict__ for ob in constructors], data=x.to_html(classes='minimalistBlack'))

@app.route("/about/")
def about():
    if SEASON_END:
        return render_template("season_end.html", name="Fantasy Analysis Coming Soon!")
    return render_template("about.html", name="About")

@app.route("/contact/")
def contact():
    if SEASON_END:
        return render_template("season_end.html", name="Fantasy Analysis Coming Soon!")
    return render_template("contact.html", name="Contact")

@app.route("/explain/")
def explain():
    if SEASON_END:
        return render_template("season_end.html", name="Fantasy Analysis Coming Soon!")
    return render_template("explain.html", name="Explain")

@app.route("/news/")
def news():
    if SEASON_END:
        return render_template("season_end.html", name="Fantasy Analysis Coming Soon!")
    articles = get_news()
    return render_template("news.html", name="News", article_list = [ob.__dict__ for ob in articles])

@app.route("/bets/")
def bets():
    if SEASON_END:
        return render_template("season_end.html", name="Fantasy Analysis Coming Soon!")
    res = get_drivers_and_consturctors()
    bet_data = get_betting_data()
    drivers_bets = bet_data[0]
    constructors_bets = bet_data[1]
    upcoming_gp_drivers = bet_data[2]
    upcoming_gp_name = bet_data[3]
    drivers = res[0]
    constructors = res[1]

    for driver_bets in drivers_bets:
        for driver in drivers:
            if similar(driver.name,driver_bets.name) > 0.5:
                #print(similar(driver.name,driver_bets.name))
                driver.odds = driver_bets.odds
                odds_values = driver.odds.split('/')
                driver.odds_numerator = int(odds_values[0])
                driver.odds_denominator = int(odds_values[1])
                driver.odds_value = int(odds_values[0]) / int(odds_values[1])
            driver.avg_points = round(driver.points / res[2], 1)

    for driver_bets_upcoming in upcoming_gp_drivers:
        for driver in drivers:
            if similar(driver.name,driver_bets_upcoming.name) > 0.5:
            
                driver.upcoming_odds = driver_bets_upcoming.odds
                odds_values = driver.upcoming_odds.split('/')
                driver.upcoming_odds_numerator = int(odds_values[0])
                driver.upcoming_odds_denominator = int(odds_values[1])
                driver.upcoming_odds_value = int(odds_values[0]) / int(odds_values[1])
        

    upcoming_drivers = drivers

    for driver in upcoming_drivers:
        if driver.upcoming_odds == 'N/A':
            upcoming_drivers.remove(driver)

    upcoming_drivers = sorted(upcoming_drivers, key=lambda x: x.price, reverse=True)
    for i in range(len(upcoming_drivers)):
        upcoming_drivers[i].price_rank = i + 1
    
    upcoming_drivers = sorted(upcoming_drivers, key=lambda x: x.avg_points, reverse=True)
    for i in range(len(upcoming_drivers)):
        upcoming_drivers[i].avg_points_rank = i + 1

    upcoming_drivers = sorted(upcoming_drivers, key=lambda x: x.upcoming_odds_value, reverse=False)
    for i in range(len(upcoming_drivers)):
        upcoming_drivers[i].upcoming_odds_rank = i + 1

    for driver in drivers:
        if driver.odds == 'N/A':
            drivers.remove(driver)

    drivers = sorted(drivers, key=lambda x: x.price, reverse=True)
    for i in range(len(drivers)):
        drivers[i].price_rank = i + 1
    
    drivers = sorted(drivers, key=lambda x: x.avg_points, reverse=True)
    for i in range(len(drivers)):
        drivers[i].avg_points_rank = i + 1

    drivers = sorted(drivers, key=lambda x: x.odds_value, reverse=False)
    for i in range(len(drivers)):
        drivers[i].odds_rank = i + 1

    for constructor_bets in constructors_bets:
        for constructor in constructors:
            if constructor.name in constructor_bets.name:
                constructor.odds = constructor_bets.odds
                odds_values = constructor.odds.split('/')
                constructor.odds_numerator = int(odds_values[0])
                constructor.odds_denominator = int(odds_values[1])
                constructor.odds_value = int(odds_values[0]) / int(odds_values[1])
            constructor.avg_points = round(constructor.points / res[2], 1)

    for constructor in constructors:
        if constructor.odds == 'N/A':
            constructors.remove(constructor)

    constructors = sorted(constructors, key=lambda x: x.price, reverse=True)
    for i in range(len(constructors)):
        constructors[i].price_rank = i + 1
    
    constructors = sorted(constructors, key=lambda x: x.avg_points, reverse=True)
    for i in range(len(constructors)):
        constructors[i].avg_points_rank = i + 1

    constructors = sorted(constructors, key=lambda x: x.odds_value, reverse=False)
    for i in range(len(constructors)):
        constructors[i].odds_rank = i + 1

    x = pd.DataFrame()
    return render_template("bets.html", name="Bets", driver_list = [ob.__dict__ for ob in drivers], upcoming_driver_list = [ob.__dict__ for ob in upcoming_drivers], constructor_list = [ob.__dict__ for ob in constructors], gp_name = upcoming_gp_name, data=x.to_html(classes='minimalistBlack'))

@app.route("/thanks/")
def thanks():
    if SEASON_END:
        return render_template("season_end.html", name="Fantasy Analysis Coming Soon!")
    return render_template("thanks.html", name="Thanks")

@app.route('/team_suggestions/analysis/', methods=['GET','POST'])
def analysis():
    if SEASON_END:
        return render_template("season_end.html", name="Fantasy Analysis Coming Soon!")

    res = get_drivers_and_consturctors()
    drivers = res[0]
    constructors = res[1]

    try:
        if request.method == "POST":
            try:
                streaks = request.form['streaks']
            except:
                streaks = False

            selected_drivers = list(map(int,request.form.getlist("selected_drivers")))
            selected_constructors = list(map(int,request.form.getlist("selected_constructors")))

            if not (len(selected_constructors) < 1 or len(selected_drivers) < 5):
                cost = request.form['budget']
                res = get_f1_data(float(cost), selected_drivers, selected_constructors, streaks)
                df = res[0].reset_index(drop=True)
                df.index += 1 
                x = df.head(30).round(2)
            else:
                x = pd.DataFrame()
        
        else:
            x = pd.DataFrame()

    except:
        x = pd.DataFrame()
        
    return render_template("fantasy_suggestions.html", name="Fantasy F1 Best Teams", driver_list = [ob.__dict__ for ob in drivers], constructor_list = [ob.__dict__ for ob in constructors], data=x.to_html(classes='minimalistBlack'))


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=False)


