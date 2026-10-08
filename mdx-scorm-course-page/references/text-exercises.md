# Text selection and correction authoring

Self-contained contract for local authors and explicitly configured hosted agents. Rechecked against mdx-scorm repository commit `9c00bc4e` (User Manual 6.18–6.19 and shared text semantics; originating cloud reference audited `1001918c`). Repository paths are maintenance provenance, not required cloud dependencies. Runtime support must be deployed by the host; updating this skill alone does not deploy the engine.

## Choose by learner action

- Select pronouns, verbs, punctuation or other single tokens directly in a sentence: `textselect`, default `mode="word"`.
- Select complete contiguous phrases directly in a sentence/passage: `textselect{mode="span"}`. Keep distinct answers distinct, even when adjacent.
- Insert, delete or replace text to correct a sentence/passage: `textedit`. Preserve the erroneous original and encode supplied corrections.
- A separate option list remains `choice`; genuine gaps remain fillblank/choicecloze. Do not force in-place text tasks into those types merely to imitate a reference page.

## Shared sections and attributes

Use exact lowercase `:::textselect` / `:::textedit`, with matching closing fences. These names and their internal markers have no Chinese aliases. Each section can occur once:

| Section | Meaning |
| --- | --- |
| `[prompt]` | Optional question instructions; Markdown formatting/media are allowed according to the existing display contract. |
| `[content]` | Required literal original text, with answer markers. It is not a Markdown rich-content area. |
| `[explanation]` | Optional source-provided Markdown explanation; omit if absent rather than inventing it. |

Do not add `[answer]`, `[options]`, `[ai]`, or item-list wrappers inside these blocks. Mark answers directly in `[content]`. Put headings, list formatting, images, Pop annotations and styled text in prompt/explanation or adjacent page content, not inside selectable text. Keep all source teaching material, but do not let general Pop/formatting rules change the answer-bearing original.

| Attribute | Values |
| --- | --- |
| `id` | Optional explicit stable ID; unique within a page. |
| `mode` | textselect only: `word` (default) or `span`. |
| `open` | Default false; explicit true allows no reference targets and uses completion instead of correctness. |
| `weight` | Nonnegative question weight; use 0 only when zero score weight is requested. |
| `scorm` | Follow existing formal participation defaults; false only for explicitly requested practice-only behavior. |
| `showExplanation` | `onSubmit` (default), `instant`, `none`. |

Omit unrequested defaults. `open=true` does not itself make score weight zero. `weight=0` does not disable correctness feedback, formal submission or restoration. Do not add `rows`, `aiScore`, `[ai]`, `share`, `shareComments`, `useManualMarking` or `weightDistribution`.

Before submission, immediate explanation display requires a nonempty selection or effective correction. Submitted/post-submit browse state follows the existing display rules; `none` hides the runtime explanation. PDF uses student/teacher profile rules instead.

## Word selection

Use one `:pick[...]` per supplied answer:

```mdx
:::textselect
[prompt]
选出所有代词。
[content]
:pick[She] gave :pick[him] a book because :pick[he] needed :pick[it].
[explanation]
She、him、he、it 都是代词。
:::
```

In word mode, each answer must cover exactly one complete tokenizer unit, including punctuation if that is the requested target. Do not mark `:pick[he]r` within “her”. Han characters are individual units; use span mode for multi-character phrases.

## Span selection

```mdx
:::textselect{mode="span"}
[prompt]
选出完整的动词短语。
[content]
She :pick[has been waiting] here. They :pick[will leave] soon.
[explanation]
保留助动词与实义动词组成的完整语块。
:::
```

Learners click the start and end tokens, then confirm in the floating toolbar. A single-token span uses the same token as both endpoints. Selected spans cannot overlap or cross a blank-line paragraph boundary. Do not merge adjacent targets unless the source treats them as one answer.

Standard scoring uses `max(0, exactCorrect - disjointExtra) / referenceTargetCount`. A partially overlapping span is a boundary error: no credit, but no extra-selection deduction. Missing targets earn no credit. For four targets, three exact choices score 3/4; adding one disjoint incorrect choice gives 2/4. Do not describe standard span scoring as per-word overlap credit.

## Correction: replacement, deletion, insertion

```mdx
:::textedit
[prompt]
改正句子中的错误。
[content]
She :fix[go]{to="went"} home yesterday.
I bought :add[a] book.
He went :del[to] home.
[explanation]
分别修正过去式、补充冠词、删除多余介词。
:::
```

