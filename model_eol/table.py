# -*- coding: utf-8 -*-
"""The retirement table, and the date it was copied.

A tool that carries a stale table and says nothing is worse than no tool: the
answer looks authoritative and is wrong. So the snapshot date and the source URL
are printed in every report, and `--check-source` compares this file against the
live page.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

SOURCE = "https://developers.openai.com/api/docs/deprecations"
SNAPSHOT = date(2026, 9, 21)
"""When this table was copied from SOURCE, by hand, entry by entry."""


@dataclass(frozen=True)
class Retirement:
    model: str
    shutdown: date
    replacement: str
    note: str = ""


# Verbatim from SOURCE. Every identifier listed under a date is its own entry,
# because "gpt-4-turbo" and "gpt-4-turbo-2024-04-09" are different strings in a
# codebase even when they die together.
RETIREMENTS: tuple[Retirement, ...] = (
    # 2026-09-28
    Retirement("gpt-3.5-turbo-instruct", date(2026, 9, 28), "gpt-5.6-terra"),
    Retirement("babbage-002", date(2026, 9, 28), "gpt-5.6-terra"),
    Retirement("davinci-002", date(2026, 9, 28), "gpt-5.6-terra"),
    Retirement("gpt-3.5-turbo-1106", date(2026, 9, 28), "gpt-5.6-terra"),
    # 2026-10-01
    Retirement("gpt-5.4-cyber", date(2026, 10, 1), "gpt-5.6-cyber"),
    # 2026-10-23
    Retirement("gpt-3.5-turbo-0125", date(2026, 10, 23), "gpt-5.6-terra"),
    Retirement("gpt-3.5-turbo", date(2026, 10, 23), "gpt-5.6-terra"),
    Retirement("gpt-3.5-turbo-completions", date(2026, 10, 23), "gpt-5.6-terra"),
    Retirement("gpt-4-0613", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("gpt-4", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("gpt-4-0613-completions", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("gpt-4-completions", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("gpt-4-1106-preview", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("gpt-4-turbo", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("gpt-4-turbo-2024-04-09", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("gpt-4-turbo-completions", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("gpt-4.1-nano", date(2026, 10, 23), "gpt-5.6-luna"),
    Retirement("gpt-4.1-nano-2025-04-14", date(2026, 10, 23), "gpt-5.6-luna"),
    Retirement("gpt-4o-2024-05-13", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("gpt-image-1", date(2026, 10, 23), "gpt-image-2"),
    Retirement("o1-2024-12-17", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("o1", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("o1-pro-2025-03-19", date(2026, 10, 23), "gpt-5.6-sol",
               "replacement needs reasoning.mode: pro"),
    Retirement("o1-pro", date(2026, 10, 23), "gpt-5.6-sol",
               "replacement needs reasoning.mode: pro"),
    Retirement("o3-mini-2025-01-31", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("o3-mini", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("ft-o4-mini-2025-04-16", date(2026, 10, 23), "gpt-5.6-terra"),
    Retirement("o4-mini-2025-04-16", date(2026, 10, 23), "gpt-5.6-terra"),
    Retirement("o4-mini", date(2026, 10, 23), "gpt-5.6-terra"),
    Retirement("ft-gpt-3.5-turbo", date(2026, 10, 23), "gpt-5.6-terra"),
    Retirement("ft-gpt-4", date(2026, 10, 23), "gpt-5.6-sol"),
    Retirement("ft-gpt-4.1-nano-2025-04-14", date(2026, 10, 23), "gpt-5.6-luna"),
    Retirement("ft-babbage-002", date(2026, 10, 23), "gpt-5.6-terra"),
    Retirement("ft-davinci-002", date(2026, 10, 23), "gpt-5.6-terra"),
    # 2026-12-11
    Retirement("gpt-5-2025-08-07", date(2026, 12, 11), "gpt-5.6-sol"),
    Retirement("gpt-5-mini-2025-08-07", date(2026, 12, 11), "gpt-5.6-terra"),
    Retirement("gpt-5-nano-2025-08-07", date(2026, 12, 11), "gpt-5.6-luna"),
    Retirement("gpt-5-pro-2025-10-06", date(2026, 12, 11), "gpt-5.6-sol",
               "replacement needs reasoning.mode: pro"),
    Retirement("o3-2025-04-16", date(2026, 12, 11), "gpt-5.6-sol"),
    Retirement("o3-pro-2025-06-10", date(2026, 12, 11), "gpt-5.6-sol",
               "replacement needs reasoning.mode: pro"),
)

BY_MODEL = {r.model: r for r in RETIREMENTS}

# Live identifiers that a naive search mistakes for a retired one, because a
# retired id is a prefix of them. Kept here so the false positive the matcher
# must not produce is written down and tested.
LIVE_LOOKALIKES = (
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-5.6-sol",
    "gpt-5.6-terra",
    "gpt-5.6-luna",
    "gpt-5.6-cyber",
    "o3-deep-research",
    "o1-mini",
)
