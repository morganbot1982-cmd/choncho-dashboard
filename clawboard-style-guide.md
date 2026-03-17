# ClawBoard Design System — Style Guide

A complete reference for replicating the ClawBoard visual style in any project. Built with Tailwind CSS 4 + CSS custom properties. The aesthetic is warm, tactile, and layered — like paper and glass on a natural desk.

> **Screenshot reference:** `/Users/userclaw/.openclaw/media/browser/da5219ec-7114-4430-9cb4-4be404326c5b.png`

---

## 1. Colour Palette

### CSS Custom Properties

```css
:root {
  --background: #e9e1d3;          /* Warm parchment base */
  --foreground: #1b1917;          /* Near-black text */
  --panel: rgba(255, 252, 247, 0.74);       /* Frosted glass panel */
  --panel-strong: rgba(255, 252, 247, 0.88); /* More opaque panel */
  --line: rgba(38, 29, 21, 0.1);  /* Subtle warm dividers */
  --muted: #6d655b;               /* Secondary text */
  --accent: #115f58;              /* Deep teal — primary action colour */
  --accent-soft: rgba(17, 95, 88, 0.12);    /* Teal tint for backgrounds */
  --accent-strong: #0f3f3b;      /* Darker teal for gradients */
  --charcoal: #1d2221;           /* Dark panels / chat background */
  --charcoal-soft: #2a3230;      /* Slightly lighter charcoal */
  --sand: #f5ecdd;               /* Tag backgrounds, warm highlights */
  --clay: #b97447;               /* Warm accent (dots, highlights) */
  --display: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
  --body: "Avenir Next", "Segoe UI", "Helvetica Neue", sans-serif;
}
```

### Colour Usage

| Use | Value | Notes |
|-----|-------|-------|
| Page background | `#e9e1d3` | Warm parchment with radial gradient overlays |
| Panel backgrounds | `rgba(255, 252, 247, 0.74)` | Semi-transparent frosted glass |
| Primary text | `#1b1917` / `zinc-950` | Near-black |
| Secondary text | `zinc-500` / `zinc-600` | For meta, labels, timestamps |
| Muted text | `#6d655b` | For less important info |
| Primary action (buttons, active states) | `#115f58` → `#0f3f3b` gradient | Deep teal |
| Warm accent | `#b97447` | Dots, ambient orbs, highlights |
| Tag backgrounds | `#f5ecdd` (sand) | Warm cream |
| Dark panels (chat, workspace) | `#1d2221` → `#1c2221` | Charcoal gradient |
| Error/warning | `amber-50`, `amber-200`, `amber-900` | Warm amber, not red |
| Success | `emerald-50`, `emerald-700` | For completed states |
| Selection highlight | `rgba(15, 118, 110, 0.18)` | Teal tint |

---

## 2. Typography

### Font Stacks

```css
/* Display / headings */
font-family: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
letter-spacing: -0.04em;

/* Body / UI */
font-family: "Avenir Next", "Segoe UI", "Helvetica Neue", sans-serif;
```

### Scale

| Element | Size | Weight | Tracking | Class |
|---------|------|--------|----------|-------|
| Hero title | `2.2rem` (md) / `1.85rem` | Normal | `-0.04em` | `display-face text-[1.85rem] md:text-[2.2rem]` |
| Section title (e.g. "Project flow") | `1.8rem` | Normal | `-0.04em` | `display-face text-[1.8rem]` |
| Stat numbers | `2rem` | Normal | `-0.04em` | `display-face text-[2rem]` |
| Card title | `15px` | Semibold (600) | `tight` | `text-[15px] font-semibold tracking-tight` |
| Body text | `14px` (`text-sm`) | Normal | Normal | `text-sm` |
| Small body / descriptions | `13px` | Normal | Normal | `text-[13px] leading-relaxed` |
| Meta labels | `11px` | Normal | `0.14em–0.18em` | `text-[11px] uppercase tracking-[0.14em]` |
| Section labels | `10px` | Normal | `0.18em–0.22em` | `text-[10px] uppercase tracking-[0.22em]` |
| Tag text | `10px` | Normal | `0.16em` | `text-[10px] uppercase tracking-[0.16em]` |
| Tiny labels | `9px` | Normal | `0.18em` | `text-[9px] uppercase tracking-[0.18em]` |

### Key Rules

- **Display headings** use the serif stack (`display-face` class) with tight negative tracking
- **All meta/labels** are uppercase with wide letter-spacing (0.14em–0.22em)
- Text rendering: `optimizeLegibility` + `-webkit-font-smoothing: antialiased`
- Body text colour: `zinc-900` on light, `white/88` on dark

