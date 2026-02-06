# Mobile UI Debug Signals

**Date:** 2026-02-06
**Scope:** Frontend Codebase (Raw Debug Dump)
**Status:** Signals Extracted

## 1. Spacing & Layout Red Flags

Patterns indicating conflicting or arbitrary spacing logic:

*   **Inline Padding/Margin Overrides**:
    *   `div.main-wrapper.grid-3.hero-content-grid`: `style="align-items: center;"` (index.html:173) - Inline alignment conflict.
    *   `div` inside hero: `style="grid-column: span 2; padding-right: 40px;"` (index.html:174) - Hardcoded padding.
    *   `p.mt-4.mb-8`: `style="max-width: 600px;"` (index.html:176) - Inline width constraint.
    *   `div` inside stats: `style="display: flex; gap: 32px; align-items: center;"` (index.html:184) - Hardcoded gap.
    *   `section.panel.reveal-panel`: `style="padding-top: 0;"` (index.html:209) - Inline padding override.
    *   `section.panel.reveal-panel` (Highlights): `style="margin-top: 80px;"` (index.html:254) - Arbitrary margin.

*   **CSS Variable Gaps**:
    *   `--padding-panel: 80px` defines vertical flow but is overridden by inline `margin-top: 80px` in HTML.
    *   `.d-flex` definition (CSS:600) forces `gap: 16px !important` on mobile, but `style="gap: 16px;"` exists inline in `index.html:180`.

## 2. Viewport & Overflow Signals

Elements potentially causing horizontal scroll or clipping:

*   **Full Width / Transformations**:
    *   `section` (Video): `style="width: 100%; height: 500px;"` inside `.main-wrapper`.
    *   `img` (Hero): `style="transform: rotate(-2deg);"` (index.html:199) - Potential overflow if close to edge.
    *   `img` (Texture): `style="width: 80%; right: -20px;"` (index.html:201) - Negative positioning explicitly pushes outside standard bounds.
    *   `.mobile-nav-overlay`: `width: 85%; max-width: 400px` (CSS:420) - Fixed width drawer logic.

## 3. Grid / Flex Misuse Indicators

Container configurations that may break on small screens:

*   **Grid Column Violations**:
    *   `div` (Hero): `style="grid-column: span 2;"` (index.html:174) - No mobile override visible in HTML; relies on CSS `.grid-3` override to `1fr`.
    *   `div.grid-3` (Highlights): `style="grid-template-columns: repeat(4, 1fr);"` (index.html:256) - **CRITICAL**: Inline style forces 4 columns. CSS mobile override targets `.grid-3` generic class, but inline style has higher specificity. This will likely break on mobile.

*   **Flex Wrapping Missing**:
    *   `div` (Stats): `style="display: flex; gap: 32px;"` (index.html:184) - `flex-wrap` is NOT specified.
    *   `div` (Connect Footer): `style="display: flex; gap: 16px; flex-wrap: wrap;"` (index.html:327) - Correctly wrapped.

## 4. Typography & Hierarchy Signals

Raw typography values extracted:

*   **Heading Sizes**:
    *   `h1`: `clamp(2.5rem, 5vw, 4.5rem)` (CSS:83) - Fluid.
    *   `h2`: `clamp(2rem, 4vw, 3rem)` (CSS:88) - Fluid.
    *   `h3`: `1.75rem` (CSS:93) - Fixed.
    *   Mobile Override `h1`: `2.5rem` (CSS:577).
    *   Mobile Override `h2`: `2rem` (CSS:583).

*   **Body Sizes**:
    *   `p`: `1.1rem` (CSS:98).
    *   Inline Override (Hero): `style="font-size: 1.25rem;"` (index.html:176).
    *   Inline Override (Intro): `style="font-size: 1.5rem;"` (index.html:211).
    *   Stats Number: `style="font-size: 3rem;"` (index.html:259).

## 5. Section Structure Patterns

Inconsistent wrapper usage detected:

1.  `section.panel.panel-hero-modern.reveal-panel` > `div.main-wrapper.grid-3.hero-content-grid`
2.  `section.panel.reveal-panel` (Intro) > `div.main-wrapper` (Text align center)
3.  `section.panel.reveal-panel` (#products) > `div.main-wrapper` > `.section-header-flex` > `.grid-3.product-grid`
4.  `section.panel.reveal-panel` (Highlights) > `div.main-wrapper` > `.grid-3` (Inline 4-col override)

*   **Canonical Pattern**: `section.panel` > `div.main-wrapper` is consistent.
*   **Deviation**: Internal grid logic varies wildly (Flex vs Grid vs Inline Grid).

## 6. Mobile-Specific CSS Gaps

*   **Missing Overrides**:
    *   `p` (Inline sizes `1.25rem`, `1.5rem`): No mobile media query resets these specific inline instances.
    *   `.stats-grid`: Defined in CSS (348) as 2-col, but HTML uses inline 4-col grid.
    *   `#video-modal`: Uses `width: 90%` (index.html:303), generally safe but inflexible.

*   **Utility Gaps**:
    *   HTML uses `.d-flex` (index.html:180). CSS defines `.d-flex` **ONLY** inside `@media (max-width: 900px)`. It is **undefined** for desktop in `leba-design.css`.
    *   HTML uses `.mb-8`, `.mt-4`, `.justify-content-between`, `.align-items-end`. **None** of these are defined in `leba-design.css`. They rely entirely on browser defaults or are effectively broken classes unless defined in a missing generic file.
