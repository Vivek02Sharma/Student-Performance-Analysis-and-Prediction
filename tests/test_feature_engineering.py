import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.feature_engineering import feature_engineering_func

# Dummy input for testing
@pytest.fixture
def dummy_data():
    data = {
        'StudentId': [1, 2],
        'INT_BMSBC103_sem1': [10, 15],
        'EXT_BMSBC103_sem1': [20, 25],
        'INT_BMSBL107_sem1': [15, 10],
        'EXT_BMSBL107_sem1': [15, 20],
        'INT_BMSBS106_sem1': [12, 10],
        'EXT_BMSBS106_sem1': [18, 15],
        'INT_BMSECO102_sem1': [14, 12],
        'EXT_BMSECO102_sem1': [16, 18],
        'INT_BMSFA105_sem1': [11, 13],
        'EXT_BMSFA105_sem1': [19, 17],
        'INT_BMSFC104_sem1': [10, 9],
        'EXT_BMSFC104_sem1': [20, 21],
        'INT_BMSFHS101_sem1': [13, 11],
        'EXT_BMSFHS101_sem1': [17, 19],
        'SGPA_sem1': [7.5, 8.0],
        'Percentage_sem1': [75.0, 80.0],
        'Remark_sem1': ['PASS', 'FAIL']
    }

    df = pd.DataFrame(data)
    return df

def test_feature_engineering(monkeypatch, dummy_data):
    # Patch the merged dataframe with dummy_data
    monkeypatch.setattr("src.feature_engineering.merged", dummy_data.copy())

    df_out, features = feature_engineering_func()

    # Validate Total Marks column
    assert df_out['Total_BMSBC103_sem1'].tolist() == [30, 40]
    assert df_out['Total_BMSBL107_sem1'].tolist() == [30, 30]
    assert df_out['Total_BMSBS106_sem1'].tolist() == [30, 25]

    # Validate failure flag
    assert df_out['Failed_any_sem1'].tolist() == [0, 1]

    # Validate features list
    expected_features = [
        'SGPA_sem1', 'Percentage_sem1', 'Failed_any_sem1',
        'Total_BMSBC103_sem1', 'Total_BMSBL107_sem1', 'Total_BMSBS106_sem1',
        'Total_BMSECO102_sem1', 'Total_BMSFA105_sem1', 'Total_BMSFC104_sem1',
        'Total_BMSFHS101_sem1'
    ]
    assert features == expected_features

# command : pytest tests/test_feature_engineering.py -v --html=reports/feature_engineering.html --self-contained-html
