# mdx-scorm syntax inventory

This file is a source-audited syntax reference for `mdx-scorm`.

Use it when generating authored lesson pages. Prefer the canonical ASCII syntax shown here, even though the runtime also supports aliases and normalization.

## Global authoring rules

- Keep directive fences on their own lines.
- Use canonical directive names in final output.
- Use `@--@` for ordinary blank positions in both `fillblank` and `choicecloze`. `@blank@` is invalid and must never appear in generated MDX.
- Nested display directives are allowed.
- Do not nest one interactive question block inside another interactive question block.
- The runtime normalizes Chinese aliases, full-width punctuation, and some mojibake prefixes, but generated output should stay canonical.
- For user-authored content, avoid general interactive JSX. Use directive blocks instead.
- Frontmatter parsing is strict and repo-specific. Do not treat it as free-form YAML.
- In `build:content`, general JSX components such as `<Choice />`, `<ShowAfterSubmit />`, and `<AiExercise />` do not execute. Prefer directive blocks for authored content.
- Local media should be authored as package-relative assets that resolve through `public/media`, not by hard-coding runtime package identity.

## Common inline formatting reminders

Use standard Markdown for normal inline emphasis:

- `**bold**`
- `*italic*`
- `~~strikethrough~~`
- `` `code` ``

This Markdown form is valid only when the formatted span does not contain an inline `pop`. Do not author forms such as:

```md
**aaa :pop[trigger]{ref=term-trigger} bbb**
```

The renderer does not support `pop` nested inside Markdown emphasis or strikethrough delimiters. When the formatted span contains `:pop[...]`, replace the whole surrounding delimiter pair with inline HTML:

- italic -> `<i>aaa :pop[trigger]{ref=term-trigger} bbb</i>`
- bold -> `<b>aaa :pop[trigger]{ref=term-trigger} bbb</b>`
- strikethrough -> `<del>aaa :pop[trigger]{ref=term-trigger} bbb</del>`
- bold italic -> `<b><i>aaa :pop[trigger]{ref=term-trigger} bbb</i></b>`
- bold italic strikethrough -> `<b><i><del>aaa :pop[trigger]{ref=term-trigger} bbb</del></i></b>`

For any other combination, retain the canonical tag order `b` outermost, then `i`, then `del`, and omit tags that do not apply. Convert only the smallest complete formatting span that contains the `pop`; keep unrelated emphasis in Markdown.

Write external webpage links with standard Markdown link syntax:

```md
[Article title](https://example.com/article)
```

This applies especially to `Source`, `Adapted from`, and reference lines. Do not use angle-bracket autolinks such as `<https://example.com>` because the course renderer does not support them. Prefer a readable article title, publication, or source label as the link text. If no label is available, write `[https://example.com](https://example.com)`.

When the source clearly needs underline, superscript, or subscript, use inline HTML because standard Markdown does not define them:

- underline -> `<u>key term</u>`
- superscript -> `10<sup>2</sup>`
- subscript -> `H<sub>2</sub>O`

Notes:

- These forms are already used in the repo's markdown demos and are compatible with the current renderer.
- If the goal is not semantic superscript/subscript but simply visual underline emphasis inside a themed sentence, `:styleText[...]` with `text-decoration=underline` can be a better fit than raw HTML.
- Do not invent pseudo-Markdown such as `^sup^` or `++underline++` unless the source explicitly uses a plugin syntax that this repo actually supports.

## Frontmatter baseline

A page needs no frontmatter by default. Add `title` only on explicit user request; preserve existing titles when editing. Example body:

```mdx
# Page heading
```

Let the course runtime supply its default feedback and numbering behavior. Do not emit `feedback`, `numberType`, `numberingType`, `numbering`, or page-level `type` unless the corresponding reference page explicitly uses a supported override or the author explicitly requests one. In particular, omit `feedback: submit` when it only restates the runtime default.

Current parser and page-control notes:

- Prefer single-line `key: value` fields.
- When explicitly required, `feedback` accepts `submit`, `submit_<n>`, and `instant`.
- `numberingStart` is a positive integer and only matters when numbering is enabled.
- Common optional page-level fields include `weights`, `scoreCardShowWeights`, `noSubmit`, `scormDebug`, `autoShowScoreCardOnSubmit`, `scoreCardGrouping`, `cardMode`, `browseMode`, `isShowDictionary`, `ai`, and `aiCompanion`.
- `weights:` supports a one-level map from interaction type to positive number, including game interaction types such as `game-matching`, `game-memorymatch`, `game-choice`, and `game-tokenbuilding`.
- `ai:` supports the documented one-level page AI object; `ai.prompt` is the only supported list shape when multiple prompts are required.
- `aiCompanion:` supports the documented one-level object shape with fields such as `enabled`, `appId`, `interactiveVisibility`, and `questionOverlay`.
- Avoid arbitrary arrays, multiline strings, and deep nested objects.

Reference files:

- `mdx-scorm/frontmatter写法规范.md`
- `mdx-scorm/User Manual.md`

`scoreCardShowWeights` controls weight-number visibility only. Resolution: explicit page frontmatter → nearest configured group → unit → course → default true. Course syntax is `Catalog { org.scorecardshowweights=false }`; unit/group use `scoreCardShowWeights=false`. Omission restores inheritance; do not add redundant page overrides. Catalog `(mdx)` entries are not an override layer.

## Media authoring

Ordinary loaded body images already open the course image viewer with zoom controls, wheel/pinch zoom, drag when zoomed, and close controls. Images inside links or interactive controls keep their original action. Use `data-image-viewer-disabled="true"` on an ancestor only when this behavior must be disabled. Do not generate zoom scripts. Print/PDF keeps static images.

Use package-relative authored paths and let the runtime normalize them through `/media/...`.

Examples:

```md
![Local image](sample-image.png)

[Local audio](u01/sample-audio.mp3)

[Local video](u01/sample-video.mp4)

<audio controls src="sample-audio.mp3"></audio>

<video controls src="u01/sample-video.mp4"></video>
```

Notes:

- Place local assets under `public/media/`.
- Preserve each external URL target exactly when wrapping it in Markdown link syntax; do not silently shorten, normalize, or replace the destination.
- Direct HTML media tags and Markdown image/link syntax are both supported. For an ordinary external webpage link, use `[display text](https://...)`, not `<https://...>`.
- Do not encode `offline_media_id` or package folder assumptions into the content path itself.

## SCORM participation rule

Most low-level interactions default to tracked mode.

- `scorm=true` is the normal default.
- `scorm=false` keeps the task usable but removes it from numbering, score cards, submit gating, `cmi.interactions.*` writes, and tracked restore.
- `ShowAfterSubmit` forces all nested interactive descendants into practice mode even if a child block was authored with `scorm=true`.

For a question that should not count toward the score, set `weight=0`, not `scorm=false`. Zero-weight formal questions retain completion checks, submission, and restoration. Question-level `weight` accepts nonnegative values; page-level `weights` still accepts positive values only. Do not generate `scorm=false` unless the user explicitly requests exclusion from formal tracking.

## Common interaction attributes

