# mdx-scorm component authoring cookbook

This cookbook gives default authoring patterns for generated lesson pages.

Use it after `syntax-inventory.md` when you need a concrete block shape. It is informed by:

- `D:\Projects\welearn-ninja\mdx-scorm-pages`
- `D:\Projects\welearn-ninja\mdx-scorm\User Manual.md`
- current `mdx-scorm` source transforms

Rules:

- Treat these as defaults, not required page templates.
- Keep generated output canonical and ASCII, even when reference pages use Chinese aliases.
- Prefer the smallest block that matches the source. Do not introduce a component just because it has a cookbook entry.
- Classify the target exercise by learner action and answer relationship before reusing a reference component. Follow `exercise-type-selection.md`; reference-course presentation never overrides incompatible target task semantics.
- If a component is not present in `mdx-scorm-pages` but is present in current `mdx-scorm`, mark it as engine-backed rather than reference-course-backed.

## Frontmatter defaults

Display-only page:

```mdx
# Page heading
```

Interactive page:

```mdx
# Page heading
```

Weighted page:

```mdx
---
scoreCardShowWeights: true
weights:
  choice: 1
  fillblank: 2
  writing: 5
---
```

AI companion page override:

```mdx
---
aiCompanion:
  enabled: true
  interactiveVisibility: always
  questionOverlay: true
---
```

Use `weights:` and `aiCompanion:` only when the page or catalog design calls for them.

Omit `feedback`, `numberType`, `numberingType`, `numbering`, and page-level `type` by default. Do not write `feedback: submit` merely to restate the runtime default. Add a supported feedback or numbering override only when the corresponding reference page explicitly uses it or the author explicitly requests it.

## Text selection and correction (engine-backed)

For selecting text in place or correcting original text, use the canonical patterns in [text-exercises.md](text-exercises.md), including word selection, span selection, all three correction operations and an explicitly open zero-weight task. These blocks use `[prompt]`, `[content]`, `[explanation]`; no separate `[answer]` section. Preserve source answer keys and errors, and omit explanations absent from the source.

Do not simulate these tasks with choicecloze, separate choice options, custom HTML buttons or hand-drawn correction marks. Runtime supplies the floating toolbar, selection highlights and feedback; author only the semantic source. Examples are schemas to adapt, not content to add to unrelated lessons.

## Choice

Default:

```mdx
:::choice
[stem]
Choose the correct answer.

[options]
A. Option A
B. Option B
C. Option C

[answer]
B

[explanation]
Optional explanation.
:::
```

Use for ordinary objective selection. For retry-until-correct card practice, consider `game-choice` instead.

For multi-select, put one correct option label on each line:

```mdx
[answer]
B
C
```

Do not write `BC`, `B C`, `B,C`, `B、C`, or any other same-line list. The runtime may accept some of these separators, but generated course content must use one answer per line. Apply the same authoring rule to multi-select `game-choice` items.

## Fillblank

Use one standalone blank per question-and-answer task, not `writing`. Omit `rows` unless explicitly requested (including in every other example in this cookbook). For a non-scoring question, add `weight=0`; retain SCORM tracking.

AI-scored question-and-answer form (replace placeholders with supplied content; do not invent answers):

```mdx
:::fillblank{aiScore=true}
[content]
Question from the source.

@--@

[answer]
Reference answer from the source.

[ai]
instruction: Evaluate the response against the supplied question and reference answer.
:::
```



Inline blanks:

```mdx
:::fillblank
[content]
Dolphins are @--@ and live in the @--@.

[answer]
mammals
ocean
:::
```

Single open short answer:

```mdx
:::fillblank{open=true}
[content]
Answer in one or two sentences.

@--@
:::
```

Use `share=true shareComments=true` only for a single standalone short-answer blank.

Use `@--@` for every ordinary blank. Do not generate `@blank@`.

## Choicecloze

Default:

```mdx
:::choicecloze
[content]
The museum has @--@ from a palace to a public cultural space.

[options]
i. evolved | ii. erased | iii. hidden | iv. delayed

[answer]
1
:::
```

Use for word-bank cloze, TRUE/FALSE/NOT GIVEN selection, or repeated fixed-option blanks. Options containing punctuation use pipe separators; answers containing `,，;；、` should use numeric positions. Preserve unrelated legal full-text answers when editing. Do not use it to imitate independent matching or a single ordered sequence merely because the source shows an option bank and answer lines.

