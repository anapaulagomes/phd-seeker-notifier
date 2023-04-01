from datetime import date
from time import struct_time

from psn.sources.daad import from_struct_time_to_date, fetch_positions


def test_from_struct_time_to_date():
    struct = struct_time((2023, 3, 31, 10, 24, 26, 4, 90, 0))
    expected_date = date(2023, 3, 31)
    assert from_struct_time_to_date(struct) == expected_date


def test_fetch_positions():
    expected_keys = ["country", "last_seen", "title", "link", "summary", "source"]
    positions = fetch_positions()
    assert list(positions[0].keys()) == expected_keys
    assert positions[0]["country"] == "Germany"
    assert positions[0]["source"] == "DAAD"
    assert isinstance(positions[0]["last_seen"], date)
