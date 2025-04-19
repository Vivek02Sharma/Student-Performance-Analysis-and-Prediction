import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error
from feature_engineering import feature_engineering_func

@pytest.fixture(scope="module")
def preprocessed_data():
    merged, features = feature_engineering_func()

    merged['Target_Remark'] = merged['Remark_sem2'].apply(lambda x: 1 if x == 'PASS' else 0)
    target_sgpa = merged['SGPA_sem2']
    X = merged[features]
    y_class = merged['Target_Remark']
    y_reg = target_sgpa

    return X, y_class, y_reg

def test_classification_pipeline(preprocessed_data):
    X, y_class, _ = preprocessed_data

    X_train, X_test, y_train, y_test = train_test_split(X, y_class, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_scaled, y_train)
    y_pred = clf.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)
    print("Classification Accuracy:", accuracy)

    # You can adjust the threshold based on real data expectations
    assert accuracy > 0.7, "Classification accuracy too low"

def test_regression_pipeline(preprocessed_data):
    X, _, y_reg = preprocessed_data

    X_train, X_test, y_train, y_test = train_test_split(X, y_reg, test_size=0.2, random_state=42)

    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print("Regression RMSE:", rmse)

    # Make sure RMSE is within acceptable range (depending on SGPA scale)
    assert rmse < 2.0, "RMSE is too high"
    
# command :  $env:PYTHONPATH="src"; pytest tests/test_modeling.py -v --html=test-reports/modeling_test_report.html --self-contained-html