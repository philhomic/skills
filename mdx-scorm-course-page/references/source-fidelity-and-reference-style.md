# Source fidelity and reference-style rules

Use this reference whenever the source is a Word document, the task provides a reference course, or the output contains glossary notes, vocabulary notes, cultural/professional terms, or unresolved editorial issues.

## 1. Keep unresolved issues outside MDX

Never place unresolved editorial issues, missing-source warnings, inferred repairs, or other TODO notes inside a generated `.mdx` page, including HTML comments.

This rule concerns production annotations, not literal source text such as “to do”, “TODO”, or quoted examples. Preserve those source strings. “Hosted mode” below means the explicitly configured protocol in hosted-protocol.md, not every chat session.

In hosted / Cloud Studio mode, never create or propose `TODO.txt`. Preserve a usable source-faithful MDX representation and expose unresolved non-blocking observations through ProductionIssue output. Ask one focused question before generation only when a missing fact, scored answer, or exercise mode is genuinely required.

For an explicit filesystem batch, use a sibling issue file when needed for handoff (ordinary local chat can report issues directly):

- create or update `TODO.txt` in that same directory
- consolidate all issues for pages in that directory into the one file
- identify the page, location, source conflict, handling used in the MDX, and required follow-up
- do not create `TODO.txt` when the directory has no unresolved issues

Use this plain-text form:

```text
[01]
page: 02_section_a.mdx
location: Section A / Blank 10
issue: The answer key gives "transformed", while the Skill Summary gives "transforms".
handling: The MDX preserves "transformed" from the answer key.
follow-up: Confirm the intended form with the author.
```

The MDX must remain clean and usable even when `TODO.txt` is removed.

## 2. Preserve Word paragraph boundaries

Treat a Word paragraph (`w:p`) as the authoritative paragraph unit.

- Merge all runs (`w:r`) and text nodes that belong to the same Word paragraph before producing Markdown.
- Do not turn run boundaries, visual line wrapping, page wrapping, text-box extraction fragments, or PDF-like line extraction into Markdown paragraph breaks.
- Within ordinary prose, normalize internal manual line breaks (`w:br`) and tabs to a space unless the source clearly uses them for a list, verse, address, option set, table-like layout, or another deliberate line-based structure.
- Preserve a real boundary between separate Word paragraphs.
- Keep headings, list items, table cells, question options, and intentionally lineated content separate according to their structural role.
- After conversion, compare paragraph counts and paragraph starts for every long reading passage. A single source paragraph must not become several MDX paragraphs without an explicit structural reason.

If the high-level DOCX extraction appears to split a paragraph, inspect `word/document.xml` or the relevant text-box XML before deciding where the paragraph ends.

## 3. Preserve every note as a reachable Pop or visible glossary entry

Build an annotation ledger before writing the passage. Each source footnote, endnote, vocabulary item, cultural term, professional term, or glossary entry must remain available exactly once as a reachable Pop definition or a visible ordinary note/glossary entry unless the user explicitly excludes it.

For each ledger item, search the associated preceding passage for a credible inline anchor in this order:

1. exact match, Unicode-aware case-insensitive match, and punctuation/hyphen normalization
2. inflectional variants, including singular/plural and verb forms such as `restore`, `restores`, `restored`, and `restoring`
3. transparent derivational variants when the definition still applies in context
4. multiword variants, shortened forms, acronyms, aliases, and reordered name forms
5. a person's full name versus an unambiguous surname, given name, initials, title plus surname, or shortened name used in the passage

Case-insensitive matching is mandatory, not an optional fallback. Compare normalized or case-folded forms, so capitalization alone never prevents anchoring. For example, a note headed `Artificial Intelligence` must match `artificial intelligence` in the passage, and `METAVERSE` must match `metaverse`. Apply word or phrase boundaries so this does not degrade into arbitrary substring matching.

Use the actual wording and casing found in the passage as the visible `:pop[...]` trigger. Preserve the note headword's original casing in the Pop definition. Do not change either surface form merely to make their capitalization agree, and do not record a capitalization-only mismatch as unanchored in `TODO.txt`. Use the glossary headword only for the stable `ref`/`def` id.

Preserve source or reference emphasis around an inline trigger, but never wrap `:pop[...]` inside Markdown `*`, `_`, `**`, `__`, `***`, `___`, or `~~` delimiters. If the trigger lies inside a bold, italic, strikethrough, or combined span, replace the complete surrounding delimiter pair with `<b>`, `<i>`, and/or `<del>` tags. For combinations, nest in the canonical order `<b><i><del>...</del></i></b>` and omit unneeded tags. Do not change the formatting scope or convert unrelated Markdown spans.

Aim to give every definition at least one credible `ref`. When a term occurs repeatedly, annotate the first or most pedagogically relevant occurrence unless the reference course clearly repeats triggers. Do not force an unrelated string match.

If no credible anchor remains after the full search, do not invent a fake inline trigger.

- In hosted / Cloud Studio mode, preserve that source entry in an ordinary glossary/notes representation and emit a non-blocking `authoring` ProductionIssue. Do not create an unreachable Pop definition and do not create `TODO.txt`.
- In local file mode, keep the entry visible in an ordinary glossary/notes section and report the missing anchor separately (or in a sibling `TODO.txt` for a batch). Do not leave an unreachable definition and remove the visible source entry.

