from datetime import datetime
import requests
from io import BytesIO
import pandas as pd
import json
from pathlib import Path
import urllib.parse

data = Path("./data/")


def get_forex(start_date: datetime, end_date: datetime | None = None) -> pd.DataFrame:
    print("1. Fetching Forex")
    url = "https://mcb.mu/webapi/mcb/ForexDataExcel"

    if end_date is None:
        end_date = start_date

    payload = {
        "StartDate": start_date.strftime("%Y-%m-%d"),
        "EndDate": end_date.strftime("%Y-%m-%d"),
        "CurrencyCode": "ALL",
        "BaseCurrency": "MUR",
    }

    try:
        res = requests.post(url, json=payload, stream=True)

        xlsx_stream = BytesIO(res.content)
        df = pd.read_excel(xlsx_stream)

        return df
    except:
        raise Exception("Failed to fetch Forex data")


def process_forex_as_json(df: pd.DataFrame) -> dict:
    print("2. Processing Forex")
    df = df[8:30]
    df.columns = [
        "Country_Name",
        "rate_date",
        "currency",
        "code",
        "unit",
        "buy_tt",
        "buy_tc_dd",
        "buy_notes",
        "sell_tt",
        "sell_tc_dd",
        "sell_notes",
    ]

    all_forex = {}
    for index, row in df.iterrows():
        country_name = row["Country_Name"]
        all_forex[country_name] = {
            "rate_date": row["rate_date"],
            "currency": row["currency"],
            "code": row["code"],
            "unit": row["unit"],
            "buy": {
                "tt": row["buy_tt"],
                "tc/dd": row["buy_tc_dd"],
                "notes": row["buy_notes"],
            },
            "sell": {
                "tt": row["sell_tt"],
                "tc/dd": row["sell_tc_dd"],
                "notes": row["sell_notes"],
            },
        }

    return all_forex


def save_to_json(filepath: Path, data: dict) -> None:
    with open(filepath.with_suffix(".json"), "w") as f:
        json.dump(data, f, indent=4)


def save_forex(country_name: str, forex: dict) -> None:
    country_name = urllib.parse.quote(country_name.lower().replace(" ", "_"))

    save_to_json(data / country_name, forex)


if __name__ == "__main__":
    today = datetime.now()

    data.mkdir(parents=True, exist_ok=True)

    df = get_forex(today)
    all_forex = process_forex_as_json(df)

    print("3. Saving Forex")
    save_forex("all", all_forex)
    for country, forex in all_forex.items():
        save_forex(country, forex)
