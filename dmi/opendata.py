# import json
from typing import Any, Dict, List

import pandas as pd
import requests

from dmi.utils import check_date_format, convert_to_pandas_df


class DMIForecastData:

    _base_url = "https://dmigw.govcloud.dk/v1/forecastedr"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _query(self, endpoint: str, params: Dict[str, Any], **kwargs) -> Dict:
        res = requests.get(
            url=f"{self._base_url}/{endpoint}",
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
            raise ValueError(
                f"Failed HTTP request with HTTP status code {http_status_code} and message: {message}"
            )

        return data

    def get_model_runs(self, model: str) -> List[str]:

        data = self._query(endpoint=f"collections/{model}/instances", params={})

        model_runs = [instance["id"] for instance in data["instances"]]

        return model_runs

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        model: str,
        model_run: str = "latest",
        parameters: List[str] = [],
        raw_forecast: bool = False,
    ) -> List[Dict] | pd.DataFrame:

        if model_run == "latest":
            endpoint = f"collections/{model}/position"
        else:
            check_date_format(model_run)
            endpoint = f"collections/{model}/instances/{model_run}/position"

        data = self._query(
            endpoint=endpoint,
            params={
                "coords": f"POINT({longitude} {latitude})",
                "crs": "crs84",
                "parameter-name": ",".join(parameters),
            },
        )

        if not raw_forecast:
            pass
            # TODO convert to Pandas df
            # df = convert_to_pandas_df(data)

        return data
