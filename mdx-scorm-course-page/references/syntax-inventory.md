# mdx-scorm syntax inventory

This file is a source-audited syntax reference for `D:\Projects\welearn-ninja\mdx-scorm`.

Use it when generating authored lesson pages. Prefer the canonical ASCII syntax shown here, even though the runtime also supports aliases and normalization.

## Global authoring rules

- Keep directive fences on their own lines.
- Use canonical directive names in final output.
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

When the source clearly needs underline, superscript, or subscript, use inline HTML because standard Markdown does not define them:

- underline -> `<u>key term</u>`
- superscript -> `10<sup>2</sup>`
- subscript -> `H<sub>2</sub>O`

Notes:

- These forms are already used in the repo's markdown demos and are compatible with the current renderer.
- If the goal is not semantic superscript/subscript but simply visual underline emphasis inside a themed sentence, `:styleText[...]` with `text-decoration=underline` can be a better fit than raw HTML.
- Do not invent pseudo-Markdown such as `^sup^` or `++underline++` unless the source explicitly uses a plugin syntax that this repo actually supports.

## Frontmatter baseline

Minimal safe page header:

```mdx
---
title: Your Page Title
feedback: submit
numbering: type
---
```

Use `numbering: none` when the page has no interactions.

Current parser and page-control notes:

- Prefer single-line `key: value` fields.
- `feedback` accepts `submit`, `submit_<n>`, and `instant`.
- `numberingStart` is a positive integer and only matters when numbering is enabled.
- Common optional page-level fields include `weights`, `scoreCardShowWeights`, `noSubmit`, `scormDebug`, `autoShowScoreCardOnSubmit`, `scoreCardGrouping`, `cardMode`, `browseMode`, `isShowDictionary`, and `ai`.
- Only `ai.prompt` supports list syntax; avoid arbitrary arrays, multiline strings, and deep nested objects.

Reference files:

- `D:\Projects\welearn-ninja\mdx-scorm\frontmatter写法规范.md`
- `D:\Projects\welearn-ninja\mdx-scorm\User Manual.md`

## Media authoring

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
- External URLs (`https://...`) are left untouched.
- Direct HTML media tags and markdown image/link syntax are both supported.
- Do not encode `offline_media_id` or package folder assumptions into the content path itself.

## SCORM participation rule

Most low-level interactions default to tracked mode.

- `scorm=true` is the normal default.
- `scorm=false` keeps the task usable but removes it from numbering, score cards, submit gating, `cmi.interactions.*` writes, and tracked restore.
- `ShowAfterSubmit` forces all nested interactive descendants into practice mode even if a child block was authored with `scorm=true`.

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

- Multi-select is created by multiple answers, for example `A C`.
- Labels can be letters, numbers, roman numerals, Chinese labels, or custom labels.
- Answers are case-insensitive and accept spaces, commas, Chinese commas, or line breaks.
- Option continuation lines are preserved.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkChoiceBlock.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\Developer Manual.md`

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

- `[content]`, `[answer]`, `[explanation]`

Key attributes:

- `open`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`

Token rules:

- `@--@` consumes the next answer from `[answer]`
- `@answer@` embeds an inline answer
- `@a|b@` allows multiple correct answers
- `\@` escapes a literal `@`

Notes:

- If `[answer]` has one non-empty line, it may use `,` `，` `;` `；` `、` separators.
- Open mode treats any non-empty input as correct.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkFillBlankBlock.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\Developer Manual.md`

### choicecloze

Canonical block:

```md
:::choicecloze
[content]
Dolphins are @--@ and remain @--@ in groups.

[options]
social | solitary | playful

[answer]
1
3
:::
```

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

Notes:

- One options line is reused for all blanks.
- Multiple options lines map one line per blank.
- Answers accept indices, letters, or direct option values.
- Open mode treats any non-empty selection as correct.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkChoiceClozeBlock.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\Developer Manual.md`

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
- Duplicate selections are allowed.
- Prefer this block only when the source clearly contains left/right pairing material.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkMatchingBlock.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\Developer Manual.md`

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
- `shuffleItems` defaults to `true`.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkSortingBlock.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\src\components\SortingBlock.tsx`

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

Supports only Chinese-to-English Translation.

Supported aliases in repo:

- `translate`, `翻译`, `翻译题`

Sections:

- `[prompt]`, `[content]`, `[题干]`
- `[answer]`, `[answers]`, `[参考答案]`, `[答案]`
- `[explanation]`, `[解析]`

