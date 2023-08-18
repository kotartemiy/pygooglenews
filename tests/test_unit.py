"""
igotnews Unit Testing
"""

import pytest

from igotnews.config import settings
from igotnews.main import GoogleNews


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.mark.asyncio
async def test_dynaconf():
    assert settings.VALUE == "On Testing"


@pytest.mark.asyncio
async def test_myllm():
    gn = GoogleNews()
    response = await gn.search("EURUSD")
    assert response is not None
