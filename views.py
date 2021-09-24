from flask import Blueprint, render_template, request
import pandas as pd
import numpy as np
from data import get_f1_data

views = Blueprint(__name__,"views")


@views.route("/")
def home():
    x = pd.DataFrame()
    return render_template("index.html", name="Fantasy F1 Best Teams", data=x.to_html(classes='minimalistBlack'))

@views.route("/about/")
def about():
    x = pd.DataFrame()
    return render_template("about.html", name="About")

@views.route('/analysis/', methods=['GET','POST'])
def analysis():
    try:
        cost = request.form['budget']
        df = get_f1_data(float(cost)).reset_index(drop=True)
        df.index += 1 
        x = df.head(30).round(2)
        # x = pd.DataFrame(np.random.randn(20, 5))
    except:
        x = pd.DataFrame()
        
    return render_template("index.html", name="Fantasy F1 Best Teams", data=x.to_html(classes='minimalistBlack'))