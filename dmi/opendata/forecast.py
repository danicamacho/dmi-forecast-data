from typing import Dict, List

import pandas as pd

from dmi.opendata.client import DMIOpenClient
from dmi.opendata.utils import check_date_format, convert_to_pandas_df


class DMIForecast(DMIOpenClient):
    def __init__(self, api_key):
        api = "forecastedr"
        version = "v1"
        super().__init__(api_key=api_key, version=version, api=api)

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
            latitude (float): latitude of coordinates.
            longitude (float): longitude of coordinates.
            model (str): name of the model
            model_run (str, optional): datetime of the specific model run.
                Must be in "%Y-%m-%dT%H%M%SZ" format. Defaults to "latest".
            parameters (List[str], optional): list of parameters to extract from the model.
                If an empty list, extracts all available parameters. Defaults to [].
            raw_forecast (bool, optional): whether to return the raw response from the model
                or a Pandas DataFrame. Defaults to False.

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
