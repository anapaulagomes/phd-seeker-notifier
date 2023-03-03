from datetime import datetime
from time import mktime
import feedparser


def from_struct_time_to_date(struct):
    return datetime.fromtimestamp(mktime(struct)).date()


def fix_link(link):
    if link.count("https://www.daad.de") > 1:
        return link.replace("https://www.daad.de", "", 1)
    return link


def fetch_positions():
    entries = feedparser.parse("https://api.daad.de/api/feeds/rss/de/phd.xml")["entries"]
    positions = []

    for entry in entries:
        positions.append({
            "country": "Germany",
            "last_seen": from_struct_time_to_date(entry["published_parsed"]),
            "title": entry["title"],
            "link": fix_link(entry["link"]),
            "summary": entry["summary"],
            "source": "DAAD",
        })
    return positions
