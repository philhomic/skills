# mdx-scorm-course-page

Author source-faithful `mdx-scorm` pages and units from Word, lesson text, exercise sheets, or reference courses. Supports local files and inline output; the hosted Cloud Studio protocol is opt-in through explicit caller orchestration.

Start with [SKILL.md](SKILL.md). It routes to the following references as needed:

- [Syntax inventory](references/syntax-inventory.md) and [component cookbook](references/component-authoring-cookbook.md): existing exercises, games, media, AI, uploads, export, and display/layout blocks.
- [Exercise selection](references/exercise-type-selection.md): choose by learner action, not a reference page's appearance.
- [Reading, Reveal and per-blank weights](references/reading-and-reveal.md): synchronized passages, staged/linked hints, timing, scoring and export boundaries.
- [Text exercises](references/text-exercises.md): word/span selection and insert/delete/replace correction.
- [Classification and knowledge graphs](references/classification-and-knowledge-graph.md): complete source contracts and validation boundaries.
- [Source fidelity](references/source-fidelity-and-reference-style.md): Word paragraphs/hierarchy, answer preservation, reachable annotations, and reference presentation.
- [Authoring heuristics](references/authoring-heuristics.md), [CSS themes](references/stylesheet-authoring.md), [static HTML](references/html-fragments.md), and [HTML Apps](references/html-apps.md).
- [Hosted protocol](references/hosted-protocol.md): candidate, issue-review and repair envelopes; not the default local response format.
- [Engine evidence](references/engine-evidence.md): source locations and the difference between implementation constraints, authoring defaults, and host integration.

The [page template](assets/course-page-template.mdx) is optional. New pages do not acquire default frontmatter, title, feedback, numbering, or input rows. Preserve intentional existing configuration when editing. Missing answers never authorize fabricated scoring or an implicit open mode. Unanchored source notes remain visible.

## Output checker

Python 3.10+; standard library only. Run commands from this skill directory:

```powershell
python scripts/validate_course_output.py C:/course/pages
python scripts/validate_course_output.py C:/course/pages --json
python scripts/validate_course_output.py C:/course/pages --allow-title unit/page.mdx
python -B scripts/test_validate_course_output.py
```

The checker is read-only. Errors fail the command; convention warnings are advisory unless `--strict-conventions` is selected. Page-specific `--allow-title`, `--allow-feedback`, `--allow-numbering`, and `--allow-choicecloze-semantic-conflict` flags record established author decisions. Do not delete source content merely to clear a warning.

The checker excludes code examples, HTML Apps and literal text-exercise content from prose rules. It does not replace the engine parser, token/answer validation, source completeness review, browser preview, HTML safety checks, or Print verification. A skill installation does not deploy those engine services.
