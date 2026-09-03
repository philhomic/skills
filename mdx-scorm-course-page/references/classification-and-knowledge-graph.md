# `classification` and `knowledgeGraph` authoring

Use this reference only when generating either of these directives. It captures the current `mdx-scorm` author contract: write the smallest valid source form, preserve supplied learning data, and let the runtime provide interaction controls and visual behavior.

Before authoring, inspect the target repo's current `User Manual.md` and, when available, the actual course page inventory. Preview diagnostics are intentionally tolerant; do not treat preview recovery as permission to write an invalid source contract.

## `classification`: learner categorization

Choose `classification` when the source asks learners to sort a defined candidate set into one or more named categories. It is not a static taxonomy or a free-response prompt.

- Write the directive name exactly as `classification`. It has no aliases.
- Put the instruction or question in ordinary page Markdown immediately before or after the directive. Do not add a `[stem]` section inside it.
- A classification needs one or more `:::target` blocks. Each target needs `[title]` and `[items]` on their own lines.
- Each non-empty ordinary line under `[items]` is one candidate. Use `:::item` only when a candidate needs multiple lines or rich Markdown.
- An item that belongs to more than one target must be repeated with exactly the same source Markdown in every relevant `[items]` section. Do not vary its wording or inline formatting; that makes it a different candidate.
- `target` and `item` are internal structural directives. Do not use either outside `classification`, and do not add other structural directives inside a classification.
- A `styleBlock` may wrap one target to change that target's presentation. It must be a direct child of `classification`, contain exactly one target, and contain no surrounding prose or additional targets.

Use this form for the supplied two-category example:

```mdx
Ordne jedes Beispiel einer oder mehreren Kategorien zu.

:::classification
:::target
[title]
### Schwache KI

[items]
medizinische Diagnostik
Gesichtserkennung
Wettervorhersage
Sprachassistenten und Chatbots
Bilderkennung
personalisierte Empfehlung
eigenständige Entwicklung komplexer Softwaresysteme
:::

:::target
[title]
### Starke KI

[items]
Haus- und Pflegeroboter
autonomes Fahren in allen Verkehrssituationen
selbstständige wissenschaftliche Forschung und Faktenprüfung
umfassende kontextbezogene Beratung in unterschiedlichen Lebensbereichen
:::
:::
```

### Attributes and behavior

- `weight` sets the base weight. `weightDistribution` accepts `shared` or `average` when the page needs normal shared-weight behavior.
- `scorm=false` makes the task practice-only. Otherwise it participates in the page's SCORM submit and scoring flow.
- Feedback comes from page frontmatter (`feedback` / `feedbackMode`), not a classification attribute. Use `feedback: instant` only when the lesson needs relation-by-relation feedback during placement.
- Do not author `open`, `share`, `shareComments`, `useManualMarking`, or a classification-specific `feedbackMode`; they are not supported. `isshared` is a legacy marker and does not enable a sharing or comments UI, so do not add it for new content.

Learners can drag an item, or select an item and choose a target; the latter also supports touch devices. An item may correctly belong to multiple targets. Scoring compares every target-item relation, so both an extra placement and an omitted required placement reduce the score. A tracked first submission is preserved; subsequent moves are only local feedback exploration.

### Classification preflight

1. Confirm every target has a non-empty title and at least one item.
2. Confirm the source, not the author, supplies every correct target-item relation.
3. Confirm each intended shared item is source-identical in each target.
4. Keep the target-by-item matrix within the SCORM learner-response limit; use parser/build diagnostics rather than guessing a safe size for a very large task.
5. Set page numbering and `scorm` deliberately, because this is an interaction.

## `knowledgeGraph`: strict display-only course map

Choose `knowledgeGraph` only for an explicit concept graph whose nodes, relationships, and optional course links can be verified. It is a display component: the runtime provides search, node detail, zoom, fit, reset, contains-branch expand/collapse, and browser-native fullscreen. Do not add SCORM weight, answers, or interaction sections to it.

### Directive envelope