For Roman-numeral options, treat the numeral as display text and use 1-based decimal positions in `[answer]`: if the correct displayed option is `iii. hidden`, write `3`, not `iii` or `ⅲ`. Uppercase alphabetic labels are different: if the options are `A. true | B. false` or the bare list `A | B`, `[answer]` may retain `B`.

Use `@--@` for every ordinary blank. Do not generate `@blank@`.

## Matching

Default:

```mdx
:::matching
[left]
Cat
Eagle

[right]
Mammal
Bird

[options]
Fish
:::
```

Use when each left item has a correct right match and item-level scoring matters. This includes evidence-to-function, statement-to-paragraph, and finding-to-claim relationships. Use `game-matching` for retry-until-complete matching practice.

## Sorting

Default:

```mdx
:::sorting
[stem]
Arrange the reading steps in order.

[items]
1. Preview headings
2. Locate key words
3. Read the target sentence
4. Check the answer
:::
```

Use only when the source clearly has ordered steps or sequences. If directions say “match each step to position 1–5” but the positions jointly reconstruct one sequence, the semantic type is still sorting.

Each item must begin with a decimal-number marker or the hyphen bullet `-`. Use forms such as:

```mdx
[items]
1. Preview headings
2. Locate key words
3. Check the answer
```

or:

```mdx
[items]
- Preview headings
- Locate key words
- Check the answer
```

Do not use bare alphabetic labels as item markers:

```mdx
[items]
A. Preview headings
B. Locate key words
C. Check the answer
```

When alphabetic labels carry source meaning and should remain visible, put a supported marker before them, for example `1. A. Preview headings` or `- A. Preview headings`.

Do not use `*` or `+` as sorting-item bullets. Although Markdown may recognize them as ordinary list markers in other contexts, this course-authoring convention accepts only decimal numbering or `-` for `sorting` items.

## Translate

Project default: use `translate` for Chinese-to-English tasks. This is a grading/authoring convention, not a parser language restriction; respect explicit manual/open/non-AI requirements.

Default:

```mdx
:::translate{type=sentence }
[prompt]
Translate into English:
如果你反复练习，表达会更自然。

[answer]
If you practice repeatedly, your expression will become more natural.

[explanation]
Focus on meaning accuracy and natural wording.
:::
```

English-to-Chinese project pattern:

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

Keep one English-to-Chinese item per block. Prefer this pattern for the project's English-to-Chinese AI-grading route. Do not silently override an explicit manual/open/non-AI request. Keep the directive and all section labels in English.

Manual marking variant:

```mdx
:::translate{type=sentence useManualMarking=true}
[prompt]
Translate into English:
如果你反复练习，表达会更自然。

[answer]
If you practice repeatedly, your expression will become more natural.
:::
```

## Writing

Default:

```mdx
:::writing
[prompt]
Write a short paragraph about one useful reading habit.

[explanation]
Optional model answer or guidance from the source.
:::
```

Peer review and teacher marking:

```mdx
:::writing{share=true shareComments=true open=true useManualMarking=true}
[prompt]
Write 80-100 words about one useful reading habit.
:::
```

Do not invent a model essay when the source does not provide one.

## Discussion / debate

Discussion:

```mdx
:::discussion
[topic]
Which reading strategy helps you most?

[guide]
Post your own view first. Then reply to a classmate.
:::
```

Debate:

```mdx
:::debate
[topic]
AI tools should be used in every reading class.

[guide]
Choose a side and give reasons.
:::
```

Use only for real class interaction, not ordinary writing prompts.

## Recorder

Reading aloud:

```mdx
:::recorder{script="Careful listening makes speaking more accurate." category="read_sentence" language="en_us" showScore=true}
Read the sentence aloud.
:::
```

Project speech with sharing:

```mdx
:::recorder{category=speak language=en_us share=true shareComments=true test_type=ielts feedbackView="transcription"}
Record your project speech here. Your recording will be shared with the class.
:::
```

## Imageupload / videoupload

Image upload:

```mdx
:::imageupload{maxAttempts=2 share=true shareComments=true useManualMarking=true}
Upload one image of your learning product.
:::
```

Video upload:

```mdx
:::videoupload{maxAttempts=2 share=true shareComments=true useManualMarking=true}
Upload a short video presentation.
:::
```

Successful upload completion earns the automatic full score. With `useManualMarking=true`, teachers can save a score and comments; the saved teacher score overrides the automatic result. Do not describe uploads as comment-only or assume AI content evaluation.

## Game matching

Default:

```mdx
:::game-matching{batchSize=4}
[left]
- cat
- eagle
- salmon

[right]
- animal
- bird
- fish
:::
```

Audio-card variant:

```mdx
:::game-matching{batchSize=3}
[left]
- cat :play[sample-audio.mp3]
- bird :play[sample-audio.mp3]

[right]
- animal sound
- flying animal
:::
```

Use for retry-until-complete matching practice. The whole game is one formal interaction.

## Game memory match

Engine-backed default; not present in the current `mdx-scorm-pages` reference project.

```mdx
:::game-memorymatch
[left]
cat
dog

[right]
猫
狗
:::
```

Use for memory-card pair matching. Keep each card on one line.

## Game choice

Default:

```mdx
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

Multi-item variant:

```mdx
:::game-choice{weight=2}
[item]
[prompt]
Choose the word that means "desk".

[options]
pen
desk
chair

[answer]
B

[item]
[prompt]
Choose the second option.

[options]
first
second
third

[answer]
2
:::
```

Use when the design wants tile-like, retry-until-correct choice practice. For ordinary exam questions, use `choice`.

## Game tokenbuilding

Default:

```mdx
:::game-tokenbuilding{space="ignore" shuffle=true}
[item]
[prompt]
:play[sample-audio.mp3] Build the word.

[answer]
cat

[tiles]
c a t x
:::
```

Sentence-building variant:

```mdx
:::game-tokenbuilding{space="ignore" shuffle=false}
[item]
[prompt]
Build the sentence. "我们喜欢阅读。"

[answer]
We like reading .

[tiles]
We like reading books .
:::
```

Use for spelling, word-building, phrase-building, or sentence-building practice.

## Style helpers

For a requested card, use `styleBlock{class="card"}`. Add only explicit custom overrides; do not repeat all system card CSS variables. For custom class styles and optional WenKai, see `syntax-inventory.md#styleblock`.


Theme-safe content box:

```mdx
:::styleBlock{class="card"}
Key content.
:::
```

One-line cue:

```mdx
::styleLine{font-style=italic margin-bottom=20} Read the passage before answering.
```

Inline emphasis:

```mdx
This is a :styleText[key idea]{color=var(--accent-1) font-weight=700}.
```

Use style helpers to express teaching function, not decoration.

## Pop

Default:

```mdx
The Palace Museum is an :pop[iconic]{ref=vocab-iconic} cultural symbol.

:::pop{def=vocab-iconic}
**iconic** *adj.* 标志性的

- iconic cultural symbol: 标志性文化符号
:::
```

For long reading courses, keep `pop` definitions near the page end and preserve full bilingual notes.

Preserve every source note as a reachable Pop definition or an ordinary visible glossary entry and search the passage case-insensitively before trying inflectional, derivational, shortened-name, acronym, and alias anchors. Capitalization alone never prevents a match: a note headed `Artificial Intelligence` matches passage text `artificial intelligence`. Use the passage form and casing as the visible trigger, preserve the note headword's casing in the definition, and require credible word or phrase boundaries. Remove only entries successfully replaced by reachable definitions. Keep unanchored notes visible and report their missing anchors separately. Follow the corresponding reference page's Pop style; in the Unit 1 pattern above, the headword is bold, the unparenthesized part-of-speech label is italic, and collocations/examples are list items.

Do not place an inline `pop` inside Markdown bold, italic, strikethrough, or combined delimiters. Preserve the same visual scope with HTML tags instead:

```mdx
<!-- Invalid -->
**aaa :pop[trigger]{ref=term-trigger} bbb**

<!-- Valid -->
<b>aaa :pop[trigger]{ref=term-trigger} bbb</b>

<!-- Valid combined formatting -->
<b><i><del>aaa :pop[trigger]{ref=term-trigger} bbb</del></i></b>
```

Use `<b>`, `<i>`, and `<del>` in that nesting order, omitting tags that do not apply. Only the smallest complete formatting span containing the trigger needs conversion; ordinary Markdown emphasis elsewhere remains unchanged.

## Collapse and showAfterSubmit

Translation reveal:

```mdx
:::showAfterSubmit
:::collapse[译文]{align=right button=true background=var(--button-bg) color=var(--button-text) padding=6 font-size=14}
中文译文。
:::
:::
```

Use this pattern when translations or explanations should unlock after formal submission.

## Splitpane

Reading plus tasks:

```mdx
:::splitpane{height="70vh" initialTopPct=0.64 minBottom=80 fitViewport fullBleed}
:::splitTop
## Reading Passage

Long source text.
:::
:::splitBottom
:::choice
[stem]
What is the main idea?

[options]
A. ...
B. ...

[answer]
B
:::
:::
:::
```

This is the default mature-course pattern for long reading passage + nearby questions.

