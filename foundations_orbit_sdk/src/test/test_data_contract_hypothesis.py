
from hypothesis import given
import hypothesis.strategies as st

from hypothesis.extra.pandas import column, columns, data_frames
import pandas as pd
import numpy as np

from foundations_orbit.contract_validators.min_max_checker import MinMaxChecker
import unittest

class TestDataContractHypothesis(unittest.TestCase):
    @st.composite
    def dataframes(draw, *strategies: st.SearchStrategy) -> st.SearchStrategy:
        names = draw(st.lists(st.integers(), unique=True, min_size=1))
        cols = [column(name, elements=draw(st.sampled_from(strategies))) for name in names]
        return draw(data_frames(cols))

    @staticmethod
    @given(dataframes(st.integers(), st.floats(), st.just(np.nan)))
    def test_min_max(df: pd.DataFrame) -> None:
        min_max = MinMaxChecker({col_name: "int" for col_name in df.columns})
        if df.empty:
            min_max.configure(df.columns, lower_bound=0, upper_bound=1)
            assert min_max.validate(df) == {}
        else:
            min_bound = min(df[col].min() for col in df.columns)
            max_bound = max(df[col].max() for col in df.columns)
            min_max.configure(df.columns, lower_bound=min_bound, upper_bound=max_bound)
            report = min_max.validate(df)
            expected = {
                col: {
                    "max_test": {
                        "max_value": df[col].max(),
                        "passed": True,
                        "upper_bound": max_bound,
                    },
                    "min_test": {
                        "min_value": df[col].min(),
                        "passed": True,
                        "lower_bound": min_bound,
                    },
                }
                for col in df.columns
            }
            assert report == expected