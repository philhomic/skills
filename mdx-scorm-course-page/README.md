# mdx-scorm-course-page

A Codex skill for turning source teaching materials into structured `mdx-scorm` lesson pages.

## When to use this skill

Use this skill when the source material is something like:

- a Word handout
- pasted lesson text
- teaching notes
- an exercise sheet
- mixed course content that should become `mdx-scorm`

It is especially useful when the target output should use supported `mdx-scorm` directive blocks instead of ad-hoc JSX.

## What it helps produce

- single-page `mdx-scorm` lessons
- template-driven unit drafts based on reference pages
- lesson pages that preserve source wording while converting structure into supported directives

## Key files

- [`SKILL.md`](./SKILL.md)
  The main skill instructions, trigger guidance, workflow, authoring heuristics, and quality constraints.

- [`assets/course-page-template.mdx`](./assets/course-page-template.mdx)
  A default page scaffold used when building new lesson pages.

- [`references/syntax-inventory.md`](./references/syntax-inventory.md)
  A source-audited syntax guide for supported `mdx-scorm` directives and related authoring patterns.

## Directory layout

```text
mdx-scorm-course-page/
├── README.md
├── SKILL.md
├── assets/
│   └── course-page-template.mdx
└── references/
    └── syntax-inventory.md
```

## Notes

- `SKILL.md` is the source of truth for how the skill should behave.
- The files under `assets/` and `references/` support the skill; they are not standalone replacements for `SKILL.md`.
