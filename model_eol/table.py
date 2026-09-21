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
    Retirement("o4-mini-2025-04-16", date(2026, 10, 23), "gpt-5.6-terra"),
    Retirement("o4-mini", date(2026, 10, 23), "gpt-5.6-terra"),
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

RETIREMENTS += (
    # Whole families the first hand-copy missed: audio, realtime, transcribe and
    # image, plus two chat snapshots. Found by --check-source, which is what that
    # command is for - 18 dated rows the table had never heard of, while every
    # date it did have matched the page exactly.
    Retirement("gpt-5.2-chat-latest", date(2026, 8, 10), "gpt-5.6-sol"),
    Retirement("gpt-5.3-chat-latest", date(2026, 8, 10), "gpt-5.6-sol"),
    Retirement("chatgpt-image-latest", date(2026, 12, 1), "gpt-image-2"),
    Retirement("gpt-image-1-mini", date(2026, 12, 1), "gpt-image-2"),
    Retirement("gpt-image-1.5", date(2026, 12, 1), "gpt-image-2"),
    Retirement("gpt-4o-audio", date(2027, 1, 20), "gpt-audio-1.5"),
    Retirement("gpt-4o-mini-audio", date(2027, 1, 20), "gpt-audio-1.5"),
    Retirement("gpt-4o-mini-realtime", date(2027, 1, 20), "gpt-realtime-2.1-mini"),
    Retirement("gpt-4o-mini-transcribe-2025-03-20", date(2027, 1, 20), "gpt-4o-mini-transcribe-2025-12-15"),
    Retirement("gpt-4o-realtime", date(2027, 1, 20), "gpt-realtime-2.1"),
    Retirement("gpt-audio", date(2027, 1, 20), "gpt-audio-1.5"),
    Retirement("gpt-audio-mini", date(2027, 1, 20), "gpt-audio-1.5"),
    Retirement("gpt-realtime", date(2027, 1, 20), "gpt-realtime-2.1"),
    Retirement("gpt-realtime-mini", date(2027, 1, 20), "gpt-realtime-2.1-mini"),
    Retirement("gpt-4o-mini-transcribe", date(2027, 2, 26), "gpt-live-transcribe or gpt-transcribe"),
    Retirement("gpt-4o-transcribe", date(2027, 2, 26), "gpt-live-transcribe or gpt-transcribe"),
    Retirement("gpt-4o-transcribe-diarize", date(2027, 2, 26), "gpt-live-transcribe or gpt-transcribe"),
    Retirement("whisper-1", date(2027, 2, 26), "gpt-live-transcribe or gpt-transcribe"),
)
RETIREMENTS += (
    # Everything else the page dates, including what is already gone. A model
    # switched off two years ago is the most useful thing this tool can find:
    # the call in that codebase is failing right now. Retired API endpoints are
    # left out - this matches model identifiers, and a path is not one.
    Retirement("code-cushman-001", date(2023, 3, 23), "gpt-4o"),
    Retirement("code-cushman-002", date(2023, 3, 23), "gpt-4o"),
    Retirement("code-davinci-001", date(2023, 3, 23), "gpt-4o"),
    Retirement("code-davinci-002", date(2023, 3, 23), "gpt-4o"),
    Retirement("ada", date(2024, 1, 4), "babbage-002"),
    Retirement("babbage", date(2024, 1, 4), "babbage-002"),
    Retirement("code-davinci-edit-001", date(2024, 1, 4), "gpt-4o"),
    Retirement("code-search-ada-code-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("code-search-ada-text-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("code-search-babbage-code-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("code-search-babbage-text-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("curie", date(2024, 1, 4), "davinci-002"),
    Retirement("davinci", date(2024, 1, 4), "davinci-002 , gpt-3.5-turbo , gpt-4o"),
    Retirement("text-ada-001", date(2024, 1, 4), "gpt-3.5-turbo-instruct"),
    Retirement("text-babbage-001", date(2024, 1, 4), "gpt-3.5-turbo-instruct"),
    Retirement("text-curie-001", date(2024, 1, 4), "gpt-3.5-turbo-instruct"),
    Retirement("text-davinci-001", date(2024, 1, 4), "gpt-3.5-turbo-instruct"),
    Retirement("text-davinci-002", date(2024, 1, 4), "gpt-3.5-turbo-instruct"),
    Retirement("text-davinci-003", date(2024, 1, 4), "gpt-3.5-turbo-instruct"),
    Retirement("text-davinci-edit-001", date(2024, 1, 4), "gpt-4o"),
    Retirement("text-search-ada-doc-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-search-ada-query-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-search-babbage-doc-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-search-babbage-query-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-search-curie-doc-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-search-curie-query-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-search-davinci-doc-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-search-davinci-query-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-similarity-ada-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-similarity-babbage-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-similarity-curie-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("text-similarity-davinci-001", date(2024, 1, 4), "text-embedding-3-small"),
    Retirement("gpt-4-0314", date(2024, 6, 13), "gpt-4o", "date given as 'at earliest'"),
    Retirement("gpt-3.5-turbo-0301", date(2024, 9, 13), "gpt-3.5-turbo"),
    Retirement("gpt-3.5-turbo-0613", date(2024, 9, 13), "gpt-3.5-turbo"),
    Retirement("gpt-3.5-turbo-16k-0613", date(2024, 9, 13), "gpt-3.5-turbo"),
    Retirement("gpt-4-1106-vision-preview", date(2024, 12, 6), "gpt-4o"),
    Retirement("gpt-4-vision-preview", date(2024, 12, 6), "gpt-4o"),
    Retirement("gpt-4-32k", date(2025, 6, 6), "gpt-4o"),
    Retirement("gpt-4-32k-0314", date(2025, 6, 6), "gpt-4o"),
    Retirement("gpt-4-32k-0613", date(2025, 6, 6), "gpt-4o"),
    Retirement("gpt-4.5-preview", date(2025, 7, 14), "gpt-4.1"),
    Retirement("o1-preview", date(2025, 7, 28), "o3"),
    Retirement("gpt-4o-audio-preview-2024-10-01", date(2025, 10, 10), "gpt-audio-1.5"),
    Retirement("gpt-4o-realtime-preview-2024-10-01", date(2025, 10, 10), "gpt-realtime-1.5"),
    Retirement("o1-mini", date(2025, 10, 27), "o4-mini"),
    Retirement("text-moderation-007", date(2025, 10, 27), "omni-moderation"),
    Retirement("text-moderation-latest", date(2025, 10, 27), "omni-moderation"),
    Retirement("text-moderation-stable", date(2025, 10, 27), "omni-moderation"),
    Retirement("codex-mini-latest", date(2026, 2, 12), "gpt-5-codex-mini"),
    Retirement("chatgpt-4o-latest", date(2026, 2, 17), "gpt-5.1-chat-latest"),
    Retirement("gpt-4o-audio-preview", date(2026, 5, 7), "gpt-audio-1.5"),
    Retirement("gpt-4o-mini-audio-preview", date(2026, 5, 7), "gpt-audio-mini"),
    Retirement("gpt-4o-mini-realtime-preview", date(2026, 5, 7), "gpt-realtime-mini"),
    Retirement("gpt-4o-realtime-preview", date(2026, 5, 7), "gpt-realtime-1.5"),
    Retirement("gpt-4o-realtime-preview-2024-12-17", date(2026, 5, 7), "gpt-realtime-1.5"),
    Retirement("gpt-4o-realtime-preview-2025-06-03", date(2026, 5, 7), "gpt-realtime-1.5"),
    Retirement("dall-e-2", date(2026, 5, 12), "gpt-image-2 , gpt-image-1 , or gpt-image-1-mini"),
    Retirement("dall-e-3", date(2026, 5, 12), "gpt-image-2 , gpt-image-1 , or gpt-image-1-mini"),
    Retirement("sora-2", date(2026, 9, 24), ""),
    Retirement("sora-2-2025-10-06", date(2026, 9, 24), ""),
    Retirement("sora-2-2025-12-08", date(2026, 9, 24), ""),
    Retirement("sora-2-pro", date(2026, 9, 24), ""),
    Retirement("sora-2-pro-2025-10-06", date(2026, 9, 24), ""),
)
RETIREMENTS += (
    # A second pass of the same --check-source, after the extractor learned to
    # read a non-breaking hyphen in a date, a month spelled in full, and a cell
    # naming two more identifiers in a parenthesis. The 23 July 2026 batch -
    # deep-research, codex, computer-use - has already gone.
    Retirement("computer-use-preview", date(2026, 7, 23), "gpt-5.6-terra"),
    Retirement("computer-use-preview-2025-03-11", date(2026, 7, 23), "gpt-5.6-terra"),
    Retirement("gpt-4o-mini-search-preview-2025-03-11", date(2026, 7, 23), "gpt-5.6-terra"),
    Retirement("gpt-4o-search-preview-2025-03-11", date(2026, 7, 23), "gpt-5.6-terra"),
    Retirement("gpt-5-chat-latest", date(2026, 7, 23), "gpt-5.6-sol"),
    Retirement("gpt-5-codex", date(2026, 7, 23), "gpt-5.6-sol"),
    Retirement("gpt-5.1-chat-latest", date(2026, 7, 23), "gpt-5.6-sol"),
    Retirement("gpt-5.1-codex", date(2026, 7, 23), "gpt-5.6-sol"),
    Retirement("gpt-5.1-codex-max", date(2026, 7, 23), "gpt-5.6-sol"),
    Retirement("gpt-5.1-codex-mini", date(2026, 7, 23), "gpt-5.6-terra"),
    Retirement("gpt-5.2-codex", date(2026, 7, 23), "gpt-5.6-sol"),
    Retirement("gpt-audio-mini-2025-10-06", date(2026, 7, 23), "gpt-audio-1.5"),
    Retirement("gpt-realtime-mini-2025-10-06", date(2026, 7, 23), "gpt-realtime-2.1-mini"),
    Retirement("o3-deep-research", date(2026, 7, 23), "gpt-5.6-sol"),
    Retirement("o3-deep-research-2025-06-26", date(2026, 7, 23), "gpt-5.6-sol"),
    Retirement("o4-mini-deep-research", date(2026, 7, 23), "gpt-5.6-sol"),
    Retirement("o4-mini-deep-research-2025-06-26", date(2026, 7, 23), "gpt-5.6-sol"),
)
RETIREMENTS += (
    # The last three the parser could not reach. Their row writes the date with
    # U+2010 HYPHEN rather than an ASCII one, and names two more identifiers in
    # a parenthesis inside the model cell: "gpt-4-0125-preview (including
    # gpt-4-turbo-preview and gpt-4-turbo-preview-completions, which point to
    # this snapshot)". Copied by hand, like the rest of the table was.
    Retirement("gpt-4-0125-preview", date(2026, 3, 26), "gpt-5 or gpt-4.1"),
    Retirement("gpt-4-turbo-preview", date(2026, 3, 26), "gpt-5 or gpt-4.1"),
    Retirement("gpt-4-turbo-preview-completions", date(2026, 3, 26), "gpt-5 or gpt-4.1"),
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
)
