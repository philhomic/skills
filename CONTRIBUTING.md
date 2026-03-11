# Contributing Skills

## Repository contract

Each skill should live in a dedicated top-level folder:

```text
<skill-name>/
├── SKILL.md
├── assets/
├── references/
├── scripts/
└── evals/
```

Only `SKILL.md` is required.

Use the optional folders only when they materially help the skill:

- `assets/` for templates and reusable output files
- `references/` for supporting documents that should be loaded only when needed
- `scripts/` for deterministic helpers that are better than repeating long instructions
- `evals/` for test prompts or benchmark inputs if you decide to evaluate the skill

## Naming

- Use a short, descriptive folder name.
- Prefer lowercase ASCII names with hyphens, for example `mdx-scorm-course-page`.
- The skill name in frontmatter should match the folder name unless there is a strong reason not to.

## `SKILL.md` expectations

At minimum, include:

- YAML frontmatter with `name` and `description`
- when the skill should trigger
- what the skill produces
- the main workflow
- references to any bundled assets, references, or scripts

## Keep the repo index up to date

When you add a new skill:

1. Create the top-level folder.
2. Add `SKILL.md`.
3. Add optional support folders only if needed.
4. Update [SKILLS.md](./SKILLS.md).
5. Update [README.md](./README.md) only if the repository-level positioning changes.
