import pytest
from packaging_demo.slow import slow_add

@pytest.mark.slow
def test_slow_add():
    sum_ = slow_add(1,2)
    assert False
    #assert sum_ == 3 