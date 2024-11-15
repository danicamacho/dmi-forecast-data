from typing import Any, Dict, List

import pandas as pd
import requests

from dmi.utils import check_date_format, convert_to_pandas_df


class DMIForecastData:
    _base_url = "https://dmigw.govcloud.dk/v1/forecastedr"

    def __init__(self, api_key: str):
        self.api_key = api_key

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
            raise ValueError(f"Failed HTTP request with HTTP status code {http_status_code} and message: {message}")

        return data

    def get_model_runs(self, model: str) -> List[str]:
        """Query the API to get available model runs (also called instances).

        Args:
            model (str): name of the model.

        Returns:
            List[str]: list of model runs, in datetime format.
        """

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
    ) -> Dict | pd.DataFrame:
        """Get forecast from a given model and a pair of coordinates

        Args:
            latitude (float): latitude of coordinates
            longitude (float): longitude of coordinates
            model (str): name of the model
            model_run (str, optional): datetime of the specific model run. Must be in "%Y-%m-%dT%H%M%SZ" format. Defaults to "latest".
            parameters (List[str], optional): list of parameters to extract from the model. If an empty list, extracts all available parameters. Defaults to [].
            raw_forecast (bool, optional): whether to return the raw response from the model or a Pandas DataFrame. Defaults to False.

        Returns:
            Dict | pd.DataFrame: Forecast. If raw_forecast=False, returns a Pandas DataFrame.
        """

        if model_run == "latest":
            endpoint = f"collections/{model}/position"
        else:
            check_date_format(model_run)
            endpoint = f"collections/{model}/instances/{model_run}/position"

        params = {
            "coords": f"POINT({longitude} {latitude})",
            "crs": "crs84",
        }

        if parameters:
            params["parameter-name"] = ",".join(parameters)

        data = self._query(endpoint=endpoint, params=params)

        if not raw_forecast:
            data = convert_to_pandas_df(data)

        return data
