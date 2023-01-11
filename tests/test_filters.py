from datetime import date

import pytest
from freezegun import freeze_time

from psn.filters import (
    filter_by_last_seen,
    filter_by_location,
    from_csv_to_dict,
    from_last_seen_to_date,
)

positions_filepath = (
    "tests/fixtures/PhD_Positions_2023-01-10"
    "[Computer Science, Machine Learning, Deep Learning].csv"
)


def test_from_csv_to_dict():
    data = from_csv_to_dict(positions_filepath)
    expected_keys = {"country", "last_seen", "title", "link"}
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert set(data[0].keys()) == expected_keys


def test_filter_by_location():
    data = from_csv_to_dict(positions_filepath)
    filtered_data = filter_by_location(data, "germany")
    assert data != filtered_data
    for position in filtered_data:
        assert position["country"].lower() == "germany"


@freeze_time("2023-01-01 14:21:34")
@pytest.mark.parametrize(
    "last_seen,expected_date",
    [
        ("about 10 hours ago", date(2023, 1, 1)),
        ("2 months ago", date(2022, 11, 2)),
        ("1 day ago", date(2022, 12, 31)),
        ("about 1 month ago", date(2022, 12, 2)),
        ("28 days ago", date(2022, 12, 4)),
        ("44 minutes ago", date(2023, 1, 1)),
        ("about 1 hour ago", date(2023, 1, 1)),
        ("about 1 year ago", date(2022, 1, 1)),
        ("about 2 years ago", date(2021, 1, 1)),
        ("about 1 second ago", date(2023, 1, 1)),
        ("about 10 seconds ago", date(2023, 1, 1)),
    ],
)
def test_from_last_seen_to_date(last_seen, expected_date):
    assert from_last_seen_to_date(last_seen) == expected_date


@freeze_time("2023-01-10 20:21:34")
def test_filter_by_last_seen():
    data = from_csv_to_dict(positions_filepath)
    filtered_data = filter_by_last_seen(data, 1)  # last day
    assert data != filtered_data
    for position in filtered_data:
        assert "hour" in position["last_seen"] or "minute" in position["last_seen"]
