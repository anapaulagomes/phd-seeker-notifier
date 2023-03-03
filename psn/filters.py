from datetime import datetime
from typing import List


def filter_by_location(positions: List[dict], country: str) -> List[dict]:
    filtered_data = []
    for position in positions:
        if position["country"].lower() == country.lower():
            filtered_data.append(position)
    return filtered_data


def filter_by_last_seen(positions: List[dict], days: int) -> List[dict]:
    filtered_data = []
    for position in positions:
        if not position["last_seen"]:
            filtered_data.append(position)
        elif (datetime.today().date() - position["last_seen"]).days < days:  # delta
            filtered_data.append(position)
    return filtered_data


def filter_by_topics(positions, topics=None):
    if not topics:
        topics = [
            "machine learning",
            "data science",
            "natural language processing",
            "nlp",
            "postdam",
            "berlin"
        ]
    filtered_data = []
    for position in positions:
        for topic in topics:
            in_title = topic in position["title"]
            in_summary = position.get("summary") and topic in position["summary"].lower()
            if in_title or in_summary:
                filtered_data.append(position)
    return filtered_data
