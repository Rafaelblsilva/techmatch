import os
from unittest import mock

import pytest


@pytest.fixture(autouse=True, name="test_env", scope="module")
def test_env():
    with mock.patch.dict(os.environ, {"ENV": "TEST"}):
        yield


@pytest.fixture(autouse=True, name="client", scope="function")
def test_client(test_env):
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as client:
        yield client