---

## 3. Panels & Cards

### Panel (main container)

```html
<section class="panel-sheen relative rounded-[1.55rem] border border-black/6 
  bg-[rgba(255,252,247,0.62)] p-3 shadow-[0_30px_50px_-34px_rgba(0,0,0,0.18)] 
  backdrop-blur-xl md:p-4">
```

**Key properties:**
- Border radius: `1.55rem` (large panels), `1.2rem` (headers), `1.3rem` (workspace)
- Border: `border-black/6` (very subtle warm border)
- Background: Semi-transparent warm white with `backdrop-blur-xl`
- Shadow: Long, soft, offset downward. Pattern: `0_Xpx_Ypx_-Zpx_rgba(0,0,0,0.12–0.18)`
- Uses `panel-sheen` pseudo-element for glass highlight (see CSS Effects below)

### Card (project card, rail item)

```html
<article class="panel-sheen relative overflow-hidden rounded-[1.08rem] border 
  border-black/6 bg-white/82 p-3 shadow-[0_14px_20px_-24px_rgba(0,0,0,0.12)]">
```

**Properties:**
- Border radius: `1.08rem` (cards), `0.9rem` (smaller items like notes, checklist)
- Background: `bg-white/82` (standard) or `bg-[rgba(255,252,247,0.84)]` (active lane)
- Shadow: `0_14px_20px_-24px_rgba(0,0,0,0.12)` (light) to `0_16px_24px_-24px_rgba(0,0,0,0.2)` (active)

### Rail Item (sidebar items — memory, checklist, deliverables)

```html
<div class="rounded-[0.9rem] border border-zinc-200 bg-white/82 p-2.5 
  shadow-[0_10px_16px_-16px_rgba(0,0,0,0.08)]">
```

### Kanban Lane

```html
<div class="rounded-[1.25rem] border border-black/6 bg-gradient-to-b 
  from-white/82 to-white/54 p-2.5">
```

Active lane variant:
```html
<div class="rounded-[1.25rem] border border-black/10 bg-gradient-to-b 
  from-[#efe3d2] to-[#e6dfd4] p-2.5">
```

---

## 4. Shadows

The shadow system uses large spreads with negative offsets to create soft, realistic depth:

| Use | Shadow |
|-----|--------|
| Page-level panel | `0 30px 50px -34px rgba(0,0,0,0.18)` |
| Header | `0 20px 42px -30px rgba(0,0,0,0.18)` |
| Stat card (light) | `0 16px 24px -22px rgba(0,0,0,0.16)` |
| Stat card (dark/strong) | `0 24px 30px -24px rgba(0,0,0,0.42)` |
| Project card | `0 14px 20px -24px rgba(0,0,0,0.12)` |
| Active project card | `0 16px 24px -24px rgba(0,0,0,0.2)` |
| Dragging card | `0 24px 45px -28px rgba(0,0,0,0.24)` |
| Rail items | `0 10px 16px -16px rgba(0,0,0,0.08)` |
| Buttons (primary) | `0 18px 28px -24px rgba(0,0,0,0.45)` |
| Buttons (secondary) | `0 12px 24px -22px rgba(0,0,0,0.22)` |
| Filter chips (active) | `0 14px 22px -20px rgba(0,0,0,0.45)` |
| Filter chips (inactive) | `0 10px 20px -22px rgba(0,0,0,0.3)` |
| Pill/badge | `0 10px 28px -24px rgba(0,0,0,0.45)` |
| Chat workspace | `0 26px 44px -28px rgba(0,0,0,0.34)` |

**Pattern:** Always use negative spread to keep shadows tight. The offset-y is always positive (light from top). Opacity range 0.08–0.45.

---

## 5. Buttons

### Primary (dark gradient)

```html
<button class="inline-flex items-center gap-2 rounded-full border border-black/10 
  bg-[linear-gradient(135deg,#1f2a28,#103f3b)] px-3.5 py-2 text-sm text-white 
  shadow-[0_18px_28px_-24px_rgba(0,0,0,0.45)] transition hover:brightness-105 
  active:scale-[0.98]">
```

### Secondary (light)

```html
<button class="inline-flex items-center gap-2 rounded-full border border-black/10 
  bg-[rgba(255,252,247,0.84)] px-3.5 py-2 text-sm text-zinc-800 
  shadow-[0_12px_24px_-22px_rgba(0,0,0,0.22)] transition duration-200 
  hover:-translate-y-px hover:bg-white active:scale-[0.98]">
```

