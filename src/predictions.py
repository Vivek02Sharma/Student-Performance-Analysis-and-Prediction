import pickle
import pandas as pd

def load_model():
    """Load the trained model from the models directory."""
    with open('models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def make_predictions(model, X_new):
    """Make predictions using the trained model."""
    return model.predict(X_new)
