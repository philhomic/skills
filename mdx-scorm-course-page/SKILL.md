---
name: mdx-scorm-course-page
description: Use this skill whenever the user wants to turn a Word handout, pasted lesson text, teaching notes, exercise sheet, or mixed lecture material into `mdx-scorm` lesson content. Use it both for single-page generation and for template-driven unit generation when the user provides a reference unit folder or reference pages and asks to make a new unit “按这个模子生成”, “参考已有页面生成”, or “照着 Unit 1 做 Unit 2”. This skill is the default choice for requests like “转成 mdx-scorm 页面”, “用指令块做课件”, “生成 src/pages 下的课程内容”, “把讲义做成一页课”, or any request to author `mdx-scorm` content with directive blocks such as `:::choice`, `:::fillblank`, `:::matching`, `:::sorting`, `:::translate`, `:::writing`, `:::recorder`, `:::imageupload`, `:::videoupload`, `styleBlock`, `collapse`, `pop`, `sticky`, `splitpane`, `columns`, `carousel`, or `iframe`. Prefer this skill even when the user only mentions Word/course content and does not explicitly name the repo. Also trigger proactively whenever the user mentions `mdx`, `scorm`, or `welearn`, because those mentions are strong signals that this skill should be considered first.
---

# mdx-scorm course page authoring

Generate complete `mdx-scorm` lesson pages from source material while staying faithful to the original wording and the repo's real directive syntax.

## What this skill produces

- One source document or pasted text becomes one complete `.mdx` lesson page by default.
- A reference unit plus a target source document can become a whole new unit draft.
- Output includes `frontmatter + page title + teaching content + practice blocks`.
- Output uses directive blocks supported by `mdx-scorm`, not ad-hoc JSX.

## Output destination rule

Before generating final page content, first determine where the result should go.

- By default, ask the user for:
  - the save folder or target path
  - the filename
- If the user gives only a folder, propose a filename before writing.
- If the user does not yet have a filename, suggest one.
- Only skip this and print the full `.mdx` inline when the user clearly asks to see it directly first.
- If the user says "先打出来看看", "直接显示", "先别写文件", or equivalent, return inline content instead of writing a file.

## Non-negotiable rules

- Preserve the author's wording as much as possible. Reorganize; do not freely rewrite.
- Do not arbitrarily compress, abridge, summarize, or omit source content. If the source includes reading passages, sources, vocabulary notes, term explanations, answer keys, translations, or other teaching material, keep them complete unless the user explicitly asks for a shortened version.
- When converting vocabulary or glossary material, keep the full original explanatory content. Do not replace full source definitions with shorter paraphrases just because the popup or page would be shorter.
- When a source page contains `Source`, `Vocabulary Focus`, `Cultural/Professional Terms`, `Answer`, `参考译文`, `Skill Summary`, or similar labeled sections, assume they are required content by default and carry them over unless the user explicitly asks to remove or shorten them.
- Use canonical ASCII directive syntax in final output even if the source material used Chinese aliases or full-width punctuation.
- Do not emit `import` statements for authored lesson pages.
- Do not emit general interactive JSX such as `<Choice />`, `<FillBlank />`, or other custom components for user-authored content.
- Do not invent correct answers, explanations, weights, or scoring settings that are not supported by the source.
- If an objective exercise is missing key data, keep it unresolved and add an HTML comment like `<!-- TODO: missing answer in source -->`.
- Default to one page. Only split into multiple pages if the user explicitly asks.
- Do not assume a fixed taxonomy of pages, a fixed folder hierarchy, or a fixed section split across projects.
- When a reference unit is provided, treat it as a set of transformation examples, not as a source of facts for the target unit.

## When `.docx` is the input

If the user gives a Word file, first use the `$docx` skill to extract readable text. Reuse that extracted text as the source of truth for the page. Only fall back to lower-level document unpacking if the extraction is clearly incomplete.

## Required references

Read these before authoring:

- `references/syntax-inventory.md` - source-audited directive and component syntax
- `assets/course-page-template.mdx` - default page scaffold

If you are using only a small subset of blocks, read the relevant sections from the syntax inventory instead of loading unrelated material.

