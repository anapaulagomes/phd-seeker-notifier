import csv
from datetime import datetime, timedelta


def from_csv_to_dict(positions_filepath):
    data = []
    with open(positions_filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            position = {
                "country": row["Country"],
                "last_updated": row["Date"],
                "title": row["Title"],
                "link": row["Link"],
            }
            data.append(position)
    return data


def filter_by_location(positions, country):
    filtered_data = []
    for position in positions:
        if position["country"].lower() == country.lower():
            filtered_data.append(position)
    return filtered_data


def filter_by_last_updated(positions, days):
    filtered_data = []
    for position in positions:
        raw_last_updated = position["last_updated"].lower()
        last_updated_at = from_last_updated_to_date(raw_last_updated)

        if not raw_last_updated:
            continue

        if (datetime.today().date() - last_updated_at).days < days:  # delta
            filtered_data.append(position)
    return filtered_data


def from_last_updated_to_date(last_updated):
    metrics = {
        "second": {"attribute": "seconds", "factor": 1},
        "minute": {"attribute": "seconds", "factor": 60},
        "hour": {"attribute": "seconds", "factor": 360},
        "day": {"attribute": "days", "factor": 1},
        "month": {"attribute": "days", "factor": 30},
        "year": {"attribute": "days", "factor": 365},
    }
    original_last_updated = last_updated
    last_updated = last_updated.lower().replace("about", "")
    last_updated = last_updated.replace("ago", "")
    last_updated = last_updated.strip()
    last_updated = last_updated.split()
    if len(last_updated) != 2:
        print(f"Failed to parse last seen: {original_last_updated}")
        return
    number, possible_metric = int(last_updated[0]), last_updated[1]
    for metric in metrics:
        if possible_metric.startswith(metric):
            kwargs = {metrics[metric]["attribute"]: number * metrics[metric]["factor"]}
            return (datetime.today() - timedelta(**kwargs)).date()

    print(f"Failed to parse last seen using metrics: {original_last_updated}")
    return
