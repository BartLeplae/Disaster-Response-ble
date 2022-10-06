""" app:

    Creates webpage with:
    - Overview of training dataset by means of various plots 
    
    to enable deployment and run in Heroku: 
        Procfile "web: gunicorn app:app"

Attributes:
    None

Input:
    Training Data with messages and classification: 
        database: "../data/DisasterResponse.db": 
        table: "DisasterMessages"
    
Output:
    Webpage: https://disaster-response-ble.herokuapp.com/
"""
import json, plotly
from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize

app = Flask(__name__)
app.secret_key = "whatever_blabla"

# load message training data
engine = create_engine('sqlite:///./data/DisasterResponse.db')
df = pd.read_sql_table('DisasterMessages', engine)
df["message_length"] = df["message"].str.len()

# Create graphs to be displayed in webpage and render to 'master.html'
@app.route('/')
@app.route('/index')
def index():

    # Create 6 graphs
    graphs = [None]*6

    # Graph 1: Correlation matrix to depict relationship between message categories
    correlation_matrix = df.corr()
    graphs[0] = px.imshow(correlation_matrix)

    # Graph 2: Bargraph to depict the categories that go along with the "aid_related" category
    # The correlation matrix depicts that there are several correlations
    df_line = df[df["aid_related"]==1]
    df_line = df_line.drop(columns=["id","message","genre","aid_related","message_length"])
    df_line = df_line.sum()
    df_line = df_line.reset_index()
    df_line.columns=(["Category","Count"])
    df_line = df_line.sort_values(by="Count",ascending=False)
    graphs[1] = px.bar(df_line,x="Category",y="Count")

    # Graph 3: Bargraph depicting the number of messages per 'genre'
    df_genre_counts = df.groupby('genre', as_index=False).agg(count=('message','count'))   
    graphs[2] = px.bar(df_genre_counts, x="genre", y="count", barmode="stack",title="Aid Related correlation")

    # Graph 4: Bargraph depicting the number of messages per 'genre', differentiated by "Aid related"
    df_aid_related = df.groupby(['aid_related','genre'], as_index=False).agg(count=('message','count'))
    df_aid_related["aid"] = df_aid_related["aid_related"].map({0: "Not Aid Related", 1: "Aid Related",})
    graphs[3] = px.bar(df_aid_related, x="genre", y="count", color="aid", barmode="stack", title="#Aid related")

    # Graph 5: Bargraph depicting the ratio of "Aid related" messages per 'genre'
    df_aid_related["count2"] = df_aid_related["count"].div(df_aid_related.groupby("genre")["count"].transform("sum"))
    graphs[4] = px.bar(df_aid_related, x="genre", y="count2", color="aid", barmode="stack", title="%Aid related")
    
    # Graph 6: Boxplot depicting the length of the messages per "genre"
    df_message_len = df[["genre","message_length"]]
    graphs[5] = px.box(df_message_len, x="genre", y="message_length", log_y=True, title="message length")

    # plot ids for the html id tag
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)] 

    # Convert the plotly figures to JSON for javascript in html template
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('master.html', ids=ids, graphJSON=graphJSON)
