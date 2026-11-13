"""Validate the production Atom feed; run from the repository root."""

from datetime import datetime
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ns = {"a": "http://www.w3.org/2005/Atom"}
feed = ET.parse("_site/feed.xml").getroot()
assert feed.tag == "{http://www.w3.org/2005/Atom}feed"

def required(element, path):
    value = element.findtext(path, namespaces=ns)
    assert value and value.strip(), f"Missing or empty {path}"
    return value.strip()

def canonical(url):
    parts = urlsplit(url)
    assert parts.scheme == "https" and parts.netloc == "ctk21.github.io", url

for field in ("title", "id", "updated"):
    required(feed, f"a:{field}")
assert required(feed, "a:id") == "https://ctk21.github.io/feed.xml", "Incorrect feed ID"
for relation, expected in (
    ("self", "https://ctk21.github.io/feed.xml"),
    ("alternate", "https://ctk21.github.io/"),
):
    link = feed.find(f"a:link[@rel='{relation}']", ns)
    assert link is not None, f"Missing feed {relation} link"
    assert link.get("href") == expected, f"Incorrect feed {relation} URL"
datetime.fromisoformat(required(feed, "a:updated").replace("Z", "+00:00"))
entries = feed.findall("a:entry", ns)
assert entries, "Feed has no entries"
ids = []
for entry in entries:
    required(entry, "a:title")
    author = entry.find("a:author", ns)
    if author is None:
        author = feed.find("a:author", ns)
    assert author is not None, "Missing author"
    required(author, "a:name")
    ids.append(required(entry, "a:id"))
    for field in ("published", "updated"):
        datetime.fromisoformat(required(entry, f"a:{field}").replace("Z", "+00:00"))
    link = entry.find("a:link[@rel='alternate']", ns)
    assert link is not None, "Missing article link"
    canonical(link.get("href", ""))

assert len(ids) == len(set(ids)), "Duplicate entry IDs"
print(f"Validated {len(entries)} Atom entries")
