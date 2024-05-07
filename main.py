from datetime import datetime
import json
from pathlib import Path
import urllib.parse
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode, urlparse, parse_qs
import re

data = Path("./data/")


def get_bank_mapping() -> dict:
    with open("banks.json", "r") as f:
        bank_mapping = json.load(f)

    return bank_mapping


def get_local_forex(filepath: Path) -> dict:
    forex = {}
    filepath = filepath.with_suffix(".json")

    if filepath.exists():
        with open(filepath, "r") as f:
            forex = json.load(f)

    return forex

def merge_url_query_params(url: str, additional_params: dict) -> str:
    url_components = urlparse(url)
    original_params = parse_qs(url_components.query)
    merged_params = {**original_params, **additional_params}
    updated_query = urlencode(merged_params, doseq=True)
    return url_components._replace(query=updated_query).geturl()


def get_image_filename(image_src: str) -> str | None:
    image_filename = None

    match = re.search(
        r"indicative_ex_rates_logo/public/banks/([^/.?]+)(?:\.webp|\.jpg|\.jpeg|\.png)?",
        image_src,
    )

    if match:
        image_filename = match.group(1)

    return image_filename


def drop_null_images(bank_mapping: dict) -> dict:
    return {k: v for k, v in bank_mapping.items() if v.get("image", None) is not None}


def normalizeStr(_str: str) -> str:
    return _str.lower().strip().replace(".", "").replace(" ", "_")


def get_web_page_content(url: str) -> str:
    page = urlopen(url)

    return page.read().decode("utf-8")


def scrap_forex_page(soup, image_initial_mapping: dict) -> dict:
    forex_content = soup.select_one("div.view.view-indicative-exchange-rate")
    forex_by_bank = forex_content.select("div.views-row")

    forex_data = {}

    for forex in forex_by_bank:
        # We use the image above the forex table to determine the bank.
        bank_img = forex.select_one("img").get("src")

        bank_img_filename = get_image_filename(bank_img)

        if not (bank_img_filename):
            raise Exception("No bank image found")
        bank_initial = image_initial_mapping.get(bank_img_filename)

        if not (bank_initial):
            raise Exception(f"Bank not in bank_mapping for image: {bank_img}")
        forex_by_country = forex.select_one("table")

        # A row, a country
        for row in forex_by_country.select("tbody > tr"):
            row_data = row.find_all("td")
            country = normalizeStr(row_data[0].text)

            forex_data.setdefault(bank_initial, {"forex": {}})["forex"][country] = {
                "buy": {
                    "tt": parse_forex_cell(row_data[1]),
                    "tcdd": parse_forex_cell(row_data[2]),
                    "notes": parse_forex_cell(row_data[3]),
                },
                "sell": {
                    "ttddtc": parse_forex_cell(row_data[4]),
                    "notes": parse_forex_cell(row_data[5]),
                },
            }

    return forex_data


def parse_forex_cell(forex_cell) -> float | None:
    value = forex_cell.text.strip()

    try:
        return float(value)
    except Exception as e:
        return None


def scrap_forex(bank_mapping: dict, date: datetime) -> dict:

    base_url = "https://www.bom.mu/markets/foreign-exchange/indicative-exchange-rate"
    query_params = {
        "field_trans_date_value[value][date]": date.strftime("%d-%m-%Y"),
        "field_bank_code_reference_tid": "All",
        "filter_currency": "All",
        "page": 0,
    }

    initial_image_mapping = {
        k: get_image_filename(v["image"])
        for k, v in drop_null_images(bank_mapping).items()
    }
    image_initial_mapping = {v: k for k, v in initial_image_mapping.items()}

    all_forex = {}
    while True:
        page_content = get_web_page_content(
            merge_url_query_params(base_url, query_params)
        )

        soup = BeautifulSoup(page_content, "html.parser")

        if soup.select("div.view-empty"):  # stop while loop
            break

        forex_data = scrap_forex_page(soup, image_initial_mapping)
        all_forex.update(forex_data)

        query_params["page"] += 1

    return all_forex


def save_to_json(filepath: Path, data: dict) -> None:
    with open(filepath.with_suffix(".json"), "w") as f:
        json.dump(data, f, indent=4)


def save_forex(
    data_dir: Path, country_name: str, forex: dict, add_dt: datetime = None
) -> None:
    country_name = urllib.parse.quote(country_name)

    previous_forex = get_local_forex(data_dir / country_name)
    # Remove the key last_update_dt
    previous_forex.pop("last_update_dt", None)

    # If the data is the same, we don't save it
    if previous_forex == forex:
        return None

    if add_dt:
        forex = {"last_update_dt": add_dt.isoformat(), **forex}

    save_to_json(data_dir / country_name, forex)


if __name__ == "__main__":
    today = datetime.now()

    data.mkdir(parents=True, exist_ok=True)

    bank_mapping = get_bank_mapping()

    print("1. Scrapping Forex")
    all_forex = scrap_forex(bank_mapping, today)

    if all_forex == {}:
        print("No Forex data")
        exit(0)

    print("2. Saving Forex")
    save_forex(data, "all", {"forex": all_forex}, today)
    for bank, bank_forex in all_forex.items():
        bank_data_dir = data / bank
        bank_name = bank_mapping[bank]["name"]

        bank_data_dir.mkdir(parents=True, exist_ok=True)

        save_forex(bank_data_dir, "all", bank_forex, today)
        for country, country_forex in bank_forex["forex"].items():
            save_forex(bank_data_dir, country, {"forex": country_forex}, today)

    exit(0)