- `:fix[go]{to="went"}` displays original “go” and defines replacement “went”.
- `:del[to]` displays original “to” and defines deletion.
- `:add[a]` defines inserted “a”; it is absent from the original shown to learners.
- Use square-bracket marker bodies. Do not use the earlier proposal `:fix{}{to="..."}`, ad-hoc arrows, deletion-line Markdown, or an answer paragraph as substitutes for these markers.
- Every marker is a distinct reference scoring point. Keep a multiword replacement in one marker when the source defines one correction.
- Inserting after the preceding word and before the following word share one boundary. Write `:add[...]` at that boundary; do not invent before/after attributes.
- Inserted/replacement strings must not have leading/trailing spaces or line breaks. The layout resolves adjacent English spacing and punctuation, and avoids mechanically inserting spaces between Chinese characters. Do not pad `:add[ a ]`.
- Do not rewrite the original to the correct text first: that erases the task. Do not add error positions or reference text unsupported by the supplied key, unless the user explicitly asks you to create new exercises and answers.

Full normalized final-text equality receives full credit even when learner-selected edit boundaries differ from the author's markers. Otherwise award confirmed correct reference points minus extra-change runs, divided by target count, with a floor of zero. Score the final text, not the number of UI operations. If multiple alignments are possible, use only confirmed points and the minimum provable number of extra-change runs; the runtime flags uncertain attribution.

Normalization unifies line endings and horizontal whitespace, trims each line's edges, but retains case and punctuation. Do not promise case-insensitive or punctuation-insensitive full-text grading.

## Open and zero-weight example

Only use open mode on an explicitly open task. This example is both open and zero-weight because both were requested:

```mdx
:::textedit{open=true weight=0}
[prompt]
自由修改下面的句子，本题不计入总分。
[content]
I like this place.
:::
```

For open selection, completion requires at least one selected range. For open correction, the normalized final text must differ from the original; a whitespace-only change is insufficient. Open tasks may retain supplied reference targets, but do not auto-judge against them. If an ordinary scored task lacks its answer, follow hosted clarification/repair rules; do not fabricate an answer or silently make it open.

## Limits and escaping

- Original text must be nonempty and at most 300 tokenizer units (English words, punctuation and Han characters); this is not a 300-character allowance. Split long passages only with source-faithful task boundaries, or explain the limit; never silently truncate.
- Markers must start/end on whole-token boundaries. No nested or overlapping markers. Selection spans cannot cross blank-line paragraph boundaries; corrections cannot span any newline.
- A replacement/insertion is trimmed, single-line and at most 1000 characters. The shared validator also limits serialized edits to 3800 characters, the result to 600 tokens and the number of edits to 300; the host remains authoritative.
- In literal text and bracket marker bodies, escape literal backslash, brackets and colon with a backslash. Encode `to` as a JSON string, including JSON escaping for double quotes/backslashes. Keep attribute delimiter quotes ASCII.
- Do not write section labels on standalone lines as exercise content or inside code examples within these sections: the text-exercise section reader reserves `[prompt]`, `[content]`, `[explanation]` as boundaries.
- Standard closed questions require at least one valid reference marker. No-op reference corrections are invalid.

## Cloud Studio and delivery

Local authors follow the destination/report rules in SKILL.md. Only explicitly configured hosted integration uses the candidate envelope in hosted-protocol.md; these types do not change that protocol. Generate canonical MDX, not editor JSON, DOM, CSS or runtime scoring code.

Cloud Studio has native rich prompt/explanation sections, a dedicated original-text/answer canvas and shared side-panel properties. Replacing the original via the canvas clears old markers. Unsupported source remains a complete source island instead of dropping content. Root native insertion is verified at page-body level; do not nest exercises inside another exercise or assume every display container supports them.

Runtime supplies the floating toolbar and inline feedback. Use built-in theme/i18n behavior rather than emitting custom buttons, summary panels or handcrafted reference-answer UI. AI companion context is already supplied by the runtime; do not invent `[ai]` configuration for these types.

PDF student projections contain prompt and original text without reference answers or explanations. Teacher projections include authored reference markers and explanations; an open question with no reference targets has no fabricated answer. Runtime `showExplanation` does not suppress teacher-profile print explanations. Do not claim that a skill ZIP installs or activates these engine/export changes on the server.

## Preflight

Check the supported shape, attrs, answer source, literal original text, token boundaries and limits above. Run the existing convention checker when file-mode tools are available, but retain Cloud Studio's host syntax/semantic validation: the bundled Python checker does not implement the complete new-type grammar. Unsupported or incomplete content should follow the original hosted uncertainty rules, not be coerced into a valid-looking question.
