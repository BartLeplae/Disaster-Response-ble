""" run:

    Creates webpage with:
    - functionality to classify messages
    - Overview of training dataset by means of various plots 
    
    to run: python run.py

Attributes:
    None

Input:
    Training Data with messages and classification: 
        database: "../data/DisasterResponse.db": 
        table: "DisasterMessages"
    ML model to classify messages into different categories: ../models/DisasterResponse.pkl
    
Output:
    Webpage: http://127.0.0.1:3000/
"""

#%%
import json
import plotly
import pandas as pd
import joblib
import string
import nltk
# from scipy import stats - Remove as not running on Heroku

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
import plotly.express as px
from sqlalchemy import create_engine
#%%

# Initiate Flask application
app = Flask(__name__)
app.secret_key = "whatever_blabla"


def tokenize(text):
    """ tokenize, convert text to lowercase, remove stopwords and punctuation and lemmatize
    Input: text string
    Returns: list of tokens
    """
    stop = set(stopwords.words('english') + list(string.punctuation))
    nltk_tokens = nltk.word_tokenize(text.lower())
    tokens = [w for w in nltk_tokens if not w in stop]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    return(tokens)

# load message training data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('DisasterMessages', engine)
df["message_length"] = df["message"].str.len()

# load trained model
model = joblib.load("../models/DisasterResponse.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    # Create 6 graphs
    graphs = [None]*7

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

    # Graph 7: Bargraph to depict the number of category occurences in the database
    df_categories = df
    df_categories = df_categories.drop(columns=["id","message","genre","message_length"])
    df_categories = df_categories.sum()
    df_categories = df_categories.reset_index()
    df_categories.columns=(["Category","Count"])
    df_categories = df_categories.sort_values(by="Count",ascending=False)
    graphs[6] = px.bar(df_categories,x="Category",y="Count",title="Number of category occurences in training set")

    # encode plotly graphs in JSON
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 
    # Transform the message length
    # mess_length = stats.percentileofscore(df["message_length"],len(query))  Remove as not running on Heroku
    mess_length = 0.2 # Replace with constant (short sentence)
    # Check for availability of Question and Exclamation mark
    if '\?' in query:
        question_mark = 1
    else:
        question_mark = 0

    if '\!' in query:
        exclamation_mark = 1
    else:
        exclamation_mark = 0 

    # Create dataframe to serve as input to the ML model
    X_query = pd.DataFrame(data = [[query,"direct",mess_length,question_mark,exclamation_mark]], columns=["message","genre","len","question_mark","exclamation_mark"])

    # use model to predict classification for query
    classification_labels = model.predict(X_query)[0]
    # classification_labels = model.predict(query)
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3000, debug=True)


if __name__ == '__main__':
    main()
# %%
