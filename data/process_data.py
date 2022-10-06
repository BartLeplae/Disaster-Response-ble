""" Process_data:

    Extract, Transform, and Load process. 
    Reads the datasets, cleans the data, and then stores it in a SQLite database. 

    to run: python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db

Attributes:
    message file, categories file, name of database to be created

Input:
    disaster_messages.csv (individual text messages)
    disaster_categries.csv (corresponding categories)
    
Output:
    DisasterResponse.db (cleaned and merged result stored in SQLite database)
"""

# import libraries
import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

#%%

def load_data(messages_filepath, categories_filepath):
    """ 
    load messages and category datasets and merge them on ID, removes the original language (keep English onl)
    input: location of both CV files
    output: dataframe with merged data
    """ 
    # Load messages and drop the original language column
    messages = pd.read_csv(messages_filepath)
    messages.drop(columns = "original", inplace=True) # Don't need the original language
    messages.drop_duplicates(subset="id", inplace=True)
    
    # Load categories and construct meaningful column names (based on the first row)
    categories = pd.read_csv(categories_filepath)
    categories.drop_duplicates(subset="id", inplace=True)

    # Merge messages and categories based on id
    df = pd.merge(messages, categories, on="id", how="inner") 
    return (df)


def clean_data(df):
    """ 
    Remove duplicate rows
    input: dataframe
    output: dataframe
    """ 
    
    categories = df['categories'].str.split(';', expand=True)
    firstrow = categories.head(1).values[0] #retain the first row of the categories to construct column names
    
    def strip_last_2(s):
        return s[:-2]

    category_colnames = np.array(list(map(strip_last_2, firstrow)))
    categories.columns = category_colnames

    categories['related'] = categories['related'].astype('str').str.replace('2', '1') # combine 2 with 1 to ensure binary categorization

    # set each category value to be the last character of the string
    for column in categories:
        categories[column] = categories[column].str[-1]
    
        # convert column from string to numeric
        categories[column] = categories[column].astype(int)
    
    # drop original column "categories" as now split
    df.drop(columns="categories", inplace=True)

    # Concatenate the split categories with the original dataframe, remove na's, make integer and drop duplicates
    df = pd.concat([df, categories], axis=1)
    df = df.dropna()
    df = df.convert_dtypes()
    df = df.drop_duplicates()

    return(df)


def save_data(df, database_filename):
    """ 
    saves dataframe to specified SQLite database (table: DisasterMessages)
    input: dataframe
    output: none
    """ 
    engine = create_engine('sqlite:///'+database_filename)
    df.to_sql('DisasterMessages', engine, index=False, if_exists='replace')
    return


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()