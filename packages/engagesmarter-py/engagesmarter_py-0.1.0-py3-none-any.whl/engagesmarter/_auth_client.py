from typing import Any

import httpx

from .constants import API_KEY_HEADER_NAME, ORG_ID_HEADER_NAME
from .errors_handler import handle_response_error
from .utils.content import prepare_content


class AuthenticatedClient:
    def __init__(
        self,
        api_url: str,
        api_key: str,
        org_id: str,
        timeout: int,
        headers: dict[str, str] | None = None,
    ):
        self.api_url = api_url
        self.api_key = api_key
        self.org_id = org_id
        self.timeout = timeout
        self._headers = headers or {}
        self._client = httpx.Client(
            base_url=self.api_url,
            headers=self.get_headers(),
            timeout=self.timeout,
        )

    def get_headers(self) -> dict[str, str]:
        """Get headers to be used in authenticated endpoints"""
        return {
            API_KEY_HEADER_NAME: self.api_key,
            ORG_ID_HEADER_NAME: self.org_id,
            **self._headers,
        }

    def _process_response(self, response: httpx.Response) -> Any:
        if not response.is_success:
            handle_response_error(response)
        return response.json()

    def get(self, url: str, **kwargs):
        res = self._client.get(url, **kwargs)
        return self._process_response(res)

    def post(self, url: str, **kwargs):
        if "content" in kwargs:
            content = kwargs["content"]
            kwargs["content"] = prepare_content(content)
        res = self._client.post(url, **kwargs)
        return self._process_response(res)

    def patch(self, url: str, **kwargs):
        if "content" in kwargs:
            content = kwargs["content"]
            kwargs["content"] = prepare_content(content)
        res = self._client.patch(url, **kwargs)
        return self._process_response(res)

    def delete(self, url: str, **kwargs):
        res = self._client.delete(url, **kwargs)
        return self._process_response(res)

    def __del__(self):
        if hasattr(self, "_client"):
            del self._client

    # Context managers

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
