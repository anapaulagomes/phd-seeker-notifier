import argparse
from pathlib import Path

from psn.filters import from_csv_to_dict, filter_by_location, filter_by_last_seen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", "-d", default=7, type=int, help="Filter by last seen in days")
    parser.add_argument("--country", "-c", default="germany", type=str, help="Filter by country")
    args = parser.parse_args()

    try:
        positions_filepath = list(Path('.').glob('*.csv'))[0]
    except IndexError:
        raise Exception("File from PhD Seeker was not found.")
    data = from_csv_to_dict(positions_filepath)
    filtered_data = filter_by_location(data, args.country)
    filtered_data = filter_by_last_seen(filtered_data, args.days)
    for position in filtered_data:
        print(position["country"], position["title"], position["last_seen"], position["link"])


if __name__ == "__main__":
    main()