### Filter Chip (active)

```html
<button class="rounded-full border border-black/10 
  bg-[linear-gradient(135deg,#1f2a28,#103f3b)] px-3 py-1.5 text-sm text-white 
  shadow-[0_14px_22px_-20px_rgba(0,0,0,0.45)] transition hover:brightness-105">
```

### Filter Chip (inactive)

```html
<button class="rounded-full border border-black/8 bg-white/70 px-3 py-1.5 
  text-sm text-zinc-600 shadow-[0_10px_20px_-22px_rgba(0,0,0,0.3)] 
  transition hover:bg-white">
```

### Key Rules

- All buttons are `rounded-full` (pill shape)
- Primary uses `135deg` gradient from `#1f2a28` to `#103f3b`
- Hover: `brightness-105` or `-translate-y-px`
- Active: `scale-[0.98]`
- Never use solid background colours — always gradients or translucent

---

## 6. Tags & Badges

### Tag

```html
<span class="rounded-full border border-zinc-200 bg-[var(--sand)]/70 px-2 py-0.5 
  text-[10px] uppercase tracking-[0.16em] text-zinc-500">
  dashboard
</span>
```

### Priority Badge

```html
<!-- High/Critical -->
<span class="rounded-full bg-teal-50 px-2 py-0.5 text-[10px] uppercase 
  tracking-[0.18em] text-teal-800">high</span>

<!-- Low/Medium -->
<span class="rounded-full bg-zinc-200/70 px-2 py-0.5 text-[10px] uppercase 
  tracking-[0.18em] text-zinc-700">medium</span>
```

### Status Pill

```html
<div class="inline-flex items-center gap-2 rounded-full border border-black/8 
  bg-[rgba(255,252,247,0.72)] px-3.5 py-1.5 text-[11px] uppercase 
  tracking-[0.18em] text-zinc-600 shadow-[0_10px_28px_-24px_rgba(0,0,0,0.45)]">
  <span class="h-2 w-2 rounded-full bg-[var(--accent)]"></span>
  Ready to work
</div>
```

---

## 7. Dark Panels (Chat / Workspace)

Used for the chat interface and project workspace thread area:

```html
<div class="panel-sheen relative overflow-hidden rounded-[1.3rem] border border-black/6 
  bg-[linear-gradient(180deg,rgba(35,42,41,0.98)_0%,rgba(28,34,33,1)_100%)] p-3 
  text-white shadow-[0_26px_44px_-28px_rgba(0,0,0,0.34)] md:p-4">
```

### Chat Messages

**User message (light bubble):**
```html
<article class="ml-auto max-w-[88%] rounded-[1.05rem] 
  bg-[linear-gradient(180deg,#fffdf9,#f2e7d7)] px-3.5 py-3 text-sm text-zinc-950 
  shadow-[0_16px_24px_-22px_rgba(0,0,0,0.34)] md:max-w-[78%]">
```

**Assistant message (dark glass bubble):**
```html
<article class="max-w-[88%] rounded-[1.05rem] border border-white/12 
  bg-[linear-gradient(180deg,rgba(255,255,255,0.12),rgba(255,255,255,0.06))] 
  px-3.5 py-3 text-sm text-white/88 
  shadow-[0_14px_24px_-22px_rgba(0,0,0,0.28)] md:max-w-[78%]">
```

**System message (amber):**
```html
<article class="max-w-[88%] rounded-[1.05rem] border border-amber-300/18 
  bg-amber-200/10 px-3.5 py-3 text-sm text-amber-50 md:max-w-[78%]">
```

### Message Role Labels

```html
<!-- User -->
<span class="rounded-full border border-black/8 bg-black/5 px-2 py-0.5 
  text-[10px] uppercase tracking-[0.16em] text-zinc-600">You</span>

<!-- Assistant -->
<span class="rounded-full border border-white/10 bg-white/8 px-2 py-0.5 
  text-[10px] uppercase tracking-[0.16em] text-white/55">Task</span>

<!-- System -->
<span class="rounded-full border border-amber-200/20 bg-amber-50/10 px-2 py-0.5 
  text-[10px] uppercase tracking-[0.16em] text-amber-100/80">System</span>
```

---

## 8. Form Inputs

