# Reading, reveal, and per-blank weights

Audited against local engine commit `b8b080d4` on 2026-10-08. This reference supports local course authoring. Use the requested local destination and report actual checks under SKILL.md. Repository paths below locate the implementation used for this audit. A skill update does not deploy engine, Studio or Print services.

## Choose by learner action

| Requested behavior | Use |
| --- | --- |
| Play audio/video with synchronized passage highlighting and click-to-seek | `reading` with inline `chunk` |
| Reveal content once in place, then remove the button | `reveal` |
| Reveal several separated regions with one button | `reveal{show=group}` and `revealed{on=group}` |
| Repeatedly expand and collapse content | Existing `collapse` |
| Make content available only after submission | Existing `showAfterSubmit` |
| Give individual non-AI fillblank blanks different scoring weights | `fillblank{interactionWeights="..."}` |

These are distinct from scored selection (`textselect`) or correction (`textedit`). Reveal is not a submission gate. Do not invent video breakpoint questions or a `videoPractice` directive.

## reading / chunk: synchronized reading

```mdx
:::reading{id="story-reading" src="story.mp3" type=audio title="Listen and read" rates="0.8,1,1.25"}
## A short story

:chunk[It was a **quiet morning**.]{id="s1" start="0" end="3.5"}

:chunk[Then the telephone rang.]{id="s2" start="3.5" end="7"}
:::
```

The example assumes the supplied audio actually matches these sentences and times. Use verified course media paths and source-supplied or measured timestamps. Missing audio/alignment does not authorize inventing a synchronized passage: preserve ordinary text and request the missing material when synchronization is required.

- `reading` is a block container; `chunk` is inline `:chunk[text]{start="..."}` inside it. Do not use block `:::chunk` or nest reading regions/chunks inside the same type.
- `src` is required. `type` is `auto` (default), `audio`, or `video`; set it explicitly when the URL extension cannot establish the media kind. Video may use `poster="story.jpg"`.
- Optional reading `id` is unique on the page; optional chunk `id` is unique in that reading region. `title` labels the player. `rates` is a comma-separated list of playback speeds (0.0625–16, subject to browser support); default is `0.5,0.8,1,1.25,1.5,2`.
- Every chunk needs non-negative `start`: decimal seconds, `m:ss`, or `h:mm:ss`, optionally with fractional seconds, such as `62.5`, `1:02.5`, `1:00:02`.
- Starts strictly increase in document order. Optional `end` must exceed its own start and may not overlap the next start or exceed known media duration. Gaps are legal. Without end, use the next start; the final chunk uses known duration, or temporarily extends while duration is unknown.
- Preserve headings, paragraphs and existing display components. Chunk content accepts inline Markdown and compatible inline helpers; do not flatten emphasis or Pop definitions. Links/buttons/Pop retain their own actions; selecting text does not trigger seeking.
- Clicking ordinary chunk text seeks to its start and continues playback; end controls highlighting, not automatic pause. Reading has no transcript or automatic follow-scroll and does not stop other players. A chunk cannot span paragraphs.
- Invalid timing disables synchronized highlighting for the region while leaving text/player available. Do not present this fallback as valid alignment.
- Reading itself registers no scored answer or completion interaction; nested native exercises retain their own tracking and scoring. Text export retains passage content and removes player/timing wrappers. Print outputs static passage content with a media link and collects the referenced media; PDF does not embed playable audio/video.

## reveal / revealed: one-way reveal

### Local inline content

```mdx
山脉 :reveal[**mountain**]{label="显示英语"}

山脉 :reveal[**mountain** :reveal[/ˈmaʊntən/]{label="显示音标"}]{label="显示英语"}
```

Without `show`, inline brackets contain the hidden content. `label` is plain button text, defaulting to `点击显示`. Hidden content may contain supported inline Markdown, StyleText, Pop or Play; their existing contracts still apply. Reveal does not itself start audio or recording.

### Local block content and staged hints

```mdx
::::reveal[Show a hint]
First identify the part of speech.

:::reveal[Show another hint]
Then check the surrounding words.
:::
::::
```

For block shorthand, brackets are the plain-text button label and the body is hidden content. Omit brackets for the default label. Use longer outer colon fences for nesting. Blocks can retain supported block components, including native exercises; preserve all question IDs and scoring attributes.

### One trigger, multiple locations

