---
name: budget-flow-visualization
description: "Use this skill when a user asks Claudia or an agent to visualize, explain, compare, animate, or audit budgets across years, especially from .xlsx/.csv budget workbooks. Trigger for requests like budget flow chart, follow the money, reallocation view, year-over-year budget comparison, interactive HTML budget dashboard, Sankey budget map, or Monarch-style money flow. The expected deliverable is usually an interactive HTML artifact backed by extracted budget data."
---

# Budget Flow Visualization Skill

Use this when the user wants to understand how budget money moves across years, categories, groups, and line items. This skill captures the GPSA budget-map pattern built from `inbox/GPSA 2026_2027_Draft.xlsx`.

## Positive Example

Use `edgar/gpsa_budget_flow.html` as the positive reference for how a finished budget-flow artifact should look and work. It is the benchmark example for:

- polished pastel visual direction
- full-width header with no source-card clutter
- D3 Sankey flow with year, section, group, and line-item controls
- smooth no-snap year-over-year animation
- stable 2026-based line-item ordering
- upstream path highlighting on stream and node clicks
- hover tooltips with dollars plus percent of total funding
- scrollable Reallocation Signals cards with diverging bars and visible scrollbar
- portable single-file HTML with hard-coded extracted budget data

## Ownership

- Claudia routes implementation to Hephaestus.
- If a source workbook is involved, also use the `xlsx` skill for extraction and verification.
- Keep the output in `edgar/` unless the user names another destination.

## Source Intake

1. Find the source budget file, usually in `inbox/` when Edgar says "inbox".
2. Inspect workbook sheet names and the first rows before designing.
3. Extract both formula and cached-value views when possible.
4. Prefer concrete line-item rows and cached totals over broken workbook summary formulas.
5. Flag source limitations inside the artifact only when they matter, such as broken `#REF!` summary formulas.

## Data Model

Normalize each budget year into:

- `revenue`
- `expenses`
- `gap`
- `categories`: section, group, amount
- `items`: section, group, item, amount

For year-over-year changes, match line items with normalized keys:

- clean spelling only enough to match obvious variants
- remove `[Pilot]` and `Pilot`
- normalize known typos when matching, but preserve source wording where the display should reflect the workbook
- compare `oldValue`, `newValue`, and `delta`

## Preferred Interface

Build a standalone HTML file when portability matters. Hard-code extracted data into the HTML unless the user wants a live-data setup. Tell the user clearly that hard-coded data means the HTML can travel alone, but it is a snapshot and must be regenerated when the workbook changes.

Recommended layout:

- Full-width title header.
- No source-workbook card in the hero area.
- Controls: section filter, year toggle, group/line-item toggle, animate/replay change.
- Main Sankey-style flow chart on the left.
- Reallocation Signals panel on the right.
- Year-over-year ledger below.

For a GPSA-style artifact, the header pattern is:

`GPSA MONEY MAP - Created by Represenative Edgar Agunias 5/18/2026`

Only reuse that exact attribution when appropriate for Edgar/GPSA work.

## Visual Design

- Use a soft pastel palette with distinct section colors.
- Do not rely on one hue family.
- Use a characterful display font plus a clean body font.
- Avoid unnecessary source cards, explainer blocks, and redundant panels.
- Keep cards at 8px radius or less.
- Let the flow chart and right-side panel end at the same vertical point; internal scrolling belongs inside the right panel.

## Sankey Behavior

Use D3 plus `d3-sankey` for browser-native HTML.

Required interaction:

- Hover on a node or stream shows dollars plus percent of total expense funding.
- Click a stream to focus its whole upstream chain back to revenue.
- Click a node bar to focus that node's upstream chain.
- Example: clicking `Travel Grant Program` highlights `Travel Grant Program -> Appropriations -> Allocations -> GPSA Revenue`.
- Dim unrelated streams and nodes slightly.
- Click the same focused item or chart background to clear focus.

Line-item ordering:

- In line-item mode, rank right-side line items by 2026 proposed amount, largest to smallest.
- Use the same 2026-based ranking during compare animation so the animation stays stable and readable.

## Compare Animation

Animate from the old budget to the proposed/new budget.

Rules:

- Use `requestAnimationFrame` and an easing function for smooth updates.
- Animate stats, flow widths, and reallocation numbers together.
- Avoid the final-frame snap by keeping a stable old/new union of rows during compare mode.
- Keep disappearing or new-only rows in the Sankey with a tiny ghost value, for example `1`, so D3 does not remove and repack nodes at the end.
- Freeze node ordering during compare mode with a rank map based on 2026 proposed values.
- Give the animate/replay button a fixed minimum width so its label does not shift layout.

## Reallocation Signals

The right panel should show all changed line items in a scrollable list, not only the top handful.

Card behavior:

- Include item name, `New` badge when `oldValue === 0 && newValue > 0`, group name, old-to-current amount, delta, and a diverging mini bar.
- Bars are centered on a zero baseline.
- Positive changes grow right from center.
- Negative changes grow left from center.
- Use a square-root scale so one huge increase does not flatten smaller reallocations.
- Keep the scrollbar visible at all times so users notice the list is scrollable.
- Do not include a redundant mini-strip above the cards if the cards already show the same signals.
- Do not include an animation-progress story block; it distracts from the money movement.

## Verification Checklist

Before handing off:

1. Run a JavaScript syntax check on the embedded script.
2. Open or reload the HTML in a browser if the environment allows it.
3. Confirm the chart renders nonblank.
4. Test year toggle, group/line-item toggle, animate/replay, hover tooltip, stream click, node click, and background clear.
5. Check that compare animation does not snap at the end.
6. Check line-item mode orders right-side nodes by the proposed/new-year amount.
7. Check the Reallocation Signals panel scrolls internally and stops before the ledger.
8. Check no important text runs out of cards or off the page.

## Handoff

Report:

- source file used
- output HTML path
- whether data is hard-coded or dynamic
- key source limitations
- verification performed

Update Hephaestus `TASK_LOG.md` for major budget visualization builds.
