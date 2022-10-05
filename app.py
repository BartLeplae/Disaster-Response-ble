
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

    # Create 6 graphs
    graphs = [None]*1

    # Graph 1: Correlation matrix to depict relationship between message categories
    correlation_matrix = df.corr()
    graphs[0] = px.imshow(correlation_matrix)

    # figures = return_figures()

    # plot ids for the html id tag
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)] 

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('master.html',
                           ids=ids,
                           figuresJSON=figuresJSON)