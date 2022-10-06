# Disaster-Response-ble
Analyze disaster data provided by Appen
Provide a model that classifies master disaster messages for use by multiple parties involved with a Disaster

## Installation
Python:
        sys
        json
        string
        plotly
        pandas
        numpy
        joblib
        stats
        nltk
        flask
        plotly.graph_objs plotly.express
        sqlalchemy sqlite3
        sklearn
        pickle


## Project motivation

Natural disasters typically result in an overload of messages through different channels
Each of the different disaster relief agencies are typically only in need of a subset of these messages.
Processing non-relevant messages is a waste of time for these teams.

Large datasets have collected for prior disasters (through social media or sent directly) and have been categorized which enables the set-up of supervised ML models which auto-categorizes similar types of messages.
This approach will have the benefit of expediting the distrubtion of relevant information.

1. What are the messages that contain relevant indicators of events for the each of disaster relief agencies?
2. Categorize the messages so that these can be sent to the appropriate disaster relief agencies
3. Visualize the available event data to enable further analysis

## File Descriptions
Code:
- load, clean data and store in db: data\ETL Pipeline Preparation.ipynb, data\process_data.py 
- create ML model: models\ML Pipeline Preparation.ipynb, model\train_classifier.py
- show data locally: app\run.py (using templates: app\templates)
- show data in Heroku: app.py (using templates: .\templates)

Input:
- disaster_messages.csv: Messages
- disaster_categories.csv: Categories (determined manually, serves as input to the supervised model)

Output:
- DisasterResponse.db: SQLight database with cleaned message and categorization data
- Results of test sets
- classifier.pkl: Final model as a pickle file (e.g.: for use by Web page that can auto-categorize)
- website https://disaster-response-ble.herokuapp.com/ (Excludes the "Classify Message" functionality due to Heroku limitations)

## Technical details
- Step 1: Run ETL pipeline that processes the messages and their corresponding categories and store these in a SQLight database
- Step 2: Run Supervised ML model with Multi-output
- Step 3: Display relevant statistics + interactive use of ML classifier through local Web Application (Flask)
- Step 4: Display relevant statistics through Web Application (Flask) hosted on Heroku server

## Instructions:
1. To run ETL pipeline that cleans data and stores in database.
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
2. To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`
3. To run web app: 
        `cd app`
        `python run.py`
        open homepage on http://127.0.0.1:3000
4. To depict in Heroku: 
        Deployed by connecting through GitHub 
        Procfile contains reference to app.py which is at the top level folder:  "web: gunicorn app:app"
        result in https://disaster-response-ble.herokuapp.com/

## Remarks
The first chart is a correlation matrix which depicts the correspondence between categories ('child_alone' shows a white vertical and horizontal bar)
The last chart shows the number of occurences in the training set ordered by volume.
1. The child_alone category has no occurences (has been excluded from the ML model to avoid modelling failures)
2. The categories offer, shops, tools, hospitals and missing_people have less than 300 occurences which limits the robustness of the ML model

Categories_occurences_trainingset.png
![Category_occurences](https://github.com/BartLeplae/Disaster-Response-ble/blob/main/Categories_occurences_trainingset.png)

## Licensing, Authors, Acknowledgements
- Author:Bart Leplae
- Acknowledgement: Made use of Udacity course materials
