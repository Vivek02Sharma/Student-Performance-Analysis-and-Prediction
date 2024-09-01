import pandas as pd

# this function add grace marks
def adding_grace(row):
    # if '*' present in row
    if '*' in row:
        num = row.split('*')
        return int(num[0]) + int(num[1])
    # '*' not present in row
    else:
        return int(row)
    
# converting the data type of the column which contain grace('*') marks
def apply_grace_marks(df,categorical_columns):
    columns_with_grace = []
    for col in categorical_columns:
        if col.startswith('INT_') or col.startswith('EXT_'):
            columns_with_grace.append(col)
            
    for col in columns_with_grace:
        df[col] = df[col].apply(adding_grace)
    return df


def clean_data():
    df = pd.read_csv('data/raw/BMS_raw.csv')
    df.dropna(how = "all",axis = 1,inplace = True)
    df.dropna(how = "all",inplace = True)
    df.drop_duplicates(inplace = True)
    df.drop(['CourseName','ExamRollNumber','StudentName'],inplace = True,axis = 1)

    # checking the datatypes of the dataset
    categorical_columns = []
    numerical_columns = []
    for column in df.columns:
        if df[column].dtypes == 'O':
            categorical_columns.append(column)
        else:
            numerical_columns.append(column)


    # print(f"Categorical columns : {categorical_columns}\n")
    # print(f"Numerical columns : {numerical_columns}")

    df = apply_grace_marks(df,categorical_columns)
    df.to_csv('data/processed/BMS_process.csv', index=False,header = True)
    



