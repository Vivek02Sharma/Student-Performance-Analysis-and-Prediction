import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error


# Load and Merge Sem1 + Sem2 data
def load_and_merge_data(sem1_path, sem2_path):
    sem1 = pd.read_json(sem1_path)
    sem2 = pd.read_json(sem2_path)

    sem1 = sem1.rename(columns={"SGPA": "SGPA_sem1", "TotalMarks": "TotalMarks_sem1"})
    sem2 = sem2.rename(columns={"SGPA": "SGPA_sem2"})

    merged = pd.merge(sem1, sem2[["StudentId", "SGPA_sem2"]], on="StudentId", how="inner")
    return merged


# Feature Engineering from Sem1
def prepare_features(data):
    int_cols = [col for col in data.columns if col.startswith("INT_")]
    ext_cols = [col for col in data.columns if col.startswith("EXT_")]

    data["Sem1_INT_Total"] = data[int_cols].sum(axis=1)
    data["Sem1_EXT_Total"] = data[ext_cols].sum(axis=1)
    data["Sem1_Total"] = data["Sem1_INT_Total"] + data["Sem1_EXT_Total"]
    data["Sem1_Percentage"] = (data["Sem1_Total"] / data["TotalMarks_sem1"]) * 100

    data["SGPA_sem1_squared"] = data["SGPA_sem1"] ** 2
    data["SGPA_sem1_log"] = np.log1p(data["SGPA_sem1"])

    features = [
        "Sem1_INT_Total", "Sem1_EXT_Total", "Sem1_Total",
        "Sem1_Percentage", "SGPA_sem1", "SGPA_sem1_squared", "SGPA_sem1_log"
    ]
    return data, features


# Predict SGPA of Sem2 for 1 student
def predict_sem2_sgpa(student_data, model, scaler, features):
    student_df = pd.DataFrame([student_data])
    student_df["TotalMarks_sem1"] = 700

    student_df, _ = prepare_features(student_df)
    X_input = scaler.transform(student_df[features])
    sgpa_pred = model.predict(X_input)[0]
    return round(sgpa_pred, 2)

# Main Code
if __name__ == "__main__":
    # Load and merge sem1 and sem2 data
    merged_df = load_and_merge_data("data/raw/sem1.json", "data/raw/sem2.json")
    
    # Prepare training data
    merged_df, feature_cols = prepare_features(merged_df)
    X = merged_df[feature_cols]
    y = merged_df["SGPA_sem2"]

    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # Optional: Evaluate model
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"📊 Model trained. RMSE on test set: {rmse:.2f}")

    # Predict for new student
    student_sem1_data = {
        "StudentId": 3735942,
        "INT_BMSBC103": 35,
        "EXT_BMSBC103": 55,
        "INT_BMSBL107": 31,
        "EXT_BMSBL107": 48,
        "INT_BMSBS106": 34,
        "EXT_BMSBS106": 51,
        "INT_BMSECO102": 34,
        "EXT_BMSECO102": 46,
        "INT_BMSFA105": 38,
        "EXT_BMSFA105": 53,
        "INT_BMSFC104": 36,
        "EXT_BMSFC104": 51,
        "INT_BMSFHS101": 39,
        "EXT_BMSFHS101": 55,
        "SGPA_sem1": 10
    }

    predicted_sgpa = predict_sem2_sgpa(student_sem1_data, model, scaler, feature_cols)
    print(f"🎯 Predicted SGPA for Sem2: {predicted_sgpa}")
