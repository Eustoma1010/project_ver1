---
target: /data/worktime/project_ver1/frontend/templates/products/trace_journey.html
total_score: 37
p0_count: 0
p1_count: 0
timestamp: 2026-07-06T01-38-39Z
slug: frontend-templates-products-trace-journey-html
---
# Design Critique: Dynamic Trace Journey Page
Target: `/data/worktime/project_ver1/frontend/templates/products/trace_journey.html`

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 4 | Real-time Blockchain sync status is explicitly communicated. |
| 2 | Match System / Real World | 4 | Clear Vietnamese language and organic symbols (leaf, shield). |
| 3 | User Control and Freedom | 3 | Standard browser back navigation works; missing back-to-home shortcut. |
| 4 | Consistency and Standards | 4 | Perfectly aligned with Verdant design tokens and font pairings. |
| 5 | Error Prevention | 4 | Defensive coding for dates and template rendering logic. |
| 6 | Recognition Rather Than Recall | 4 | Information is divided into clean chunked groups. |
| 7 | Flexibility and Efficiency | 3 | Copy shortcuts are provided, but no keyboard accelerators. |
| 8 | Aesthetic and Minimalist Design | 4 | Striking visuals tailored by product category; no AI design slop. |
| 9 | Error Recovery | 4 | Handles blockchain RPC node exceptions gracefully. |
| 10 | Help and Documentation | 3 | Explains blockchain validation concepts directly in context. |
| **Total** | | **37/40** | **Excellent** |

## Anti-Patterns Verdict

* **LLM Assessment**: Excellent rating. The page looks human-designed, custom-tailored for each category (Green, Blue, Brown/Gold) with dedicated background highlights. No text gradients, glassmorphism defaults, or unmeaningful section mark eyebrows are present.
* **Deterministic scan**: The automated detector found 3 warnings/advisories, all of which are false positives:
  1. `broken-image`: Dynamic QR code image lacking static `src`.
  2. `design-system-color`: Scrollbar styling uses rgba(0, 0, 0, 0.1).
  3. `single-font`: Typographic analysis missed the custom serif Tailwind declaration.
* **Visual overlays**: Overlays unavailable (headless run).

## Overall Impression
The dynamic tracing page is exceptionally beautiful, modern, and trustworthy. The category-based color theme gives it an artisanal, high-end feel.

## What's Working
- Splendid category-based dynamic color scheme which gives product-specific visual identity.
- Clean typography hierarchy using Playfair Display for headings and Be Vietnam Pro for body copy.
- Clear structural division between product details, certificates, and supply chain timeline.

## Priority Issues

- **[P2] Missing dynamic home link in header**:
  - *Why it matters*: Users scanning QR codes on physical goods might want to navigate back to the main e-commerce storefront to continue shopping, rather than being stuck on a single-page silo.
  - *Fix*: Add a clear back-to-home logo/navigation button in the header.
  - *Suggested command*: `/impeccable layout`
- **[P3] Minor layout shift during dynamic QR image loading**:
  - *Why it matters*: The `<img>` tag has no dimensions, which can cause a small page jump when the API generates the QR code URL.
  - *Fix*: Provide a default loading spinner placeholder or set static aspect-ratio styles on the wrapper.
  - *Suggested command*: `/impeccable polish`

## Persona Red Flags

* **Jordan (First-Timer)**: Technical cryptographic terms ("Sổ cái", "TxHash") might be slightly confusing without a quick tooltip or simpler translation.
* **Casey (Distracted Mobile User)**: Casey is holding their phone with one hand while shopping. Small copy buttons and explorer link targets could be slightly padded for better thumb touch targets (minimum 44x44pt).

## Minor Observations
- Active milestone step is highlighted with a pulse glow ring, which is an excellent micro-interaction.

## Questions to Consider
- Can we add a direct "Mua lại sản phẩm này" (Reorder this product) CTA at the bottom of the page?
- Should we add a button to download the PDF certificate for quality audits?
