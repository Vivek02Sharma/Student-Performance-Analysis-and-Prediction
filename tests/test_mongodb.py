import os
import sys
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

# Fix src path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mongodb import get_data_from_mongodb, student_data


@patch("src.mongodb.MongoClient")
def test_get_data_from_mongodb(mock_mongo_client):
    # Mock the collection
    mock_collection = MagicMock()
    mock_collection.find.return_value = [
        {"StudentId": 101, "Name": "Alice", "Score": 88},
        {"StudentId": 102, "Name": "Bob", "Score": 76}
    ]

    # Mock DB and collection access
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection

    mock_client = MagicMock()
    mock_client.__getitem__.return_value = mock_db
    mock_mongo_client.return_value = mock_client

    # Run the function
    get_data_from_mongodb("mock_collection")

    # Assertions
    file_path = "data/raw/BMS_raw.csv"
    assert os.path.exists(file_path), "CSV file not created"

    df = pd.read_csv(file_path)
    assert len(df) == 2
    assert "StudentId" in df.columns


@patch("src.mongodb.MongoClient")
def test_student_data_valid_id(mock_mongo_client):
    # Mock sem1 and sem2 collections
    mock_sem1 = MagicMock()
    mock_sem2 = MagicMock()
    mock_sem1.find_one.return_value = {"StudentId": 101, "SGPA": 8.5}
    mock_sem2.find_one.return_value = {"StudentId": 101, "SGPA": 9.0}

    # Mock student_db with sem1 and sem2 collections
    mock_student_db = {
        "sem1": mock_sem1,
        "sem2": mock_sem2
    }

    # Create a fake client
    mock_client = MagicMock()
    mock_client.__getitem__.side_effect = lambda name: mock_student_db if name == "student_db" else None
    mock_mongo_client.return_value = mock_client

    # Run the function
    sem1, sem2 = student_data(101)

    # Assertions
    assert sem1["SGPA"] == 8.5
    assert sem2["SGPA"] == 9.0


def test_student_data_invalid_id():
    sem1, sem2 = student_data("invalid_id")
    assert sem1 is None
    assert sem2 is None
