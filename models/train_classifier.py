""" train_classifier

    Machine Learning Pipeline:
    - Split the data into a training set and a test set. 
    - Machine learning pipeline uses NLTK, as well as scikit-learn's Pipeline and GridSearchCV
    - Final model that uses the message column to predict classifications for 36 categories (multi-output classification). 

    to run: python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl

Attributes:
    name of database that includes messages + categories
    name of model file (pickle format) to be created

Input:
    DisasterResponse.db (cleaned and merged messages + categories stored in SQLite database)

Output:   
    Model exported to a pickle file.
"""

# import libraries
import sys
import pandas as pd
import numpy as np
import nltk
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from sqlalchemy import create_engine
from nltk.stem import WordNetLemmatizer
import sqlite3
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.multioutput import MultiOutputClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import QuantileTransformer
import pickle

def load_data(database_filepath):
    # load data from database: all records from DisasterMessages table to df DataFrame
    database_url = "sqlite:///"+database_filepath
    engine = create_engine(database_url)
    connection = engine.connect()
    query = "SELECT * FROM DisasterMessages"
    df = pd.read_sql(query, connection)
    connection.close()

    # Load X: "message" field + calculated fields "message_length", "question_mark" and "exclamation mark"
    qt = QuantileTransformer(n_quantiles=10, random_state=0)
    df["message_length"] = df["message"].str.len()
    df["len"] = qt.fit_transform(df[["message_length"]])
    df["question_mark"] = 0
    df["exclamation_mark"] = 0
    df.loc[df['message'].str.contains('\?'),"question_mark"] = 1
    df.loc[df['message'].str.contains('\!'),"exclamation_mark"] = 1
    X = df[["message","genre","len","question_mark","exclamation_mark"]]

    # Load Y: 36 category columns mu
    N_CATEGORIES = 36 #number of category columns
    df_y = df.iloc[:,-N_CATEGORIES-4:-4]
    df_y_sufficient_data =  df_y.loc[:,(df_y.sum(axis=0) > 50)] #only retain those columns that have more than 50 positive values
    Y = df_y_sufficient_data.values
    N_CATEGORIES = df_y_sufficient_data.shape[1]

    category_names = df_y_sufficient_data.columns.tolist()
    
    return(X, Y, category_names)

def tokenize(text):
    # Bring to lowercase, remove stopwords and punctuation
    stop = set(stopwords.words('english') + list(string.punctuation))
    nltk_tokens = nltk.word_tokenize(text.lower())
    tokens = [w for w in nltk_tokens if not w in stop]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    return(tokens)

def build_model():
    # Define the model:
    # Input: "Message", "Genre", "message_length" (quantile transformed), "question_mark", "exclamation_mark"
    # - apply tfidf to 'message'
    # - apply onehot encoding for 'genre'
    # Apply Logistic Regression against each of the categories
 
    tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize, strip_accents="unicode", sublinear_tf=True)
    onehot = OneHotEncoder(drop="first")
    clmn = ColumnTransformer([("tfidf", tfidf_vectorizer, "message"),("onehot", onehot, ["genre"])], remainder="passthrough")
    mo = MultiOutputClassifier(LogisticRegression(solver="liblinear"))
    pipeline = Pipeline([('clmn', clmn), ('mo', mo)])

   # Apply GridSearchCV to identify the optimal:
   # - minimum of word occurences (for TFIDF)
   # - Inverse of regularization strength (smaller value = stronger regularization)
    parameters = [{
        'clmn__tfidf__min_df': [25,50],
        'mo__estimator__C': [5,1,0.5]
    }]
    cv = model_selection.GridSearchCV(pipeline, parameters)

    return(cv)


def evaluate_model(model, X_test, Y_test, category_names):
    # test the model against the test set
    Y_pred = model.predict(X_test)

    # list the parameters provided to GridSearchCV for optimization
    best_parameters = model.best_estimator_.get_params()
    for param_name in sorted(best_parameters.keys()):
        if param_name in ('clmn__tfidf__min_df','mo__estimator__C'):
            print("\t%s: %r" % (param_name, best_parameters[param_name]))

    # print the result for every of the categories + the total based on the weighted average
    classification_result_cv = list()
    i = 0
    for category in category_names:
        weighted_avg = classification_report(Y_test[:,i], Y_pred[:,i],zero_division=1,output_dict=True)['weighted avg']
        classification_result_cv.append(weighted_avg)
        print(category,weighted_avg)
        i += 1

    df_result_cv = pd.DataFrame(classification_result_cv)
    print(df_result_cv.describe())
    return


def save_model(model, model_filepath):
    pickle.dump(model, open(model_filepath, 'wb'))
    return


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()