import json
import os

import pytest


@pytest.fixture
def data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "tests/data_test")
    file_path = os.path.join(data_dir, "test_vacancies.json")
    with open(file_path, encoding="utf-8") as r:
        file = json.load(r)
    return file