After conversion, remove only the original entries that were successfully replaced by reachable Pop definitions. In hosted mode, keep unanchored entries once in the ordinary glossary/notes representation; do not duplicate them.

Before finalizing, verify:

- source annotation count equals reachable Pop definitions plus preserved unanchored glossary/notes entries
- every `ref` has one matching `def`
- every `def` has a credible `ref` in both hosted and local modes; unanchored notes remain visible without a fake trigger
- capitalization-only headword/anchor differences were matched and preserve their respective source casing
- different source notes were not silently merged

## 4. Let the reference course control presentation

When a reference course or corresponding reference page is provided:

- treat the target Word document as authoritative for facts, wording, answers, translations, and note content
- treat the corresponding reference page as authoritative for presentation patterns, provided its syntax is valid
- inventory the reference pattern before writing: heading depth, label order, bold/italic use, punctuation, parentheses, list structure, spacing, directive placement, reveal structure, and layout
- apply that pattern consistently to semantically parallel target content
- do not paste Word formatting unchanged when the reference course has already established a different house style

For the supplied Unit 1 reference, vocabulary Pop definitions use this pattern:

```mdx
:::pop{def=vocab-restore}
**restore** *v.* 【六级高频词】恢复；修复

- restore confidence 恢复信心
- restore a building 修复建筑
:::
```

Therefore:

- show the headword in bold
- show the part-of-speech label in italics, without parentheses
- turn collocations/examples into Markdown list items
- preserve all source meanings, labels, collocations, examples, and bilingual content while restyling them

Do not assume this exact pattern for an unrelated reference course; infer and follow that course's own corresponding pattern.

## 5. Italicize part-of-speech labels

In English course content, format part-of-speech abbreviations as italic Markdown whenever they function as grammatical labels.

Examples include:

- `*n.*`
- `*v.*`
- `*adj.*`
- `*adv.*`
- `*prep.*`
- `*pron.*`
- `*conj.*`
- `*num.*`
- `*art.*`
- `*aux.*`
- `*modal v.*`
- `*phr. v.*`

Do not leave labels such as `adj.`, `n.`, `v.`, or `adv.` in plain text. Do not add parentheses unless the corresponding reference page explicitly uses them.

## 6. Omit feedback and numbering configuration by default

Use the course runtime's feedback and numbering defaults unless the user or the corresponding reference page explicitly specifies an override.

Default:

```mdx
# Page heading
```

Do not add frontmatter `title` unless the user explicitly requests it; preserve an existing title during unrelated edits. Body headings are independent. Omit the whole frontmatter when no settings are needed.

Do not add any of these fields by default:

- `feedback`
- `numberType`
- `numberingType`
- `numbering`
- a page-level `type`

In particular, do not write `feedback: submit` merely to restate the course's default submit behavior. Only copy `feedback` when the corresponding reference page clearly contains it, or when the author explicitly requests a feedback mode. Preserve the exact supported value used by that project.

Only copy a supported numbering field when the corresponding reference page clearly contains it, or when the author explicitly requests it. Preserve the exact supported key and value used by that project; do not translate an omitted default into `none` or `type`.

## 7. Final fidelity pass

Before packaging a page or unit:

1. compare Word paragraph units with MDX prose paragraphs
2. compare the content-derived heading ledger with the page map; confirm that child headings were not promoted, top-level section counts did not drift without a content-based reason, and no split duplicated parent context
3. compare the annotation ledger with Pop definitions and refs
4. confirm only successfully converted entries were removed from end lists; unanchored notes remain visible
5. compare representative target blocks against the corresponding reference page's style schema
6. scan part-of-speech labels for missing italics
7. scan for an inline `pop` enclosed by Markdown emphasis or strikethrough delimiters
8. scan frontmatter for default `feedback` and numbering keys that should have been omitted
9. scan for editorial TODO comments; preserve literal source text such as “to do” or “TODO”
10. run `scripts/validate_course_output.py` on the output directory and review warnings; its coverage is limited to conventions and lightweight structure

## 8. Let content control Word heading hierarchy

Use DOCX structural metadata as evidence, not as the final source of truth. For every candidate heading, consider both:

- content evidence: visible numbering, heading wording, umbrella-and-subsection relationships, introductions, parallel sibling labels, and the scope of the following paragraphs
- DOCX evidence: paragraph style (`pStyle`), outline level (`outlineLvl`), list identity and level (`numId` / `ilvl`), and indentation

Resolve the hierarchy from the complete content pattern. When these sources conflict, follow a clear content relationship. In particular, numbered headings such as `2.1` and `2.2` remain children of `2` unless the document's actual wording and organization give strong contrary evidence, even when all three paragraphs share the same Word outline level or style.

Before mapping headings to pages, create a heading ledger with at least:

- source heading text
- visible number or label
- content-inferred level and parent
- relevant DOCX metadata
- target page
- any metadata/content conflict and its resolution

Do not turn a subsection into a peer page solely because it is long, visually prominent, or uses the same Word style as a top-level heading. Do not change three content-defined parts into four page-level parts merely to fit a reference template. If a long source section must span more than one page, preserve the parent-child relationship, assign each source span once, and do not repeat the parent introduction to make each page appear standalone.