```mdx
:reveal[Show English]{show=english}

山脉 :revealed[**mountain**]{on=english}

高原 :revealed[**plateau**]{on=english}

:::revealed{on=english}
Both words describe landforms.
:::
```

Use a shared group only for intentionally linked content. `show="english phonetics"` opens multiple whitespace-separated groups; `on` accepts exactly one non-empty group. Several triggers may control the same group; a trigger disappears once all its targets are open. An opened child cannot escape a still-hidden parent.

```mdx
:::reveal[Show both]{show="english phonetics" align=center}
:::

:revealed[mountain]{on=english} :revealed[/ˈmaʊntən/]{on=phonetics}
```

Authoring constraints:

- A `show` trigger cannot also have `label` or block body content. Its bracket label must be plain text, not rich Markdown or another interaction.
- `reveal` does not accept `on`. `revealed` requires `on` and does not accept `show` or `label`.
- Do not invent Reveal `def/ref`, boolean conditions or reverse-collapse behavior. Existing Pop `def/ref` remains separate.
- Ensure each group has intended targets and a reachable trigger. Do not put the only trigger inside its own hidden target or create cycles with no visible entry.
- Local reveals are independent. Use stable, unique `id` for dynamically reordered local instances.
- Shared style attributes on `reveal` style the button, not hidden content. Use existing StyleText/StyleBlock inside the body for content styling. `button=false` gives a text-like trigger; block controls support `align`, `fullWidth`, `labelAlign`. Prefer theme tokens for colors.

Runtime and export boundaries:

- Clicking reveals content in place and removes the trigger; it does not toggle closed.
- Hidden children stay mounted; native questions still register, restore and score. Reveal itself is not a question. Do not use it to exclude a hidden question from submission, change its weight, or imply `scorm=false`.
- Progress survives same-session page revisits for the current practice mode; page reset/new practice clears the corresponding reveal progress. Browser refresh does not persist click progress. Successful restoration of a formally submitted remote attempt expands all reveals; an empty/failed read or unsubmitted draft does not.
- Print expands the content and hides buttons in both student and teacher profiles; native question answers/explanations still follow the selected profile. Content export removes Reveal wrappers recursively, keeping native question export semantics. Never rely on Reveal to keep authored answers secret in print/export.

## fillblank: final per-blank weights

```mdx
:::fillblank{interactionWeights="1,1,3"}
[content]
One @cat@ and one @dog@ are @--@.
[answer]
animals
:::
```

- This attribute belongs to `fillblank`; do not generalize it to other question types.
- Supply one non-negative finite number per actual blank, in body order, including both embedded answers (`@cat@`) and `[answer]`-backed `@--@` blanks. Zero is legal; it removes that blank's score weight without making it untracked practice.
- These are final weights, overriding question `weight`, `weightDistribution` and page type weights; do not multiply or divide them again. In the example, getting only the first two blanks right gives 2/5 of the score weight.
- Canonical authoring uses comma-separated numbers. The engine also accepts Chinese commas, enumeration commas, or whitespace. Avoid empty entries, negative values, non-finite values, or a count mismatch.
- Do not combine with `aiScore=true`. Invalid configuration blocks normal submission rather than silently reverting to equal weights.
- Omit the attribute when no per-blank weighting was requested; omission restores the existing shared/average rules. Do not change answers or infer unequal weights from perceived difficulty.

## Authoring checks and maintenance evidence

Check real assets/timestamps, chunk order and end boundaries; correct inline/block forms; reveal label/body distinction, group reachability and matching targets; hidden-question scoring intent; and weight count/AI compatibility. The bundled Python convention checker is not a semantic validator for these contracts. When the target engine is available, use its parser and feature-specific checks; do not claim cloud deployment or live service validation from a documentation check.

Verified source locations relative to the engine repository:

- `packages/mdx-semantics/src/reading-semantics.ts`; `mdx-scorm/src/components/reading/readingTimeline.ts`, `readingSyntax.test.ts`, `readingTimeline.test.ts`.
- `mdx-scorm/src/mdx/remarkReveal.ts`, `remarkReveal.test.ts`; `mdx-scorm/src/components/Reveal.tsx`, `Reveal.scorm.test.tsx`; `mdx-scorm/docs/reveal.md`.
- `mdx-scorm/scripts/lib/fillBlankInteractionWeights.mjs`; `mdx-scorm/src/components/FillBlankBlock.tsx`, `FillBlankInteractionWeights.test.tsx`; `mdx-scorm/User Manual.md` sections 5.16 and 6.2.6.