## Modes

### Page mode

Use when the user wants one page or one small content slice converted into `mdx-scorm`.

### Template unit mode

Use when the user provides:

- a reference unit folder, reference pages, or an existing `src/pages/...` subtree
- and a target Word file or target source text
- and asks for a new unit or multi-page structure based on the reference

In this mode, do not start by copying folder structure blindly. First infer how the reference unit transforms source text into pages.

## Page mode workflow

1. Identify the source form:
   - Word document
   - pasted text
   - mixed text plus exercise fragments
   - whether the user wants a file written or only an inline preview
2. Extract and normalize the content:
   - keep original wording
   - remove obvious Word noise, duplicate blank lines, broken numbering, stray bullets
   - keep exercise stems/options/answers/explanations intact when present
3. Detect the page structure:
   - page title
   - intro or lead-in
   - explanation/content sections
   - exercises
   - answer or explanation fragments
   - footnotes, endnotes, glossary items, vocabulary notes, or term explanations that may need inline annotation
4. Map exercises to supported blocks:
   - single/multi-choice -> `:::choice`
   - fill-in-the-blank -> `:::fillblank`
   - word-bank cloze -> `:::choicecloze`
   - matching -> `:::matching`
   - ordering/steps -> `:::sorting`
   - translation -> `:::translate`
   - short writing/essay -> `:::writing`
   - speaking/recording -> `:::recorder`
   - image/video submission -> upload blocks
5. Build the page:
   - start from `assets/course-page-template.mdx`
   - set frontmatter defaults intelligently
   - use headings and plain markdown for exposition
   - use directive blocks for interactions and display containers
6. Self-check before finalizing:
   - no unsupported syntax
   - no imports
   - no general JSX interaction components
   - no fabricated answers
   - no silent compression or omission of labeled source sections
   - no shortened vocabulary / glossary definitions unless explicitly requested
   - directive fences are balanced
   - if interactions exist, numbering mode is set deliberately

## Template unit mode workflow

### 1. Observe the reference pages

For each relevant reference page, record only visible facts first:

- title style
- content length
- heading structure
- directive usage
- presence of exercises, answers, translations, vocabulary, summaries, or projects
- whether the page mostly preserves source text, reorganizes it, annotates it, or converts it into interactions

Do not begin by assigning a fixed page type.

### 2. Link reference pages to reference source spans

If the user also provides a reference Word document or source text, identify which source spans each reference page most likely comes from.

Think in terms of:

- `reference page -> source spans`

not:

- `reference page -> fixed page category`

### 3. Infer transformation patterns

For each reference page, summarize what transformation it applies to the source. Use only broad, reusable patterns:

- `retain` - largely preserve source text with light formatting
- `compress` - condense longer prose into a shorter page
- `reorder` - rearrange source order for page readability
- `split` - divide one source span across multiple pages
- `merge` - combine several nearby spans into one page
- `annotate` - add vocabulary, terms, translation, hints, or layout around source text
- `interactive-convert` - turn exercise material into directive-based interactions
- `summary-extract` - extract skills, rules, or conclusions from longer explanation

Do not overfit these patterns to one textbook.

### 4. Segment the target source by its own signals

Segment the target Word or pasted text using the target material's own signals:

- titles and subheadings
- directions, source, answer, vocabulary, translation markers
- exercise numbering, options, word banks
- paragraph-topic changes
- bilingual switches
- obvious shifts between exposition, exercises, notes, and summaries

These are candidate source spans, not pre-decided pages.

### 5. Soft-match target spans to reference transformation patterns

For each target span, decide which transformation pattern fits best.

Only after that, use the most similar reference page as a structural example.

The reference page provides:

- organization
- presentation style
- directive habits
- naming cues

The target source provides:

- facts
- wording
- answers
- explanations
- terminology

Never let reference content leak into target content.

### 6. Generate a unit plan before writing pages

Before generating files, produce a plan that includes:

- proposed pages or folders
- which target spans feed each page
- which reference pages influenced each page
- which transformation pattern is being used
- confidence level
- mismatches, additions, or missing elements

