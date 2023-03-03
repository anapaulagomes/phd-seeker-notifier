import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from psn.notify import send_email
from psn.sources.daad import fetch_positions
from psn.filters import filter_by_last_seen, filter_by_location, filter_by_topics
from psn.sources.phd_seeker.adapters import from_csv_to_dict


def print_found_positions(country, last_seen_in_days, positions):
    table = Table(title=f"PhD positions in {country} (last {last_seen_in_days} days)")

    table.add_column("Country", justify="center", style="cyan", no_wrap=True)
    table.add_column("Last Seen", justify="center", style="cyan", no_wrap=True)
    table.add_column("Title", justify="left", style="magenta")
    table.add_column("Source", justify="center", style="cyan")
    table.add_column("Link", justify="left", style="green")

    for position in positions:
        table.add_row(
            position["country"],
            str(position["last_seen"]),
            position["title"],
            position["source"],
            position['link'],
            # f"[link={position['link']}]here[/]",
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
    parser.add_argument(
        "--sources", "-s", type=str, help="Sources splitted by comma",
        default="phd_seeker,daad"
    )
    parser.add_argument(
        "--send-email", "-e", action="store_true", help="Send e-mail"
    )
    args = parser.parse_args()
    positions = []

    if "phd_seeker" in args.sources:
        try:
            positions_filepath = list(Path(".").glob("*.csv"))[0]
        except IndexError:
            raise Exception("File from PhD Seeker was not found.")
        positions.extend(from_csv_to_dict(positions_filepath))
    if "daad" in args.sources:
        positions.extend(filter_by_topics(fetch_positions()))

    filtered_data = filter_by_location(positions, args.country)
    filtered_data = filter_by_last_seen(filtered_data, args.days)
    print_found_positions(args.country, args.days, filtered_data)

    if args.send_email:
        send_email(filtered_data, args.country)


if __name__ == "__main__":
    main()
