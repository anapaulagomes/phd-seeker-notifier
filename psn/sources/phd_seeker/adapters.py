import csv
from datetime import datetime, timedelta, date
from typing import List


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


def from_csv_to_dict(positions_filepath) -> List[dict]:
    data = []
    with open(positions_filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            raw_last_seen = row["Date"].lower()
            last_seen_at = from_last_seen_to_date(raw_last_seen)
            position = {
                "country": row["Country"],
                "last_seen": last_seen_at,
                "title": row["Title"],
                "link": row["Link"],
                "source": "PhD Seeker",
            }
            data.append(position)
    return data
