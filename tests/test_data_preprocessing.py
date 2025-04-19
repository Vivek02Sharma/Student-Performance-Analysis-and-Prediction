import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from pandas.testing import assert_series_equal
from src.data_preprocessing import adding_grace, apply_grace_marks

# ---------- UNIT TESTS FOR adding_grace() ----------

@pytest.mark.parametrize("input_value, expected_output", [
    ("10*5", 15),     # with grace
    ("20", 20),       # no grace
    ("0*3", 3),       # zero + grace
    ("", None),       # empty string
    ("abc", None),    # invalid value
    (None, None),     # None input
])
def test_adding_grace(input_value, expected_output):
    assert adding_grace(input_value) == expected_output


# ---------- UNIT TESTS FOR apply_grace_marks() ----------

def test_apply_grace_marks():
    df = pd.DataFrame({
        'INT_SUB1': ['20*5', '15*0', '30', ''],
        'EXT_SUB1': ['10*2', '25', '5*1', 'abc'],
        'Other_Column': [1, 2, 3, 4]
    })

    expected_INT = pd.Series([25, 15, 30, None], name="INT_SUB1")
    expected_EXT = pd.Series([12, 25, 6, None], name="EXT_SUB1")

    categorical_columns = ['INT_SUB1', 'EXT_SUB1', 'Other_Column']
    processed_df = apply_grace_marks(df.copy(), categorical_columns)

    assert_series_equal(processed_df['INT_SUB1'], expected_INT)
    assert_series_equal(processed_df['EXT_SUB1'], expected_EXT)

# command : pytest .\tests\test_data_preprocessing.py -v --html=reports/test_report.html --self-contained-html
