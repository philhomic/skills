# Game rounds and completed answers

Applies to `game-choice`, `game-matching`, `game-memorymatch`, and `game-tokenbuilding`. Use games only when the requested learner activity calls for them. Keep the full authored question bank in source.

## Sampling and order

- Block attribute `limit` is optional. Omission uses the full bank; a positive integer selects at most that many items. A value above the bank size uses the full bank. Zero, negative, fractional, or nonnumeric values are configuration errors.
- `shuffleQuestions` defaults to `false`; use `true` or `false`. Without it, take the first N items. With it, shuffle the full bank before taking N, without duplicates within a round. Separate rounds may overlap or even repeat.
- Choice and tokenbuilding count questions/rounds; matching and memorymatch count pairs. `limit=6` means 12 memory cards. Matching's `batchSize` only controls visible pairs, not the total selected pairs.
- Mounting or redoing starts a new selection/order. Answering, feedback, or an ordinary rerender does not reshuffle. Changes to these settings during a round apply on redo/remount. Navigation reshuffles only if the component remounts.
- `shuffleQuestions` does not shuffle choice options. Tokenbuilding's existing `shuffle` controls candidate tiles separately; memory card positions are shuffled separately.
- Completion summaries and progress use the selected total. Unfinished progress and selected item identities are not persisted; completed state restoration requires a matching total.
- Studio's native editor keeps all authored items in source order. Its per-round quantity and random-order controls affect the learner runtime, not the editing canvas.

```md
:::game-matching{limit=2 shuffleQuestions=true batchSize=1}
[left]
- cat
- dog
- bird
[right]
- 猫
- 狗
- 鸟
:::
```

## Tokenbuilding correct feedback

After a correct check, tiles are displayed as one continuous answer during the existing 520 ms feedback interval. Wrong/unchecked answers remain editable tiles; judging, scoring, and automatic advancement are unchanged.

Optional item attribute `answerDisplay` supplies plain text for this feedback only. In authored MDX, escape the item attribute braces (block directive braces stay unescaped):

```md
:::game-tokenbuilding{shuffle=false}
[item]\{answerDisplay="unhappy"\}
[prompt]
Build the word.
[answer]
un happy
[tiles]
un happy very
:::
```

When omitted or whitespace-only, single English letter tokens join into a word; ordinary words are spaced, common punctuation/contractions attach, and consecutive Han characters join. This is formatting, not an alternative answer or judging rule. For ambiguous affixes, mixed languages, hyphens, or quotes, supply explicit display text. `space` still controls judging only. HTML/Markdown is not executed. Encode attribute quotes/braces with `&quot;`, `&#123;`, `&#125;` and literal ampersands with `&amp;`.

## Static output and themes

Print exports use the full authored bank in source order, irrespective of `limit` and `shuffleQuestions`. `answerDisplay` does not replace teacher reference answers; these still derive from `[answer]`. Student output hides reference answers. No check, retry, or completion UI is printed. Verify Bundle and target PDF separately when delivering exports.

With `cardMode: false`, ordinary question outer padding and decoration are removed; internal inputs/options retain their spacing. Do not remove internal control borders. Card mode on keeps the normal theme cards. Bauhaus and Newsprint blank controls do not receive outer-card decorations; their configuration error cards also respect card mode off.

Implementation evidence: `mdx-scorm/src/components/useGameQuestionOrder.ts`, `gameTokenBuildingAnswerDisplay.ts`, `mdx-scorm/src/styles/global/03-primitives.css`, Studio `mdxR4ComponentCodec.ts`, and `packages/book-export`. Skill maintenance alone does not update deployed runtimes, installed Skills, or cloud Agents.
