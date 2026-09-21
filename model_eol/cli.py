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
from .source import check_all
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


def _check_source() -> int:
    """Exit 0 when every page still matches, 1 when something needs a person,
    2 when a page could not be reached - a check that could not run must not
    read as a pass."""
    print(f"model-eol - comparing the table copied {SNAPSHOT.isoformat()} against the live pages")
    print()
    unreachable = questions = 0
    for result in check_all():
        print(f"{result.provider}  {result.url}")
        if not result.ok:
            print(f"  could not reach it: {result.error}")
            unreachable += 1
            print()
            continue
        if not result.missing and not result.unknown:
            print("  matches: every identifier in the table is still on the page, and the "
                  "page names none we do not have")
            print()
            continue
        if result.unknown:
            questions += len(result.unknown)
            print(f"  {len(result.unknown)} identifier(s) on the page that this table does "
                  f"not have - these are the ones that matter:")
            for name in result.unknown[:12]:
                print(f"      {name}")
            if len(result.unknown) > 12:
                print(f"      ... and {len(result.unknown) - 12} more")
        if result.missing:
            print(f"  {len(result.missing)} identifier(s) in the table the page no longer "
                  f"shows - usually a row dropped after the model was switched off:")
            for name in result.missing[:6]:
                print(f"      {name}")
            if len(result.missing) > 6:
                print(f"      ... and {len(result.missing) - 6} more")
        print()

    if unreachable:
        print(f"{unreachable} page(s) could not be read, so this says nothing about them.")
        return 2
    if questions:
        print(f"{questions} identifier(s) need a person to look. This cannot tell a new "
              f"retirement from a model merely mentioned in a sentence.")
        return 1
    print("The table still matches all three pages.")
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
    parser.add_argument("--check-source", action="store_true",
                        help="ask each provider's page whether this table is still what it "
                             "publishes. The only command here that uses the network")
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

    if args.check_source:
        return _check_source()

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
