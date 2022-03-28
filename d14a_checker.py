import datetime
import json
import time
from typing import Union, Any

import pandas as pd
import requests as requests

from list_tracker import DEF_14A_KEY, SYMBOL_KEY, SNP_CSV_FILENAME, \
    SECURITY_KEY

RECHECK_TIME_MONTHS = 10
SEARCH_ENDPOINT = "https://efts.sec.gov/LATEST/search-index"


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def iso_date(date: datetime.date):
    month_str = str(date.month)
    if date.month < 10:
        month_str = "0" + month_str
    date_str = str(date.day)
    if date.day < 10:
        date_str = "0" + date_str
    return f"{date.year}-{month_str}-{date_str}"


def check_d14a(series: pd.Series):
    symbol = series[SYMBOL_KEY]
    security = series[SECURITY_KEY]
    search_params = json.dumps({
        "dateRange": "custom",
        "category": "custom",
        "entityName": symbol,
        "startdt": iso_date(
            datetime.date.today() - datetime.timedelta(days=1)),
        "enddt": iso_date(datetime.date.today()),
        "forms": ["DEF 14A"]
    })
    response = requests.post(SEARCH_ENDPOINT, data=search_params)
    response_dict: dict[str, Any] = json.loads(response.content.decode())
    results = response_dict["hits"]["hits"]
    if len(results) > 0:
        date = results[0]["_source"]["file_date"]
        print(f"Found DEF 14A for {symbol} ({security}) filed on {date}")
        return date


def main():
    snp500: pd.DataFrame = pd.read_csv(SNP_CSV_FILENAME)
    for idx, series in snp500.iterrows():
        def_14a_found_date: Union[str, float] = series[DEF_14A_KEY]
        if isinstance(def_14a_found_date, float):
            needs_rechecking = True
        elif isinstance(def_14a_found_date, str):
            date = datetime.date.fromisoformat(def_14a_found_date)
            needs_rechecking = diff_month(datetime.date.today(),
                                          date) >= RECHECK_TIME_MONTHS
        else:
            raise Exception("The type of def_14a_found_date was unexpected! "
                            "Did you mess with the CSV?")

        if needs_rechecking:
            filed_date = check_d14a(series)
            time.sleep(1)
            if filed_date is not None:
                snp500.loc[idx, DEF_14A_KEY] = filed_date
                snp500.to_csv(SNP_CSV_FILENAME, index=False)


if __name__ == '__main__':
    main()
