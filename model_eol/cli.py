# -*- coding: utf-8 -*-
"""What in this repository stops working, when, and what replaces it.

    py -m model_eol.cli .
    py -m model_eol.cli . --within 30
    py -m model_eol.cli . --json report.json

Exit 0 when nothing retires inside the window, 1 when something does, 2 when the
question could not be asked - an unreadable path, a table older than the source.
A check that cannot run must not look like a pass.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .scan import group_by_date, scan
from .table import RETIREMENTS, SNAPSHOT, SOURCES


def _print_report(hits, today: date, within: int) -> int:
    print(f"model-eol - tables copied {SNAPSHOT.isoformat()}")
    for provider, url in SOURCES.items():
        print(f"  {provider:<10} {url}")
    age = (today - SNAPSHOT).days
    if age > 60:
        print(f"  WARNING: that table is {age} days old. Re-check the source before trusting it.")
    print()

    if not hits:
        print("No retired model identifiers found.")
        print("This says nothing about ids built at runtime from variables or config.")
        return 0

    grouped = group_by_date(hits)
    urgent = 0
    for shutdown, items in grouped.items():
        days = (shutdown - today).days
        when = f"in {days} days" if days > 0 else (
            "TODAY" if days == 0 else f"{abs(days)} days ago - already gone")
        print(f"{shutdown.isoformat()}  {when}")
        models = {}
        for hit in items:
            models.setdefault(hit.model, []).append(hit)
        for model, occurrences in sorted(models.items()):
            first = occurrences[0]
            chained = (f"  (which itself retires {first.replacement_dies.isoformat()})"
                       if first.replacement_dies else "")
            print(f"    [{first.provider}] {model}  ->  {first.replacement}{chained}"
                  f"   {len(occurrences)} occurrence(s)")
            for hit in occurrences[:3]:
                print(f"        {hit.path}:{hit.line}  {hit.text}")
            if len(occurrences) > 3:
                print(f"        ... and {len(occurrences) - 3} more")
        if days <= within:
            urgent += len(items)
        print()

    if urgent:
        print(f"{urgent} occurrence(s) retire within {within} days.")
        return 1
    print(f"Nothing retires within {within} days. The earliest is "
          f"{min(grouped).isoformat()}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(prog="model-eol", description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="file or directory to scan")
    parser.add_argument("--within", type=int, default=90,
                        help="exit 1 if something retires within this many days (default 90)")
    parser.add_argument("--json", type=Path, help="write the findings here")
    parser.add_argument("--list", action="store_true", help="print the table and exit")
    parser.add_argument("--today", help="pretend today is this ISO date, for tests")
    parser.add_argument("--exclude", action="append", default=[], metavar="GLOB",
                        help="skip paths matching this glob; repeatable. Use it for "
                             "documentation that lists model ids rather than calls them")
    args = parser.parse_args(argv)

    if args.list:
        print(f"{len(RETIREMENTS)} identifiers from {len(SOURCES)} providers, "
              f"copied {SNAPSHOT.isoformat()}")
        for provider, url in SOURCES.items():
            entries = [r for r in RETIREMENTS if r.provider == provider]
            print(f"\n{provider}  ({len(entries)} identifiers)  {url}")
            for r in sorted(entries, key=lambda r: (r.shutdown, r.model)):
                tail = f"  [{r.note}]" if r.note else ""
                print(f"  {r.shutdown.isoformat()}  {r.model:<40} -> {r.replacement}{tail}")
        return 0

    today = date.fromisoformat(args.today) if args.today else date.today()

    root = Path(args.path)
    if not root.exists():
        print(f"nothing to scan at {root}", file=sys.stderr)
        return 2

    hits = scan(root, tuple(args.exclude))

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps({
            "sources": SOURCES,
            "table_snapshot": SNAPSHOT.isoformat(),
            "scanned": str(root),
            "today": today.isoformat(),
            "within_days": args.within,
            "findings": [{
                "path": h.path, "line": h.line, "model": h.model,
                "provider": h.provider,
                "shutdown": h.shutdown.isoformat(), "replacement": h.replacement,
                "replacement_dies": (h.replacement_dies.isoformat()
                                     if h.replacement_dies else None),
                "days_left": (h.shutdown - today).days, "text": h.text,
            } for h in hits],
        }, indent=2), encoding="utf-8")

    return _print_report(hits, today, args.within)


if __name__ == "__main__":
    raise SystemExit(main())