```html
<!-- Text input -->
<input class="w-full rounded-[0.9rem] border border-black/10 bg-white px-3 py-2.5 
  text-sm text-zinc-900 outline-none transition focus:border-teal-600" />

<!-- Search input -->
<input class="min-w-[220px] flex-1 rounded-full border border-black/8 bg-white/78 
  px-3.5 py-2 text-sm text-zinc-900 outline-none transition focus:border-teal-600" />

<!-- Textarea -->
<textarea class="min-h-[110px] w-full rounded-[0.9rem] border border-black/10 
  bg-white px-3 py-2.5 text-sm text-zinc-900 outline-none transition 
  focus:border-teal-600" />

<!-- Select -->
<select class="w-full rounded-[0.9rem] border border-black/10 bg-white px-3 py-2.5 
  text-sm text-zinc-900 outline-none transition focus:border-teal-600" />

<!-- Dark textarea (in chat panel) -->
<textarea class="min-h-[60px] w-full resize-y border-0 bg-transparent text-sm 
  text-white placeholder:text-white/35 focus:outline-none" />
```

**Key rules:**
- Border radius: `0.9rem` for standard inputs, `rounded-full` for search
- Focus: `border-teal-600` (the accent colour)
- Background: solid `bg-white` on light panels, `bg-transparent` on dark

---

## 9. CSS Effects

### Panel Sheen (glass highlight)

```css
.panel-sheen {
  position: relative;
  overflow: hidden;
}
.panel-sheen::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(135deg, rgba(255,255,255,0.42), transparent 34%),
    linear-gradient(180deg, transparent, rgba(255,255,255,0.14));
  opacity: 0.9;
}
```

### Ambient Orbs (coloured blurs)

```css
.ambient-orb {
  position: absolute;
  border-radius: 999px;
  filter: blur(24px);
  opacity: 0.6;
  pointer-events: none;
}
```

Usage:
```html
<!-- Teal orb (top-left) -->
<div class="ambient-orb left-[-4rem] top-[-3rem] h-32 w-32 bg-[rgba(17,95,88,0.18)]" />

<!-- Clay/warm orb (bottom-right) -->
<div class="ambient-orb bottom-[-5rem] right-[14%] h-40 w-40 bg-[rgba(185,116,71,0.14)]" />
```

### Panel Noise (subtle dot texture)

```css
.panel-noise::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.16;
  background-image: radial-gradient(rgba(255,255,255,0.88) 0.45px, transparent 0.45px);
  background-size: 8px 8px;
  mask-image: linear-gradient(to bottom, black, transparent 85%);
}
```

### Shell Grid (background grid pattern)

```css
.shell-grid {
  background-image:
    linear-gradient(to right, rgba(38,29,21,0.03) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(38,29,21,0.03) 1px, transparent 1px);
  background-size: 32px 32px;
}
```

### Body Background (layered radial gradients)

```css
body {
  background:
    radial-gradient(circle at top left, rgba(17,95,88,0.16), transparent 26%),
    radial-gradient(circle at 78% 10%, rgba(185,116,71,0.12), transparent 18%),
    radial-gradient(circle at bottom right, rgba(32,35,34,0.08), transparent 22%),
    linear-gradient(180deg, rgba(255,250,242,0.62), rgba(233,225,211,0)),
    var(--background);
}
```

---

## 10. Stat Cards (Header)

### Light variant

```html
<div class="rounded-[1rem] border border-black/6 bg-white/72 px-3.5 py-3 
  shadow-[0_16px_24px_-22px_rgba(0,0,0,0.16)]">
  <div class="flex items-center justify-between text-zinc-500">
    <span class="text-[10px] uppercase tracking-[0.18em]">Projects</span>
    <span class="rounded-full border border-current/10 p-1.5"><!-- icon --></span>
  </div>
  <div class="mt-3 display-face text-[2rem] text-zinc-950">4</div>
  <p class="mt-1 text-xs leading-relaxed text-zinc-500">Tracked across every lane</p>
</div>
```

### Dark/strong variant (highlighted stat)

```html
<div class="rounded-[1rem] border border-black/6 
  bg-[linear-gradient(145deg,#1f2a28,#102f2c)] px-3.5 py-3 text-white 
  shadow-[0_24px_30px_-24px_rgba(0,0,0,0.42)]">
  <div class="flex items-center justify-between text-white/50">
    <span class="text-[10px] uppercase tracking-[0.18em]">Active</span>
    <span class="rounded-full border border-current/10 p-1.5"><!-- icon --></span>
  </div>
  <div class="mt-3 display-face text-[2rem] text-white">2</div>
  <p class="mt-1 text-xs leading-relaxed text-white/66">Work currently being pushed</p>
</div>
```

