import pandas as pd
from datetime import datetime

def check_date_format(date, format="%Y-%m-%dT%H%M%SZ"):
    try:
        datetime.strptime(date, format)
    except:
        raise AttributeError(f"The given date {date} is not in the correct format {format}")
    
def convert_to_pandas_df(raw_response) -> pd.DataFrame:
    timestamps = raw_response['domain']['axes']['t']['values']

    df = pd.DataFrame({'datetime': pd.to_datetime(timestamps)})

    for parameter in raw_response['ranges'].keys():
        df[parameter] = raw_response['ranges'][parameter]['values']

    return df