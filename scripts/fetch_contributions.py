#!/usr/bin/env python3
import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "Meet141106"
OUT = Path("data/contributions.json")
URL = f"https://github.com/users/{USERNAME}/contributions"


def main():
    response = requests.get(URL, timeout=30, headers={"User-Agent": "Meet141106-profile-art/1.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        date = cell.get("data-date")
        level = int(cell.get("data-level", "0"))
        count = 0
        label = cell.get("aria-label", "")
        match = re.search(r"(\d+) contribution", label)
        if match:
            count = int(match.group(1))
        days.append({"date": date, "count": count, "level": level})
    if not days:
        raise RuntimeError("No contribution cells found. GitHub may have changed its public contribution HTML.")

    counts = [d["count"] for d in days]
    current = 0
    for d in reversed(days):
        if d["count"] > 0:
            current += 1
        elif current:
            break
    longest = best = run = 0
    best_day = None
    for d in days:
        if d["count"]:
            run += 1
            longest = max(longest, run)
            if d["count"] > best:
                best = d["count"]
                best_day = d["date"]
        else:
            run = 0

    months = {}
    for d in days:
        month = d["date"][:7]
        months[month] = months.get(month, 0) + d["count"]

    payload = {
        "username": USERNAME,
        "fetched_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "days": days,
        "stats": {
            "total": sum(counts),
            "current_streak": current,
            "longest_streak": longest,
            "best_day": best_day,
            "best_day_count": best,
            "active_days": sum(1 for c in counts if c > 0),
        },
        "monthly_totals": months,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Fetched {len(days)} contribution days; total={payload['stats']['total']}")


if __name__ == "__main__":
    main()
