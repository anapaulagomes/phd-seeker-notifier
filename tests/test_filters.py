from datetime import date

import pytest
from freezegun import freeze_time

from psn.filters import (
    filter_by_last_seen,
    filter_by_location, filter_by_topics,
)
from psn.sources.phd_seeker.adapters import from_csv_to_dict


positions_filepath = (
    "tests/fixtures/PhD_Positions_2023-01-10"
    "[Computer Science, Machine Learning, Deep Learning].csv"
)


def test_filter_by_location():
    data = from_csv_to_dict(positions_filepath)
    filtered_data = filter_by_location(data, "germany")
    assert data != filtered_data
    for position in filtered_data:
        assert position["country"].lower() == "germany"


@freeze_time("2023-01-10 20:21:34")
def test_filter_by_last_seen():
    data = from_csv_to_dict(positions_filepath)
    filtered_data = filter_by_last_seen(data, 1)  # last day
    assert data != filtered_data
    for position in filtered_data:
        assert position["last_seen"] is None or isinstance(position["last_seen"], date)


@pytest.mark.parametrize("positions,topics,number_of_expected_positions", [
    ([], "", 0),
    ([
         {
             "country": "Brazil",
             "last_seen": date(2023, 3, 13),
             "title": "Digital Twin Model for Coexistence of Wi-Fi and IoT in Smart Cities",
             "link": "https://toca.fm",
             "source": "PhD Dreams",
         },
         {
             "country": "Germany",
             "last_seen": date(2023, 3, 13),
             "title": "PhD in Computer Science",
             "summary": "Specialized in IoT",
             "link": "",
             "source": "PhD Seeker",
         }
     ], "iot, internet of things", 2),
    ([
         {
             "country": "Brazil",
             "last_seen": date(2023, 3, 13),
             "title": "Digital Twin Model for Coexistence of Wi-Fi and IoT in Smart Cities",
             "link": "https://toca.fm",
             "source": "PhD Dreams",
         },
         {
             "country": "Germany",
             "last_seen": date(2023, 3, 13),
             "title": "PhD in Computer Science",
             "summary": "Specialized in IoT",
             "link": "",
             "source": "PhD Seeker",
         }
     ], "NLP", 0),
    ([
         {
             "country": "UK",
             "last_seen": date(2023, 3, 13),
             "title": "Digital Twin Model for Coexistence of Wi-Fi and IoT in Smart Cities",
             "link": "https://toca.fm",
             "source": "PhD Dreams",
         },
         {
             "country": "Germany",
             "last_seen": date(2023, 3, 13),
             "title": "PhD in Computer Science",
             "summary": "Specialized in Internet of Things",
             "link": "",
             "source": "PhD Seeker",
         }
     ], "internet of things", 1)
])
def test_filter_by_topics(positions, topics, number_of_expected_positions):
    assert len(filter_by_topics(positions, topics)) == number_of_expected_positions
