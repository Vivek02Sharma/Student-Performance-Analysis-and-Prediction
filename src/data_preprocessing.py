import pandas as pd
from src.logger import logging

def adding_grace(row):
    try:
        if row is None or str(row).strip() == "":
            return None
        if '*' in str(row):
            num = str(row).split('*')
            return int(num[0]) + int(num[1])
        else:
            return int(row)
    except ValueError:
        return None

    
# converting the data type of the column which contain grace('*') marks
def apply_grace_marks(df,categorical_columns):
    columns_with_grace = [col for col in categorical_columns if col.startswith(('INT_', 'EXT_'))]
    for col in columns_with_grace:
        df[col] = df[col].astype(str).apply(adding_grace)
    return df


def clean_data():
    try:
        logging.info("Starting data cleaning process.")
        df = pd.read_csv('data/raw/BMS_raw.csv')
        df = df.dropna(how = "all")
        df = df.drop(['CourseName','ExamRollNumber','StudentName'],axis = 1)
        df = df.drop_duplicates()

        # checking the datatypes of the dataset
        categorical_columns = []
        numerical_columns = []
        for column in df.columns:
            if df[column].dtypes == 'O':
                categorical_columns.append(column)
            else:
                numerical_columns.append(column)


        df = apply_grace_marks(df,categorical_columns)
        df.to_csv('data/processed/BMS_process.csv', index = False,header = True)
        logging.info("Data cleaning is done.")
    except Exception as e:
        logging.error(f"An error occurred during the data cleaning process: {e}\n")
        return None
    