Key attributes:

- `type=sentence|passage`
- `rows=<positive integer>`
- `open`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`

Notes:

- `type` maps to `markingType`.
- In open mode, any non-empty input is treated as complete.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkTranslateBlock.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\src\components\TranslateBlock.tsx`

### writing

Canonical block:

```md
:::writing{agent="quanjing" rows=5}
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
- `[explanation]`, `[解析]`, `[范文]`, `[指导]`

Key attributes:

- `agent`
- `rows=<positive integer>`
- `open`
- `scorm=true|false`
- `weight`
- `weightDistribution=shared|average`
- `isshared=true|false`

Notes:

- Prefer `writing` for short answer, paragraph writing, or essay tasks.
- Do not invent a model essay if the source does not provide one.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkWritingBlock.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\src\components\WritingBlock.tsx`

### discussion / debate

Canonical block:

```md
:::discussion{rows=4}
[topic]
Which matters more in language learning, input or output?

[guide]
Post your own view first. Then try quoting and replying to a classmate.
:::
```

Debate variant:

```md
:::debate{rows=4}
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
- optional empty-state or helper sections may be added in JSX, but authored directive usage should stay simple

Key attributes:

- `rows=<positive integer>`
- `labels=none`
- `supportLabel`
- `opposeLabel`
- `isshared=true|false`
- `scorm=true|false`

Notes:

- This is a completion-oriented threaded class interaction, not a normal essay box.
- Use it only when the lesson truly expects class discussion or debate.
- Joined-class state affects completion at runtime; do not use it as a generic replacement for `writing`.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\User Manual.md`
- `D:\Projects\welearn-ninja\mdx-scorm\src\pages\01_showpowers\11.8_Discussion_demos.mdx`

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
- `isshared=true|false`

Notes:

- Use only when the lesson really needs speaking/recording.
- `category="speak"` can omit `script`, but do not rely on that unless the prompt text is clearly the spoken content.
- `recordOnly=true` skips scoring and detail fetching but still counts the task as completed.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkRecorderBlock.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\Developer Manual.md`

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
- `isshared=true|false`

Notes:

- Completion-only upload task.
- After a successful upload, the latest preview is shown on the page.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkImageUploadBlock.ts`

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
- `isshared=true|false`

Notes:

- Completion-only upload task.
- After a successful upload, the latest preview is shown on the page.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkVideoUploadBlock.ts`

## Display blocks and helpers

### styleBlock

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

- `background`, `background-color`, `background-image`
- `box-shadow`
- `border-*`
- `color`
- `font-size`, `font-weight`
- `letter-spacing`, `line-height`
- `list-style-*`, `list-marker-*`
- `margin*`, `padding*`, `max-width`, `opacity`
- `text-align`, `text-decoration*`, `text-shadow`, `text-indent`, `text-underline-offset`

Notes:

- Numeric values are treated as `px` for supported properties.
- CSS functions like `var(...)`, `calc(...)`, `clamp(...)`, `min(...)`, and `max(...)` are supported.
- Prefer theme tokens from `D:\Projects\welearn-ninja\mdx-scorm\src\global.css` and `D:\Projects\welearn-ninja\mdx-scorm\src\themes\*.css` when styling authored content.
- Prefer semantic tokens such as `var(--card-bg)`, `var(--card-border)`, `var(--card-shadow)`, `var(--text-strong)`, `var(--text-muted)`, `var(--quote-bg)`, `var(--quote-text)`, `var(--accent-1)`, and `var(--surface-1)` over hard-coded colors.
- `styleText` and `styleLine` use the same style whitelist and the same variable/expression support.
- Authoring preference order: semantic component token -> shared text/surface/accent token -> literal CSS value.

Theme-aware example:

```md
:::styleBlock{background=var(--card-bg) border-color=var(--card-border) box-shadow=var(--card-shadow) border-radius=var(--card-radius) padding=var(--card-padding)}
This box adapts across themes.
:::
```

Suggested authoring mappings:

- neutral content box -> `var(--card-bg)` + `var(--card-border)` + `var(--card-shadow)`
- term popup / glossary body -> card tokens, with optional `var(--accent-1)` on the key term
- reading tip / reminder -> `var(--quote-bg)` + `var(--quote-text)`
- popup or collapse trigger -> `--button-*` tokens first, then `--choice-option-*` if it behaves more like a chip
- inline emphasis -> `var(--accent-1)` or `var(--text-strong)` instead of literal highlight colors
- sticky reminder body -> `var(--quote-bg)` / `var(--quote-text)` first, card tokens second

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\components\styleProps.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkStyleBlock.ts`

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

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkStyleInline.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\User Manual.md`

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

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkStyleInline.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\src\utils\mdxUtils.ts`

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

