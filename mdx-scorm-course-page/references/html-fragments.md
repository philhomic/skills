# HTML element code

This reference applies to static HTML fragments. For an explicitly requested executable HTML App, use `html-apps.md` instead. For a card in an MDX page, prefer `styleBlock{class="card"}`; the inline HTML styling below is only for an explicit HTML-only request.

Use only when the user explicitly asks for static course HTML code. By default return one `html` fenced code block, containing the requested elements and nothing else. Do not substitute a file, download address, full document, or rendered preview for that code. An explicit file-delivery request takes precedence; the content remains a safe fragment unless a different scope was requested. Do not run the MDX page template or MDX-only output validator on a standalone HTML response.

## Format and safety

- Explicitly self-close every permitted HTML void element using a space followed by `/>`: write `<img src="known-image.png" alt="Description" />`, `<br />`, `<hr />`, `<source src="known-audio.mp3" type="audio/mpeg" />`, and `<track ... />`. Never generate bare `<img ...>`, `<br>`, or other unclosed void tags, and do not use `</img>` or `</br>`. This is the required course authoring convention even where ordinary HTML permits omitting the slash. Keep non-void elements paired, such as `<p>...</p>` and `<div>...</div>`. Apply the same convention to HTML embedded in generated MDX. Existing tag restrictions still apply.
- Use normal HTML with quoted attributes and `style="property: value;"`, not JSX `style={{...}}` or `className`.
- Keep each opening tag and all its attributes on one line. Separate elements with ordinary newlines if helpful, but no blank lines between tags. Avoid four-space indentation when embedding raw HTML into Markdown.
- Output elements only: no doctype, `html`, `head`, `body`, `style`, stylesheet links, or imports.
- Do not emit `script`, `iframe`, `object`, `embed`, `meta`, `base`, event attributes such as `onclick`/`onerror`, `srcdoc`, JavaScript, or executable URL schemes. Do not disguise scripts in CSS or URLs. Use ordinary HTTPS links or known package-relative media paths; do not invent asset paths.
- Escape text and quoted attribute values correctly. Treat supplied prose as text, not executable markup.
- Use semantic elements such as `section`, `div`, `p`, headings, lists, tables, `span`, `strong`, `em`, `a`, and `img`. Provide descriptive link text and image alt text. Do not create nonfunctional buttons or imitate scored interactions with HTML; use the supported directives when the user requests actual course interaction.
- Inside a pure HTML fragment, use HTML consistently rather than Markdown headings, emphasis, or MDX directives.
- Runtime sanitization is a backstop, not proof that arbitrary HTML/CSS is safe. Keep styles local; avoid global selectors, fixed overlays, and unnecessary remote resources.

## Verified theme variables

Maintenance source: mdx-scorm `src/styles/global/01-foundation.css` and `02-markdown-content.css`, inspected 2026-09-07. These names are bundled for cloud use; repository access is not required.

| Purpose | Existing variables | CSS usage |
| --- | --- | --- |
| Body typography | `--mdx-font-size`, `--mdx-line-height`, `--mdx-letter-spacing` | `font-size`, `line-height`, `letter-spacing` |
| Font families | `--font-body`, `--font-heading`, `--font-ui`, `--font-mono` | `font-family` |
| Text hierarchy | `--text-1`, `--text-strong`, `--text-muted`, `--text-subtle`, `--text-quiet`, `--text-inverse` | `color`; choose for the actual background |
| Card surface | `--card-bg`, `--card-border`, `--card-radius`, `--card-padding`, `--card-shadow` | `background`, `border`, `border-radius`, `padding`, `box-shadow` |
| Shared surfaces and accents | `--surface-1`, `--surface-2`, `--accent-1`, `--accent-2` | Surface background or restrained accent color |
| Notes and quotations | `--quote-bg`, `--quote-text` | `background`, `color` |
| Borders and depth | `--border`, `--border-soft`, `--border-strong`, `--radius`, `--shadow` | `border`, `border-radius`, `box-shadow` |
| Button appearance | `--button-bg`, `--button-text`, `--button-border`, `--button-radius`, `--button-padding`, `--button-shadow` | Use only for meaningful supported controls or links |
| Option appearance | `--choice-option-bg`, `--choice-option-text`, `--choice-option-border`, `--choice-option-radius`, `--choice-option-shadow` | Reference styling only; HTML does not implement choice scoring |

- Prefer inherited typography for normal content; when explicit body sizing is needed, use `font-size: var(--mdx-font-size)`, not an invented `--font-size` token. Avoid fixed pixel sizes that defeat course font controls.
- `--card-bg` may be a gradient: use `background: var(--card-bg)`, not `background-color`.
- A border color alone does not draw a border. Use `border: 1px solid var(--card-border)` when a border is intended.
- Prefer semantic card/quote/text tokens before literals. Use literal spacing or layout values where no suitable token exists; do not invent token names.
- These variables are supplied by the course theme. If the user explicitly intends another host, add appropriate `var(--token, fallback)` values rather than assuming that host defines them. Static Print/PDF has its own theme projection; do not promise identical rendering without checking that output.

## Example

```html
<section style="background: var(--card-bg); color: var(--text-1); border: 1px solid var(--card-border); border-radius: var(--card-radius); padding: var(--card-padding); font-family: var(--font-body); font-size: var(--mdx-font-size); line-height: var(--mdx-line-height);">
<h2 style="color: var(--text-strong); margin: 0 0 0.6em; font-family: var(--font-heading); font-size: 1.3em;">Reading reminder</h2>
<p style="margin: 0;">Read the passage and identify its main idea.</p>
</section>
```

Before returning, check the actual fragment: element-only output, explicit ` />` on every permitted void element, matching end tags on non-void elements, one-line opening tags, no blank lines, quoted inline styles, no executable content, and existing variables used with compatible properties. For a full MDX candidate containing raw HTML, leave necessary separation around the HTML block and keep directives outside it; the no-blank-lines rule concerns the HTML fragment itself.
