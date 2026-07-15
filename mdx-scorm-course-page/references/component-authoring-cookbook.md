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
- If a component is not present in `mdx-scorm-pages` but is present in current `mdx-scorm`, mark it as engine-backed rather than reference-course-backed.

## Frontmatter defaults

Display-only page:

```mdx
---
title: Page Title
feedback: submit
numbering: none
---
```

Interactive page:

```mdx
---
title: Page Title
feedback: submit
numbering: none
---
```

Weighted page:

```mdx
---
title: Page Title
feedback: submit
numbering: none
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
title: Page Title
feedback: submit
numbering: none
aiCompanion:
  enabled: true
  interactiveVisibility: always
  questionOverlay: true
---
```

Use `weights:` and `aiCompanion:` only when the page or catalog design calls for them.

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

## Fillblank

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

## Choicecloze

Default:

```mdx
:::choicecloze
[content]
The museum has @--@ from a palace to a public cultural space.

[options]
evolved | erased | hidden | delayed

[answer]
1
:::
```

Use for word-bank cloze, TRUE/FALSE/NOT GIVEN selection, or repeated fixed-option blanks.

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

Use when each left item has a correct right match and item-level scoring matters. Use `game-matching` for retry-until-complete matching practice.

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

Use only when the source clearly has ordered steps or sequences.

## Translate

Default:

```mdx
:::translate{type=sentence rows=4}
[prompt]
Translate into English:
如果你反复练习，表达会更自然。

[answer]
If you practice repeatedly, your expression will become more natural.

[explanation]
Focus on meaning accuracy and natural wording.
:::
```

Manual marking variant:

```mdx
:::translate{type=sentence rows=4 useManualMarking=true}
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
:::writing{rows=6}
[prompt]
Write a short paragraph about one useful reading habit.

[explanation]
Optional model answer or guidance from the source.
:::
```

Peer review and teacher marking:

```mdx
:::writing{rows=6 share=true shareComments=true open=true useManualMarking=true}
[prompt]
Write 80-100 words about one useful reading habit.
:::
```

Do not invent a model essay when the source does not provide one.

## Discussion / debate

Discussion:

```mdx
:::discussion{rows=4}
[topic]
Which reading strategy helps you most?

[guide]
Post your own view first. Then reply to a classmate.
:::
```

Debate:

```mdx
:::debate{rows=4}
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

Manual marking for upload blocks is comment-only.

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

Theme-safe content box:

```mdx
:::styleBlock{background=var(--card-bg) border-color=var(--card-border) border-radius=12 padding=12}
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