# UI Design & Implementation Audit

**Date:** 2026-02-06
**Scope:** Frontend Codebase (HTML/CSS)
**Status:** Audit Complete

## 1. Design System Reverse Engineering

The current UI is built on a "patchwork" system where variables exist but are inconsistently applied or overridden by inline styles.

### Typography
| Element | Observed System Behavior | Deviation / Issues |
| :--- | :--- | :--- |
| **Headings** | Uses `Poppins` via `--font-headings`. Sizes use `clamp()` in CSS. | HTML frequently overrides sizes inline (e.g., `<h1 style="font-size: 3rem">`). |
| **Body** | Uses `Open Sans` via `--font-body`. | Inconsistent scaling. Paragraphs often have hardcoded `max-width: 700px` or inline sizes (`1.25rem`). |
| **Weights** | 400, 600, 800 loaded. | Usage is inconsistent. Some labels are `600`, others bolded via `<strong>` or inline `font-weight: 700`. |

### Spacing & Layout
| Element | Observed System Behavior | Deviation / Issues |
| :--- | :--- | :--- |
| **Grid System** | `.grid-3` is the primary layout engine (3-column). | Frequent inline overrides (e.g., `grid-template-columns: repeat(4, 1fr)`). |
| **Vertical Rhythm** | CSS defines `--padding-panel: 80px`. | HTML relies on missing utility classes (`mt-4`, `mb-8`) which are **NOT defined in CSS**, forcing developers to add inline `style="margin-top:..."`. |
| **Container** | `.main-wrapper` caps width at 1400px. | Padding varies between `0 40px` (desktop) and `0 24px` (mobile). |

### Colors
*   **Primary:** `#0b1a15` (Deep Dark Green) - Consistently used.
*   **Accent:** `#c4f135` (Lime Green) - Used for highlights and buttons.
*   **Secondary:** `#3e4e4a` (Muted Text) - Often overridden by inline hex codes or opaque white values in dark mode.

## 2. Visual Hierarchy Failures

The dominance of content is often confused due to styling conflicts:

*   **Ghost Utilities**: The HTML uses classes like `mt-8`, `mb-4`, `text-center`, `d-flex` which are partially or wholly missing from the stylesheet. This results in elements collapsing into each other unless inline styles are manually added.
*   **Competing Weights**: Section labels (`.label-text`) and Headings sometimes lack sufficient contrast in size or spacing to clearly delineate sections.
*   **Button Hierarchy**: Primary and Outline buttons often sit too close together without sufficient spacing (due to missing gap utilities in supposed flex containers).

## 3. Alignment & Spacing Breakdown

*   **Arbitrary Values**: Spacing is not tokenized. One section might use `80px`, another `60px` (inline), another `100px`.
*   **Grid Inconsistency**: While `.grid-3` is standard, content often breaks alignment because internal padding of cards (e.g., `padding: 40px` vs `padding: 20px`) varies across components.
*   **Text alignment**: Centered text layouts (`.page-header-text`) often sit above left-aligned grids without a clear visual anchor, creating a jagged reading path.

## 4. Responsiveness & Mobile Failures

*   **Desktop-First Architecture**: The HTML structure heavily favors desktop grids. Mobile is handled via aggressive `flex-direction: column` overrides rather than specific mobile-first grid definitions.
*   **Hidden Content**: Mobile navigation relies on a separate "Overlay" structure that duplicates links, raising maintenance risks (zombie menu items found and cleaned).
*   **Font Scaling**: While Headings use `clamp()`, body text often remains static (`1.1rem` or inline `1.25rem`), potentially feeling too large or too small on mobile without fluid typography.

## 5. Root Cause Analysis

**1. Missing Utility Layer**
The codebase relies on a utility-class methodology (Tailwind-style logical classes like `mt-4`, `d-flex`) but **fails to implement the CSS library** to support them. This forces every specific spacing requirement to be written as an inline style.

**2. Inline Style Dependency**
Over 40% of layout logic (margins, specific widths, font overrides) resides in HTML `style="..."` attributes. This makes the design system distinct from the actual implementation.

**3. Component Isolation**
Components (like the Product Card vs Gallery Item) look like they were designed in isolation, resulting in different padding/border-radius tokens being used (`--radius-lg` vs hardcoded `8px`).

## 6. Constraints for Future Fixes

*   **Global CSS File (`leba-design.css`)**: All styles must live here. No preprocessor (SASS/LESS) is currently configured.
*   **Batch HTML Updates**: Since components are not templated (no React/Vue/Partial includes), any system change requires a regex-based batch script (`standardize_layout.py`) to propagate across 50+ HTML files.
*   **GSAP Dependency**: Animations are tightly coupled to the DOM structure (`.reveal-panel`). Layout changes must preserve these class hooks.