Do not jump straight into full unit generation when the mapping is still fuzzy.

### 7. Generate pages after the mapping is stable

Generate pages only after a soft alignment exists between:

- target source spans
- reference transformation patterns
- reference page structure

Page boundaries are a result of this mapping, not a preset.

### 8. Surface mismatches instead of forcing the fit

If the target material does not align cleanly with the reference:

- report the mismatch
- suggest a revised split
- suggest an added page, removed page, merged page, or standalone page

Do not force the target into the reference shape just for symmetry.

## Frontmatter defaults

Use the simplest valid frontmatter that matches the page.

- Always include `title`.
- Use `feedback: submit` unless the user already asked for a different behavior.
- If the page includes interactive blocks, default to `numbering: type`.
- If the page is display-only, default to `numbering: none`.
- Only add fields like `browseMode`, `scormDebug`, `scoreCardShowWeights`, `showai`, or `ai:` when the user explicitly needs them.

## Authoring heuristics

### Prefer plain markdown for exposition

Use standard headings, paragraphs, lists, blockquotes, tables, images, audio, and video unless a display directive is clearly helpful.

### Prefer the simplest supported directive

- Use `styleBlock` only when local styling or boxed emphasis is useful.
- Use `collapse` for optional extra explanation.
- Use `pop` primarily for inline annotation derived from the source, especially footnotes, endnotes, vocabulary notes, and term explanations.
- Use `splitpane` when learners need to keep a long reference text visible while answering questions or completing a task.
- Use `sticky` when learners need to repeatedly glance at a short reference block such as a word bank, checklist, or compact note.
- Use `splitpane`, `columns`, `carousel`, and `iframe` only when the source clearly calls for layout or embedded content.

### Long expository page variation rule

When generating a long explanation-heavy page, do not start from a rigid page skeleton and do not insert display directives just to avoid visual monotony.

Instead, classify each content span by teaching function, then choose the lightest expression that improves comprehension or scanability.

Use this decision order:

1. Is this span normal continuous exposition that should be read straight through?
2. If not, is it mainly a reminder, mini-summary, optional supplement, term note, side-by-side comparison, or reference/task pairing?
3. Can plain markdown already express it clearly enough?
4. If an upgrade is helpful, choose the lightest supported directive first.
5. Only move to layout-oriented directives when lighter options would not reduce reading burden enough.

Default signal-to-format mapping:

- explanation prose -> plain markdown
- key reminder or reading cue -> `styleLine`
- mini-summary, boxed example, or compact standalone note -> `styleBlock`
- optional extra explanation -> `collapse`
- inline term explanation -> `pop`
- side-by-side comparison or paired reference -> `columns`
- long source material plus nearby task area -> `splitpane`
- short reusable reference that must stay visible across several items -> `sticky`

Guardrails:

- Do not add a directive only because the page feels too plain.
- Do not wrap ordinary exposition in `styleBlock` just to create variety.
- Do not place core understanding-critical content inside `collapse`.
- Do not force a long explanation into inline `pop`.
- Do not use `columns` just because two groups of content exist; use it only when side-by-side reading has real value.
- On explanation-heavy pages, treat `sticky`, `splitpane`, `carousel`, and `iframe` as low-frequency tools that need a clear reading or task-driven reason.

Page feel target:

- aim for "textbook-like, but not dull"
- let variation support comprehension rather than decoration
- keep change types sparse and stable within the same page so the page does not feel improvised section by section

### Content and style quality constraints

#### Content completeness rule

Preserve all source information that carries teaching, structural, or answer-related value.

You may reorganize content, fold it, or restyle it, but do not silently thin a complete source entry into a reduced version that drops definitions, labels, collocations, bilingual notes, source metadata, or exercise-critical details.

In short:

- folding is allowed
- silent omission is not

#### Structural consistency rule

Within the same section or heading level, entries with the same semantic structure should use the same presentation pattern by default.

Do not mix card blocks, plain paragraphs, side-by-side layouts, or other display modes for parallel items unless the source structure genuinely differs.

#### Border-radius discipline rule

