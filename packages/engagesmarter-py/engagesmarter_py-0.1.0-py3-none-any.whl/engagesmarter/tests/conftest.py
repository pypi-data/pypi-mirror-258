import os
from unittest import mock

import pytest

from hedwig.client import EngageSmarterClient
from hedwig.client.resources.agents import AgentsResource
from hedwig.client.resources.conversations import ConversationsResource
from hedwig.client.resources.runs import RunsResource
from hedwig.client.resources.tags import TagsResource


@pytest.fixture
def api_key() -> str:
    """API key."""
    return "API_KEY"


@pytest.fixture
def org_id() -> str:
    """Org ID."""
    return "ORG_ID"


@pytest.fixture
def custom_api_url() -> str:
    """Custom API URL."""
    return "http://localhost:1234"


@pytest.fixture
def local_api_url() -> str:
    """Localhost API URL."""
    return os.getenv("API_URL")


@pytest.fixture
def mock_httpx_client():
    return mock.Mock()


@pytest.fixture
def mock_engagesmarter_client() -> EngageSmarterClient:
    """Client pointing at mock API."""
    return EngageSmarterClient(
        api_key="API_KEY",
        org_id="ORG_ID",
        api_url="http://not_a_real_url",
    )


@pytest.fixture
def local_engagesmarter_client() -> EngageSmarterClient:
    """Client pointing at locally hosted API."""
    return EngageSmarterClient(
        api_url=os.getenv("API_URL"),
        api_key=os.getenv("ENGAGE_SMARTER_API_KEY"),
        org_id=os.getenv("ENGAGE_SMARTER_ORG_ID"),
    )


@pytest.fixture
def agents(
    local_engagesmarter_client: EngageSmarterClient,
) -> AgentsResource:
    """Agents resource pointing at locally hosted API."""
    return local_engagesmarter_client.agents


@pytest.fixture
def conversations(
    local_engagesmarter_client: EngageSmarterClient,
) -> ConversationsResource:
    """Conversations resource pointing at locally hosted API."""
    return local_engagesmarter_client.conversations


@pytest.fixture
def runs(
    local_engagesmarter_client: EngageSmarterClient,
) -> RunsResource:
    """Runs resource pointing at locally hosted API."""
    return local_engagesmarter_client.runs


@pytest.fixture
def tags(
    local_engagesmarter_client: EngageSmarterClient,
) -> TagsResource:
    """Tags resource pointing at locally hosted API."""
    return local_engagesmarter_client.tags
