# -*- coding: utf-8 -*-
"""Tests for the matcher, which is where this tool earns or loses trust.

The false positive is the failure mode that matters: a retired id is a prefix of
several live ones, and a report that flags `gpt-4o` as dead is a report nobody
reads twice.
"""

import unittest
from datetime import date

from model_eol.cli import main
from model_eol.scan import find_in_text, group_by_date
from model_eol.table import BY_MODEL, LIVE_LOOKALIKES, RETIREMENTS, SOURCES


class TestMatching(unittest.TestCase):
    def test_finds_a_retired_id(self):
        hits = find_in_text('model = "gpt-4-0613"')
        self.assertEqual([h.model for h in hits], ["gpt-4-0613"])

    def test_does_not_match_inside_a_live_lookalike(self):
        for live in LIVE_LOOKALIKES:
            with self.subTest(live=live):
                hits = find_in_text(f'model = "{live}"')
                self.assertEqual(hits, [], f"{live} is live and must not be reported")

    def test_longest_identifier_wins(self):
        hits = find_in_text('model = "gpt-4-turbo-2024-04-09"')
        self.assertEqual([h.model for h in hits], ["gpt-4-turbo-2024-04-09"])

    def test_suffixed_variant_is_its_own_entry(self):
        hits = find_in_text('"gpt-4-0613-completions"')
        self.assertEqual([h.model for h in hits], ["gpt-4-0613-completions"])

    def test_o1_and_o1_mini_are_told_apart(self):
        """Both are retired, on different dates, and the longer name must not be
        reported as the shorter one. o1-mini was in this suite as a live
        look-alike until --check-source read the page and found it had been
        switched off on 27 October 2025 - the assumption was mine, and the
        check is what caught it."""
        self.assertEqual([h.model for h in find_in_text('"o1"')], ["o1"])
        hits = find_in_text('"o1-mini"')
        self.assertEqual([h.model for h in hits], ["o1-mini"])
        self.assertEqual(hits[0].shutdown, date(2025, 10, 27))

    def test_word_in_prose_is_not_a_match(self):
        # A retired id inside a longer word must not fire.
        self.assertEqual(find_in_text("myo1thing and gpt-4x"), [])

    def test_line_numbers_are_reported(self):
        hits = find_in_text('one\ntwo "gpt-4-turbo"\nthree')
        self.assertEqual(hits[0].line, 2)

    def test_several_ids_on_one_line(self):
        hits = find_in_text('fallback = ["gpt-4-turbo", "gpt-3.5-turbo-1106"]')
        self.assertEqual(sorted(h.model for h in hits),
                         ["gpt-3.5-turbo-1106", "gpt-4-turbo"])


class TestTable(unittest.TestCase):
    def test_a_replacement_is_either_named_or_honestly_absent(self):
        """Five Sora rows carry no replacement because the page gives none. They
        used to hold the literal string "---", which the report printed to the
        user as `-> ---`. An empty value is the honest shape; the CLI turns it
        into words."""
        blank = [r.model for r in RETIREMENTS if not r.replacement]
        self.assertEqual(sorted(blank), sorted(m for m in blank if m.startswith("sora-")),
                         "only the rows whose source published no replacement may be blank")
        for r in RETIREMENTS:
            self.assertNotIn("---", r.replacement, f"{r.model} carries a placeholder")

    def test_no_row_pretends_to_be_a_fine_tune_identifier(self):
        """`ft-gpt-4` is not an identifier any codebase contains. OpenAI writes a
        fine-tune as `ft:gpt-4:org:suffix:id`, and the base model inside it is
        matched by the ordinary rule - six `ft-*` rows inflated the count and
        matched nothing."""
        self.assertEqual([r.model for r in RETIREMENTS if r.model.startswith("ft-")], [])
        hits = find_in_text('model = "ft:gpt-4:acme:suffix:abc123"')
        self.assertEqual([h.model for h in hits], ["gpt-4"])

    def test_no_duplicate_identifiers(self):
        models = [r.model for r in RETIREMENTS]
        self.assertEqual(len(models), len(set(models)))

    def test_a_replacement_that_is_itself_retired_is_reported_as_such(self):
        """Google's own page does this: eight of its rows send you to a model
        that also has a shutdown date. Silently repeating the advice would be
        the failure; the tool has to say that the destination dies too."""
        chained = [r for r in RETIREMENTS if r.replacement in BY_MODEL]
        self.assertTrue(chained, "if the sources stop chaining, drop this test")
        for r in chained:
            hits = find_in_text(f'model = "{r.model}"')
            self.assertEqual(hits[0].replacement_dies, BY_MODEL[r.replacement].shutdown,
                             f"{r.model} -> {r.replacement} loses its second date")

    def test_a_replacement_outside_the_table_has_no_second_date(self):
        entry = next(r for r in RETIREMENTS if r.replacement not in BY_MODEL)
        hits = find_in_text(f'model = "{entry.model}"')
        self.assertIsNone(hits[0].replacement_dies)

    def test_every_provider_is_represented(self):
        providers = {r.provider for r in RETIREMENTS}
        self.assertEqual(providers, set(SOURCES))

    def test_lookalikes_are_not_in_the_table(self):
        for live in LIVE_LOOKALIKES:
            self.assertNotIn(live, BY_MODEL)


