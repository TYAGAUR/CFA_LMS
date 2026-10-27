# P-07 UI/UX Specification & Design System

| Field | Value |
|---|---|
| Document ID | P-07 |
| Version | 0.1 — Draft |
| Owner | UX/UI designer |
| Last updated | 2026-10-23 |
| Related | Prototype (P-02), P-03 screen inventory, C-08 Accessibility |

## 1. Principles
1. **Always show the next step.** Every screen tells the student what to do next. A locked state explains exactly how to unlock.
2. **Calm focus.** Content first; motion only to confirm actions or show progress.
3. **Friendly expertise.** Keep the prototype's tone: plain English, Indian context (₹, local names), and a light touch of humour in "Funny use case" boxes.
4. **Mobile-first for students; desktop-first for staff.**
5. **Accessible by default.** WCAG 2.1 AA, keyboard-complete, reduced-motion respected.

## 2. Brand application (decision D-008)
- **Web UI:** the prototype design system below (Figtree, indigo/cyan palette).
- **Exported documents** (notes, revision sheets, QBank PDFs/DOCX): the BRD §9 style (navy/gold/teal, Bahnschrift, footer "Karan Singh, CFA").
- **Product name:** pending decision O-08. Logo and wordmark are placeholders until it is made.

## 3. Design tokens
Taken from the prototype's `:root`. In code they live in `frontend/src/styles/tokens.css` as CSS custom properties. Tailwind (if used) maps onto them.

### 3.1 Colour

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#F3F5FC` | `#0A0C22` | Page background |
| `--surface` | `#FFFFFF` | `#131637` | Cards, panels |
| `--ink` | `#101433` | `#EEF0FF` | Primary text |
| `--mut` | `#5A6285` | `#9CA4CC` | Secondary text |
| `--line` | `#DDE1EE` | `#262B5C` | Borders, dividers |
| `--brand` | `#211C84` | `#B9C4FF` | Brand text, active states |
| `--brand2` | `#2F2AA0` | `#8FA0FF` | Brand secondary |
| `--accent` | `#4A6CF7` | `#6B87FF` | Primary buttons, links, focus |
| `--cy` | `#6FD3E8` | (same) | Highlights, progress gradient, focus ring |
| `--coral` | `#F0876A` | (same) | "Review again", decorative |
| `--soft` | `#EAF8FC` | `#10294A` | Selected backgrounds, example boxes |
| `--panel` / `--panel-ink` | `#211C84` / `#FFF` | `#1B1F63` / `#FFF` | Dark panels, table headers, formula boxes |
| `--good` / `--goodbg` | `#1F8F55` / `#E4F5EC` | `#4CC98A` / `#0F2A20` | Success, done |
| `--bad` / `--badbg` | `#C0392B` / `#FCEBE8` | `#FF8577` / `#341614` | Errors, wrong answers, "watch out" |
| `--warn` / `--warnbg` | `#B7791F` / `#FFF4DC` | `#F2C062` / `#33270E` | Warnings, "funny use case" |
| `--lock` | `#E3E6F2` | `#1D2049` | Locked items |

All text/background pairs must reach a 4.5:1 contrast ratio (3:1 for large text and UI parts). Check `--mut` on `--bg` and `--warn` on `--warnbg` with a contrast tool before sign-off.

### 3.2 Typography
- **Family:** Figtree (self-hosted WOFF2, weights 300–800), falling back to `system-ui, -apple-system, "Segoe UI", sans-serif`. Load it with `next/font/local`, not base64 inlining as in the prototype.
- **Scale:** body 15px/1.5 · small 13px · label 12px uppercase +0.14em · h-md `clamp(22px, 2.6vw, 30px)` weight 300 · h-lg `clamp(30px, 4.6vw, 52px)` weight 300 with **bold emphasis** in `--brand`.
- **Numbers:** `font-variant-numeric: tabular-nums` for scores, timers and tables.

### 3.3 Spacing, radius, elevation
- **Spacing:** 4px base (4, 8, 10, 12, 14, 16, 18, 20, 22, 26, 34).
- **Radius:** cards 6px, pills/buttons 24px, avatars 50%.
- **Shadow:** `--shadow` (light `0 6px 24px rgba(33,28,132,.10)`).
- **Layout:** content max width 1240px, side gutter 16px.

### 3.4 Motion
- Fade-in views (0.45 s); progress bars ease `cubic-bezier(.2,.8,.2,1)` over ~1 s; confetti only on major achievements (Phase 5).
- Everything is disabled under `prefers-reduced-motion: reduce`.

## 4. Component inventory

