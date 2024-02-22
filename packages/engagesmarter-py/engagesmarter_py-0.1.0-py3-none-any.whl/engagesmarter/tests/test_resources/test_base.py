from hedwig.client import EngageSmarterClient
from hedwig.client.resources.base import BaseResource


def test_base_resource_init(mock_engagesmarter_client: EngageSmarterClient) -> None:
    auth_client = mock_engagesmarter_client._client
    base_resource = BaseResource(client=auth_client)
    assert base_resource.client == auth_client
