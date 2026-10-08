# Page presentation and authoring heuristics

Use with SKILL.md. For exercise selection read exercise-type-selection.md; for Word/Pop fidelity read source-fidelity-and-reference-style.md; for standalone CSS read stylesheet-authoring.md.

### Prefer plain markdown for exposition

Use standard headings, paragraphs, lists, blockquotes, tables, images, audio, and video unless a display directive is clearly helpful.

### Prefer the simplest supported directive

- Use `styleBlock` only when local styling or boxed emphasis is useful.
- Use `play` for short inline audio cues or pronunciation prompts.
- Use `collapse` for optional extra explanation.
- Use `pop` primarily for inline annotation derived from the source, especially footnotes, endnotes, vocabulary notes, and term explanations.
- Use `wide` only when a table, code block, or other wide content needs its own horizontal scrolling area.
- Use `splitpane` when learners need to keep a long reference text visible while answering questions or completing a task.
- Use `sticky` when learners need to repeatedly glance at a short reference block such as a word bank, checklist, or compact note.
- Use `splitpane`, `columns`, `carousel`, and `iframe` only when the source clearly calls for layout or embedded content.
- Use `showAfterSubmit` only when the page really has a formal first-pass task and a meaningful post-submit follow-up.
- Use `discussion` / `debate` only when the source truly expects threaded class interaction, not as a substitute for ordinary writing prompts.
- Use `game-matching`, `game-memorymatch`, `game-choice`, and `game-tokenbuilding` only when the source or reference explicitly asks for game-like retry practice; keep exam-style items in normal interaction blocks.
- Do not downgrade an explicit matching or ordering task to `choicecloze` because the reference course lacks an example of `matching` or `sorting`; use the supported semantically correct directive.
- Use `aiexercise`, `media`, `exportcontent`, and `askAI` only when the user explicitly wants generated practice, transcript-aware media, export tooling, or inline AI assistance on the page.

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

### Mature reading-course page patterns

Use these patterns when the target material resembles the mature reading-course references:

- Long reading passage plus nearby questions: use `splitpane`; put the source passage in `splitTop` and questions/tasks in `splitBottom`.
- Passage vocabulary, footnotes, and professional terms: use inline `:pop[...]` triggers and place the matching `:::pop{def=...}` definitions near the page end.
- Paragraph translations or answer explanations that should unlock only after submission: wrap them in `:::showAfterSubmit` and `:::collapse[...]`.

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

Treat `pop` as the default annotation mechanism for Word footnotes/endnotes and end-of-passage vocabulary, cultural/professional term, and glossary sections.

- Build a ledger of every source annotation before editing the passage.
- Preserve each ledger item once as a reachable Pop definition or a visible ordinary note/glossary entry.
- Search the preceding associated passage first with Unicode-aware case-insensitive comparison, then with punctuation/hyphen normalization, inflectional, transparent derivational, multiword, shortened-name, acronym, and alias variants.
- Treat capitalization-only differences as direct matches. For example, an end note headed `Artificial Intelligence` matches passage text `artificial intelligence`.
- Preserve source casing on both sides: use the exact passage form in the visible `:pop[...]` trigger, keep the note headword's original form in the Pop definition, and use the headword only to derive the stable id. Do not rewrite either surface form merely to make their capitalization agree.
- Preserve surrounding emphasis without wrapping `:pop[...]` in Markdown delimiters. If the source or reference applies bold, italic, strikethrough, or a combination across text that contains the trigger, wrap the complete formatted span with `<b>`, `<i>`, and/or `<del>` in canonical nesting order; keep Markdown emphasis for spans that do not contain `pop`.
- Require credible word or phrase boundaries after case normalization; do not accept an unrelated substring merely because its folded casing matches.
- Remove only entries successfully replaced by reachable Pop definitions; preserve unanchored entries in the visible note/glossary list.
- If no credible anchor exists, do not invent a ref. In hosted / Cloud Studio mode, preserve the source entry in its ordinary glossary/notes form and expose one non-blocking `authoring` ProductionIssue; do not create an unreachable Pop definition and do not create `TODO.txt`. In local file mode, also preserve the entry visibly and report the missing anchor separately; do not leave an unreachable definition.
- Follow the corresponding reference page's Pop body style. For the supplied Unit 1 pattern, use a bold headword, an italic unparenthesized part-of-speech label, and Markdown list items for collocations/examples.

