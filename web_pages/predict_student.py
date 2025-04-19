import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load the trained model and scaler
with open("models/sgpa_model1.pkl", "rb") as f:
    model = pickle.load(f)
with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Feature Engineering
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

# Prediction function
def predict_sem2_sgpa(student_data):
    student_df = pd.DataFrame([student_data])
    student_df["TotalMarks_sem1"] = 700

    student_df, features = prepare_features(student_df)
    X_input = scaler.transform(student_df[features])
    sgpa_prediction = model.predict(X_input)[0]
    return round(sgpa_prediction, 2)

def student_predict():
    # Streamlit UI
    st.title("🎓 Semester 2 SGPA Prediction")

    st.markdown("Enter your Semester 1 internal and external marks below:")

    # Input form
    with st.form("student_input_form"):
        cols = st.columns(7)
        int_ext_data = {}

        subjects = [
            "BMSBC103", "BMSBL107", "BMSBS106", "BMSECO102", 
            "BMSFA105", "BMSFC104", "BMSFHS101"
        ]

        for subject in subjects:
            int_col = f"INT_{subject}"
            ext_col = f"EXT_{subject}"
            int_val = cols[subjects.index(subject)].number_input(int_col, min_value=0, max_value=40, step=1)
            ext_val = cols[subjects.index(subject)].number_input(ext_col, min_value=0, max_value=60, step=1)
            int_ext_data[int_col] = int_val
            int_ext_data[ext_col] = ext_val

        sgpa_sem1 = st.slider("Semester 1 SGPA", min_value=0.0, max_value=10.0, value=8.0, step=0.01)

        submitted = st.form_submit_button("Predict SGPA for Sem 2")

    # Handle prediction
    if submitted:
        student_data = {
            "StudentId": 1,  
            **int_ext_data,
            "SGPA_sem1": sgpa_sem1
        }
        predicted_sgpa = predict_sem2_sgpa(student_data)
        st.success(f"🎯 Predicted SGPA for Semester 2 is: **{predicted_sgpa}**")
