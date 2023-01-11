import csv
from datetime import date, datetime, timedelta
from typing import List


def from_csv_to_dict(positions_filepath) -> List[dict]:
    data = []
    with open(positions_filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            position = {
                "country": row["Country"],
                "last_seen": row["Date"],
                "title": row["Title"],
                "link": row["Link"],
            }
            data.append(position)
    return data


def filter_by_location(positions: List[dict], country: str) -> List[dict]:
    filtered_data = []
    for position in positions:
        if position["country"].lower() == country.lower():
            filtered_data.append(position)
    return filtered_data


def filter_by_last_seen(positions: List[dict], days: int) -> List[dict]:
    filtered_data = []
    for position in positions:
        raw_last_seen = position["last_seen"].lower()
        last_seen_at = from_last_seen_to_date(raw_last_seen)

        if not raw_last_seen:
            continue

        if (datetime.today().date() - last_seen_at).days < days:  # delta
            filtered_data.append(position)
    return filtered_data


def from_last_seen_to_date(last_seen: str) -> date:
    metrics = {
        "second": {"attribute": "seconds", "factor": 1},
        "minute": {"attribute": "seconds", "factor": 60},
        "hour": {"attribute": "seconds", "factor": 360},
        "day": {"attribute": "days", "factor": 1},
        "month": {"attribute": "days", "factor": 30},
        "year": {"attribute": "days", "factor": 365},
    }
    original_last_seen = last_seen
    last_seen = last_seen.lower().replace("about", "")
    last_seen = last_seen.replace("ago", "")
    last_seen = last_seen.strip()
    last_seen = last_seen.split()
    if len(last_seen) != 2:
        print(f"Failed to parse last seen: {original_last_seen}")
        return
    number, possible_metric = int(last_seen[0]), last_seen[1]
    for metric in metrics:
        if possible_metric.startswith(metric):
            kwargs = {metrics[metric]["attribute"]: number * metrics[metric]["factor"]}
            return (datetime.today() - timedelta(**kwargs)).date()

    print(f"Failed to parse last seen using metrics: {original_last_seen}")
    return