Unless the user explicitly requests input rows or height, omit `rows` for every component. Supported row attributes below document capability, not defaults to generate.

Most formal interaction directives support the following current attributes:

- `id`: stable interaction id, useful for manual marking and long-term restore stability.
- `weight`: nonnegative base weight; use `0` for a non-scoring formal question.
- `weightDistribution=shared|average`: child-slot weight behavior.
- `scorm=true|false`: `false` makes the interaction practice-only.
- `open`: completion-only mode for supported items.
- `isshared=true|false`: legacy SCORM shared marker.

Current subjective sharing is controlled by `share`, not legacy `isshared`:

- `share=true`: opens the current shared-response UI and sets the SCORM shared marker.
- `share=true shareComments=true`: also enables peer comments in the shared-response panel.
- `shareComments=true` without `share=true` has no UI effect.

Manual marking is explicit per formal interaction:

- `useManualMarking=true`: scored teacher marking for `writing`, `translate`, `recorder`, and supported `fillblank` shapes.
- `useManualMarking=true`: scored teacher marking with comments for `imageupload` and `videoupload`.
- `fillblank useManualMarking=true` is valid only for `aiScore=true` or a single standalone open blank.
- Practice-only interactions (`scorm=false` or inside `showAfterSubmit`) do not infer manifest manual marking.

## Interactive blocks

### choice

Canonical block:

```md
:::choice
[stem]
Choose the correct answer.

[options]
A. Option one
B. Option two

[answer]
A

[explanation]
Optional explanation.
:::
```

Supported aliases in repo:

- `choice`, `选择题`

Sections:

- `[stem]`, `[options]`, `[answer]`, `[explanation]`
- Chinese section names also work at runtime, but do not generate them by default

Key attributes:

- `open`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`

Notes:

- Multi-select is authored with one answer label per line, for example `A` on one line and `C` on the next.
- With `open=true`, zero or more answer labels are valid. A supplied answer is a reference answer and does not participate in scoring; an empty `[answer]` section is valid and must not be auto-filled.
- Labels can be letters, numbers, roman numerals, Chinese labels, or custom labels.
- The runtime accepts spaces, commas, Chinese commas, or line breaks, but generated course content must use line breaks only. Do not author `AC`, `A C`, `A,C`, `A，C`, `A、C`, or other same-line multi-answer forms.
- Option continuation lines are preserved.

Source of truth:

- `mdx-scorm/src/mdx/remarkChoiceBlock.ts`
- `mdx-scorm/Developer Manual.md`

### fillblank

Canonical block:

```md
:::fillblank
[content]
Dolphins are @--@ and live in the @--@.

[answer]
mammals
ocean

[explanation]
Optional explanation.
:::
```

Supported aliases in repo:

- `fillblank`, `fill-blank`, `填空`, `填空题`

Sections:

- `[content]`, `[answer]`, `[explanation]`, `[ai]`, `[template]`

Key attributes:

- `open`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `aiScore=true|false`
- `share=true|false`
- `shareComments=true|false`
- `isshared=true|false`
- `useManualMarking=true|false`

Token rules:

- `@--@` consumes the next answer from `[answer]`
- `@answer@` embeds an inline answer
- `@a|b@` allows multiple correct answers
- `\@` escapes a literal `@`
- `@blank@` is not an authored blank token; use `@--@`. Do not replace literal quoted/source examples blindly.

Notes:

- If `[answer]` has one non-empty line, it may use `,` `，` `;` `；` `、` separators.
- Open mode treats any non-empty input as correct.
- Ordinary FillBlank answer comparisons normalize straight/curly single and double quotation marks; preserve curly visible prose and do not claim this behavior for every interaction.
- `rows` now accepts a positive integer for standalone FillBlank textareas, including AI FillBlank; the runtime default is 2. It does not resize inline blanks. Omit it unless the user explicitly requests rows or input height.
- `aiScore=true` is mainly for one standalone short-answer blank; `[template]` may provide initial textarea scaffolding.
- `share=true shareComments=true` only exposes the current shared-response UI for a single standalone short-answer blank.
- `useManualMarking=true` is supported only for `aiScore=true` or a single standalone open blank.

Source of truth:

- `mdx-scorm/src/mdx/remarkFillBlankBlock.ts`
- `mdx-scorm/Developer Manual.md`

For requested per-blank non-AI scoring, `interactionWeights="1,1,3"` supplies final weights in actual blank order, including embedded answers. It overrides `weight`, `weightDistribution` and page type weights. Supply one finite nonnegative number per blank; do not combine with `aiScore=true`. Invalid configuration blocks normal submission. See [reading-and-reveal.md](reading-and-reveal.md#fillblank-final-per-blank-weights).

### choicecloze

Canonical block:

```md
:::choicecloze
[content]
Dolphins are @--@ and remain @--@ in groups.

[options]
i. social | ii. solitary | iii. playful

[answer]
1
3
:::
```

Answer indexing:

- `[answer]` may use a matching uppercase alphabetic option label when the options are written as `A. ...`, `B. ...`, `C. ...` or as a bare label list such as `A | B | C`; retaining `A`, `B`, or `C` is valid.
- When options are labeled with ASCII or Unicode Roman numerals (`i.`, `ii.`, `iii.` or `ⅰ.`, `ⅱ.`, `ⅲ.`), `[answer]` must use the corresponding 1-based decimal position (`1`, `2`, `3`, ...).
- Never place Roman numerals such as `ii` or `ⅲ` in `[answer]`. Unlabeled option lists should also use decimal positions.

Supported aliases in repo:

- `choicecloze`, `choice-cloze`, `选词填空`, `选词填空题`

Sections:

- `[content]`, `[options]`, `[answer]`, `[explanation]`

Key attributes:

- `open`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`

Token rules:

- `@--@` consumes options and answers in order
- `@answer@` embeds the correct value inline and still consumes one options line
- `\@` escapes a literal `@`
- `@blank@` is not an authored blank token; use `@--@`. Do not replace literal quoted/source examples blindly.

Notes:

- One options line is reused for all blanks.
- Multiple options lines map one line per blank.
- Answers accept indices, letters, or direct option values.
- Open mode treats any non-empty selection as correct.

Source of truth:

- `mdx-scorm/src/mdx/remarkChoiceClozeBlock.ts`
- `mdx-scorm/Developer Manual.md`

### matching

Canonical block:

```md
:::matching
[left]
Cat
Eagle

[right]
Mammal
Bird

[options]
Fish

[explanation]
Cats are mammals, eagles are birds.
:::
```

Supported aliases in repo:

- `matching`, `match`, `匹配`, `匹配题`, `配对`, `配对题`

Sections commonly used:

- `[left]`, `[right]`, `[options]`, `[explanation]`

Key attributes:

- `open`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`
- `shuffleOptions=false`
- compatibility aliases: `shuffle=false`, `shuffleOptions=false`

Notes:

- Open mode accepts any non-empty selection.
- Duplicate selections are allowed, but candidate display values across `[right]` and `[options]` must be unique. Repeating the same display value as two authored candidates raises a runtime error.
- Prefer this block only when the source clearly contains left/right pairing material.

Source of truth:

- `mdx-scorm/src/mdx/remarkMatchingBlock.ts`
- `mdx-scorm/Developer Manual.md`

### game-matching

All four games support optional `limit` and `shuffleQuestions`; tokenbuilding also supports item `answerDisplay`. Read [game-rounds.md](game-rounds.md) for defaults, redo/restoration, escaped MDX item attributes, Studio, and print behavior.

Canonical block:

```md
:::game-matching{batchSize=4}
[left]
- :play[cat.mp3] cat
- dog
- bird

[right]
- 猫
- 狗
- 鸟
:::
```

Sections:

- `[left]`, `[right]`

Key attributes:

- `batchSize=<positive integer>`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`

Notes:

- Whole game registers as one formal interaction.
- Use for retry-until-complete matching practice, not ordinary exam-style matching.
- Only `[left]` and `[right]` are supported; no `[options]` or `[explanation]`.
- Left and right sections must contain the same number of cards.
- The nth left card matches the nth right card.
- Each card must be authored as one line.
- Right-card identities must not duplicate.
- The first `:play[...]` in a card line is supported; write audio as `:play[audio.mp3]`, not `:play[label]{src="audio.mp3"}`.

Source of truth:

- `mdx-scorm/src/mdx/remarkGameMatchingBlock.ts`
- `mdx-scorm/src/components/GameMatchingBlock.tsx`
- `mdx-scorm/User Manual.md`
- `mdx-scorm-pages/pages/01_interactive_powers/02_gamelike_interactions/01_game_matching.mdx`

### game-memorymatch

Canonical block:

```md
:::game-memorymatch{weight=2}
[left]
- cat
- dog
- :play[bird.mp3] bird

[right]
- 猫
- 狗
- 鸟
:::
```

Sections:

- `[left]`, `[right]`

Key attributes:

- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`

Notes:

- Whole game registers as one formal interaction.
- Use for memory-card pair matching.
- Only `[left]` and `[right]` are supported; no `[options]`, `[answer]`, or `[explanation]`.
- Left and right sections must contain the same number of cards.
- The nth left card matches the nth right card.
- Each card must be authored as one line.
- Card content may include normal single-line Markdown, images, and the first `:play[...]`.
- This block is engine-backed in current `mdx-scorm`; it is not present in the current `mdx-scorm-pages` reference project.

Source of truth:

- `mdx-scorm/src/mdx/remarkGameMemoryMatchBlock.ts`
- `mdx-scorm/src/components/GameMemoryMatchBlock.tsx`
- `mdx-scorm/User Manual.md`

### game-choice

Canonical block:

```md
:::game-choice
[item]
[prompt]
Which word means "book"?

[options]
cat
book
desk

[answer]
B
:::
```

Multi-item block:

```md
:::game-choice{weight=2}
[item]
[prompt]
Select vowels.

[options]
あ
か
い
さ

[answer]
A
C

[item]
[prompt]
Pick the English word.

[options]
桌子
book
猫

[answer]
2
:::
```

Sections:

- repeated `[item]`
- per item: `[prompt]`, `[options]`, `[answer]`

Key attributes:

- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`

Notes:

- Whole game registers as one formal interaction.
- Use for tile-like retry-until-correct choice practice. For ordinary quiz questions, prefer `choice`.
- Each `[item]` must include `[prompt]`, `[options]`, and `[answer]`.
- `[options]` supports 2 to 6 one-line options.
- Answers may be option labels `A`-`F`, numbers `1`-`6`, or unambiguous option text.
- Multiple answer lines create a multi-select item. Put exactly one option label on each line; do not concatenate labels or separate multiple labels on one line.

Source of truth:

- `mdx-scorm/src/mdx/remarkGameChoiceBlock.ts`
- `mdx-scorm/src/components/GameChoiceBlock.tsx`
- `mdx-scorm/User Manual.md`
- `mdx-scorm-pages/pages/01_interactive_powers/02_gamelike_interactions/03_game_choice.mdx`

### game-tokenbuilding

Answer comparisons normalize straight/curly quotation marks while preserving authored display text. This does not imply quote equivalence in every other component.


Canonical block:

```md
:::game-tokenbuilding{space="ignore" shuffle=true}
[item]
[prompt]
:play[cat.mp3] Build the word.

[answer]
c a t

[tiles]
c a t x
:::
```

Multi-item block:

```md
:::game-tokenbuilding{space="ignore" shuffle=true}
[item]\{space="strict" shuffle=false\}
[prompt]
Build the phrase.

[answer]
in to

[tiles]
in to into

[item]
[prompt]
Build the sentence.

[answer]
I ran into him .
:::
```

Sections:

- repeated `[item]`
- per item: `[prompt]`, `[answer]`, optional `[tiles]`

Key attributes:

- `space=ignore|strict`
- `shuffle=true|false`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`

Notes:

- Whole game registers as one formal interaction.
- Use for spelling, word-building, phrase-building, or sentence-building practice.
- `[answer]` is required; `[tiles]` is optional and falls back to answer tokens when omitted.
- `[answer]` and `[tiles]` split tokens by whitespace. Include punctuation as its own token when students must select it.
- `space` and `shuffle` may be set on the whole block or on an individual `[item]\{...\}`; item-level values override block-level values. Escape item attribute braces in authored MDX; block attribute braces stay unescaped.
- `space="ignore"` compares the joined answer after whitespace removal; `space="strict"` compares the token sequence.

Source of truth:

- `mdx-scorm/src/mdx/remarkGameTokenBuildingBlock.ts`
- `mdx-scorm/src/components/GameTokenBuildingBlock.tsx`
- `mdx-scorm/User Manual.md`
- `mdx-scorm-pages/pages/01_interactive_powers/02_gamelike_interactions/02_game_tokenbuilding.mdx`

### classification

Use for assigning items to one or more category targets. The stem belongs in ordinary prose outside the directive; do not invent internal `[stem]`, `[answer]`, or `[options]` sections.

```mdx
Classify the animals.

::::classification
:::target
[title]
Mammals
[items]
Cat
Dog
:::
:::target
[title]
Birds
[items]
Eagle
:::
::::
```

- Require one or more `target` blocks, each with `[title]` and nonempty `[items]`. Each nonempty ordinary item line is one candidate.
- Use `:::item` inside `[items]` to wrap one multiline/rich Markdown candidate. `target` and `item` are internal structures, never standalone questions.
- To put one candidate in multiple categories, repeat exactly the same source, including inline Markdown, in each corresponding `[items]` section. Different source creates different candidates. Preserve supplied membership; do not guess answers.
- A `styleBlock` directly inside `classification` may wrap exactly one `target` and no other content. Do not nest other structural directives in the classification structure; do not nest interactive questions inside items.
- Supported outer attributes: `weight`, `weightDistribution=shared|average`, `isshared`, `scorm`. Feedback inherits page `feedback` / `feedbackMode`; there is no question-level `feedbackMode` attribute. Do not use `open`, `share`, `shareComments`, or `useManualMarking`.
- Learners can drag candidates or select a candidate then a target, including on touch devices. Multiple target membership is allowed. Completion requires every candidate to be placed at least once; scoring counts correct, incorrect, and missing relations.
- Print/PDF is static: student output shows candidates and empty targets; teacher output shows correct membership. Runtime support is not proof that every rich source shape has native visual-editor support; preserve source when the editor falls back.
- Before returning, check nesting/fences, required sections, actual candidates, identical source for repeated candidates, and the absence of unsupported attributes. The bundled recurring-output script is not the full runtime classification parser; use host validation when available.

### sorting

Canonical block:

```md
:::sorting
[stem]
Arrange the steps in order.

