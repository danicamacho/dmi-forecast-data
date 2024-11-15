from datetime import datetime
from typing import Dict

import pandas as pd


def check_date_format(date: str, format="%Y-%m-%dT%H%M%SZ"):
    """Raise error if the string is not the correct datetime format

    Args:
        date (str): string containing date.
        format (str, optional): datetime format. Defaults to "%Y-%m-%dT%H%M%SZ".

    Raises:
        AttributeError: The string date is not in the correct format
    """
    try:
        datetime.strptime(date, format)
    except:
        raise AttributeError(f"The given date {date} is not in the correct format {format}")


def convert_to_pandas_df(raw_response: Dict) -> pd.DataFrame:
    """Convert the API response into a Pandas dataframe

    Args:
        raw_response (Dict): API response with raw forecast

    Returns:
        pd.DataFrame: forecast in a Pandas Dataframe, including Timestamps
    """
    timestamps = raw_response["domain"]["axes"]["t"]["values"]

    df = pd.DataFrame({"datetime": pd.to_datetime(timestamps)})

    for parameter in raw_response["ranges"].keys():
        df[parameter] = raw_response["ranges"][parameter]["values"]

    return df