- Write the source directive name exactly as `knowledgeGraph`; its capital `G` is required.
- Its body must contain exactly one fenced code block labelled `json`. The content is strict JSON: no comments, trailing commas, single-quoted strings, or unquoted keys. Do not place prose, JSX, another directive, or a second code block beside it.
- The only attributes are `layout`, `direction`, `height`, `title`, and `density`. Unknown attributes fail validation.
- Defaults: `layout="dagre"`, `direction="LR"`, `height=460`, `title="知识图谱"`, and `density="auto"`.
- Layouts are `dagre`, `force`, `radial`, and `circular`. Directions are `LR`, `RL`, `TB`, and `BT`, and only affect `dagre`; specifying one for another layout produces a warning.
- `height` is a finite positive number in CSS pixels (not `460px`); values below `320` warn about readability. Density is `auto`, `compact`, `normal`, or `comfortable`. `title=""` hides the visible title but retains an accessible name.

The course-wide reference at `D:\Projects\welearn-ninja\mdx-scorm-pages\pages\00_course_info\01_course_info.mdx` demonstrates a valid default-attribute graph with categories, descriptions, `contains` hierarchy, a `related` edge, and exact `.mdx` lesson links.

Start with a minimal graph and add only source-supported data:

````mdx
:::knowledgeGraph{layout="dagre" direction="LR" height=460 title="课程知识图谱" density="auto"}
```json
{
  "categories": [
    { "id": "concept", "label": "核心概念" }
  ],
  "nodes": [
    { "id": "overview", "label": "课程总览", "category": "concept" },
    { "id": "topic-a", "label": "主题 A", "description": "用来源材料支持的简短说明。", "category": "concept" }
  ],
  "edges": [
    { "source": "overview", "target": "topic-a", "relation": "contains" }
  ]
}
```
:::
````

To place a graph inside a rich Markdown container such as `collapse`, use an outer fence with more colons than the inner graph fence.

### JSON contract

The root may contain only `nodes`, optional `edges`, and optional `categories`.

- `nodes` is required and must leave at least one valid node. Every node has a unique, non-empty `id` and non-empty `label`; optional strings are `description`, `lesson`, and `category`.
- `categories` contains unique, non-empty `{ "id", "label" }` objects. A node `category` must match a declared category id exactly.
- `edges` contains `{ "source", "target", "relation", "label"? }`. Both ends must name different, existing nodes. `relation` is exactly `contains`, `prerequisite`, or `related`.
- Do not add undocumented fields to the root, nodes, categories, or edges.
- No duplicate relation is allowed. `related` is undirected for duplicate detection. A node may have at most one `contains` parent; `contains`, `prerequisite`, and their combined directed graph must each be acyclic. `related` cycles, disconnected subgraphs, and multiple roots are allowed.

`lesson`, when supplied, is a navigation target relative to the course `pages/` directory, for example `01_grammar/02_past_tense.mdx`. It must use `/`, include `.mdx`, have no leading slash, `./`, `../`, backslash, URL scheme, query, hash, or `scoid`, and match a real final page path with exact casing. It may point to a real `issco: false` page. Before finalizing a new unit, compare each `lesson` value with the final page inventory, including pages created in the same request; omit a link whose target cannot be verified.

### Authoring boundaries and preflight

- Select a layout for the learning structure: `dagre` for directed hierarchy/sequence, `force` for associative networks, `radial` for root-centered structure, and `circular` for a stable author-order overview. Learners do not choose a different layout.
- Do not author `src`, external data, `version`, groups/combos, custom colors/themes, legend/minimap/toolbars, node shapes, animations, edge-label policies, fullscreen alternatives, or a learner layout switcher. Those are outside the source contract or runtime-managed.
- Use the same five-attribute-plus-JSON source shape for runtime, Cloud Studio preview/editing, and Print/PDF. Print/PDF turns a valid graph into static paginated content, so do not make essential teaching instructions depend on Canvas-only controls.
- Validate strict JSON, the five attributes, unique IDs, endpoints, duplicate edges, relation cycles, categories, and exact `lesson` paths before calling the graph done. A preview can render remaining valid data with diagnostics, but the strict course build rejects schema, reference, path, and cycle errors.
- Check the rendered graph on the intended viewport/LMS: width fills its container, `height` controls only in-page height, and browser/LMS iframe permissions may deny native fullscreen. Do not promise a CSS fullscreen fallback.