[items]
1. Read the prompt
2. Mark key clues
3. Draft the answer
4. Check and revise

[explanation]
Optional explanation.
:::
```

Supported aliases in repo:

- `sorting`, `sort`, `排序`, `排序题`

Sections:

- `[stem]`, `[prompt]`, `[content]`
- `[items]`, `[item]`, `[options]`, `[list]`, `[sorting]`, `[sequence]`
- `[explanation]`, `[explain]`

Key attributes:

- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`
- `shuffleItems=false`
- compatibility aliases: `shuffle=false`, `shuffleOptions=false`

Notes:

- No open mode.
- If `[items]` is omitted, top-level list lines may be treated as sorting items.
- Author every sorting item with decimal numbering or the hyphen bullet `-`, such as `1. Item text` or `- Item text`.
- Do not use `*` or `+` as sorting-item bullets.
- Bare alphabetic markers such as `A. Item text` are not supported item markers. If the source label must remain visible, prepend a supported list marker, for example `1. A. Item text` or `- A. Item text`.
- `shuffleItems` defaults to `true`.

Source of truth:

- `mdx-scorm/src/mdx/remarkSortingBlock.ts`
- `mdx-scorm/src/components/SortingBlock.tsx`

### textselect / textedit

Engine-backed text exercises. Use exact lowercase names; no aliases. Read [Text exercises](text-exercises.md) for the complete self-contained contract and examples before generating them.

- `textselect{mode="word"}`: mark each answer in literal `[content]` with `:pick[word]`; use `mode="span"` for `:pick[complete phrase]`.
- `textedit`: encode source-supported corrections as `:fix[old]{to="new"}`, `:del[old]`, `:add[new]`. Use square brackets, not `:fix{}{to="..."}`, `:fix[]{...}` or a separate `[answer]` section.
- Both use optional Markdown `[prompt]`, required literal `[content]`, optional Markdown `[explanation]`; never repeat a section. The original content remains visible to learners, with answers hidden until feedback is allowed.
- Supported attrs: `id`, `open`, `weight`, `scorm`, `showExplanation`; only textselect has `mode`. Omit unrequested attrs. `open=true` is completion-based; `weight=0` independently excludes score weight while preserving formal participation. Do not add `aiScore`, `[ai]`, `rows`, `share`, `useManualMarking` or `weightDistribution`.
- Keep each original passage within 300 tokenizer units; do not truncate to fit. No nested markers, token-fragment answers, overlapping answers, or rich content inside `[content]`.
- The bundled Python validator is not a full text-exercise grammar checker; retain host validation.

### translate

Canonical block:

```md
:::translate{type=sentence}
[prompt]
Translate into English:
敏捷的棕色狐狸跳过了那只懒狗。

[answer]
The quick brown fox jumps over the lazy dog.

[explanation]
Optional explanation.
:::
```

Project authoring default: Chinese-to-English translation. The parser itself has no language-direction restriction; verify the target grading service before promising other directions.

Supported aliases in repo:

- `translate`, `翻译`, `翻译题`

Sections:

- `[prompt]`, `[content]`, `[题干]`
- `[answer]`, `[answers]`, `[参考答案]`, `[答案]`
- `[explanation]`, `[解析]`
- `[ai]`, `[ai点评]`, `[智能点评]`

Key attributes:

- `type=sentence|passage`
- `rows=<positive integer>`
- `open`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`
- `useManualMarking=true|false`

Notes:

- `type` maps to `markingType`.
- In open mode, any non-empty input is treated as complete.
- `[ai]` accepts `instruction`, `appId`, and `language`.
- `useManualMarking=true` enables scored teacher marking for formal translate blocks.
- For the default English-to-Chinese AI-grading workflow, prefer the following AI fill-in shape. Explicit manual/open/non-AI requirements take precedence; do not silently enable AI.

```mdx
:::fillblank{aiScore=true}
[content]
21. Please translate the following sentence into Chinese.

> Meanwhile, China, with its steadfast commitment and remarkable progress in green development, has emerged as a champion in the global transition to renewable energy, serving as a beacon of hope in the fight against climate change.

@--@

[answer]
与此同时，中国凭借在绿色发展领域的坚定承诺与显著进展，已成为全球向可再生能源转型的引领者，在应对气候变化的行动中扮演着希望的灯塔。

[ai]
instruction: 这是一道句子英译中的题目。请重点评价翻译质量，给出翻译的优缺点。
:::
```

- Use one block per English-to-Chinese item, with exactly one `@--@`, the complete Chinese reference translation in `[answer]`, and an English-to-Chinese quality-evaluation instruction in `[ai]`. Use only the English directive and section labels shown above, even when a supplied source template uses Chinese aliases.

Source of truth:

- `mdx-scorm/src/mdx/remarkTranslateBlock.ts`
- `mdx-scorm/src/components/TranslateBlock.tsx`

For `translate` with `open=true`, a configured `[ai]` section can provide AI feedback without displaying a score; completion remains based on nonempty input. Do not add AI configuration without source/user intent.

### writing

Canonical block:

```md
:::writing{agent="quanjing" }
[prompt]
Write about your favorite season.

[explanation]
Model essay or guidance.
:::
```

Supported aliases in repo:

- `writing`, `写作`, `写作题`

Sections:

- `[prompt]`, `[content]`, `[题干]`, `[写作要求]`
- `[explanation]`, `[解析]`, `[范文]`, `[sampleanswer]`, `[指导]`, `[guidance]`
- `[ai]`, `[ai点评]`, `[智能点评]`

Key attributes:

- `agent`
- `rows=<positive integer>`
- `open`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `share=true|false`
- `shareComments=true|false`
- `isshared=true|false`
- `useManualMarking=true|false`

Notes:

- Use `writing` for paragraph composition or essay tasks. For question answering / short answers, use one standalone `fillblank` blank per question; use `aiScore=true` when AI scoring is requested.
- With `open=true`, a configured `[ai]` section can provide AI feedback without displaying a score; completion remains based on nonempty input.
- Do not invent a model essay if the source does not provide one.
- Use `share=true shareComments=true` only when peer review or shared writing discussion is intended.
- `useManualMarking=true` enables scored teacher marking and can coexist with AI writing feedback.

Source of truth:

- `mdx-scorm/src/mdx/remarkWritingBlock.ts`
- `mdx-scorm/src/components/WritingBlock.tsx`

### discussion / debate

Canonical block:

```md
:::discussion
[topic]
Which matters more in language learning, input or output?

[guide]
Post your own view first. Then try quoting and replying to a classmate.
:::
```

Debate variant:

```md
:::debate
[topic]
Universities should make AI writing tools mandatory in every writing class.

