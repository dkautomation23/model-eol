# model-eol

[![CI](https://github.com/dkautomation23/model-eol/actions/workflows/ci.yml/badge.svg)](https://github.com/dkautomation23/model-eol/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/dkautomation23/model-eol/badge)](https://scorecard.dev/viewer/?uri=github.com/dkautomation23/model-eol)
[![CodeQL](https://github.com/dkautomation23/model-eol/actions/workflows/codeql.yml/badge.svg)](https://github.com/dkautomation23/model-eol/actions/workflows/codeql.yml)

What in this repository stops working, when, and what replaces it — across
OpenAI, Anthropic and Google.

```bash
py -m model_eol.cli .
```

Exit 0 when nothing retires inside the window, 1 when something does, 2 when the
question could not be asked. Python standard library only, no dependencies, no
API key, no account, no network call — the table ships with the tool.

## Why this exists

On **23 October 2026** OpenAI retires twenty-nine model identifiers in one day,
including `gpt-4-0613`, `gpt-4-turbo`, `o1`, `o3-mini` and `o4-mini`. Four more
went on **28 September**, twenty-five days earlier: `gpt-3.5-turbo-instruct`,
`babbage-002`, `davinci-002` and `gpt-3.5-turbo-1106`. On **11 December** the
`gpt-5` and `o3` snapshots follow. Counts come from the table itself —
`py -m model_eol.cli --list` prints every one with its date.

The scale is not a guess. GitHub code search, 21 September 2026:

| Identifier | Files on GitHub |
|---|---|
| `gpt-4-0613` | **96,640** |
| `gpt-4-turbo` in Python alone | 86,528 |
| `o1-preview` | 63,104 |
| `gpt-3.5-turbo-0301` | 57,088 |

Every one of those files is a hardcoded string that returns an error on a known
date. Nothing warns you: the call works today, works tomorrow, and then does
not. The first question anyone in that position has is not *how do I migrate* —
it is **does this affect me, and how long have I got.** This answers that in one
run.

## The part that is not a grep

A retired identifier is a prefix of live ones. `gpt-4` dies on 23 October;
`gpt-4o`, `gpt-4o-mini` and `gpt-4.1` do not. `o1` dies; `o1-mini` does not.
`gpt-3.5-turbo` dies; `gpt-5.6-terra` is its replacement.

A substring search reports all of them, and a report with false alarms in it is
read once and then ignored — which is the same as not running it. Two rules
prevent that:

- a match may not touch another identifier character on either side, so `gpt-4`
  cannot match inside `gpt-4o`;
- the alternation is ordered longest-first, so `gpt-4-turbo-2024-04-09` is
  reported as itself rather than as `gpt-4-turbo`.

Ten live look-alikes are listed in [`table.py`](model_eol/table.py) and the test
suite asserts that not one of them is ever reported.

## A real run

Against a real repository, on 21 September 2026:

```console
$ py -m model_eol.cli ../some-agent --within 30
model-eol - table copied 2026-09-21 from https://developers.openai.com/api/docs/deprecations

2026-09-28  in 7 days
    davinci-002  ->  gpt-5.6-terra   1 occurrence(s)
        tests/hermes_cli/test_openai_picker_curated.py:48  "gpt-3.5-turbo", "davinci-002", ...

2026-10-23  in 32 days
    gpt-3.5-turbo  ->  gpt-5.6-terra   7 occurrence(s)
        optional-skills/mlops/research/dspy/SKILL.md:328  cheap_lm = dspy.OpenAI(model="gpt-3.5-turbo")
        ... and 4 more

8 occurrence(s) retire within 30 days.
```

Exit code 1. In CI that fails the build while there is still time to fix it,
which is the only moment the information is worth anything.

## Your replacement can be dead too

Google's own deprecation page sends `gemini-2.5-flash-image`, which retires on
**2 October 2026**, to `gemini-3.1-flash-image-preview` — which retired on
**25 June 2026**. Eight of its rows chain like this. Following the advice on the
page moves you from one shutdown date to an earlier one.

So when a recommended replacement is itself in the table, the report says so:

```console
2026-10-02  in 11 days
    [Google] gemini-2.5-flash-image  ->  gemini-3.1-flash-image-preview  (which itself retires 2026-06-25)
```

## Three providers, one report

```console
$ py -m model_eol.cli ../some-agent --within 60
model-eol - tables copied 2026-09-21
  OpenAI     https://developers.openai.com/api/docs/deprecations
  Anthropic  https://docs.anthropic.com/en/docs/about-claude/model-deprecations
  Google     https://ai.google.dev/gemini-api/docs/deprecations

2025-10-28  328 days ago - already gone
    [Anthropic] claude-3-5-sonnet-20241022  ->  claude-sonnet-4-6   1 occurrence(s)

2026-06-01  112 days ago - already gone
    [Google] gemini-2.0-flash  ->  gemini-3.6-flash   1 occurrence(s)

2026-10-23  in 32 days
    [OpenAI] gpt-4-turbo  ->  gpt-5.6-sol   1 occurrence(s)
```

183 identifiers in all: 136 from OpenAI, 28 from Google, 19 from Anthropic, each
carrying the provider that published it and the date that provider gave.

## Usage

```bash
py -m model_eol.cli .                          # this directory
py -m model_eol.cli src/app.py                 # one file
py -m model_eol.cli . --within 30              # fail only on the next 30 days
py -m model_eol.cli . --json report.json       # machine-readable
py -m model_eol.cli . --exclude 'docs/*'       # skip files that list ids rather than call them
py -m model_eol.cli --list                     # print the whole table
```

`--exclude` exists because a repository that documents model names matches
itself: a changelog, a compatibility table, or this tool's own table. Without
the flag the report is mostly documentation and the real call site is buried in
it.

## The table can check itself against the page

Every other command here works offline. This one is the exception and is opt-in
for that reason, because "is this table still what the provider publishes" is a
question that cannot be answered without asking the provider.

```console
$ py -m model_eol.cli --check-source
model-eol - comparing the table copied 2026-09-21 against the live pages

OpenAI  https://developers.openai.com/api/docs/deprecations
  1 identifier(s) on the page that this table does not have - these are the ones that matter:
      gpt-5.3-codex

Anthropic  https://docs.anthropic.com/en/docs/about-claude/model-deprecations
  11 identifier(s) on the page that this table does not have
...
27 identifier(s) need a person to look. This cannot tell a new retirement from a
model merely mentioned in a sentence.
```

Exit 0 when the pages match, 1 when something needs a person, 2 when a page
could not be read — a check that could not run must not read as a pass.

**It earned its place the first time it ran.** The table had been copied by hand
and covered 40 OpenAI identifiers. The check found **102 more** the page dates,
including whole families the hand-copy had missed — audio, realtime, transcribe,
deep-research, codex — and every model already switched off, which is the most
useful thing this can report: `gpt-3.5-turbo-0301`, `o1-preview`, `gpt-4-0314`
and the whole 23 July 2026 batch are dead now, and a codebase naming one is
failing today rather than in October.

Getting there took three passes, and each one was a character rather than an
idea: one section writes its dates with U+2010 HYPHEN instead of an ASCII one,
another spells the month in full, and one cell names three identifiers inside a
parenthesis. The twenty-seven that remain are models the pages name without
dating — Anthropic's active list, Google's "No shutdown date announced" — and
the command says a person must look rather than pretending to a verdict.

It also found two errors in this repository's own list of live look-alikes —
identifiers a test asserted must never be reported. `o1-mini` was switched off on
**27 October 2025** and `o3-deep-research` on **23 July 2026**. Both assumptions
were mine; the check is what caught them, and the tests now assert the dates.

Every date the hand-copied table already had matched the page exactly, which is
the other half of what this command is for.

## Honest limits

- **The table is a dated snapshot, not a feed.** It was copied by hand on
  21 September 2026 from the source named above, and every report prints that
  date. Past sixty days the tool says out loud that the table is old. A silent
  stale table would be worse than no tool.
- **Only literal strings are found.** A model id assembled at runtime —
  `f"gpt-{version}"`, a value from an environment variable, a row in a
  database — is invisible here and always will be. "No findings" means no
  literals, not no exposure.
- **`--check-source` needs a person.** It says which identifiers the page names
  that the table does not have. It cannot tell a newly dated retirement from a
  model mentioned in a sentence, and it says so in its own output rather than
  pretending to a verdict.
- **Three providers, and only what they published.** Anthropic lists one model
  as deprecated with a retirement date "to be announced", and Google lists
  dozens with "No shutdown date announced". Those rows are left out rather than
  given a date this tool invented. A model missing here is not a model that is
  safe.
- **Replacement suggestions are OpenAI's, not mine.** The tool repeats what the
  deprecation page says replaces each model. Whether that replacement suits your
  prompts, your latency budget or your costs is a question this cannot answer.
- **A clean exit is not a migration.** It says nothing breaks on a published
  date. It does not say your prompts still behave the same on a newer model,
  which only an evaluation on your own data can tell you.

## Licence

MIT, © Dmytro Galko. See [LICENSE](LICENSE).