---

## 11. Layout Patterns

### Page Structure

```
body (shell-grid background)
└── main (min-h-[100dvh] px-3 py-3 md:px-5 md:py-4)
    └── max-w-[1540px] mx-auto flex flex-col gap-3
        ├── header (panel-sheen panel-noise)
        ├── filter bar (flex flex-wrap gap-2)
        └── content (board / workspace)
```

### Board Grid

```html
<div class="grid gap-2 xl:grid-cols-3 2xl:grid-cols-6">
  <!-- 6 kanban lanes -->
</div>
```

### Workspace Layout (project page)

```html
<section class="grid gap-3 xl:grid-cols-[minmax(0,1.22fr)_360px]">
  <!-- Left: Chat panel (dark) -->
  <!-- Right: Sidebar rail (360px, sticky) -->
</section>
```

### Sidebar Rail

```html
<aside class="grid content-start gap-2.5 xl:sticky xl:top-4">
  <!-- Collapsible sections: memory, subtasks, artifacts, activity, status -->
</aside>
```

---

## 12. Border Radius Scale

| Use | Radius |
|-----|--------|
| Page-level panels | `1.55rem` |
| Header | `1.2rem` |
| Workspace container | `1.3rem` |
| Kanban lanes | `1.25rem` |
| Project cards | `1.08rem` |
| Chat bubbles | `1.05rem` |
| Stat cards | `1rem` |
| Rail items, inputs | `0.9rem` |
| Inner cards | `0.8rem` |
| Buttons, tags, pills | `rounded-full` (9999px) |

---

## 13. Spacing

- Page padding: `12px` (mobile) / `20px` (desktop)
- Panel padding: `12px` / `16px`
- Card padding: `12px` (p-3)
- Gap between sections: `12px` (gap-3)
- Gap between rail items: `10px` (gap-2.5)
- Gap within cards: `8px` (gap-2)

---

## 14. Icons

Uses **Phosphor Icons** (`@phosphor-icons/react`):
- Size 12–16px depending on context
- Weight: regular (default), `fill` for active/pinned states
- Commonly used: `Kanban`, `FolderOpen`, `GearSix`, `Target`, `ArrowRight`, `NotePencil`, `PaperPlaneTilt`, `CheckCircle`, `FileText`, `ClockCounterClockwise`, `PushPin`, `Trash`, `Sparkle`, `Plus`, `X`, `CaretDown`, `DotsSixVertical`

---

## 15. Transitions & Interactions

- Standard transition: `transition` (150ms ease)
- Hover lift: `hover:-translate-y-px`
- Active press: `active:scale-[0.98]`
- Hover brightness: `hover:brightness-105`
- Drag state: `rotate-1 shadow-[0_24px_45px_-28px_rgba(0,0,0,0.24)]`
- Loading spinner: `animate-spin` on `ClockCounterClockwise` icon
- Pulsing indicator: `animate-pulse` on status dots

---

## 16. Dependencies

```json
{
  "@phosphor-icons/react": "^2.1.7",
  "clsx": "^2.1.1",
  "tailwindcss": "^4.1.0",
  "@tailwindcss/postcss": "^4.1.0"
}
```

PostCSS config:
```js
export default { plugins: { "@tailwindcss/postcss": {} } };
```

Global CSS starts with:
```css
@import "tailwindcss";
```

---

## 17. Design Principles

1. **Warm, not cold** — No pure whites or blues. Everything skews warm (cream, sand, clay, parchment).
2. **Glass, not flat** — Panels use `backdrop-blur`, semi-transparent backgrounds, and `panel-sheen` overlays.
3. **Soft depth** — Shadows are large but tightly spread (negative spread values). Creates floating-paper feel.
4. **Ambient light** — Coloured orbs (teal top-left, clay bottom-right) add life without distraction.
5. **Serif for display, sans for UI** — Headings use serif font for warmth; everything else is clean sans-serif.
6. **Uppercase labels** — All meta text (timestamps, categories, section headers) is uppercase with wide tracking.
7. **Dark for focus** — Chat/workspace panels use charcoal backgrounds to create focus and contrast with the warm light surroundings.
8. **Pill shapes everywhere** — Buttons, tags, badges, pills are all `rounded-full`. Only containers use large border-radius.
9. **Minimal borders** — Borders are nearly invisible (`border-black/6`). Depth comes from shadows, not lines.
10. **Texture is subtle** — Grid pattern, noise dots, and sheen overlays add richness at low opacity.
