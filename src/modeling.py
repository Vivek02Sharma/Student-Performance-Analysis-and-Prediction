import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
from sklearn.preprocessing import StandardScaler
from feature_engineering import feature_engineering_func


merged, features = feature_engineering_func()
# Define Target (Predict Sem2 Outcome)

# Option 1: Classification (PASS/FAIL)
merged['Target_Remark'] = merged['Remark_sem2'].apply(lambda x: 1 if x == 'PASS' else 0)

# Option 2: Regression (SGPA_sem2)
target_sgpa = merged['SGPA_sem2']

X = merged[features]
y = merged['Target_Remark']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize Features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model 1: Random Forest Classifier (PASS/FAIL)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train_scaled, y_train)
y_pred = clf.predict(X_test_scaled)
print("Classification Results:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Cross-Validation
cv_scores = cross_val_score(clf, X, y, cv=5)
print("Cross-Validation Accuracy:", np.mean(cv_scores))

# Model 2: Linear Regression (SGPA Prediction)
X_train_sgpa, X_test_sgpa, y_train_sgpa, y_test_sgpa = train_test_split(X, target_sgpa, test_size=0.2, random_state=42)
reg = LinearRegression()
reg.fit(X_train_sgpa, y_train_sgpa)
y_pred_sgpa = reg.predict(X_test_sgpa)

print("\nRegression Results:")
rmse = np.sqrt(mean_squared_error(y_test_sgpa, y_pred_sgpa))
print("RMSE:", rmse)
print("R² Score:", reg.score(X_test_sgpa, y_test_sgpa))

# Feature Importance (Classification)
plt.figure(figsize=(10, 6))
plt.barh(features, clf.feature_importances_)
plt.title("Feature Importance (Random Forest)")
plt.show()

# Scatter Plot for Regression Predictions
plt.figure(figsize=(10, 6))
plt.scatter(y_test_sgpa, y_pred_sgpa, alpha=0.5)
plt.xlabel("Actual SGPA (Sem2)")
plt.ylabel("Predicted SGPA (Sem2)")
plt.title("Actual vs Predicted SGPA")
plt.plot([0, 10], [0, 10], color='red')
plt.show()