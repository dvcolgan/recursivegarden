import pytest


@pytest.fixture(autouse=True)
def django_db_for_all_tests(db):
    pass
