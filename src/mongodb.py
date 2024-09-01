from pymongo import MongoClient
import pandas as pd

def get_data_from_mongodb(collection_name):
    client = MongoClient("mongodb://localhost:27017/")
    mydb = client['student_db']
    collection = mydb[collection_name]
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))

    # removing the '_id' column
    if '_id' in df.columns:
        df.drop('_id', axis=1, inplace=True)
        df.to_csv('data/raw/BMS_raw.csv', index=False)
    

