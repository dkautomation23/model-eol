# model-eol

[![CI](https://github.com/dkautomation23/model-eol/actions/workflows/ci.yml/badge.svg)](https://github.com/dkautomation23/model-eol/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/dkautomation23/model-eol/badge)](https://scorecard.dev/viewer/?uri=github.com/dkautomation23/model-eol)
[![CodeQL](https://github.com/dkautomation23/model-eol/actions/workflows/codeql.yml/badge.svg)](https://github.com/dkautomation23/model-eol/actions/workflows/codeql.yml)

What in this repository stops working, when, and what replaces it.

```bash
py -m model_eol.cli .
```

Exit 0 when nothing retires inside the window, 1 when something does, 2 when the
question could not be asked. Python standard library only, no dependencies, no
API key, no account, no network call — the table ships with the tool.

## Why this exists

On **23 October 2026** OpenAI retires eighteen model identifiers in one day,
including `gpt-4-0613`, `gpt-4-turbo`, `o1`, `o3-mini`, `o4-mini` and every
`ft-*` fine-tune built on them. Five days earlier, on **28 September**,
`gpt-3.5-turbo-instruct`, `babbage-002`, `davinci-002` and `gpt-3.5-turbo-1106`
go. On **11 December** the `gpt-5` and `o3` snapshots follow.

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

## Honest limits

- **The table is a dated snapshot, not a feed.** It was copied by hand on
  21 September 2026 from the source named above, and every report prints that
  date. Past sixty days the tool says out loud that the table is old. A silent
  stale table would be worse than no tool.
- **Only literal strings are found.** A model id assembled at runtime —
  `f"gpt-{version}"`, a value from an environment variable, a row in a
  database — is invisible here and always will be. "No findings" means no
  literals, not no exposure.
- **OpenAI only.** Anthropic and Google publish their own retirement schedules
  and neither is in this table yet. The table is one file; adding a provider is
  adding entries, not rewriting the matcher.
- **Replacement suggestions are OpenAI's, not mine.** The tool repeats what the
  deprecation page says replaces each model. Whether that replacement suits your
  prompts, your latency budget or your costs is a question this cannot answer.
- **A clean exit is not a migration.** It says nothing breaks on a published
  date. It does not say your prompts still behave the same on a newer model,
  which only an evaluation on your own data can tell you.

## Licence

MIT, © Dmytro Galko. See [LICENSE](LICENSE).
