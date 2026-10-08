#!/usr/bin/env python3
"""Regression checks for real masking, answer and convention boundaries."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from validate_course_output import Exceptions, inspect_text


def cloze(options="cat | dog", answer="1"):
    return f":::choicecloze\n[content]\nThe @--@ sleeps.\n[options]\n{options}\n[answer]\n{answer}\n:::\n"


class CourseOutputTests(unittest.TestCase):
    def codes(self, text, **kwargs):
        return {i.code for i in inspect_text(text, **kwargs)}

    def test_fenced_code_is_not_a_course(self):
        bad = ':pop[term]{ref=missing}\n' + cloze(answer="9") + '<https://example.com>\n<!-- TODO: demonstration -->'
        for opener, closer in [("```mdx", "```"), ("~~~~mdx", "~~~~"), ("`````md", "`````")]:
            with self.subTest(opener=opener):
                self.assertEqual(inspect_text(opener + "\n" + bad + "\n" + closer), [])

    def test_longer_outer_fence_can_contain_inner_fences(self):
        self.assertEqual(inspect_text('````mdx\n```html app\n<script>TODO</script>\n```\n' + cloze(answer="9") + '````'), [])

    def test_html_app_does_not_trigger_course_checks(self):
        value = '```html app\n<style>.x{color:red}</style>\n<script>const x = ":pop[test]{ref=bad}";</script>\n<p>TODO</p>\n```'
        self.assertEqual(inspect_text(value), [])

    def test_inline_code_and_raw_code_regions_are_ignored(self):
        value = '`<https://example.com>` and ``:pop[test]{ref=bad}``\n<pre>\n' + cloze(answer="9") + '\n</pre>'
        self.assertEqual(inspect_text(value), [])

    def test_source_to_do_is_preserved(self):
        self.assertEqual(inspect_text('What do you have to do?\nTODO is the name used in the source.\n待确认是原文的术语。'), [])
        self.assertEqual(self.codes('<!-- TODO: missing answer -->'), {"editorial-note"})

    def test_text_content_has_no_prose_lints(self):
        value = ':::textedit{open=true}\n[content]\nTODO <https://example.com> @blank@ `literal`\n:::'
        self.assertEqual(inspect_text(value), [])

    def test_text_prompt_is_still_checked(self):
        value = ':::textselect{open=true}\n[prompt]\n<https://example.com>\n[content]\nA literal sentence.\n:::'
        self.assertEqual(self.codes(value), {"web-link-form"})

    def test_text_code_like_original_remains_literal(self):
        value = ':::textedit{open=true}\n[content]\n<script>hello</script>\n:::'
        self.assertEqual(inspect_text(value), [])

    def test_duplicate_unsupported_and_missing_text_sections(self):
        value = ':::textselect\n[prompt]\nChoose.\n[answer]\nA\n[prompt]\nAgain\n:::'
        self.assertEqual(self.codes(value), {"text-section", "duplicate-text-section", "missing-text-content"})

    def test_text_attributes_exclude_quoted_values(self):
        value = ':::textselect{id="a b c" mode="span" open=true}\n[content]\nA sentence.\n:::'
        self.assertEqual(inspect_text(value), [])
        self.assertIn('text-attribute', self.codes(value.replace('mode="span"', 'rows=4')))
        self.assertIn('text-mode', self.codes(value.replace('mode="span"', 'mode="phrase"')))

    def test_valid_text_markers_are_not_rewritten(self):
        value = ':::textedit\n[content]\nShe :fix[go]{to="went"} home. I bought :add[a] book. He went :del[to] home.\n:::'
        self.assertEqual(inspect_text(value), [])

    def test_cloze_pipe_priority_and_existing_text_answers(self):
        cases = [('Hello, world | Goodbye', '1'), ('cat | dog', 'dog'), ('A. cat | B. dog', 'B'), ('A | B', 'B'), ('cat, dog; fox', '3')]
        for options, answer in cases:
            with self.subTest(options=options, answer=answer):
                self.assertEqual(inspect_text(cloze(options, answer)), [])

    def test_cloze_out_of_range_is_error(self):
        issue = inspect_text(cloze(answer="3"))[0]
        self.assertEqual((issue.code, issue.severity), ('cloze-index', 'error'))

    def test_cloze_separate_option_groups_are_not_flattened(self):
        value = cloze('red | blue\ncat | dog | fox', '2\n3')
        self.assertEqual(inspect_text(value), [])
        self.assertIn('cloze-index', self.codes(value.replace('[answer]\n2\n3', '[answer]\n3\n3')))

    def test_case_sensitive_component_names_and_ai_attribute(self):
        self.assertIn('text-directive-case', self.codes(':::TextSelect\n[content]\n:pick[She] came.\n:::'))
        self.assertIn('ai-score-case', self.codes(':::fillblank{aiscore=true}\n[content]\n@--@\n:::'))

    def test_cloze_roman_and_punctuation_answers_are_advisory(self):
        for options, answer, code in [('i. cat | ii. dog', 'ii', 'cloze-roman'), ('Hello, world | Bye', 'Hello, world', 'cloze-answer')]:
            with self.subTest(answer=answer):
                issue = inspect_text(cloze(options, answer))[0]
                self.assertEqual((issue.code, issue.severity), (code, 'warning'))

    def test_blank_token_only_checked_in_exercises(self):
        self.assertEqual(inspect_text('The source discusses @blank@.'), [])
        self.assertIn('blank-token', self.codes(cloze().replace('@--@', '@blank@')))
        self.assertNotIn('blank-token', self.codes(cloze().replace('@--@', '`@blank@`')))

    def test_game_choice_item_sections_receive_multiselect_checks(self):
        value = ':::game-choice\n[item]\n[prompt]\nChoose two.\n[options]\ncat\ndog\nfox\n[answer]\nB C\n:::'
        self.assertIn('multiselect-lines', self.codes(value))
        self.assertEqual(inspect_text(value.replace('B C', 'B\nC')), [])

    def test_choice_full_text_is_not_a_same_line_list(self):
        value = ':::choice\n[stem]\nChoose.\n[options]\nA. B C\nB. other\nC. third\n[answer]\nB C\n:::'
        self.assertNotIn('multiselect-lines', self.codes(value))

    def test_nested_and_long_directive_fences(self):
        value = '::::collapse[Practice]\n' + cloze() + '::::'
        self.assertEqual(inspect_text(value), [])
        self.assertIn('cloze-index', self.codes(value.replace('[answer]\n1', '[answer]\n8')))

    def test_pop_errors_and_visible_unanchored_note(self):
        self.assertIn('missing-pop-definition', self.codes(':pop[word]{ref=missing}'))
        body = ':pop[word]{ref=x}\n:::pop{def=x}\nDefinition.\n:::\n'
        self.assertEqual(inspect_text(body), [])
        self.assertIn('duplicate-pop-definition', self.codes(body + ':::pop{def=x}\nOther.\n:::'))
        self.assertIn('unreachable-pop', self.codes(':::pop{def=x}\nDefinition.\n:::'))
        self.assertEqual(inspect_text('## Glossary\nUnanchored term: full source definition.'), [])

    def test_frontmatter_nested_keys_and_explicit_exceptions(self):
        text = '---\ntitle: Existing\nfeedback: instant\nnumbering: all\nai:\n  title: Nested\n---\n# Body'
        self.assertEqual(len(inspect_text(text)), 3)
        allow = Exceptions(title={'page.mdx'}, feedback={'page.mdx'}, numbering={'page.mdx'})
        self.assertEqual(inspect_text(text, exceptions=allow), [])

    def test_translation_open_manual_and_custom_instruction(self):
        for attrs in ['open=true', 'useManualMarking=true']:
            value = f':::translate{{{attrs}}}\n[prompt]\nTranslate into Chinese.\n:::'
            self.assertEqual(inspect_text(value), [])
        value = ':::fillblank{aiScore=true}\n[content]\nTranslate into Chinese.\n@--@\n[answer]\n中文\n[ai]\ninstruction: Assess accuracy and natural Chinese.\n:::'
        self.assertEqual(inspect_text(value), [])

    def test_semantic_cue_from_other_question_does_not_leak(self):
        self.assertEqual(inspect_text('# Matching exercise\nMatch each statement.\n' + cloze()), [])
        self.assertIn('cloze-semantics', self.codes(cloze().replace('The @--@ sleeps.', 'Match each statement @--@.')))

    def test_cli_separates_warnings_from_errors_without_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / 'page.mdx'
            page.write_text('---\ntitle: Existing\n---\n# Body', encoding='utf-8')
            before = page.read_bytes()
            cmd = [sys.executable, str(Path(__file__).with_name('validate_course_output.py')), str(page), '--json']
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)['warnings'], 1)
            strict = subprocess.run(cmd + ['--strict-conventions'], capture_output=True)
            self.assertEqual(strict.returncode, 1)
            self.assertEqual(page.read_bytes(), before)
            page.write_text(cloze(answer='8'), encoding='utf-8')
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)


if __name__ == '__main__':
    unittest.main()
