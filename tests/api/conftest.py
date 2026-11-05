import os

import pytest
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def session():
    """One shared HTTP session for the whole test run."""
    with requests.Session() as s:
        yield s