class TestGrouping(unittest.TestCase):
    def test_groups_are_sorted_by_date(self):
        hits = find_in_text('"o3-2025-04-16" "gpt-3.5-turbo-instruct"')
        dates = list(group_by_date(hits))
        self.assertEqual(dates, sorted(dates))
        self.assertEqual(dates[0], date(2026, 9, 28))


class TestExitCodes(unittest.TestCase):
    def setUp(self):
        import tempfile, pathlib
        self.dir = pathlib.Path(tempfile.mkdtemp())

    def write(self, name, text):
        p = self.dir / name
        p.write_text(text, encoding="utf-8")
        return p

    def test_clean_repository_exits_zero(self):
        self.write("a.py", 'model = "gpt-5.6-sol"')
        self.assertEqual(main([str(self.dir), "--today", "2026-09-21"]), 0)

    def test_imminent_retirement_exits_one(self):
        self.write("a.py", 'model = "gpt-3.5-turbo-instruct"')
        self.assertEqual(main([str(self.dir), "--today", "2026-09-21", "--within", "30"]), 1)

    def test_outside_the_window_exits_zero(self):
        self.write("a.py", 'model = "o3-2025-04-16"')   # 11 December
        self.assertEqual(main([str(self.dir), "--today", "2026-09-21", "--within", "30"]), 0)

    def test_exclude_skips_documentation_that_only_lists_ids(self):
        """A repository documenting model names matches itself without this."""
        self.write("call.py", 'model = "gpt-3.5-turbo-instruct"')
        (self.dir / "docs").mkdir(exist_ok=True)
        (self.dir / "docs" / "table.md").write_text(
            "retired: gpt-3.5-turbo-instruct", encoding="utf-8")
        with_docs = main([str(self.dir), "--today", "2026-09-21", "--within", "30"])
        self.assertEqual(with_docs, 1)
        only_docs = main([str(self.dir), "--today", "2026-09-21", "--within", "30",
                          "--exclude", "call.py"])
        self.assertEqual(only_docs, 1, "the doc still matches, which is why the flag exists")
        nothing = main([str(self.dir), "--today", "2026-09-21", "--within", "30",
                        "--exclude", "call.py", "--exclude", "docs/*"])
        self.assertEqual(nothing, 2,
                         "excluding everything means nothing was checked, which is not a pass")

    def test_check_source_does_not_pass_while_printing_a_problem(self):
        """It used to. A page that had dropped a row we hold printed the warning
        and then returned 0 with "the table still matches all three pages" -
        a check contradicting itself in one screen. Codex found it."""
        from model_eol import cli as cli_module
        from model_eol.source import Comparison

        real = cli_module.check_all
        cli_module.check_all = lambda: [
            Comparison("OpenAI", "http://x.example", True, missing=("gpt-4-0613",), unknown=()),
        ]
        try:
            self.assertEqual(cli_module.main(["--check-source"]), 1)
        finally:
            cli_module.check_all = real

    def test_check_source_passes_only_when_nothing_was_reported(self):
        from model_eol import cli as cli_module
        from model_eol.source import Comparison

        real = cli_module.check_all
        cli_module.check_all = lambda: [
            Comparison("OpenAI", "http://x.example", True, missing=(), unknown=()),
        ]
        try:
            self.assertEqual(cli_module.main(["--check-source"]), 0)
        finally:
            cli_module.check_all = real

    def test_missing_path_exits_two(self):
        self.assertEqual(main([str(self.dir / "nope"), "--today", "2026-09-21"]), 2)


if __name__ == "__main__":
    unittest.main()
