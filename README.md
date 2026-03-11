# skills

A repository for reusable Codex skills.

This repo is organized so it can grow from one skill into a stable multi-skill library without changing the top-level structure every time a new skill is added.

## What lives here

Each skill lives in its own top-level folder:

```text
skills/
├── README.md
├── SKILLS.md
├── CONTRIBUTING.md
└── <skill-name>/
    ├── SKILL.md
    ├── assets/
    ├── references/
    ├── scripts/
    └── evals/
```

Only `SKILL.md` is required. The other folders are optional and should appear only when the skill actually needs them.

## Included skills

See [SKILLS.md](./SKILLS.md) for the current catalog.

## Current focus

The first skill in this repository is [`mdx-scorm-course-page`](./mdx-scorm-course-page/), which helps turn source teaching materials into structured `mdx-scorm` lesson pages.

## Adding new skills

Use [CONTRIBUTING.md](./CONTRIBUTING.md) when adding or updating a skill in this repository. It defines:

- folder structure
- naming expectations
- what belongs in `SKILL.md`
- when to add `assets/`, `references/`, `scripts/`, or `evals/`
- how to keep the root catalog in sync
