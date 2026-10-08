# Course stylesheet authoring

For a CSS-only request, return one complete `css` code block without MDX, HTML, or `<style>` tags. Treat this as an appearance task: preserve the runtime layout instead of generating layout resets or repair overrides.

Use supplied verified DOM selectors, the requested preset, and explicit additional requirements; do not invent classes or require content changes. Additional user requirements take precedence over a generic preset. A CSS block is copyable stylesheet code, not a full MDX candidate. Do not append explanations or create a file unless the user requested that delivery form.

Keep supplied mandatory layout rules intact when they are part of the user's explicit stylesheet contract; do not counteract them with other rules. Encoded SVG decoration must not replace component icons or intercept clicks. Omit empty placeholder rules. Ordinary appearance requests follow the geometry-preservation constraints below.

- `.mdx-content` is shared by `.scorm-shell__body.mdx-content` (outer scroll container), `.scorm-shell__content.mdx-content` (inner content area), and nested markdown. Do not treat the outermost match as an ordinary box to decorate. Do not add or reset container padding, margins, dimensions, max-width, display, positioning, overflow, flex/grid, transform, zoom, or box-sizing. Typography tokens and text colors may target markdown wrappers.
- Preserve the shell, SplitPane sections/divider, columns, wide content, carousel, collapse, popup, and interaction geometry, scrolling, and dragging. This includes layout variables, shorthand declarations, and media queries. Current runtime content uses `max-width: 1080px; margin: 0 auto; padding: 12px 20px 0`; fullBleed compensates with `width: calc(100% + 40px); margin-left: -20px`; sections have `padding: 16px`. These explain the contract; do not copy them into generated overrides. Do not change authored `fullBleed`, `fitViewport`, or split ratios to implement a theme.
- Use existing color tokens for page appearance, without adding decorative boxes to shell or nested markdown wrappers. Keep heading, quote, and teaching-callout decoration local. Preserve `--mdx-font-size` inheritance and proportional heading sizes so font controls remain effective.
- Interaction card outer backgrounds and their existing `::after` overlay must be transparent. `--card-highlight-bg` paints an overlay across the whole card, not an ordinary base background: never assign it an opaque color or gradient. Do not add card overlays, lower whole-card opacity, or repair occlusion with z-index.
- Scope transparency to `.interaction-card.card` and its known `::after`. Do not globally clear `--card-bg`, make every `.card` or descendant transparent, or hide all pseudo-elements. Teaching callouts may have backgrounds. Inputs, options, dropdown panels, drag targets, and feedback need their own readable surfaces and paired foreground/background colors; dropdowns must not show underlying text through them. Preserve selection, success/error, disabled, drag, and keyboard-focus indicators.
- Limit every custom rule, including media queries and card transparency, to the requested theme. Default light uses `html:root:not([data-theme])`, not `[data-theme='light']`; for explicitly requested light/dark styling use `html:root:is(:not([data-theme]), [data-theme='dark'])` for shared rules and separate palettes. Do not use `!important` or override runtime geometry through specificity.

Include these appearance rules under the selected theme scope (default-only example):

```css
html:root:not([data-theme]) .interaction-card.card {
  background: transparent;
}
html:root:not([data-theme]) .interaction-card.card::after {
  background: transparent;
}
```

Before returning CSS, check that no selector or variable changes shell/layout geometry and no background shorthand or more-specific rule cancels card transparency. For browser verification when available, check narrow vertical and wide horizontal splits, centered desktop content, ChoiceCloze dropdowns, theme switching, and font controls. Distinguish static review from actual browser evidence.
