# Exercise-type selection and reference conflict rules

Use this reference whenever source exercises are converted into interactive directives, especially when a supplied reference course uses a different exercise type.

## 1. Classify the task before looking at the reference component

Describe the learner's required action without naming an MDX component. Then identify the answer relationship.

| Learner action and answer relationship | Default directive |
|---|---|
| Select one or more answers from a separate option list | `choice` |
| Select individual words/punctuation within original text (圈选题) | `textselect{mode="word"}` |
| Select complete contiguous phrases within original text (语块圈选) | `textselect{mode="span"}` |
| Correct original text by inserting, deleting or replacing fragments (改错题) | `textedit` |
| Enter an answer without a supplied option bank | `fillblank` |
| Answer a question in prose (问答题) | One standalone `fillblank` blank per question; omit `rows` |
| Answer a question with requested AI scoring | `fillblank{aiScore=true}` with one standalone blank |
| Complete genuine blanks from a shared or repeated option set | `choicecloze` |
| Map each item independently to a function, definition, paragraph, or counterpart | `matching` |
| Group items into one or more named categories | `classification` |
| Reconstruct one ordered sequence of steps, events, sentences, or argument stages | `sorting` |
| Translate Chinese source text into English | `translate` |
| Translate English source text into Chinese | `fillblank` with `aiScore=true` |
| Produce extended original text | `writing` |

For synchronized media reading, one-way or linked hints, or requested per-blank weights, read [reading-and-reveal.md](reading-and-reveal.md). Reading and Reveal are presentation features, not replacement question types. Use `collapse` for reversible expansion and `showAfterSubmit` for post-submit content; hidden Reveal children still participate in scoring.

A non-scoring question uses `weight=0`, not `scorm=false`. Ordinary question answering is not a writing assignment: reserve `writing` for paragraph composition or essays. Do not set `rows` unless explicitly requested.

For text selection/correction, read `text-exercises.md`. A request to identify pronouns or verb phrases in a passage is selection, not a separate-option choice or blank exercise. A supplied erroneous sentence plus its corrections is a textedit task; preserve its original errors and encode the corrections. Missing answers require clarification under SKILL.md uncertainty rules, not fabricated targets or an implicit open mode.

Do not classify by surface appearance alone. An option bank plus answer lines does not automatically make an exercise a `choicecloze`.

Translation direction is part of the task semantics. The project defaults to `translate` for Chinese-to-English grading and AI FillBlank for English-to-Chinese. The parser does not validate a language direction; the external service and explicit manual/open/non-AI choices must be considered separately. Default AI pattern:

```mdx
:::fillblank{aiScore=true}
[content]
21. Please translate the following sentence into Chinese.

> English source sentence.

@--@

[answer]
完整的中文参考译文。

[ai]
instruction: 这是一道句子英译中的题目。请重点评价翻译质量，给出翻译的优缺点。
:::
```

Use one block per translation item. Keep exactly one `@--@` after the English source text. Use this when AI translation feedback is intended. Do not enable AI merely to satisfy a template when the user explicitly requests manual, open, or non-AI work; preserve that choice and explain any service limitation.

## 2. Use this evidence priority

Judge the exercise from all available source evidence in this order:

1. learner action and answer topology
2. directions
3. item structure, option structure, and answer key
4. exercise title or label
5. corresponding reference-course component

Exercise titles and directions can be imprecise. Resolve them against the actual relationship encoded by the items and answers.

## 3. Distinguish matching, sorting, and choicecloze

Use `matching` when every left-side item has an independently scorable right-side counterpart. Typical signals include:

- “match each evidence type to its function”
- “match each statement to the paragraph”
- terms paired with definitions
- findings paired with claims or categories

Use `sorting` when all supplied items form one intended order. Typical signals include:

- “the steps are in the wrong order”
- “reconstruct the logical flow”
- “arrange the events in chronological order”
- “put the stages in the correct sequence”

Some ordering directions say “match each step to position 1–5.” Do not let the verb *match* override the task topology. If the positions jointly express one sequence, use `sorting`.

Use `choicecloze` only when learners fill actual gaps in continuous or itemized content from a shared/repeated fixed option set. Appropriate examples include:

- a word-bank summary cloze
- repeated TRUE/FALSE/NOT GIVEN blanks
- repeated fixed labels inserted into genuine blank positions

Do not use `choicecloze` merely to simulate matching or ordering with blank labels.

## 4. Treat the reference course as conditional guidance

The target source controls:

- what learners must do
- the answer relationship
- facts, wording, options, and answers

The reference course may control:

- page organization
- heading and label style
- directive placement
- reveal behavior
- spacing, emphasis, and other compatible presentation patterns

Copy the reference interaction type only when the target task is semantically compatible. If it is incompatible, choose the supported target-faithful directive and retain only compatible visual and structural patterns.

The absence of `matching` or `sorting` in the reference package is not a reason to fall back to `choicecloze`.

## 5. Record confidence and ask only when needed

For each exercise in the unit plan, record:

- source exercise title or location
- learner action
- answer relationship
- selected directive
- reference page influence
- confidence: high, medium, or low

Use these thresholds:

- **High confidence:** directions, items, and answers agree. Select the semantically correct directive without asking.
- **Medium confidence:** labels and answer topology conflict, or two directives would create materially different learner actions. Ask the author before generating that exercise when practical.
- **Low confidence:** directions, options, or answers are incomplete enough that the intended action cannot be recovered. Ask the author. For an explicitly non-interactive batch, keep unresolved exercises as plain Markdown and report the issue separately; a filesystem batch may record it in a sibling `TODO.txt`.

Do not ask merely because the target differs from the reference. Ask because the target itself remains ambiguous.

## 6. Unit 9 regression cases

### Evidence-to-function task

Source direction:

> Match each evidence type to its function in the author's argument.

The items map independently from evidence types to argument functions.

Decision: `matching`, not `choicecloze`.

### Finding-to-claim task

Source direction:

> Match each finding from Section B with the claim from Section A whose scope it most directly limits or extends.

Each finding maps to one claim or to “no direct match.”

Decision: `matching`, not `choicecloze`.

### Argument-flow task

Source direction:

> The following sentences describe the steps of the author's central argument, but they are in the wrong order. Reconstruct the logical flow by matching each step (A–E) to its correct position in the argument sequence (1–5).

Although the sentence contains *matching*, the five items jointly form one logical sequence.

Decision: `sorting`, not `choicecloze`.

### Summary cloze

The summary contains eight textual blanks completed from one eight-item Word Bank.

Decision: `choicecloze`.

## 7. Final semantic QA

Before packaging:

1. compare every source exercise with its generated directive
2. verify that the generated interaction preserves the original learner action
3. verify translation direction: Chinese-to-English may use `translate`; English-to-Chinese follows the AI `fillblank` project default unless an explicit different grading mode applies
4. search `choicecloze` blocks for matching or ordering cues
5. run `scripts/validate_course_output.py`
6. inspect semantic warnings against the actual source/user decision; they are heuristic suggestions, not engine errors. Page exception flags record known decisions without requiring repeated approval.