## Sticky

```mdx
:::sticky{top=0 zIndex=5}
:::styleBlock{background=var(--quote-bg) color=var(--quote-text) border-color=var(--card-border) border-radius=12 padding=12}
Word Bank: evolve, blend, inherit, promote
:::
:::
```

Use for short reference material repeatedly needed across several items.

## Columns

```mdx
:::columns{ratios="1 1"}
:::col
English examples.
:::
:::col
Chinese notes.
:::
:::
```

Use only when side-by-side reading is useful.

## Carousel

```mdx
:::carousel{loop=true}
[slide Concept]
Short explanation.

[slide Practice]
:::choice
[stem]
Pick the answer.

[options]
A. One
B. Two

[answer]
B
:::
:::
```

Use for staged presentation or compact walkthroughs, not ordinary long content.

## Wide

```mdx
:::wide{width=1080}
| Term | Definition | Example |
| --- | --- | --- |
| previewing | quick first look | scan headings |
:::
```

Use for wide tables or code-like material that would otherwise become unreadable.

## Iframe

```mdx
:::iframe{src="/media/feixiang.html" title="Embedded page" height="520px"}
:::
```

Use only for a real embedded page or external resource.

## Media

Simple full player:

```mdx
:::media{src="sample-audio.mp3" title="Listening"}
:::
```

Transcript toggle:

```mdx
:::media{src="sample-video.mp4" type="video" aspect="16/9" transcript="toggle"}
Transcript or teaching notes.
:::
```

Submitted transcript:

```mdx
:::media{src="sample-audio.mp3" transcript="submitted"}
Transcript shown after formal submission.
:::
```

Use Markdown links or HTML media tags for simple embeds; use `media` for full controls or transcript behavior.

## External webpage links

Use standard Markdown links in source credits and ordinary prose:

```md
Source: [Article title](https://example.com/article)
```

Do not use angle-bracket autolinks such as `<https://example.com/article>`. If the source contains only a URL and no useful title or label, write `[https://example.com/article](https://example.com/article)`.

## askAI

Long prompt definition:

```mdx
:::askAI{def=reading-help}
Explain the difficult points in this passage. Keep the answer brief and cite the source text.
:::

You can :askAI[ask AI]{ref=reading-help title="Reading help"} after reading.
```

Inline prompt:

```mdx
:askAI[Ask AI]{prompt="Explain this paragraph in simple terms." title="Reading help"}
```

Use only when inline AI assistance is part of the course design.

## aiexercise

```mdx
:::aiexercise{trigger="manual" source="page" mode="practice" appId="demo-app-id"}
[types]
choice
translate

[count]
2

[intro]
Generate a short extra practice round.
:::
```

Use for runtime-generated practice, not static authored questions.

## exportcontent

```mdx
:::exportcontent{scope="page" format="markdown" locale="zh" profile="student"}
:::
```

Use only when the page itself needs export tooling.

## Mature reading-course page patterns

Long reading and exam questions:

- Use `splitpane`.
- Put the passage in `splitTop`.
- Put questions in `splitBottom`.
- Put vocabulary/term `pop` definitions after the splitpane.
- Put paragraph translations in `showAfterSubmit` + `collapse[译文]`.

Unit project:

- Use normal markdown for project steps.
- Use theme-safe `styleBlock` / `styleLine` only for headings, task requirements, and compact emphasis.

## Classification patterns

Use the complete minimal classification example and structural rules in `syntax-inventory.md#classification`. For multi-category membership, repeat the exact candidate source under both targets, for example `Tomato` under Fruit and Vegetable only when the supplied source defines those categories that way. For a rich candidate, wrap one item:

```mdx
:::item
:styleText[Tomato]{color=var(--accent-1) font-weight=700}
:::
```

Place this item inside a target's `[items]`; use the identical wrapper body in every target to which it belongs. Do not add an answer section. Classification is engine-backed.

## Knowledge graphs and HTML code

For a runnable HTML App, follow `html-apps.md`; static HTML fragment rules below apply only to static HTML requests.


For an explicitly requested knowledge map, follow `syntax-inventory.md#knowledgegraph`, including inventory-backed lesson links. For explicit HTML code requests, read `html-fragments.md`; return an `html` code block of elements, without files, download links, or a full document.

## Synchronized reading, staged reveals, and weighted blanks

See [reading-and-reveal.md](reading-and-reveal.md) for complete examples of audio/video Reading with timed Chunk, local/nested Reveal, linked show/on regions and final per-blank weights. Check timing, label/body distinctions and hidden-question scoring before adapting the examples.
