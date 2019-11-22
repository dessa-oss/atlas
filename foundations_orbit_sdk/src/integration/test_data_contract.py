import os
from pandas import DataFrame
from hypothesis import given, assume, settings
import hypothesis.strategies as st
from hypothesis.extra.pandas import data_frames, column

from foundations_orbit.data_contract import DataContract
from foundations_contrib.global_state import redis_connection
from foundations_spec import Spec, set_up, tear_down


@st.composite
def dataframes(draw, *strategies: st.SearchStrategy) -> st.SearchStrategy:
    names = draw(st.lists(st.integers(), unique=True, min_size=1))
    cols = [column(name, elements=draw(st.sampled_from(strategies))) for name in names]
    return draw(data_frames(cols))


class TestDataContract(Spec):
    @set_up
    def set_up(self):
        self.project_name = self.faker.word()
        os.environ["PROJECT_NAME"] = self.project_name
        self.redis = redis_connection
        self.redis.flushall()

    @tear_down
    def tear_down(self):
        os.environ.pop("PROJECT_NAME")

    @given(
        dataframes(
            st.integers(min_value=-100, max_value=100),
            st.floats(min_value=-100, max_value=100, allow_nan=False),
        )
    )
    @settings(max_examples=5)
    def test_validate_method_creates_a_project_in_redis(self, df: DataFrame):
        assume(not df.empty)
        data_contract = DataContract("some_contract", df)
        data_contract.validate(df)
        actual_name, _ = self.redis.zscan('projects')[1][0]
        self.assertEqual(self.project_name, actual_name.decode())
