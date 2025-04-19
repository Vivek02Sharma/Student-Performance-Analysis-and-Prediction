from pymongo import MongoClient
import pandas as pd
from src.logger import logging
import os

def get_data_from_mongodb(collection_name):
    try:
        # logging.info("Retrieving the dataset...")
        client = MongoClient("mongodb://localhost:27017/")
        mydb = client['student_db']
        collection = mydb[collection_name]
        cursor = collection.find()
        df = pd.DataFrame(list(cursor))

        # removing the '_id' column
        if '_id' in df.columns:
            df = df.drop('_id', axis = 1)

        os.makedirs('data/raw', exist_ok = True)
        df.to_csv('data/raw/BMS_raw.csv', index = False,header = True)
        logging.info(f"Data successfully retrieved from collection: {collection_name} and saved to 'data/raw/BMS_raw.csv'.")

    except  Exception as e:
        logging.error(f"An error occurred while retrieving data from MongoDB: {e}")
        return None

def student_data(student_id):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["student_db"]
    sem1_collection = db["sem1"]
    sem2_collection = db["sem2"]

    try:
        student_id = int(student_id)
    except ValueError:
        print(f"ERROR: Invalid student_id: {student_id}")
        return None, None

    sem1_data = sem1_collection.find_one({"StudentId": student_id})
    sem2_data = sem2_collection.find_one({"StudentId": student_id})
    return sem1_data, sem2_data