Read and follow [source-fidelity-and-reference-style.md](source-fidelity-and-reference-style.md) for the complete matching order, reference-style rules, and count checks.

### Pop extraction strategy from Word or pasted notes

Normalize each note into an id, headword, full body, note category, and associated source span. Match and format it with [source-fidelity-and-reference-style.md](source-fidelity-and-reference-style.md); compare candidate anchors case-insensitively while retaining their original surface casing. Before packaging, compare source-note count against reachable Pop definitions plus preserved visible notes and run `scripts/validate_course_output.py`.

### Theme-aware styling rules

When you use `styleBlock`, `styleText`, or `styleLine`, prefer the repo's theme tokens over hard-coded colors.

Default decision rule:

1. For a card, first use `styleBlock{class="card"}`. For other styling or explicitly requested overrides, use an existing semantic token when it expresses the intent.
2. If no semantic token fits, try a broader shared token such as `--text-*`, `--surface-*`, or `--accent-*`.
3. Only if neither exists, use a literal CSS value.

- These style directives support `var(...)` and CSS expressions such as `calc(...)`, `clamp(...)`, `min(...)`, and `max(...)`.
- Prefer semantic tokens so the page keeps working across theme switches.
- Good defaults:
  - card-like container -> `styleBlock{class="card"}`
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
:::styleBlock{class="card"}
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
:::styleBlock{class="card"}
Detailed notes that stay theme-safe.
:::
:::

:pop[Palace Museum]{ref=term-palace}

:::pop{def=term-palace}
:::styleBlock{class="card"}
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

When the source does not specify a special look, use the built-in card class for cards and text/quote tokens for other styling before reaching for literal colors.

### Teaching intent to token patterns

When the source suggests a teaching function but does not prescribe exact colors, prefer these mappings:

- neutral content box
  - use `styleBlock{class="card"}`
- term / glossary / concept card
  - use `styleBlock{class="card"}` for the body
  - optionally highlight the term itself with `:styleText[...,]{color=var(--accent-1) font-weight=700}`
- reading tip / strategy reminder
  - use `background=var(--quote-bg)` `color=var(--quote-text)`
  - for short one-line reminders, `styleLine` is usually enough
  - always write it as `::styleLine{...} text`, not bracket-label form
- exercise directions / task instruction
  - prefer `color=var(--text-strong)` with minimal styling
  - if boxed treatment is helpful, use `styleBlock{class="card"}` before adding custom styling
- answer explanation / after-check feedback
  - prefer `styleBlock{class="card"}` for a neutral card or quote tokens for a teacher note
  - avoid loud accent backgrounds unless the source clearly calls for it
- important warning / common mistake
  - first try `color=var(--accent-1)` for inline emphasis
  - if a card is needed, use `styleBlock{class="card"}` with accent text instead of inventing a new warning palette
- popup trigger / reveal trigger
  - prefer `--button-*` tokens when it behaves like a button
  - prefer `--choice-option-*` tokens when it visually behaves like a selectable chip or option
- sticky checkpoint / progress reminder
  - prefer `var(--quote-bg)` and `var(--quote-text)` for note-like reminders
  - use an inner `styleBlock{class="card"}` if longer sticky content needs a card

These are defaults, not rigid categories. Follow the source's teaching purpose first, then choose the lightest token pattern that communicates it.

### Styling self-check

Before finalizing a page that contains style attrs:

- scan style attrs for hard-coded hex, `rgb(...)`, or `hsl(...)` values
- keep them only when the source or reference genuinely requires a fixed visual signal
- otherwise replace them with the nearest theme token
- if both trigger and body are styled, ensure trigger tokens and body tokens are chosen separately
- prefer consistency across the same page: similar note boxes should usually share the same token pattern
