import pytest

from app.utils import counter
from app.utils.counter import CounterDowload


@pytest.fixture(autouse=True)
def temp_counter_file(tmp_path, monkeypatch):
    monkeypatch.setattr(counter, "PATH_DATA_JSON", tmp_path / "counter.json")


def test_add_one():
    assert CounterDowload().get_counter() == 0
    CounterDowload().add_one()
    assert CounterDowload().get_counter() == 1
