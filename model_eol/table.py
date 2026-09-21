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

SOURCES = {
    "OpenAI": "https://developers.openai.com/api/docs/deprecations",
    "Anthropic": "https://docs.anthropic.com/en/docs/about-claude/model-deprecations",
    "Google": "https://ai.google.dev/gemini-api/docs/deprecations",
}
SOURCE = SOURCES["OpenAI"]
"""Kept for callers written before the second and third provider existed."""

SNAPSHOT = date(2026, 9, 21)
"""When these tables were copied from SOURCES, entry by entry."""


@dataclass(frozen=True)
class Retirement:
    model: str
    shutdown: date
    replacement: str
    note: str = ""
    provider: str = "OpenAI"


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

RETIREMENTS += (
    # Anthropic. Retirement date and replacement exactly as the page gives
    # them. Rows whose retirement reads "to be announced" are left out
    # rather than given a date this tool invented.
    Retirement("claude-1.0", date(2024, 11, 6), "claude-haiku-4-5-20251001", provider="Anthropic"),
    Retirement("claude-1.1", date(2024, 11, 6), "claude-haiku-4-5-20251001", provider="Anthropic"),
    Retirement("claude-1.2", date(2024, 11, 6), "claude-haiku-4-5-20251001", provider="Anthropic"),
    Retirement("claude-1.3", date(2024, 11, 6), "claude-haiku-4-5-20251001", provider="Anthropic"),
    Retirement("claude-instant-1.0", date(2024, 11, 6), "claude-haiku-4-5-20251001", provider="Anthropic"),
    Retirement("claude-instant-1.1", date(2024, 11, 6), "claude-haiku-4-5-20251001", provider="Anthropic"),
    Retirement("claude-instant-1.2", date(2024, 11, 6), "claude-haiku-4-5-20251001", provider="Anthropic"),
    Retirement("claude-2.0", date(2025, 7, 21), "claude-opus-4-8", provider="Anthropic"),
    Retirement("claude-2.1", date(2025, 7, 21), "claude-opus-4-8", provider="Anthropic"),
    Retirement("claude-3-sonnet-20240229", date(2025, 7, 21), "claude-sonnet-4-6", provider="Anthropic"),
    Retirement("claude-3-5-sonnet-20240620", date(2025, 10, 28), "claude-sonnet-4-6", provider="Anthropic"),
    Retirement("claude-3-5-sonnet-20241022", date(2025, 10, 28), "claude-sonnet-4-6", provider="Anthropic"),
    Retirement("claude-3-opus-20240229", date(2026, 1, 5), "claude-opus-4-8", provider="Anthropic"),
    Retirement("claude-3-5-haiku-20241022", date(2026, 2, 19), "claude-haiku-4-5-20251001", provider="Anthropic"),
    Retirement("claude-3-7-sonnet-20250219", date(2026, 2, 19), "claude-sonnet-4-6", provider="Anthropic"),
    Retirement("claude-3-haiku-20240307", date(2026, 4, 20), "claude-haiku-4-5-20251001", provider="Anthropic"),
    Retirement("claude-opus-4-20250514", date(2026, 6, 15), "claude-opus-4-8", provider="Anthropic"),
    Retirement("claude-sonnet-4-20250514", date(2026, 6, 15), "claude-sonnet-4-6", provider="Anthropic"),
    Retirement("claude-opus-4-1-20250805", date(2026, 8, 5), "claude-opus-4-8", provider="Anthropic"),
)

