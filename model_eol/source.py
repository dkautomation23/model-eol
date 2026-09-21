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
IDENTIFIER = {
    "OpenAI": re.compile(r"\b(?:ft-)?(?:gpt|o[1-4]|davinci|babbage|text-embedding)[A-Za-z0-9.\-]*"),
    "Anthropic": re.compile(r"\bclaude-[A-Za-z0-9.\-]+"),
    "Google": re.compile(r"\bgemini-[A-Za-z0-9.\-]+"),
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

    # Presence is checked by looking for the name itself, not by asking whether
    # the identifier regex produced it. The regex is a net for names we have
    # never seen; using it here reported `ada`, `whisper-1` and forty-two
    # others as gone from a page that plainly lists them.
    missing = sorted(model for model in ours if model not in text)
    # A model this table names as a replacement is a live one by definition:
    # reporting it as "unknown" every run is noise, and noise is how a check
    # gets ignored. Same for anything too short to be a real identifier - a
    # page mentioning "gpt" in a sentence is not a retirement row.
    replacements = {word
                    for entry in BY_MODEL.values()
                    for word in entry.replacement.replace(" or ", " ").split()}
    unknown = sorted(
        name for name in on_page
        if name not in BY_MODEL
        and name not in replacements
        and len(name) > 12
        and not name.endswith("-")
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