- `D:\Projects\welearn-ninja\mdx-scorm\src\markdown\remarkInlineAudio.ts`

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

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkCollapseBlock.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\User Manual.md`

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
- Duplicate `def` ids are allowed but later definitions win.
- Missing `ref` falls back to inline `markdown` or `source`.
- Do not nest `pop` inside another `pop` label.
- In authored lesson pages, `pop` is best treated as an inline annotation tool: use it for footnotes, endnotes, vocabulary notes, and term explanations that belong to the reading flow.
- Prefer `ref/def` when the annotation content comes from source notes or glossary material, so the inline trigger and note body stay separate.
- Keep `def` blocks outside interactive question blocks; use inline `ref` markers inside the prose where the explained term actually appears.
- Recommended mapping workflow:
  - collect note sources first
  - normalize each note into `term/phrase + note body + likely anchor`
  - anchor only when the inline match is credible
  - otherwise keep the material as a glossary or note list instead of forcing `pop`

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
keep it as a normal glossary list; do not force an inline `pop`.
```

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkPop.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\src\markdown\remarkDisplayDirectives.ts`

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
- Prefer note-like tokens such as `var(--quote-bg)` / `var(--quote-text)` or card tokens such as `var(--card-bg)` / `var(--card-border)` for the inner styled content.
- Best use case: a short reference block that learners must repeatedly glance at, such as a word bank, prompt checklist, compact formula list, or reminder.
- Use it to reduce repeated scrolling, not as a generic highlight effect.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkStickyBlock.ts`

### wide

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

- `D:\Projects\welearn-ninja\mdx-scorm\User Manual.md`

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

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkSplitPaneBlock.ts`

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

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkColumnsBlock.ts`

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

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkCarouselBlock.ts`

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

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkIframeBlock.ts`

### showaftersubmit

Canonical block:

```md
:::showAfterSubmit
This content appears only after the page has really entered submitted state.
:::
```

Supported aliases in repo:

- `showAfterSubmit`, `提交后显示`, `提交后内容`

Notes:

- Visibility wrapper only; no extra attrs in the current implementation.
- The block appears after formal submit, including instant-mode auto-submit pages.
- `RESET` hides it again.
- Nested interactive descendants are forced into practice mode.
- Good for post-submit explanations, extension reading, or optional follow-up practice.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\User Manual.md`

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

- `D:\Projects\welearn-ninja\mdx-scorm\User Manual.md`

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

- `D:\Projects\welearn-ninja\mdx-scorm\User Manual.md`
- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkExportContentBlock.ts`

### chatwithai

Canonical block:

```md
:::chatwithai{target="/01_showpowers/28_chatwithai_demos" scope="page" showControls=false maxTurns=4}
:::
```

Supported aliases in repo:

- `chatwithai`, `AI对话`

Key attributes:

- `target`
- `targetPath`
- `scope=page|folder`
- `showControls=true|false`
- `maxTurns`
- `appId`
- `title`
- `placeholder`
- `outOfScopeMessage`

Notes:

- Page/folder-scoped AI chat helper, not a scored interaction.
- Use only when the user explicitly wants a contextual AI chat panel in the lesson.

Source of truth:

- `D:\Projects\welearn-ninja\mdx-scorm\src\mdx\remarkChatWithAiBlock.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\src\chatWithAi\types.ts`
- `D:\Projects\welearn-ninja\mdx-scorm\src\pages\01_showpowers\28_ChatWithAI_demos.mdx`

## Generation advice

- For regular handouts, plain markdown + `choice` / `fillblank` / `matching` / `sorting` / `translate` / `writing` is usually enough.
- Use `scorm=false` only for clearly optional practice.
- Use `showAfterSubmit` when follow-up content should unlock only after the formal tracked task is finished.
- Do not introduce `discussion`, `debate`, `recorder`, upload blocks, `splitpane`, `columns`, `carousel`, `iframe`, `aiexercise`, `exportcontent`, or `chatwithai` unless the source or user explicitly asks for them.
- If a display block only adds decoration and not clarity, skip it.