RETIREMENTS += (
    # Google. The page lists many models with "No shutdown date announced";
    # only rows carrying both a date and a replacement are here, for the same
    # reason.
    Retirement("gemini-embedding-exp", date(2025, 10, 30), "gemini-embedding-2", provider="Google"),
    Retirement("gemini-embedding-exp-03-07", date(2025, 10, 30), "gemini-embedding-2", provider="Google"),
    Retirement("gemini-2.0-flash-preview-image-generation", date(2025, 11, 14), "gemini-2.5-flash-image", provider="Google"),
    Retirement("gemini-2.5-flash-preview-05-20", date(2025, 11, 18), "gemini-3.6-flash", provider="Google"),
    Retirement("gemini-2.5-pro-preview-03-25", date(2025, 12, 2), "gemini-3.1-pro-preview", provider="Google"),
    Retirement("gemini-2.5-pro-preview-05-06", date(2025, 12, 2), "gemini-3.1-pro-preview", provider="Google"),
    Retirement("gemini-2.5-pro-preview-06-05", date(2025, 12, 2), "gemini-3.1-pro-preview", provider="Google"),
    Retirement("gemini-2.0-flash-lite-preview", date(2025, 12, 9), "gemini-2.5-flash-lite", provider="Google"),
    Retirement("gemini-2.0-flash-lite-preview-02-05", date(2025, 12, 9), "gemini-2.5-flash-lite", provider="Google"),
    Retirement("gemini-2.0-flash-live-001", date(2025, 12, 9), "gemini-3.8-live", provider="Google"),
    Retirement("gemini-live-2.5-flash-preview", date(2025, 12, 9), "gemini-3.8-live", provider="Google"),
    Retirement("gemini-2.5-flash-image-preview", date(2026, 1, 15), "gemini-2.5-flash-image", provider="Google"),
    Retirement("gemini-2.5-flash-preview-09-25", date(2026, 2, 17), "gemini-3.6-flash", provider="Google"),
    Retirement("gemini-3-pro-preview", date(2026, 3, 9), "gemini-3.1-pro-preview", provider="Google"),
    Retirement("gemini-2.5-flash-lite-preview-09-2025", date(2026, 3, 31), "gemini-3.1-flash-lite", provider="Google"),
    Retirement("gemini-robotics-er-1.5-preview", date(2026, 4, 30), "gemini-robotics-er-1.6-preview", provider="Google"),
    Retirement("gemini-3.1-flash-lite-preview", date(2026, 5, 25), "gemini-3.1-flash-lite", provider="Google"),
    Retirement("gemini-2.0-flash", date(2026, 6, 1), "gemini-3.6-flash", provider="Google"),
    Retirement("gemini-2.0-flash-001", date(2026, 6, 1), "gemini-3.6-flash", provider="Google"),
    Retirement("gemini-2.0-flash-lite", date(2026, 6, 1), "gemini-3.1-flash-lite", provider="Google"),
    Retirement("gemini-2.0-flash-lite-001", date(2026, 6, 1), "gemini-3.1-flash-lite", provider="Google"),
    Retirement("gemini-3-pro-image-preview", date(2026, 6, 25), "gemini-3-pro-image", provider="Google"),
    Retirement("gemini-3.1-flash-image-preview", date(2026, 6, 25), "gemini-3.1-flash-image", provider="Google"),
    Retirement("gemini-robotics-er-1.6-preview", date(2026, 8, 31), "gemini-robotics-er-2-preview", provider="Google"),
    Retirement("gemini-omni-flash-preview", date(2026, 9, 30), "gemini-omni-1.1-flash", provider="Google"),
    Retirement("gemini-2.5-flash-image", date(2026, 10, 2), "gemini-3.1-flash-image-preview", provider="Google"),
    Retirement("gemini-3.1-flash-lite", date(2027, 5, 7), "gemini-3.5-flash-lite", provider="Google"),
    Retirement("gemini-embedding-001", date(2028, 5, 14), "gemini-embedding-2", provider="Google"),
)

BY_MODEL = {r.model: r for r in RETIREMENTS}

# Live identifiers that a naive search mistakes for a retired one, because a
# retired id is a prefix of them. Kept here so the false positive the matcher
# must not produce is written down and tested.
LIVE_LOOKALIKES = (
    "claude-opus-4-5-20251101",
    "claude-sonnet-4-5-20250929",
    "claude-haiku-4-5-20251001",
    "claude-sonnet-4-6",
    "claude-opus-4-8",
    "gemini-3.6-flash",
    "gemini-2.5-flash",
    "gemini-embedding-2",
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
