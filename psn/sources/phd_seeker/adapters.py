import csv
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
