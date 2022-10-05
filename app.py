
import json, plotly
from flask import Flask, render_template
from wrangle_data import return_figures
import pandas as pd
import joblib
import plotly.express as px
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = "whatever_blabla"

# load message training data
engine = create_engine('sqlite:///./data/DisasterResponse.db')
df = pd.read_sql_table('DisasterMessages', engine)
df["message_length"] = df["message"].str.len()

@app.route('/')
@app.route('/index')
def index():

    figures = return_figures()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)