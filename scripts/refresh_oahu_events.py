#!/usr/bin/env python3
"""Daily conservative event feed: published curated dates, expiry, no invented listings."""
import json
from datetime import datetime, date, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
root=Path(__file__).resolve().parents[1]
source=root/"data"/"oahu-events-curated.json"
dest=root/"data"/"oahu-events-current.json"
today=datetime.now(ZoneInfo("Pacific/Honolulu")).date()
entries=json.loads(source.read_text(encoding="utf-8"))
current=[]
for event in entries:
    try:
        start=date.fromisoformat(event["start"])
        end=date.fromisoformat(event["end"])
        url=event["url"]
        if not url.startswith("https://") or end<start or not event["title"].strip():
            continue
        if end>=today:
            current.append(event)
    except (ValueError,KeyError,TypeError):
        continue
current.sort(key=lambda e:e["start"])
payload={"as_of_hawaii":today.isoformat(),"updated_utc":datetime.now(timezone.utc).isoformat(),"source_type":"curated official/organizer links, not a live API","events":current}
dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"{len(current)} current curated events; Hawaii date {today}")
