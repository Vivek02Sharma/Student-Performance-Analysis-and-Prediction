import pandas as pd

sem1 = pd.read_csv('notebooks/BMS_sem1_process.csv')
sem2 = pd.read_csv('notebooks/BMS_sem1_process.csv')
merged = pd.merge(sem1, sem2, on='StudentId', suffixes=('_sem1', '_sem2'))

def feature_engineering_func():

    # 1. Total Marks per Subject in Sem1
    subjects_sem1 = ['BMSBC103', 'BMSBL107', 'BMSBS106', 'BMSECO102', 'BMSFA105', 'BMSFC104', 'BMSFHS101']
    for subj in subjects_sem1:
        merged[f'Total_{subj}_sem1'] = merged[f'INT_{subj}_sem1'] + merged[f'EXT_{subj}_sem1']

    # 2. Failure Flag for Sem1
    merged['Failed_any_sem1'] = merged['Remark_sem1'].apply(lambda x: 1 if x == 'FAIL' else 0)

    # 3. Aggregate Features
    features = [
        'SGPA_sem1', 'Percentage_sem1', 'Failed_any_sem1',
        'Total_BMSBC103_sem1', 'Total_BMSBL107_sem1', 'Total_BMSBS106_sem1',
        'Total_BMSECO102_sem1', 'Total_BMSFA105_sem1', 'Total_BMSFC104_sem1',
        'Total_BMSFHS101_sem1'
    ]

    return merged, features


def feature_engineering_func1(data=None):
    """
    Feature engineering for predicting sem2 results from sem1 data.
    Input:
        data: optional, a pandas DataFrame. If None, load full dataset from file.
    Output:
        processed_df: DataFrame with engineered features
        features: list of selected feature columns
    """
    if data is None:
        # Fallback: load pre-merged sem1-sem2 data (if used for training)
        data = pd.read_csv("data/processed/merged_data.csv")

    df = data.copy()

    # Extract only sem1 internal and external marks
    int_cols = [col for col in df.columns if col.startswith("INT_") and "_sem1" in col]
    ext_cols = [col for col in df.columns if col.startswith("EXT_") and "_sem1" in col]

    # Handle cases where input is raw sem1 (without _sem1 suffix)
    if not int_cols or not ext_cols:
        int_cols = [col for col in df.columns if col.startswith("INT_")]
        ext_cols = [col for col in df.columns if col.startswith("EXT_")]

        # Add _sem1 suffix to column names to be consistent
        df.rename(columns={col: f"{col}_sem1" for col in int_cols + ext_cols}, inplace=True)
        int_cols = [f"{col}_sem1" for col in int_cols]
        ext_cols = [f"{col}_sem1" for col in ext_cols]

    # Total internal and external per student
    df["Total_Internal_sem1"] = df[int_cols].sum(axis=1)
    df["Total_External_sem1"] = df[ext_cols].sum(axis=1)
    df["Total_Marks_sem1"] = df["Total_Internal_sem1"] + df["Total_External_sem1"]

    # Average marks
    df["Avg_Internal_sem1"] = df[int_cols].mean(axis=1)
    df["Avg_External_sem1"] = df[ext_cols].mean(axis=1)

    # Binary flag for each subject fail (optional)
    for col in int_cols + ext_cols:
        df[f"{col}_fail"] = df[col] < 17  # Assuming 17 is passing marks

    # Encode categorical features
    if "Remark_sem1" in df.columns:
        df["Remark_sem1"] = df["Remark_sem1"].map({"PASS": 1, "FAIL": 0}).fillna(0)

    # Final feature selection
    basic_features = [
        "SGPA_sem1", "Percentage_sem1", "Total_Internal_sem1", "Total_External_sem1",
        "Total_Marks_sem1", "Avg_Internal_sem1", "Avg_External_sem1", "Remark_sem1"
    ]

    fail_flags = [col for col in df.columns if col.endswith("_fail")]
    features = basic_features + fail_flags

    return df, features


