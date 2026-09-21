# -*- coding: utf-8 -*-
"""Compare the shipped table against the pages it was copied from.

Every other command here works offline and says so. This one is the exception,
and it is opt-in for that reason: it is the answer to "is this table still
what the provider publishes", which cannot be answered without asking the
provider.

What it reports is deliberately narrow. It does not re-parse three differently
shaped pages into a new table - that would be a second implementation to keep
right, and a wrong one would be worse than a stale table. It reports two facts
that are cheap to establish and hard to get wrong:

  * an identifier in our table that no longer appears on the page at all,
    which usually means the provider dropped the row after the model was
    switched off;
  * an identifier the page names that our table has never heard of, which is
    the case that matters - it is a retirement we are not warning anybody
    about.

Both are reported as questions for a human, not as errors. The tool cannot
tell a genuinely new retirement from a model merely mentioned in prose.
"""

from __future__ import annotations

import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from .table import BY_MODEL, SOURCES

USER_AGENT = "model-eol/0.1 (+https://github.com/dkautomation23/model-eol)"
TIMEOUT = 20

# Identifiers each provider actually uses, kept deliberately loose: this is a
# presence check, not a parser. Anything caught here is shown to a person.
#
# The lookbehind rather than \b: a hyphen counts as a word boundary, so
# `\bbabbage-code-001` matches happily inside `code-search-babbage-code-001`
# and reports a fragment of another model's name as an unknown one.
ID_CHAR = "A-Za-z0-9._-"
_EDGE = rf"(?<![{ID_CHAR}])"

# Bare family names, which appear in prose on every one of these pages.
FAMILY_WORDS = {"gpt", "o1", "o3", "o4", "claude", "gemini", "davinci", "babbage",
                "whisper", "chatgpt", "text-embedding"}
IDENTIFIER = {
    "OpenAI": re.compile(
        _EDGE + r"(?:ft-)?(?:gpt|o[1-4]|davinci|babbage|whisper|chatgpt|computer-use"
                r"|text-embedding)[A-Za-z0-9.\-]*"),
    "Anthropic": re.compile(_EDGE + r"claude-[A-Za-z0-9.\-]+"),
    "Google": re.compile(_EDGE + r"gemini-[A-Za-z0-9.\-]+"),
}


@dataclass(frozen=True)
class Comparison:
    provider: str
    url: str
    ok: bool
    missing: tuple = ()      # in our table, not on the page
    unknown: tuple = ()      # on the page, not in our table
    error: str = ""


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:  # noqa: S310
        raw = response.read()
    return raw.decode("utf-8", errors="replace")


def strip_markup(html: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", text)


def compare(provider: str, url: str, html: str) -> Comparison:
    text = strip_markup(html)
    on_page = set(IDENTIFIER[provider].findall(text))
    ours = {model for model, entry in BY_MODEL.items() if entry.provider == provider}

    # Presence is checked on a token edge, not as a substring. A page that
    # mentions only `gpt-4o` used to convince this that `gpt-4` was present as
    # well, because one name contains the other - the same prefix problem the
    # scanner solves, arriving from the other side.
    def present(name: str) -> bool:
        pattern = re.compile(rf"(?<![{ID_CHAR}]){re.escape(name)}(?![{ID_CHAR}])")
        return pattern.search(text) is not None

    missing = sorted(model for model in ours if not present(model))
    # A model this table names as a replacement is a live one by definition:
    # reporting it as "unknown" every run is noise, and noise is how a check
    # gets ignored. Same for anything too short to be a real identifier - a
    # page mentioning "gpt" in a sentence is not a retirement row.
    replacements = {word
                    for entry in BY_MODEL.values()
                    for word in entry.replacement.replace(" or ", " ").split()}
    # No length filter. `len(name) > 12` was quietly dropping every short new
    # name: a `gpt-6` appearing on the page would never have been reported.
    # What is actually being excluded is a bare family prefix - `gpt`, `o1`,
    # `claude` - which is a word in a sentence rather than a model id.
    unknown = sorted(
        name for name in on_page
        if name not in BY_MODEL
        and name not in replacements
        and not name.endswith("-")
        and any(char.isdigit() for char in name)
        and name not in FAMILY_WORDS
    )
    return Comparison(provider, url, True, tuple(missing), tuple(unknown))


def check_all() -> list:
    results = []
    for provider, url in SOURCES.items():
        try:
            html = fetch(url)
        except (urllib.error.URLError, OSError, ValueError) as error:
            results.append(Comparison(provider, url, False, error=str(error)))
            continue
        results.append(compare(provider, url, html))
    return results
