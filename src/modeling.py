from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
from src.logger import logging

def train_model(X, y):
    """Train a machine learning model."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, X_test, y_test

def save_model(model, filepath):
    """Save the trained model to a file."""
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)

def load_model(filepath):
    """Load a trained model from a file."""
    with open(filepath, 'rb') as f:
        return pickle.load(f)
