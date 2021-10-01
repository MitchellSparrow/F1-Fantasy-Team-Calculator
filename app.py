from flask import Flask, render_template,request, send_from_directory
import pandas as pd
from data import get_f1_data, get_drivers_and_consturctors

app = Flask(__name__, static_folder='static', static_url_path='')


@app.route("/")
def home():
    res = get_drivers_and_consturctors()
    drivers = res[0]
    constructors = res[1]
    x = pd.DataFrame()
    return render_template("index.html", name="Fantasy F1 Best Teams", driver_list = [ob.__dict__ for ob in drivers], constructor_list = [ob.__dict__ for ob in constructors], data=x.to_html(classes='minimalistBlack'))

@app.route("/about/")
def about():
    x = pd.DataFrame()
    return render_template("about.html", name="About")

@app.route('/analysis/', methods=['GET','POST'])
def analysis():
    res = get_drivers_and_consturctors()
    drivers = res[0]
    constructors = res[1]

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
        
    return render_template("index.html", name="Fantasy F1 Best Teams", driver_list = [ob.__dict__ for ob in drivers], constructor_list = [ob.__dict__ for ob in constructors], data=x.to_html(classes='minimalistBlack'))


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == '__main__':
    app.run()


