import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from psn.notify import send_email
from psn.sources.phd_seeker.filters import filter_by_last_seen, filter_by_location
from psn.sources.phd_seeker.adapters import from_csv_to_dict


def print_found_positions(country, last_seen_in_days, positions):
    table = Table(title=f"PhD positions in {country} (last {last_seen_in_days} days)")

    table.add_column("Country", justify="center", style="cyan", no_wrap=True)
    table.add_column("Last Seen", justify="center", style="cyan", no_wrap=True)
    table.add_column("Title", justify="left", style="magenta")
    table.add_column("Link", justify="left", style="green")

    for position in positions:
        table.add_row(
            position["country"],
            position["last_seen"],
            position["title"],
            f"[link={position['link']}]here[/]",
        )

    console = Console()
    console.print(table)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--days", "-d", default=7, type=int, help="Filter by last seen in days"
    )
    parser.add_argument(
        "--country", "-c", default="germany", type=str, help="Filter by country"
    )
    args = parser.parse_args()

    try:
        positions_filepath = list(Path(".").glob("*.csv"))[0]
    except IndexError:
        raise Exception("File from PhD Seeker was not found.")
    data = from_csv_to_dict(positions_filepath)
    filtered_data = filter_by_location(data, args.country)
    filtered_data = filter_by_last_seen(filtered_data, args.days)
    print_found_positions(args.country, args.days, filtered_data)
    send_email(filtered_data, args.country)


if __name__ == "__main__":
    main()
