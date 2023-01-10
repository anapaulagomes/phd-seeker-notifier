from psn.filters import filter_by_location, from_csv_to_dict


positions_filepath = "tests/fixtures/PhD_Positions_2023-01-10[Computer Science, Machine Learning, Deep Learning].csv"


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
