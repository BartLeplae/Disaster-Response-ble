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

#%%
# load messages dataset
def load_data(messages_filepath, categories_filepath):
    # messages = 
    # messages.head()
    pass


def clean_data(df):
    pass


def save_data(df, database_filename):
    pass  


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