Use border radius sparingly and consistently.

Reserve it for true card containers or clearly bounded reveal bodies. Avoid stacking multiple rounded wrappers in dense content areas, and do not introduce radius-heavy styling that makes text or nested blocks visually push past the container edge.

#### Spacing discipline rule

Keep spacing stable across the page.

Do not create variety by randomly enlarging padding, margin, or line height. Similar blocks should usually share similar internal and external spacing, so the reading rhythm stays steady across long pages.

#### Emphasis discipline rule

Do not stack emphasis styles unless the content truly needs a stronger teaching signal.

Avoid combining colored backgrounds, borders, shadows, large font jumps, and bold text on ordinary informational content. If one light emphasis device is enough, stop there.

#### Typography discipline rule

Keep typography conservative and readable.

Do not vary font size, weight, alignment, indentation, or decoration casually across normal content. Use typography changes only when they clearly express hierarchy, instruction, or contrast that plain markdown cannot communicate well.

### Collapse authoring rule

`collapse` supports both:

- its own component-specific control attrs such as `align`, `fullWidth`, `labelAlign`, `arrowPosition`, and `button`
- normal style attrs from the shared style whitelist

Important distinction:

- `align`, `fullWidth`, `labelAlign`, `arrowPosition`, and `button` are not CSS properties
- they control trigger layout and collapse behavior
- style attrs such as `background`, `color`, `border-radius`, and `padding` still apply to the trigger itself
- if the revealed body needs styling, put that styling inside an inner `styleBlock`

Use these component-specific attrs deliberately:

- `align` controls where the trigger sits in the layout
- `fullWidth` makes the trigger span the available width
- `labelAlign` controls alignment inside the trigger
- `arrowPosition` controls whether the arrow appears on the left or right
- `button` controls whether the trigger uses button-like presentation

### Splitpane vs sticky decision rule

Choose between them by reference length and reuse pattern:

- Prefer `splitpane` when:
  - the reference material is long
  - the learner must read and answer in parallel
  - repeated up/down scrolling would interrupt the task
- Prefer `sticky` when:
  - the reference block is short
  - the learner needs to look back at it many times across multiple items
  - fixing it near the top removes repetitive scrolling
- Do not use either just for decoration.
- If the reference is long and central, choose `splitpane` before considering `sticky`.
- If one page contains both a long passage and a short reusable aid, `splitpane` can hold the long passage while `sticky` can hold the compact aid only if the page truly needs both.

Typical mappings:

- long passage + reading questions -> `splitpane`
- long article + translation/writing task -> `splitpane`
- word bank reused across several blanks -> `sticky`
- short formula list / prompt checklist / step reminder -> `sticky`
- one short note beside one question -> plain markdown or `styleBlock`, not `sticky`

### Annotation and reference burden patterns

Use these three components as a small decision set:

- `pop`
  - use when the learner needs an explanation for a specific word or phrase inside the reading flow
  - typical source signals: footnotes, endnotes, vocabulary notes, glossary items tied to inline terms
- `sticky`
  - use when the learner needs to repeatedly consult a short reference block while doing several items
  - typical source signals: word banks, compact checklists, short prompt reminders, brief rule lists
- `splitpane`
  - use when the learner must keep a long source text visible while working on nearby tasks
  - typical source signals: reading passage plus questions, long source article plus translation or writing task

Quick contrast:

- explanation attached to one term -> `pop`
- short reusable reference across many items -> `sticky`
- long reading source plus task area -> `splitpane`

Do not substitute one for another just because the layout looks attractive. Choose the component that reduces the learner's scrolling and context-switching cost most directly.

Mini examples:

```mdx
Text with inline annotation:
The museum's :pop[digital initiatives]{ref=term-digital-initiatives} attract younger audiences.

:::pop{def=term-digital-initiatives}
digital initiatives: projects that use digital tools to expand access, interaction, or communication.
:::
```

```mdx
Short reusable reference:
:::sticky{top=0 zIndex=5}
:::styleBlock{background=var(--quote-bg) color=var(--quote-text) border-color=var(--card-border) border-radius=12 padding=12}
Word Bank: evolve, blend, inherit, promote, accessible
:::
:::

:::fillblank
[content]
The museum hopes to @--@ tradition and modern life.

[answer]
blend
:::
```