[guide]
Post your stance and explain your reasons clearly.
:::
```

Supported aliases in repo:

- `discussion`, `讨论`, `讨论题`
- `debate`, `辩论`, `辩论题`

Sections:

- `[topic]`
- `[guide]`
- optional `[empty]` defines the empty-state text; it is supported in the directive, not only JSX

Key attributes:

- `rows=<positive integer>`
- `labels` / `label` (including `none`)
- `mode=debate` on `discussion`
- `preset=opinion|essay|proposal|project|summary|reflection|report`
- `supportLabel`
- `opposeLabel`
- `isshared=true|false`
- `scorm=true|false`

Notes:

- This is a completion-oriented threaded class interaction, not a normal essay box.
- Use it only when the lesson truly expects class discussion or debate.
- Completion requires class readiness, joined-class access and the learner's published post; an editor draft alone is insufficient. Published-state changes update page completion.
- Joined-class state affects completion at runtime; do not use it as a generic replacement for `writing`.

Source of truth:

- `mdx-scorm/User Manual.md`
- `mdx-scorm/src/pages/01_showpowers/11.8_Discussion_demos.mdx`

### recorder

Canonical block:

```md
:::recorder{script="Read this sentence." category="read_sentence" language="en_us"}
Please read the sentence aloud.
:::
```

Supported aliases in repo:

- `recorder`, `录音`, `录音题`

Prompt source:

- Directive body becomes the prompt markdown.

Key attributes:

- `script`
- `category=read_word|read_sentence|read_chapter|speak`
- `language=en_us|zh_cn`
- `recordOnly=true|false`
- `phoneme_output=0|1`
- `readtype_diagnosis=0|1`
- `test_type=ielts|nmet`
- `scorePolicy=service|completionOnly`
- `feedbackView=default|transcription`
- `allowPlayback=true|false`
- `showScore=true|false`
- `showScoreDetail=true|false`
- `maxScoreAttempts`
- `pollIntervalMs`
- `maxScoreWaitMs`
- `detailPollIntervalMs`
- `detailMaxWaitMs`
- `preferJsonDetail=true|false`
- `showXmlFallback=true|false`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `share=true|false`
- `shareComments=true|false`
- `isshared=true|false`
- `useManualMarking=true|false`

Notes:

- Use only when the lesson really needs speaking/recording.
- `category="speak"` can omit `script`, but do not rely on that unless the prompt text is clearly the spoken content.
- `recordOnly=true` skips scoring and detail fetching but still counts the task as completed.
- `scorePolicy="completionOnly"` keeps recorder completion/scoring flow but makes platform scoring completion-based.
- `category="speak" feedbackView="transcription"` stores transcription-only feedback and implicitly uses completion-only platform scoring.
- `useManualMarking=true` enables scored teacher marking unless the effective recorder policy is completion-only.

Source of truth:

- `mdx-scorm/src/mdx/remarkRecorderBlock.ts`
- `mdx-scorm/Developer Manual.md`

### imageupload

Canonical block:

```md
:::imageupload{maxAttempts=3}
Please upload one image.
:::
```

Supported aliases in repo:

- `imageupload`, `image-upload`, `图片题`, `图片上传`

Prompt source:

- Directive body becomes `promptMarkdown`

Key attributes:

- `maxAttempts`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `share=true|false`
- `shareComments=true|false`
- `isshared=true|false`
- `useManualMarking=true|false`

Notes:

- Upload completion earns the automatic full score for this interaction; pending/failed uploads do not establish completion. Use `weight=0` only when requested to remove its score weight while retaining tracking.
- After a successful upload, the latest preview is shown on the page.
- `useManualMarking=true` enables teacher score and comment entry; a saved teacher score overrides the automatic score. Uploading does not imply AI evaluation of media quality.

Source of truth:

- `mdx-scorm/src/mdx/remarkImageUploadBlock.ts`

### videoupload

Canonical block:

```md
:::videoupload{maxAttempts=3}
Please upload one short video.
:::
```

Supported aliases in repo:

- `videoupload`, `video-upload`, `视频题`, `视频上传`

Prompt source:

- Directive body becomes `promptMarkdown`

Key attributes:

- `maxAttempts`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `share=true|false`
- `shareComments=true|false`
- `isshared=true|false`
- `useManualMarking=true|false`

Notes:

- Upload completion earns the automatic full score for this interaction; pending/failed uploads do not establish completion. Use `weight=0` only when requested to remove its score weight while retaining tracking.
- After a successful upload, the latest preview is shown on the page.
- `useManualMarking=true` enables teacher score and comment entry; a saved teacher score overrides the automatic score. Uploading does not imply AI evaluation of media quality.

Source of truth:

- `mdx-scorm/src/mdx/remarkVideoUploadBlock.ts`

## Display blocks and helpers

### reading / chunk

Use `:::reading{src="lesson.mp3" type=audio}` with inline `:chunk[Passage text]{start="0" end="3.5"}` for synchronized text. Read [reading-and-reveal.md](reading-and-reveal.md#reading--chunk-synchronized-reading) for media, timing, nesting and export constraints. Reading itself is not scored.

### reveal / revealed

Local inline: `:reveal[**answer**]{label="Show answer"}`. Local block: `:::reveal[Show hint]` wraps hidden body content. Linked regions: `:reveal[Show]{show=group}` with `:revealed[content]{on=group}` or block `:::revealed{on=group}`. Read [reading-and-reveal.md](reading-and-reveal.md#reveal--revealed-one-way-reveal): label/content semantics change with `show`, hidden questions still score, and print expands the content.

### styleBlock

Default card form: `:::styleBlock{class="card"}`. Do not rebuild the system card CSS with inline variables. `class="first second"` supports multiple space-separated classes without dots; inline styles remain explicit overrides. For reusable custom styling, scope a page-local `<style>` to a distinctive class and include it on every page that needs it. Cloud Studio retains the stylesheet as source; check applied CSS in the course preview. Runtime, HTML builds, and Print preserve classes, but Print sanitizes styles: do not rely on web theme selectors, exact DOM-child selectors, imports, font-face, animation, or fixed/clipped whole-page containers.



Canonical block:

```md
:::styleBlock{background-color=#fff6e5 border-radius=12 padding=16}
This is a styled block.
:::
```

Supported aliases in repo:

- `styleBlock`, `style-block`

Use for:

- local card styling
- emphasis boxes
- styling content inside `collapse`, `pop`, or normal markdown sections

Allowed style keys:

- `background`, `background-color`, `background-image`, `background-position`, `background-repeat`, `background-size`
- `box-shadow`
- `border`, `border-color`, `border-radius`, `border-style`, `border-width`
- `border-bottom`, `border-bottom-color`, `border-bottom-style`, `border-bottom-width`
- `border-left`, `border-left-color`, `border-left-style`, `border-left-width`
- `border-right`, `border-right-color`, `border-right-style`, `border-right-width`
- `border-top`, `border-top-color`, `border-top-style`, `border-top-width`
- `color`
- `font-family`, `font-size`, `font-weight`, `font-style`
- `letter-spacing`, `line-height`
- `list-style-position`, `list-style-type`
- `list-marker-color`, `list-marker-size`, `list-marker-weight`
- `margin`, `margin-bottom`, `margin-left`, `margin-right`, `margin-top`
- `max-width`, `min-height`, `opacity`
- `outline`, `outline-color`, `outline-offset`, `outline-style`, `outline-width`
- `overflow-wrap`
- `padding`, `padding-bottom`, `padding-left`, `padding-right`, `padding-top`
- `text-align`, `text-align-last`, `text-decoration`, `text-decoration-color`, `text-decoration-style`, `text-decoration-thickness`, `text-indent`, `text-shadow`, `text-transform`, `text-underline-offset`
- `vertical-align`
- `word-break`, `word-spacing`

Notes:

- Numeric values are treated as `px` for supported properties.
- CSS functions like `var(...)`, `calc(...)`, `clamp(...)`, `min(...)`, and `max(...)` are supported.
- Prefer theme tokens from `mdx-scorm/src/global.css` and `mdx-scorm/src/themes/*.css` when styling authored content.
- Prefer semantic tokens such as `var(--card-bg)`, `var(--card-border)`, `var(--card-shadow)`, `var(--text-strong)`, `var(--text-muted)`, `var(--quote-bg)`, `var(--quote-text)`, `var(--accent-1)`, and `var(--surface-1)` over hard-coded colors.
- `styleText` and `styleLine` use the same style whitelist and the same variable/expression support.
- Authoring preference order: semantic component token -> shared text/surface/accent token -> literal CSS value.

Theme-aware example:

```md
:::styleBlock{class="card"}
This box adapts across themes.
:::
```

Suggested authoring mappings:

- neutral content box -> `styleBlock{class="card"}`
- term popup / glossary body -> `styleBlock{class="card"}`, with optional `var(--accent-1)` on the key term
- reading tip / reminder -> `var(--quote-bg)` + `var(--quote-text)`
- popup or collapse trigger -> `--button-*` tokens first, then `--choice-option-*` if it behaves more like a chip
- inline emphasis -> `var(--accent-1)` or `var(--text-strong)` instead of literal highlight colors
- sticky reminder body -> `var(--quote-bg)` / `var(--quote-text)` first, an inner `styleBlock{class="card"}` when a card is needed

Source of truth:

- `packages/mdx-semantics/src/style-semantics.ts`
- `mdx-scorm/src/components/styleProps.ts`
- `mdx-scorm/src/mdx/remarkStyleBlock.ts`

For explicitly requested WenKai text, use `font-family="LXGW WenKai"` on `styleText`, `styleLine`, or `styleBlock`. The bundled regular font is supported in `build:html`; do not promise PDF font support. Prefer `styleText` for precise spans because nested headings/components may override inherited fonts. Example: `:styleText[“示例文字”]{font-family="LXGW WenKai"}`.

### styleText

Canonical inline form:

```md
Normal text with :styleText[highlight]{color=#f97316 font-weight=700}.
```

Use for:

- inline emphasis
- short highlighted terms

Notes:

- Keep it short and inline.
- It uses the same style whitelist as `styleBlock`.

Source of truth:

- `mdx-scorm/src/mdx/remarkStyleInline.ts`
- `mdx-scorm/User Manual.md`

### styleLine

Repo-supported forms:

```md
::styleLine[Centered notice]{text-align=center color=#0f172a padding=6 border-radius=8 background-color=#f3f4f6}
```

or shorthand:

```md
::styleLine{text-align=right color=#334155} Shorthand form notice.
```

Use for:

- compact notices
- one-line highlighted reminders

Notes:

- The repo supports both bracket-label form and line-start shorthand form.
- The build pipeline normalizes shorthand text into bracket-label form.
- Same style whitelist as `styleBlock`.
- For authored lesson pages generated by this skill, always prefer the line-start shorthand form:

```md
::styleLine{text-align=center color=var(--quote-text) background=var(--quote-bg) padding=8 border-radius=999} Centered notice
```

Source of truth:

- `mdx-scorm/src/mdx/remarkStyleInline.ts`
- `mdx-scorm/src/utils/mdxUtils.ts`

### play

Canonical inline form:

```md
:play[sample-audio.mp3]
```

Use for:

- inline audio trigger

Notes:

- The label content becomes `labelMarkdown`; if no explicit `src` attribute is present, that label is used as the source.
- Good for quick pronunciation/listening cues inside normal text.

Source of truth:

- `mdx-scorm/src/markdown/remarkInlineAudio.ts`

### askAI

Inline canonical form:

```md
:askAI[Ask AI]{prompt="Explain this paragraph in simple terms." title="Reading help" app_id="kb-001"}
```

Definition/reference form for longer prompts:

```md
:::askAI{def=reading-help}
Use this page's reading material. Explain difficult points briefly and cite the source text when possible.
:::

Read the passage, then :askAI[ask the AI companion]{ref=reading-help title="Reading help"}.
```

Supported aliases in repo:

- `askAI`, `ask-ai`, `问AI`, `AI伴学`

Key attributes:

- `prompt`
- `ref`
- `def`
- `app_id`
- `title`

Notes:

- `askAI` is a content-level service trigger, not a formal interaction. It does not score, submit, or enter the interaction schema.
- `:::askAI{def=...}` stores a current-page prompt and is pruned from visible output.
- `prompt` wins over `ref`; missing prompt/ref opens the AI companion with an empty prompt.
- The inline label supports normal inline markdown and `styleText`; do not rely on nested `pop`, `play`, or another `askAI`.

Source of truth:

- `mdx-scorm/src/mdx/remarkAskAI.ts`
- `mdx-scorm/src/components/AskAI.tsx`

### collapse

Canonical block:

```md
:::collapse[Show details]{button=true align=right background-color=#fff3c7 border-radius=999 padding=8}
:::styleBlock{background-color=#fff6e5 border-radius=12 padding=16}
This content is revealed on click.
:::
:::
```

Key attributes:

- `button`
- `align=left|center|right`
- `fullWidth=true|false`
- `labelAlign=left|center|right`
- `arrowPosition=left|right`
- style attributes from the same whitelist as `styleBlock`

Notes:

- The bracket label supports markdown, including nested `:styleText`.
- Style attributes affect the trigger, not the revealed body.
- Use `styleBlock` inside for content styling.
- Prefer trigger tokens such as `var(--button-bg)`, `var(--button-text)`, and `var(--button-border)` on `collapse` itself, then use `var(--card-*)` or `var(--quote-*)` inside the revealed body.

Source of truth:

- `mdx-scorm/src/mdx/remarkCollapseBlock.ts`
- `mdx-scorm/User Manual.md`

### pop

Canonical form:

```md
:pop[Term label]{ref=term-1}

:::pop{def=term-1}
# Title
- item A
- item B
:::
```

Notes:

- Style attributes on inline `pop` apply to the trigger.
- `ref`/`def` are internal lookup attributes.
- The runtime allows duplicate `def` ids and lets later definitions win, but generated lesson pages must keep ids unique.
- Missing `ref` falls back to inline `markdown` or `source`.
- Do not nest `pop` inside another `pop` label.
- Do not enclose an inline `pop` in Markdown emphasis or strikethrough delimiters (`*`, `_`, `**`, `__`, `***`, `___`, or `~~`). When surrounding source formatting must remain, use `<b>`, `<i>`, and/or `<del>` around the complete span instead.
- In authored lesson pages, `pop` is best treated as an inline annotation tool: use it for footnotes, endnotes, vocabulary notes, and term explanations that belong to the reading flow.
- Prefer `ref/def` when the annotation content comes from source notes or glossary material, so the inline trigger and note body stay separate.
- Keep `def` blocks outside interactive question blocks; use inline `ref` markers inside the prose where the explained term actually appears.
- Recommended mapping workflow:
  - collect note sources first
  - normalize each note into `term/phrase + note body + likely anchor`
  - preserve every source note as a reachable Pop definition or a visible glossary/notes entry
  - search case-insensitively first, then try punctuation-normalized, inflectional, derivational, multiword, shortened-name, acronym, and alias variants for a credible anchor
  - treat capitalization-only differences as direct matches, preserve the passage's casing in the visible trigger, and preserve the note headword's casing in the definition
  - if no credible anchor exists, never invent a ref; keep the ordinary glossary/notes entry visible and report the missing anchor separately
  - remove only glossary/note entries successfully replaced by reachable Pop definitions; unanchored entries remain once as ordinary source-faithful content

Authoring examples:

```md
Source-style note:
The Palace Museum has undergone digital transformation.1
1. digital transformation: the use of digital technology to improve access and communication.

Author as:
The Palace Museum has undergone :pop[digital transformation]{ref=term-digital-transformation}.

:::pop{def=term-digital-transformation}
digital transformation: the use of digital technology to improve access and communication.
:::
```

```md
Source-style glossary:
Vocabulary
- emblem: a symbol or sign that represents something

Passage:
These products feature royal emblems.

Author as:
These products feature royal :pop[emblems]{ref=term-emblem}.

:::pop{def=term-emblem}
emblem: a symbol or sign that represents something
:::
```

```md
Source-style glossary with no safe anchor:
Glossary
- heritage: cultural traditions and historical objects passed down over time

Passage does not contain the word.

Preferred handling:
keep the ordinary glossary entry visible and report the missing anchor separately; do not create an unreachable Pop definition. Do not remove source content into an unreachable definition.
```

Source of truth:

- `mdx-scorm/src/mdx/remarkPop.ts`
- `mdx-scorm/src/markdown/remarkDisplayDirectives.ts`

### sticky

Canonical block:

```md
:::sticky{top=0 zIndex=5}
:::styleBlock{background-color=#fff7ed border=1px solid #fdba74 border-radius=12 padding=12}
This block sticks while scrolling.
:::
:::
```

Supported aliases in repo:

- `sticky`, `吸顶`, `粘性`

Key attributes:

- `top`
- `zIndex`
- `class`
- `className`

Notes:

- Display-only. No scoring or SCORM writing.
- Sticky positioning comes from `sticky`; visual styling normally belongs in nested content such as `styleBlock`.
- Prefer note-like tokens such as `var(--quote-bg)` / `var(--quote-text)` or an inner `styleBlock{class="card"}` for a card.
- Best use case: a short reference block that learners must repeatedly glance at, such as a word bank, prompt checklist, compact formula list, or reminder.
- Use it to reduce repeated scrolling, not as a generic highlight effect.

Source of truth:

- `mdx-scorm/src/mdx/remarkStickyBlock.ts`

### wide

Wide content inherits the course font size (`--mdx-font-size`) in the current runtime. Do not add a fixed font size to compensate for historical behavior.

Canonical block:

```md
:::wide{width=1080}
| Col 1 | Col 2 | Col 3 | Col 4 |
| --- | --- | --- | --- |
| A | B | C | D |
:::
```

Supported aliases in repo:

- `wide`, `widecontent`, `宽内容`

Key attributes:

- `width`
- `class`
- `className`

Notes:

- Display-only container for locally scrollable wide tables, code blocks, or diagrams.
- Use it only when normal page width would make the content unreadable.

Source of truth:

- `mdx-scorm/User Manual.md`

### splitpane

Canonical block:

```md
:::splitpane{height="70vh" initialTopPct=0.62 minBottom=80 fullBleed fitViewport}
:::splitTop
Top content
:::
:::splitBottom
Bottom content
:::
:::
```

Supported aliases in repo:

- `splitpane`, `split-pane`, `分栏`, `分屏`, `上下分屏`
- `splitTop`, `上栏`, `上屏`
- `splitBottom`, `下栏`, `下屏`

Key attributes:

- `height`
- `initialTopPct`
- `minTop`
- `minBottom`
- `fullBleed`
- `fitViewport`

Notes:

- Nested splitpanes are ignored.
- Use only when the lesson truly needs a two-pane layout.
- Best use case: a long reference passage or source text that learners must keep visible while answering questions, translating, or writing.
- Treat it as a reading-area + task-area pattern whose purpose is to reduce back-and-forth scrolling.

Source of truth:

- `mdx-scorm/src/mdx/remarkSplitPaneBlock.ts`

Authoring comparison:

- inline explanation for one term -> `pop`
- short reusable reference block -> `sticky`
- long reference source plus task area -> `splitpane`

### columns / col

Canonical block:

```md
:::columns{ratios="2 1 1"}
:::col
Left content
:::
:::col
Middle content
:::
:::col
Right content
:::
:::
```

Supported aliases in repo:

- container: `columns`, `column-layout`, `columnlayout`, `分列`, `多栏`
- child: `col`, `栏`, `列`

Key attributes:

- `ratios`

Notes:

- Display-only.
- Invalid or missing ratios fall back to `1`.
- Avoid nested columns.

Source of truth:

- `mdx-scorm/src/mdx/remarkColumnsBlock.ts`

### carousel

Canonical block:

```md
:::carousel{loop=true autoNextSlide=true}
[slide Intro]
Welcome to slide 1.

[slide Practice]
:::choice
[stem]
Pick the correct option.

[options]
A. One
B. Two

[answer]
B
:::
:::
```

Supported aliases in repo:

- `carousel`, `轮播`

Key attributes:

- `loop`
- `autoNextSlide`

Notes:

- Slides are defined by `[slide Title]` headers.
- If no slide header is present, the whole body becomes one fallback slide.
- Carousel itself is display-only; nested interactions provide scoring.

Source of truth:

- `mdx-scorm/src/mdx/remarkCarouselBlock.ts`

### iframe

Canonical block:

```md
:::iframe{src="/media/feixiang.html" title="Embedded page" height="520px"}
:::
```

Supported aliases in repo:

- `iframe`, `嵌入页`, `内嵌页`

Key attributes:

- required source: `src` or `url`
- `title`
- `className` or `class`
- `height`
- `fullBleed`
- `wideOnWeb`
- compatibility alias: `breakout`
- `fitBody`
- `loading`
- `allow`
- `referrerPolicy`
- `sandboxMode=strict|relaxed|trusted`
- `trusted`
- `allowFullscreen`

Notes:

- Unsafe schemes are blocked at runtime.
- Use only when the source clearly requires external or embedded content.

Source of truth:

- `mdx-scorm/src/mdx/remarkIframeBlock.ts`

### media

Canonical block:

```md
:::media{src="sample-video.mp4" type="video" title="Library video" aspect="16/9" transcript="toggle"}
Transcript or teaching notes for the media.
:::
```

Supported aliases in repo:

- `media`

Key attributes:

- `src`
- `type=auto|audio|video`
- `title`
- `poster`
- `aspect`
- `height`
- `transcript=submitted|toggle|never`
- `transcriptOpen=true|false`
- `preload=none|metadata|auto`
- `loop=true|false`
- `muted=true|false`
- `playsInline=true|false`
- `rates`

Notes:

- Prefer `media` for a full audio/video player with transcript behavior.
- Use Markdown image/media links or HTML `audio`/`video` for simpler media embeds.
- `transcript=submitted` shows the transcript only after a formal submit path exists and the page has been submitted.

Source of truth:

- `mdx-scorm/src/mdx/remarkMediaBlock.ts`
- `mdx-scorm/src/components/MediaBlock.tsx`

### showAfterSubmit

Canonical block:

```md
:::showAfterSubmit
This content appears only after the page has really entered submitted state.
:::
```

Supported aliases in repo:

- `showAfterSubmit`, `showaftersubmit`, `提交后显示`, `提交后内容`

Notes:

- Visibility wrapper only; no extra attrs in the current implementation.
- The block appears after formal submit, including instant-mode auto-submit pages.
- `RESET` hides it again.
- Nested interactive descendants are forced into practice mode.
- Good for post-submit explanations, extension reading, or optional follow-up practice.

Source of truth:

- `mdx-scorm/User Manual.md`

### aiexercise

Canonical block:

```md
:::aiexercise{trigger="manual" source="page" mode="practice" appId="demo-app-id"}
[types]
choice
translate

[count]
2

[intro]
Generate a short extra practice round.

[extraContext]
Focus on reading comprehension and bilingual transfer.
:::
```

Supported aliases in repo:

- `aiexercise`, `AI练习`, `智能练习`

Sections:

- `[types]`
- `[count]`
- `[intro]`
- `[extraContext]`

Key attributes:

- required: `types`, `count`
- optional: `appId`, `mode`, `trigger`, `source`, `extraContext`, `contentLanguage`, `questionLanguage`, `answerLanguage`

Notes:

- Runtime AI practice generator, not a static authored question block.
- `mode="practice"` generates `scorm=false` items; `mode="formal"` generates tracked items.
- If wrapped by `showAfterSubmit`, generated items still behave as practice-only.
- Use only when the user explicitly wants runtime AI-generated follow-up tasks.

Source of truth:

- `mdx-scorm/User Manual.md`

### exportcontent

Canonical block:

```md
:::exportcontent{target="/01_showpowers/23_exportcontent_demos" scope="page" locale="zh" showControls=false}
:::
```

Supported aliases in repo:

- `exportcontent`, `导出内容`, `内容导出`

Key attributes:

- `target`
- `scope=page|folder|course`
- `locale=zh|en`
- `profile=student|teacher`
- `format=markdown|text`
- `showControls=true|false`

Notes:

- Export tool block, not a learner task.
- Layout containers are flattened in export; teacher export usually appends answers after prompts.
- Use only when the user explicitly wants on-page export tooling.

Source of truth:

- `mdx-scorm/User Manual.md`
- `mdx-scorm/src/mdx/remarkExportContentBlock.ts`

### knowledgeGraph

Use the exact case-sensitive name `knowledgeGraph`, with exactly one fenced `json` block and no other body content. Use strict JSON, without comments or trailing commas.

````mdx
:::knowledgeGraph{layout="dagre" direction="LR" height=460 density="auto"}
```json
{
  "nodes": [
    { "id": "topic", "label": "Topic" },
    { "id": "concept", "label": "Concept" }
  ],
  "edges": [
    { "source": "topic", "target": "concept", "relation": "contains" }
  ]
}
```
:::
````

- Only five directive attributes: `layout` (`dagre`, `force`, `radial`, `circular`), `direction` (`LR`, `RL`, `TB`, `BT`, only meaningful for dagre), `height` (finite positive CSS-pixel number, no `px` suffix), optional visible `title`, and `density` (`auto`, `compact`, `normal`, `comfortable`). Graph title is separate from frontmatter title.
- Top-level JSON: required nonempty `nodes`; optional `edges` and `categories` arrays. No other fields, `version`, `src`, external JSON, or JavaScript objects.
- Nodes: required unique nonempty `id` and `label`; optional `description`, `lesson`, `category`.
- Categories: required unique `id` and `label`. A node category must reference a declared category.
- Edges: required `source`, `target`, `relation`; optional `label`. Endpoints must exist and differ. Relations are only `contains`, `prerequisite`, `related`.
- Each node has at most one contains parent. Contains, prerequisite, and their combined directed graph must all be acyclic. Related cycles are allowed. Do not create duplicate relations.
- `lesson` must match a trusted course page inventory exactly: case-sensitive, relative to `pages/`, `/` separators, `.mdx` extension, no leading slash, `./`, `../`, query/hash, scheme, or `scoid`. Pages with `issco: false` are allowed. If no inventory is supplied, omit optional lesson links; ask only if navigation is required.
- Use longer outer directive fences when nesting, and an outer response code fence longer than the embedded JSON fence. Do not let nested fences truncate the complete MDX candidate.
- Do not invent author parameters for colors, theme, toolbar, node shapes, fullscreen mode, or learner layout switching. Print/PDF produces static content, not Canvas interactions. The detailed reference is [classification-and-knowledge-graph.md](classification-and-knowledge-graph.md).
- Check strict JSON, allowed fields/values, unique identifiers, references, exact lesson paths, and cycles before returning. Host runtime validation remains authoritative; the bundled recurring-output script does not implement the graph schema.

### HTML App

For explicitly requested runnable custom mini-interactions, read `html-apps.md`. Use an exact lowercase `html app` fence at page-body level. Ordinary `html` fences remain code displays. This is not a formal/scored exercise or a replacement for native components.

### retired chatwithai

`chatwithai` is retired in the current project.

Use:

- `aiCompanion` frontmatter or catalog config for the shell/menu AI entry.
- `askAI` for an inline content-authored AI trigger.
- `aiexercise` for runtime-generated practice.

Do not generate new `chatwithai` page content.

## Generation advice

- For regular handouts, plain markdown + `choice` / `fillblank` / `matching` / `sorting` / `translate` / `writing` is usually enough.
- Use `weight=0` for non-scoring questions; use `scorm=false` only for explicitly untracked practice.
- Use `showAfterSubmit` when follow-up content should unlock only after the formal tracked task is finished.
- Do not introduce `game-matching`, `game-memorymatch`, `game-choice`, `game-tokenbuilding`, `discussion`, `debate`, `recorder`, upload blocks, `splitpane`, `columns`, `carousel`, `iframe`, `media`, `askAI`, `aiexercise`, or `exportcontent` unless the source or user explicitly asks for them.
- Do not generate retired `chatwithai` content.
- If a display block only adds decoration and not clarity, skip it.
