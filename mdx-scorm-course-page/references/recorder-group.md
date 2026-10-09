# Paged recording practice

Use `recorderGroup` when several recording exercises should occupy one card at a time. Keep ordinary `recorder` for a single exercise or when all prompts should remain visible. This is a recording-only container, not a general slide container.

```md
::::recorderGroup{id="unit1-reading"}
:::recorder{id="word" category="read_word" language="en_us" script="apple"}
Read **apple** aloud.
:::

:::recorder{id="sentence" category="read_sentence" language="en_us" script="I eat an apple every day."}
Read: I eat an apple every day.
:::

:::recorder{id="chapter" category="read_chapter" language="en_us" script="This is my garden. I water the flowers every morning."}
This is my garden. I water the flowers every morning.
:::
::::
```

- The group accepts only direct `recorder` children and only the group attribute `id`. Put instructions in each child's body. Do not add a group-level prompt, nested groups, other question types, or `autoNext`.
- Keep source wording in the prompt and assessment `script`. Do not shorten the service script merely to reduce visible height. Mixing word, sentence, and passage categories is supported.
- Give each group a page-unique stable ID and each child a group-unique stable ID. Stored child IDs use `group/child`. Do not reuse published IDs for different exercises. Automatic IDs exist; source edits can change them. The native editor pins existing automatic IDs before structural changes.
- Put language, scoring, weight, sharing, and feedback attributes on individual recorders. The group does not score separately. Do not invent group-level defaults.
- Navigation is manual, does not wrap, and is locked while recording, uploading, or scoring. Switching pauses media playback. A one-item group has no navigation buttons.
- All children participate in submission and restoration, including hidden ones. The completed count follows recorder completion (an answer attempt), not assessment success. Reopening starts at the first child while answers use the normal restoration mechanism.
- ScoreCard groups children visually and reveals the selected child before locating it. Browse statistics remain per child. Static export expands all children.
- Cloud Studio's native implementation supports Slash insertion, direct prompt editing, child Recorder properties, adding/removing/reordering children, and undo/redo. The editor expands children for authoring; the learning view remains paged. At least one child must remain. Unknown attributes or unsupported child structure keep the complete group source-owned without discarding content. Check deployment status before promising these editing controls on a hosted instance.

Engine implementation baseline: `99b9b178`. This reference does not prove that a hosted editor, build service, print engine, or installed Publisher has been upgraded. Confirm the target runtime supports this syntax before generating it for an older deployment.