```mdx
Long reference plus tasks:
:::splitpane{height="72vh" initialTopPct=0.6 minBottom=120 fitViewport}
:::splitTop
## Reading Passage

Long passage content stays here.
:::
:::splitBottom
:::choice
[stem]
What is the author's main point?

[options]
A. ...
B. ...

[answer]
A
:::
:::
:::
```

### Pop authoring rule

Treat `pop` as the default annotation mechanism when the source contains:

- Word footnotes or endnotes
- end-of-text vocabulary explanations
- term or phrase explanations after the passage
- glossary-style note lists that explain words appearing in the text

Authoring preference:

- put the clickable term or phrase inline in the running text with `:pop[...]{ref=...}`
- put the actual note content in `:::pop{def=...}` outside interactive question blocks
- preserve note wording faithfully; do not rewrite source annotations unless cleanup is unavoidable
- if the same term appears multiple times and the same explanation applies, reuse the same `ref`/`def`
- if a glossary item does not clearly map to any inline occurrence, keep it as a normal glossary section instead of forcing a fake inline annotation

In short: when the source is trying to explain a word or phrase inside the reading flow, prefer `pop`.

### Pop extraction strategy from Word or pasted notes

When converting source annotations into `pop`, follow this sequence:

1. Identify annotation sources:
   - Word footnotes
   - Word endnotes
   - glossary lists after the passage
   - vocabulary/terms sections that define words used in the text
2. Normalize them into note records:
   - note id
   - source label or marker if present
   - term or phrase being explained
   - note body
   - likely anchor paragraph or sentence
3. Anchor each note to the passage conservatively:
   - first prefer exact term matches in the related sentence or paragraph
   - if there are multiple matches, prefer the occurrence nearest the relevant source span
   - if the note clearly belongs to a numbered footnote marker, attach it where that marker appears
4. Generate `pop` only when the anchor is credible:
   - inline trigger in the prose -> `:pop[term]{ref=...}`
   - note body outside the interaction block -> `:::pop{def=...}`
5. If anchoring is weak or ambiguous:
   - keep the note as a normal glossary or note list
   - do not force a guessed inline `pop`
   - add a TODO comment only when the missing mapping matters to the page

Extra handling rules:

- Prefer the original annotated term or phrase as the popup trigger text.
- Do not silently merge different notes just because the terms look similar.
- If a vocabulary section explains a word that appears many times, annotate only the most relevant first occurrence unless the source clearly expects repeated annotation.
- If the note body is long, keep the trigger short and move the detail into the `def` body.
- If the note belongs to a word-bank, answer key, or exercise-only metadata rather than the running text, do not convert it into `pop`.

Mini examples:

```mdx
Word-like source:
The Palace Museum has undergone digital transformation.1

1. digital transformation: the use of digital technology to improve access and communication.

Preferred authoring:
The Palace Museum has undergone :pop[digital transformation]{ref=term-digital-transformation}.

:::pop{def=term-digital-transformation}
digital transformation: the use of digital technology to improve access and communication.
:::
```

```mdx
Word-like source:
Vocabulary
- emblem: a symbol or sign that represents something

Passage line:
These products feature royal emblems.

Preferred authoring:
These products feature royal :pop[emblems]{ref=term-emblem}.

:::pop{def=term-emblem}
emblem: a symbol or sign that represents something
:::
```

```mdx
Word-like source:
Glossary
- heritage: cultural traditions and historical objects passed down over time

Passage:
The section does not actually use this word anywhere.

Preferred handling:
Keep it as a normal glossary list.
Do not invent a fake inline `:pop[heritage]{...}` anchor.
```

### Theme-aware styling rules

When you use `styleBlock`, `styleText`, or `styleLine`, prefer the repo's theme tokens over hard-coded colors.

Default decision rule:

1. If an existing semantic token expresses the intent, use `var(--token)`.
2. If no semantic token fits, try a broader shared token such as `--text-*`, `--surface-*`, or `--accent-*`.
3. Only if neither exists, use a literal CSS value.

