# Engine evidence and validation boundaries

Maintenance update: 2026-10-08, local `welearn-ninja` commit `b8b080d4`; selectively incorporates capability guidance from `mdx-scorm-course-page-updated-20261008.zip` while retaining local authoring behavior. Previous baseline: 2026-09-30, engine `9c00bc4e`, repository skill `7771917`. These are audit provenance, not a minimum-version claim. Recheck the actual target runtime when it differs. No engine deployment is performed by installing this skill.

Paths below are relative to the `welearn-ninja` repository. The local maintenance checkout is `D:\Projects\welearn-ninja`; cloud callers do not need that filesystem.

| Capability | Source of truth / useful check |
| --- | --- |
| Reading media/timeline | `packages/mdx-semantics/src/reading-semantics.ts`; `mdx-scorm/src/components/reading/readingTimeline.ts`, `readingSyntax.test.ts`, `readingTimeline.test.ts` |
| Reveal syntax, hidden children and restore | `mdx-scorm/src/mdx/remarkReveal.ts`; `mdx-scorm/src/components/Reveal.tsx`, `Reveal.scorm.test.tsx`; `mdx-scorm/docs/reveal.md` |
| Reading/Reveal print profiles | `packages/book-export/tests/reading.test.mjs`, `reveal.test.mjs`; static prose/media links and native question profile rules |
| Final per-blank weights | `mdx-scorm/scripts/lib/fillBlankInteractionWeights.mjs`; `mdx-scorm/src/components/FillBlankInteractionWeights.test.tsx` |
| Upload scoring and teacher marking | `mdx-scorm/src/components/MediaUpload.tsx`, `MediaUpload.alignment.test.tsx`; completion-based score and score-and-comment marking |
| Discussion completion | `mdx-scorm/src/components/Discussion.tsx`, `Discussion.completion.test.tsx`; published content and class access, not drafts |
| Text exercise attributes and raw body | `mdx-scorm/src/mdx/remarkTextSelectBlock.ts`, `remarkTextEditBlock.ts` |
| Text markers, token boundaries, limits, normalization | `packages/mdx-semantics/src/text-select-semantics.ts`, `text-edit-semantics.ts`; `packages/mdx-semantics/tests/text-exercise-semantics.test.mjs` |
| Text exercise export | `packages/mdx-semantics/src/text-exercise-export.ts`; `packages/book-export/src/text-exercise-print.ts` |
| Classification relations and source identity | `packages/mdx-semantics/src/classification-semantics.ts`; `mdx-scorm/src/components/Classification.tsx` |
| Strict graph data and lesson paths | `packages/mdx-semantics/src/knowledge-graph.ts`; `mdx-scorm/docs/knowledge-graph-authoring.md` |
| ChoiceCloze delimiter priority and answer forms | `mdx-scorm/src/components/ChoiceClozeBlock.tsx`; shared export semantics must agree |
| Matching duplicate candidate display values | `mdx-scorm/src/components/Matching.tsx` |
| Zero question weight versus tracking | `mdx-scorm/User Manual.md`, common interaction attributes; page `weights` remain positive-only |
| Page configuration | `mdx-scorm/frontmatter写法规范.md`, `mdx-scorm/src/utils/frontmatter.ts`; defaults are different from required source fields |
| Translation | `mdx-scorm/src/components/Translate.tsx`, `translateScoring.ts`, `mdx-scorm/src/mdx/remarkTranslateBlock.ts`; the parser/service bridge has no language-direction parameter that proves universal grading support |
| Pop definitions | `mdx-scorm/src/mdx/remarkPop.ts`; definitions are collected out of visible flow, so unreferenced definitions do not preserve learner-visible notes |
| Style classes | `mdx-scorm/src/mdx/remarkStyleBlock.ts`, `mdx-scorm/src/components/StyleBlock.tsx`; `class` and `className` are forwarded |
| Wide content and font inheritance | `mdx-scorm/src/components/WideContent.tsx`, shared Markdown styles |
| Font availability | `mdx-scorm/src/styles/global/00-optional-wenkai.css`; optional web font support is not proof of PDF font embedding |
| Image viewer | `mdx-scorm/src/components/CourseImageViewer.tsx`; interactive ancestors and the opt-out attribute matter |
| Catalog score-weight visibility | `mdx-scorm/src/utils/catalogConfigMd.ts`; verify effective inheritance at the target course |
| HTML App envelope / runtime | `packages/mdx-semantics/src/html-app.ts`, `mdx-scorm/src/htmlApp/runtime.ts`, `media.ts`; trusted author code, not a JavaScript sandbox |
| Discussion/debate directive fields | `mdx-scorm/src/mdx/remarkDiscussionBlock.ts`; `[empty]`, presets and labels are directive features |

## Keep three kinds of rules distinct

1. **Engine constraints:** marker grammar, allowed fields, valid references, scoring semantics, token/response limits.
2. **Authoring defaults:** no redundant frontmatter, one answer per line, preferred translation/short-answer routes, card reuse, supported canonical spellings.
3. **Integration protocols:** hosted chat/generate/review/repair envelopes and metadata, activated only by a trusted matching host.

An authoring default must not be described as a parser prohibition. Valid old content and explicit user choices survive unrelated edits. Exact-match answer strings and text-edit originals are not typography targets.

## Validation layers

- The bundled Python checker reads files and reports targeted errors plus convention warnings. It masks code examples and HTML Apps and protects literal text-exercise content. It does not implement all directive syntax, tokenization, graph cycles, classification matrices, HTML safety, scoring, or complete source coverage.
- Shared semantic parsers can validate new-type example models independently of a browser. That is stronger than a regex check, but it does not prove UI behavior or deployed service availability.
- Browser preview, compiled/runtime modes, HTML packages, and student/teacher Print projections are separate verification surfaces. State which were exercised. Do not infer PDF success from browser success, or cloud deployment from local source support.
- Resolve convention warnings against source and user intent. Exception flags record an existing decision; they are not a demand to ask the user again.