| Component | Prototype reference | Notes |
|---|---|---|
| App header (logo, nav, XP chip, theme toggle, avatar menu) | `header.top` | The XP chip is hidden until Phase 5 |
| Announcement ticker | `.ticker` | Phase 5; pauses on hover/focus; must have a pause control (WCAG 2.2.2) |
| Button (primary, ghost, small, success) | `.btn` | Disabled state with `aria-disabled` |
| Pill / tag (difficulty, status) | `.pill` | Colour plus text, never colour alone |
| Card | `.card` | |
| Progress ring | `.ring` | `role="img"` with an aria-label such as "Equities 40% complete" |
| Meter bar | `.meter` | `role="progressbar"` with values |
| Subject tile | `.subj` | |
| Sub-tabs (subjects) | `.subtabs` | Scrolls horizontally on mobile |
| LM rail and module accordion | `.rail`, `.mod` | States: done, current, locked, open. Lock icon has a text alternative. |
| Content pane with tabs | `.pane`, `.ptabs` | ARIA tabs pattern |
| Notes blocks | `.notes`, `.box.ex/.wo/.fx/.fun` | Rendered from the JSON block schema (A-03) |
| Waterfall infographic | `.wf` | Needs a text equivalent |
| Video player | `.player` | Real player (Bunny/Video.js) with watermark overlay and chapter list (`.vlist`) |
| Quiz overlay | `.ov`, `.qbox`, `.opt` | Phase 2. Options are a radio group (fix from prototype); focus is trapped in the dialog; Escape asks for confirmation before discarding. |
| Result ring and review list | `.bigring`, `.rv` | Phase 2 |
| Chip filters, segmented control, range slider | `.chip`, `.seg` | Test builder |
| Flashcard flip | `.flip` | Phase 3; keyboard: Space flips, 1/2/3 rate |
| Toast | `.toast` | `role="status"` |
| Empty, loading (skeleton) and error states | — | New; required for every data view |
| Admin data table | — | New: sort, filter, paginate, bulk select, CSV export |
| Form controls and validation messages | — | New; inline errors linked with `aria-describedby` |

## 5. Information architecture

```
Student
├── Home (dashboard)
├── Learn
│   └── Subject → LM rail → [Notes | Videos | Resources | Revision* | Infographic]
├── Practice*        (custom tests, chapter/master quizzes, history)
├── Revise*          (flashcards, revision log)
├── Exam readiness*  (EOC, Premium Pack, mocks, analytics)
├── Contests*        (Phase 5)
├── Search · Bookmarks
└── Profile (devices, consents, my data)
Staff (/admin)
├── Users · Batches & enrolments
├── Catalogue (subjects/LMs/topics/LOS)
├── Resources · Notes studio* · QBank* · Review queue* · Flashcards*
├── Unlock rules · Mock rules*
├── Reports · Audit log · Data requests
└── Settings (super admin)
* later phase
```

## 6. Key screen specifications (Phase 1)

### S-05 Dashboard
- **Hero card:** "Continue where you left off" with the LM title, a progress meter and the primary button (BR-PRG-07).
- **Grid:** 10 subject tiles (ring + "x of n LMs").
- **Side column:** pending items, recent activity, exam countdown.
- **Mobile:** single column; the hero card is first.

### S-06 Subject view
- **Desktop:** the rail (340px, sticky) next to the pane. **Mobile:** the rail collapses into a "Chapters" drawer.
- **Locked LM:** the rail item can be tapped and shows its unmet conditions in the pane.
- **Pane footer bar** (as in the prototype `.pbar`): status text plus the main action ("Mark as learned", or "Take chapter quiz" from Phase 2).

### S-07 Video view
- 16:9 player, with the chapter list beside it on desktop and below it on mobile. Speed menu, captions, keyboard shortcuts (Space, ←/→ 10 s).
- The watermark moves position every 30 s, at 15% opacity.

### S-16 Unlock rule editor
- Subject picker → condition rows (type, parameters, operator, value) joined by ALL/ANY → plain-language preview → "Test with student" → save with a reason.

## 7. Responsive breakpoints
- **≤ 640px:** phone; single column; bottom navigation for Home, Learn, Practice, Revise, Profile.
- **641–980px:** tablet; rail as a drawer.
- **> 980px:** desktop two-column layouts (the prototype's breakpoint was 980px).

## 8. Accessibility checklist (summary; full audit in C-08)
- All interactive elements are native buttons or links with visible focus (`--cy` 3px ring).
- No information is conveyed by colour alone: lock, done and wrong states also have icons and text.
- Dialogs trap focus and return it on close; Escape behaviour is confirmed.
- Moving content (ticker, watermark) can be paused or is non-essential.
- Every interactive target is at least 24×24px.
- Forms have labels and error text; the timer has an `aria-live="polite"` region updated each minute, not every second.

## 9. Content and voice guidelines (UI copy)
- Use sentence case. Be direct: "Take chapter quiz", not "Click here to start your quiz".
- Locked messages say what to do: "Score at least 80% in the LM2 quiz to open LM3. Your best: 70%."
- Errors say what happened and what to do next. No blame, no codes in the main text (a reference ID can go in small print).
- Numbers: Indian digit grouping for ₹ (₹1,80,000). Dates as "3 Oct 2026". Times in IST.

## 10. Deliverables
- A Figma file (or equivalent) with the token library, components and all S-01–S-20 screens at mobile and desktop sizes.
- A clickable flow for WF-01, WF-04 and WF-05 for usability testing with 5 students and 2 staff.
