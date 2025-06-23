
from ..engine import LifeEngine

def test_simple_run():
    eng = LifeEngine([1, 5])
    res = eng.run()
    assert res.final_age >= 0
    assert len(res.log) >= 1
