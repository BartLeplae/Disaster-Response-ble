# Disaster-Response-ble
Analyze disaster data from Appen
Provide a model that classifies master disaster messages for use by multiple parties involved with the Disaster

## Installation
Python:
...


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
- IncidentTicketAnalysis.ipynb (Jupyter notebook / Python code)

Input:
- disaster_messages.csv: Messages
- disaster_categories.csv: Categories (determined manually as input to the supervised model)

Output:
- DisasterResponse.db: SQLight database with cleaned message and categorization data
- Results of test sets
- classifier.pkl: Final model as a pickle file (e.g.: for use by Web page that can auto-categorize)

## Technical details
- Step 1: Run ETL pipeline that processes the messages and their corresponding categories and store these in a SQLight database
- Step 2: Run Supervised ML model with Multi-output
- Step 3: Display relevant statistics through Web Application (Flask)

## Instructions:
1. To run ETL pipeline that cleans data and stores in database.
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
2. To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`
3. To run web app: 
        `cd app`
        `python run.py`
        Click the `PREVIEW` button to open the homepage

## Licensing, Authors, Acknowledgements
- Author:Bart Leplae
- Acknowledgement: Made use of Udacity course materials

