#!/usr/bin/env python3
"""
Collect the live data every dynamic SVG needs and write data/contributions.json.

1. Daily contribution counts, scraped from GitHub's public, unauthenticated
   calendar fragment  https://github.com/users/<user>/contributions
   (the same HTML the profile page uses -- no token, no GraphQL).
2. A few profile facts (public repos, top languages) from the REST API.
   Uses $GITHUB_TOKEN when present (Actions provides it automatically) only to
   lift the rate limit; works anonymously too. If the API is unavailable the
   previous values are kept so the card never goes blank.

    python scripts/fetch_contributions.py
"""
import collections
import datetime as dt
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import USERNAME, DATA_PATH  # noqa: E402

UA = {"User-Agent": "vigneshwar-profile-readme/1.0"}
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def fetch_days():
    url = f"https://github.com/users/{USERNAME}/contributions"
    resp = requests.get(url, headers=UA, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        sys.exit("no calendar cells found -- GitHub markup may have changed")

    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue
        text = tips.get(td.get("id"), "")
        m = re.match(r"([\d,]+)", text)
        count = int(m.group(1).replace(",", "")) if m else 0
        days.append({"date": date, "count": count, "level": int(td.get("data-level") or 0)})
    days.sort(key=lambda d: d["date"])
    return days


def streaks(days):
    # current: today may not be "done" yet, so a zero today doesn't break it
    i = len(days) - 1
    if days[i]["count"] == 0:
        i -= 1
    end = i
    while i >= 0 and days[i]["count"] > 0:
        i -= 1
    cur = end - i
    current = {"length": cur, "start": days[i + 1]["date"] if cur else None,
               "end": days[end]["date"] if cur else None}

    best = run = 0
    best_rng = (None, None)
    start = 0
    for k, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                start = k
            run += 1
            if run > best:
                best, best_rng = run, (days[start]["date"], d["date"])
        else:
            run = 0
    return current, {"length": best, "start": best_rng[0], "end": best_rng[1]}


def fetch_profile(previous):
    headers = dict(UA, Accept="application/vnd.github+json")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        user = requests.get(f"https://api.github.com/users/{USERNAME}", headers=headers, timeout=30)
        user.raise_for_status()
        u = user.json()
        repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos",
                             params={"per_page": 100, "type": "owner", "sort": "pushed"},
                             headers=headers, timeout=30)
        repos.raise_for_status()
        rs = [r for r in repos.json() if not r.get("fork")]
        langs = collections.Counter(r["language"] for r in rs if r.get("language"))
        total = sum(langs.values()) or 1
        return {
            "public_repos": u.get("public_repos", 0),
            "followers": u.get("followers", 0),
            "member_since": (u.get("created_at") or "")[:4],
            "languages": [{"name": n, "share": round(c / total, 3)} for n, c in langs.most_common(5)],
            "last_push": rs[0]["pushed_at"][:10] if rs else None,
        }
    except Exception as exc:  # network / rate limit -> keep last good values
        print(f"profile API unavailable ({exc}); keeping previous values", file=sys.stderr)
        return previous or {"public_repos": None, "followers": None, "member_since": "",
                            "languages": [], "last_push": None}


def build(days, profile):
    total = sum(d["count"] for d in days)
    active = [d for d in days if d["count"] > 0]
    best = max(days, key=lambda d: d["count"])
    current, longest = streaks(days)

    by_wd = collections.Counter()
    for d in days:
        by_wd[dt.date.fromisoformat(d["date"]).weekday()] += d["count"]
    top_wd = WEEKDAYS[by_wd.most_common(1)[0][0]] if total else None

    last30 = sum(d["count"] for d in days[-30:])
    prev30 = sum(d["count"] for d in days[-60:-30])

    return {
        "username": USERNAME,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": len(active),
        "avg_per_active_day": round(total / len(active), 1) if active else 0,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "most_active_weekday": top_wd,
        "last_30_days": last30,
        "previous_30_days": prev30,
        "profile": profile,
        "days": days,
    }


if __name__ == "__main__":
    previous = None
    if os.path.exists(DATA_PATH):
        try:
            previous = json.load(open(DATA_PATH, encoding="utf-8")).get("profile")
        except Exception:
            pass
    data = build(fetch_days(), fetch_profile(previous))
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
    print(f"wrote data/contributions.json: {data['total_contributions']} contributions, "
          f"{data['active_days']} active days, streak {data['current_streak']['length']} / "
          f"longest {data['longest_streak']['length']}, repos {data['profile'].get('public_repos')}")