- These style directives support `var(...)` and CSS expressions such as `calc(...)`, `clamp(...)`, `min(...)`, and `max(...)`.
- Prefer semantic tokens so the page keeps working across theme switches.
- Good defaults:
  - card-like container -> `background=var(--card-bg)` `border-color=var(--card-border)` `box-shadow=var(--card-shadow)`
  - emphasized text -> `color=var(--text-strong)` or `color=var(--accent-1)`
  - quiet helper text -> `color=var(--text-muted)` or `color=var(--text-quiet)`
  - soft quote / note area -> `background=var(--quote-bg)` `color=var(--quote-text)`
  - button-like or trigger styling -> prefer `--button-*` or `--choice-option-*` tokens when they match the intent
- Prefer token families in this order:
  - semantic component tokens such as `--card-*`, `--button-*`, `--choice-option-*`
  - text tokens such as `--text-strong`, `--text-muted`, `--text-subtle`, `--text-quiet`
  - shared surface/accent tokens such as `--surface-1`, `--surface-2`, `--accent-1`, `--accent-2`
- Avoid hard-coded hex colors unless:
  - the source explicitly requires a fixed brand color
  - the reference page clearly relies on a one-off visual signal that is not covered by tokens
  - a CSS value must stay literal, such as a very specific gradient or image URL
- Use style directives for teaching function, not decoration. If plain markdown communicates the same thing, skip the style wrapper.
- Keep style spans local and minimal. Do not restyle whole pages when a heading, a short note, or a single boxed section is enough.
- For `styleLine`, always author it in the line-start shorthand form: `::styleLine{...} Your line text`.
- Even though the repo supports bracket-label `::styleLine[...]{...}`, generated lesson content should consistently use the line-start shorthand form.

Example patterns:

```mdx
:::styleBlock{background=var(--card-bg) border-color=var(--card-border) box-shadow=var(--card-shadow) border-radius=var(--card-radius) padding=var(--card-padding)}
Key reminder content.
:::

:styleText[core idea]{color=var(--accent-1) font-weight=700}

::styleLine{background=var(--quote-bg) color=var(--quote-text) padding=8 border-radius=999} Reading tip
```

### Theme-aware display directive patterns

If the page needs reveal, glossary, or sticky reminder behavior, keep those wrappers theme-safe too.

- `collapse`
  - trigger styles belong on `:::collapse[...] {...}`
  - revealed body styles usually belong on an inner `:::styleBlock{...}`
- `pop`
  - keep `:pop[term]{ref=...}` lightweight
  - put rich popup body content in `:::pop{def=...}`
  - when popup content needs visual treatment, style the body with an inner `styleBlock`
- `sticky`
  - positioning belongs on `:::sticky{top=... zIndex=...}`
  - visual treatment usually belongs on nested content, not on the sticky wrapper itself

Recommended patterns:

```mdx
:::collapse[Show notes]{button=true background=var(--button-bg) color=var(--button-text) border-color=var(--button-border) border-radius=999 padding=8}
:::styleBlock{background=var(--card-bg) border-color=var(--card-border) box-shadow=var(--card-shadow) border-radius=var(--card-radius) padding=var(--card-padding)}
Detailed notes that stay theme-safe.
:::
:::

:pop[Palace Museum]{ref=term-palace}

:::pop{def=term-palace}
:::styleBlock{background=var(--card-bg) border-color=var(--card-border) box-shadow=var(--card-shadow) border-radius=var(--card-radius) padding=16}
**Palace Museum / Forbidden City**

A theme-aware glossary popup body.
:::
:::

:::sticky{top=0 zIndex=5}
:::styleBlock{background=var(--quote-bg) color=var(--quote-text) border-color=var(--card-border) border-radius=12 padding=12}
Reading checkpoint or reminder.
:::
:::
```

### Common token cheat sheet

Use these as the first-choice pool when generating style attrs:

- container/card: `--card-bg`, `--card-border`, `--card-shadow`, `--card-radius`, `--card-padding`
- text hierarchy: `--text-strong`, `--text-muted`, `--text-subtle`, `--text-quiet`, `--text-inverse`
- accents/surfaces: `--accent-1`, `--accent-2`, `--surface-1`, `--surface-2`
- note/quote surfaces: `--quote-bg`, `--quote-text`
- button-like trigger styling: `--button-bg`, `--button-text`, `--button-border`, `--button-radius`, `--button-shadow`
- choice-like trigger styling: `--choice-option-bg`, `--choice-option-text`, `--choice-option-border`, `--choice-option-radius`, `--choice-option-shadow`

When the source does not specify a special look, default to card/text/quote tokens before reaching for literal colors.

### Teaching intent to token patterns

When the source suggests a teaching function but does not prescribe exact colors, prefer these mappings:

- neutral content box
  - use `background=var(--card-bg)` `border-color=var(--card-border)` `box-shadow=var(--card-shadow)`
- term / glossary / concept card
  - use card tokens for the body
  - optionally highlight the term itself with `:styleText[...,]{color=var(--accent-1) font-weight=700}`
- reading tip / strategy reminder
  - use `background=var(--quote-bg)` `color=var(--quote-text)`
  - for short one-line reminders, `styleLine` is usually enough
  - always write it as `::styleLine{...} text`, not bracket-label form
- exercise directions / task instruction
  - prefer `color=var(--text-strong)` with minimal styling
  - if boxed treatment is helpful, use card tokens before accent-heavy styling
- answer explanation / after-check feedback
  - prefer card or quote tokens, depending on whether the tone is neutral explanation or teacher note
  - avoid loud accent backgrounds unless the source clearly calls for it
- important warning / common mistake
  - first try `color=var(--accent-1)` for inline emphasis
  - if a box is needed, combine `var(--card-bg)` with accent text instead of inventing a new warning palette
- popup trigger / reveal trigger
  - prefer `--button-*` tokens when it behaves like a button
  - prefer `--choice-option-*` tokens when it visually behaves like a selectable chip or option
- sticky checkpoint / progress reminder
  - prefer `var(--quote-bg)` and `var(--quote-text)` for note-like reminders
  - switch to card tokens if the sticky block contains longer content

These are defaults, not rigid categories. Follow the source's teaching purpose first, then choose the lightest token pattern that communicates it.

### Styling self-check

Before finalizing a page that contains style attrs:

- scan style attrs for hard-coded hex, `rgb(...)`, or `hsl(...)` values
- keep them only when the source or reference genuinely requires a fixed visual signal
- otherwise replace them with the nearest theme token
- if both trigger and body are styled, ensure trigger tokens and body tokens are chosen separately
- prefer consistency across the same page: similar note boxes should usually share the same token pattern

### Handle incomplete exercises conservatively

- Missing answer for an objective item: keep the exercise as plain markdown or add an HTML TODO comment.
- Missing explanation: omit `[explanation]`.
- Missing options for a choice question: do not force it into `:::choice`.
- Missing prompt for translate/writing: do not synthesize one.

## Output modes

### If the user gave a target path

Write the `.mdx` file directly.

### If the user did not give a target path yet

Ask for:

- the save folder or target path
- the filename

If needed, suggest a filename before writing.

### If the user explicitly wants inline output

Return:

- a suggested filename
- the complete `.mdx` content
- a short note for any unresolved TODOs

### If the user asked for a whole unit

Return the unit plan first unless the mapping is already obvious from context and the user explicitly wants immediate generation.

## Report format to the user

Lead with what you generated, then mention:

- where the page was written, or the suggested filename
- which directive types were used
- whether any unresolved source gaps were kept as TODO comments

For unit work, also mention:

- how the target material was split
- which reference pages or patterns were reused
- which pages were high-confidence vs low-confidence
- any mismatches that need review

## Quick reminders

- Canonical syntax wins over aliases in generated output.
- `mdx-scorm` dynamic/user-authored content should stay directive-based.
- Be faithful to the source.
- When unsure, choose simpler syntax over clever syntax.
- Learn transformation patterns from the reference unit; do not copy its facts into the target unit.



