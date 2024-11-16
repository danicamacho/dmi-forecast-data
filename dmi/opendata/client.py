from abc import ABC
from typing import Any, Dict

import requests


class DMIOpenClient(ABC):
    _base_url = "https://dmigw.govcloud.dk/{version}/{api}"

    def __init__(self, api_key: str, version: str, api: str):
        self.api_key = api_key
        self.version = version
        self.api = api
        self.api_url = self._build_api_url()

    def _build_api_url(self):
        return self._base_url.format(version=self.version, api=self.api)

    def _query(self, endpoint: str, params: Dict[str, Any], **kwargs) -> Dict:
        """Query the given endpoing of the API

        Args:
            endpoint (str): enpoint of the API to query
            params (Dict[str, Any]): Parameters to build the query

        Raises:
            ValueError: if API returns a different status than 200

        Returns:
            Dict: data of the API response
        """
        res = requests.get(
            url=f"{self.api_url}/{endpoint}",
            params={
                "api-key": self.api_key,
                **params,
            },
            **kwargs,
        )

        data = res.json()

        http_status_code = data.get("http_status_code", 200)

        if http_status_code != 200:
            message = data.get("message")
            raise ValueError(f"Failed HTTP request with HTTP status code {http_status_code} and message: {message}")

        return data
