import json
from pathlib import Path
from playwright.sync_api import APIRequestContext, APIResponse
from fixtures.logging_fixture import logger
from tests.base_test import log_information


class ApiBase:
    """Sends JSON HTTP requests through one shared Playwright request context and logs each call."""

    _PROJECT_ROOT = Path(__file__).resolve().parent.parent
    _DATA_DIR = _PROJECT_ROOT / "data"
    _SUPPORTED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
    _DEFAULT_HEADERS = {"Accept": "application/json"}

    def __init__(self, request_context: APIRequestContext):
        """
        Args:
            request_context: Playwright request context created once by the api_context fixture.
        """
        self.request = request_context

    def load_payload(self, file_name: str) -> dict:
        """
        Load a request body from a JSON file in the data folder.

        Args:
            file_name: File name inside data/, e.g. "create_order_api.json".

        Returns:
            dict: The parsed JSON, ready to send as a request body.

        Raises:
            FileNotFoundError: If the file does not exist in data/.
        """
        _path = self._DATA_DIR / file_name
        with open(_path, encoding="utf-8") as _file:
            return json.load(_file)

    def submit_api(self, method: str, url: str, headers: dict | None = None,
                   data: dict | None = None, params: dict | None = None, multipart: dict | None = None) -> APIResponse:
        """
        Send a JSON request and log it.

        Args:
            method: HTTP method, e.g. "get" or "POST" (case does not matter).
            url: Path relative to the API base URL, e.g. "/api/ecom/auth/login".
            headers: Extra headers for this request, added to the JSON defaults.
            data: Request body, sent as JSON.
            params: Query string parameters.
            multipart: Multipart for image

        Returns:
            APIResponse: The response.

        Raises:
            ValueError: If the method is not supported.
        """
        _method = method.upper()
        if _method not in self._SUPPORTED_METHODS:
            raise ValueError(f"Unsupported HTTP method: {method}")

        logger.info(f"{_method} {url} | params: {params}")
        _headers = {**self._DEFAULT_HEADERS, **(headers or {})}
        _response = self.request.fetch(url, method=_method, headers=_headers, data=data, params=params, multipart=multipart)
        logger.info(f"Response {_response.status} {_response.status_text} | {_method} {url}")
        return _response

    def submit_get_api(self, url: str, params: dict | None = None, headers: dict | None = None) -> APIResponse:
        """
        Send a GET request.

        Args:
            url: Path relative to the API base URL.
            params: Query string parameters.
            headers: Extra headers for this request.

        Returns:
            APIResponse: The response.
        """
        return self.submit_api("GET", url, headers=headers, params=params)

    def submit_post_api(self, url: str, data: dict | None = None, headers: dict | None = None, multipart: dict | None = None) -> APIResponse:
        """
        Send a POST request with a JSON body.

        Args:
            url: Path relative to the API base URL.
            data: Request body, sent as JSON.
            headers: Extra headers for this request.
            multipart: Multipart for image.

        Returns:
            APIResponse: The response.
        """
        return self.submit_api("POST", url, headers=headers, data=data, multipart=multipart)

    def submit_put_api(self, url: str, data: dict, headers: dict | None = None) -> APIResponse:
        """
        Send a PUT request with a JSON body.

        Args:
            url: Path relative to the API base URL.
            data: Request body, sent as JSON.
            headers: Extra headers for this request.

        Returns:
            APIResponse: The response.
        """
        return self.submit_api("PUT", url, headers=headers, data=data)

    def submit_delete_api(self, url: str, params: dict | None = None, headers: dict | None = None) -> APIResponse:
        """
        Send a DELETE request.

        Args:
            url: Path relative to the API base URL.
            params: Query string parameters.
            headers: Extra headers for this request.

        Returns:
            APIResponse: The response.
        """
        log_information(f"DELETE {url} | params: {params}")
        response = self.submit_api("DELETE", url, params=params, headers=headers)
        log_information(f"Response {response.status} {response.status_text} | DELETE {url}")
        if not response.ok:
            log_information(f"Body: {response.text()}")
        return response
