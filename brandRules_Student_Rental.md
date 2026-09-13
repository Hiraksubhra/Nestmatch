# brandRules.md — NestMatch Design System & Brand Identity

> **Purpose:** This file defines every visual, tonal, and component-level decision for the NestMatch product. All contributors — human and AI — must follow these rules when building UI. This is the design system source of truth.

---

## Table of Contents

1. [Brand Identity](#1-brand-identity)
2. [Color System](#2-color-system)
3. [Typography](#3-typography)
4. [Spacing & Layout](#4-spacing--layout)
5. [Iconography](#5-iconography)
6. [Component Library](#6-component-library)
7. [Motion & Animation](#7-motion--animation)
8. [Imagery & Photography](#8-imagery--photography)
9. [Voice & Tone](#9-voice--tone)
10. [Accessibility Standards](#10-accessibility-standards)
11. [Tailwind Config Reference](#11-tailwind-config-reference)
12. [Page-Level Design Patterns](#12-page-level-design-patterns)
13. [Anti-Patterns](#13-anti-patterns)

---

## 1. Brand Identity

### Name & Logo
- **Product Name:** NestMatch
- **Tagline:** *Find your space, find your people.*
- **Logo Concept:** A geometric nest icon (simplified concentric arcs) combined with a subtle map pin shape. The nest communicates home; the pin communicates location. The logo mark should work in monochrome.
- **Logo Usage:** Always use the SVG version. Never stretch, recolor, or add drop shadows to the logo. Maintain at least 16px clear space on all sides.

### Brand Personality
NestMatch speaks with the confidence of a knowledgeable senior student — someone who's been through the housing search and wants to make it easier for you. The brand is:

- **Trustworthy, not corporate.** We're not a bank. We're a platform students can confide in.
- **Local & warm, not clinical.** We know Pune's localities, Bangalore's traffic, and what "2km from campus" means.
- **Direct, not chatty.** Every word in our UI earns its place. No filler. No marketing speak.
- **Optimistic, not naive.** We acknowledge housing is stressful but position every feature as a step toward resolution.

---

## 2. Color System

### Core Palette

```
Primary      #2563EB   --color-primary        Deep Cobalt Blue
Primary Dark #1D4ED8   --color-primary-dark   Hover / active state
Primary Light #DBEAFE  --color-primary-light  Backgrounds, tags
Accent       #F59E0B   --color-accent         Warm Amber (verified badge, ratings, highlights)
Accent Light #FEF3C7   --color-accent-light   Accent backgrounds
Success      #16A34A   --color-success        Booking confirmed, active badge
Danger       #DC2626   --color-danger         Errors, declined states
Warning      #D97706   --color-warning        Pending verification
Neutral 50   #F9FAFB   --color-neutral-50     Page background
Neutral 100  #F3F4F6   --color-neutral-100    Card backgrounds, inputs
Neutral 200  #E5E7EB   --color-neutral-200    Dividers, borders
Neutral 400  #9CA3AF   --color-neutral-400    Placeholder text, muted labels
Neutral 600  #4B5563   --color-neutral-600    Secondary body text
Neutral 800  #1F2937   --color-neutral-800    Primary body text
Neutral 900  #111827   --color-neutral-900    Headings
```

### Color Usage Rules

**Primary Blue** is for:
- Primary action buttons (CTAs).
- Active navigation state.
- Links that trigger navigation.
- Focus rings.

**Amber Accent** is for:
- Verified listing badges.
- Star ratings.
- Featured/highlighted items.
- Price display (rent amount).

**Neutral palette** handles all body text, backgrounds, and structural elements.

**Never use:**
- Multiple accent colors on the same page without semantic reason.
- Decorative gradients as background washes (this is the AI-default trap).
- Pure black (`#000`) — use `neutral-900`.
- Pure white as a text color — use on `neutral-800` or darker backgrounds only.

### Dark Mode
Not in scope for v1. Design for light mode only. The color token system (`--color-*`) is set up to allow a future dark mode theme swap.

---

## 3. Typography

### Typeface Selection

**Heading Font:** `Plus Jakarta Sans` (Google Fonts)
- A modern geometric humanist sans-serif. Clear, warm, with excellent legibility on screens.
- Weights used: 600 (SemiBold) for headings, 700 (Bold) for display/hero.

**Body Font:** `Inter` (Google Fonts)
- Industry-standard for UI. Optimized for pixel rendering at small sizes.
- Weights used: 400 (Regular) for body, 500 (Medium) for labels/UI text.

**Monospace (optional, for metadata/codes):** `JetBrains Mono`
- Use sparingly — only for displaying lease IDs, reference numbers, or technical details.

### Type Scale

```
Display    3.5rem  / 56px  — Hero headline only (Home page H1)
H1         2.25rem / 36px  — Page titles
H2         1.75rem / 28px  — Section headings
H3         1.375rem/ 22px  — Card titles, subsections
H4         1.125rem/ 18px  — Labels, sidebar headings
Body LG    1.125rem/ 18px  — Long-form reading (listing descriptions)
Body       1rem    / 16px  — Default body text
Body SM    0.875rem/ 14px  — Supporting text, meta info
Caption    0.75rem / 12px  — Image captions, timestamps, tiny labels
```

**Line heights:**
- Display/H1: 1.1
- H2/H3/H4: 1.3
- Body text: 1.6
- Caption: 1.4

**Max line length:** 68ch for body text, 48ch for captions.

### Typography Rules

- Use **sentence case** for all UI copy (buttons, labels, headings). NOT ALL CAPS.
- Heading hierarchy must be sequential — never skip levels (H1 → H2 → H3).
- Price/rent amounts: `Inter 700` in `color-neutral-900`, prefixed with ₹.
- Do NOT accent a single word in a headline with a different color (AI-generated tell).
- Badge/tag text: always `Body SM`, `Inter 500`.

---

## 4. Spacing & Layout

### Spacing Scale (rem-based, Tailwind-compatible)

```
4px   (1)    — Micro gaps (icon to label)
8px   (2)    — Compact component internal spacing
12px  (3)    — Default padding inside small components
16px  (4)    — Default internal padding (cards, inputs)
24px  (6)    — Section separation (within a component)
32px  (8)    — Component-to-component spacing
48px  (12)   — Section padding (page-level)
64px  (16)   — Hero/section vertical padding
96px  (24)   — Major section gaps (homepage sections)
```

### Layout Grid

- **Max content width:** `1280px` (centered, `mx-auto`).
- **Page horizontal padding:** `px-4` (mobile) → `px-6` (tablet) → `px-8` (desktop).
- **Main layout:** 12-column grid (`grid-cols-12` with `gap-6`).

**Common layouts:**
- Search page: 3-col filters + 9-col content (at md+).
- Listing detail: 8-col content + 4-col sticky sidebar (at lg+).
- Flatmates browse: 4-col card grid (at lg), 2-col (md), 1-col (sm).
- Full-width sections on home: no grid, full `w-full`.

### Breakpoints (Tailwind defaults)

```
sm:   640px   — Large mobile / small tablet
md:   768px   — Tablet portrait
lg:   1024px  — Tablet landscape / small laptop
xl:   1280px  — Desktop
2xl:  1536px  — Large desktop
```

---

## 5. Iconography

**Icon Library:** `lucide-react` (already bundled with shadcn/ui).

### Amenity Icons (Listing Detail & Cards)

```
Wi-Fi         → <Wifi />
Air Conditioning → <Wind />
Laundry       → <WashingMachine /> or <Shirt />
Meals Included → <UtensilsCrossed />
Parking       → <Car />
Gym           → <Dumbbell />
Power Backup  → <Zap />
Security      → <Shield />
Furnished     → <Sofa />
CCTV          → <Camera />
```

### UI Icons

```
Search        → <Search />
Filter        → <SlidersHorizontal />
Save/Bookmark → <Bookmark /> / <BookmarkCheck />
Location      → <MapPin />
Verified      → <BadgeCheck /> (amber colored)
Star/Rating   → <Star />
Chat/Message  → <MessageSquare />
User          → <User />
Calendar      → <Calendar />
Upload        → <Upload />
Back          → <ArrowLeft />
Close         → <X />
Menu          → <Menu />
```

**Icon sizing:**
- Inside buttons: `w-4 h-4` (16px).
- Amenity icons: `w-5 h-5` (20px) with text label below.
- Navigation icons: `w-5 h-5`.
- Hero/feature icons: `w-8 h-8` (32px).

**Icon color:** Always inherit from text color via `currentColor`. Never hardcode icon fill colors.

---

## 6. Component Library

All components are built with `shadcn/ui` as the base layer and customized with these tokens.

### Button

```
Variants:
  primary     — bg-primary text-white, hover: bg-primary-dark
  secondary   — bg-white border border-neutral-200 text-neutral-800, hover: bg-neutral-50
  ghost       — transparent, hover: bg-neutral-100
  danger      — bg-danger text-white

Sizes:
  sm    — h-8 px-3 text-sm
  md    — h-10 px-4 text-base   (default)
  lg    — h-12 px-6 text-base

Rules:
- Always use full-width buttons on mobile inside forms.
- Loading state: spinner replaces icon, text changes to "Loading..."
- Destructive actions must use the danger variant AND require confirmation.
- No gradient fills on buttons.
```

### Card (Listing Card)

```
Structure:
  - Image: aspect-[4/3] rounded-t-xl object-cover
  - Body: p-4
    - Title: H4 (Inter Medium, truncate to 2 lines)
    - Price: Body LG bold (₹12,000/mo)
    - Location: Caption with MapPin icon
    - Amenity icons: 4 max, show +N if more
    - Verified badge: amber BadgeCheck icon + "Verified" label
  - Footer: p-3 border-t border-neutral-100 (Save button)

Shadow: shadow-sm on default, shadow-md on hover
Radius: rounded-xl (12px) on the card
Transition: hover shadow transition (200ms ease)
```

### Input

```
Base: h-10 px-3 rounded-lg border border-neutral-200 bg-white
  text-neutral-800 placeholder:text-neutral-400
  focus: outline-none ring-2 ring-primary/30 border-primary
  error: border-danger ring-danger/30
  
Error message: text-danger text-sm mt-1
Label: Body SM Medium, mb-1 text-neutral-600
```

### Badge / Tag

```
Variants:
  default     — bg-neutral-100 text-neutral-600
  verified    — bg-accent-light text-amber-700
  active      — bg-green-50 text-success
  pending     — bg-yellow-50 text-warning
  inactive    — bg-neutral-100 text-neutral-400
  type        — bg-primary-light text-primary (property type)

Size: text-xs px-2 py-0.5 rounded-full font-medium
```

### Avatar

```
Sizes: w-8 h-8 (sm), w-10 h-10 (md/default), w-12 h-12 (lg), w-16 h-16 (xl)
Fallback: initials on neutral-200 background, neutral-600 text
Radius: rounded-full always
```

### Form Wizard (Multi-step)

```
Progress: step dots at top, filled = primary, current = ring-2 ring-primary, future = neutral-200
Step label: Caption text below each dot
Navigation: Back (ghost button, left) + Next/Submit (primary button, right)
Container: max-w-2xl mx-auto card with p-8
```

### Map Component

```
Container: rounded-xl overflow-hidden border border-neutral-200
Height: h-64 on detail page sidebar, h-96 on full map view
Blurred pin: Before inquiry, show approximate location (blurred/offset pin)
Zoom controls: Bottom-right, styled to match neutral palette
```

### Amenity Grid

```
Layout: grid grid-cols-4 gap-3 (listing detail), flex flex-wrap gap-2 (listing card)
Each item: flex flex-col items-center gap-1 p-3 rounded-lg bg-neutral-50
Icon: w-5 h-5 text-neutral-600
Label: Caption text-neutral-600 text-center
```

---

## 7. Motion & Animation

### Principles

- **One orchestrated moment:** The listing card grid fades in on load (staggered, 50ms between cards). That's the one page-load animation. Nothing else auto-animates.
- **Action-response motion only after that:** Open/close modals, accordion expand, tab switch — these are acceptable because they show what changed.
- **No hover wiggle, bounce, or float animations on cards.**
- **Respect `prefers-reduced-motion`:** Wrap all animations in the media query. Provide instant/static fallback.

### Approved Transitions

```css
/* Standard UI transition */
transition: all 150ms ease-in-out;

/* Card hover shadow lift */
transition: box-shadow 200ms ease, transform 200ms ease;
transform: translateY(-2px);   /* max lift */

/* Modal open */
animation: fadeIn 200ms ease-out;
@keyframes fadeIn { from { opacity: 0; transform: scale(0.97); } to { opacity: 1; transform: scale(1); } }

/* Staggered list entry */
animation: slideUp 300ms ease-out both;
animation-delay: calc(var(--index) * 50ms);
@keyframes slideUp { from { opacity: 0; translateY(12px); } to { opacity: 1; translateY(0); } }
```

### Loading States

- **Skeleton loaders:** Use for listing cards and conversation list. Match the card structure with `animate-pulse` and `bg-neutral-200` blocks.
- **Spinner:** 20px, primary color, for button loading states and page-level loading.
- **Shimmer:** For photo gallery while images load.

---

## 8. Imagery & Photography

### Listing Photos
- **Minimum:** 3 photos required to publish a listing.
- **Cover photo:** 16:9 or 4:3 recommended. Displayed full-width in the gallery hero.
- **Thumbnails:** Shown in a strip below the hero (4 thumbs + "+N" overflow).
- **Processing:** Cloudinary auto-transforms to webp format, max 1920px wide.

### Illustration Style (Home Page, Empty States)
- Use flat, geometric illustrations in the brand palette (cobalt + amber, on neutral-50).
- Source: unDraw.co (filter by brand colors), or commission custom illustrations.
- Never use stock photography of interiors on the home page — only on actual listings.

### Empty States
Each empty state needs:
- A small illustration (not an icon alone).
- A clear H3 heading: "No listings found here yet."
- A single supporting sentence: "Try adjusting your filters or searching a different area."
- One CTA if applicable: "Browse all listings →"

---

## 9. Voice & Tone

### Core Principles

- **Specific over vague.** "3 BHK, Koregaon Park" not "a great option near your campus."
- **Action verbs.** "Save listing" not "Add to favourites" (unless that's the established label).
- **No fake urgency.** Never write "Only 2 rooms left!" unless it's real data.
- **No apology in errors.** "We couldn't find that listing." Not "We're so sorry, something went wrong!"

### Copy Examples

| Context | Write This | Not This |
|---|---|---|
| Primary CTA | "Search homes" | "Start your journey today!" |
| Empty search | "No listings match your filters." | "Oops! Nothing here yet." |
| Pending listing | "Your listing is under review." | "Hang tight, we're checking things out!" |
| Verified badge | "Verified by NestMatch" | "✓ Trusted!" |
| Booking confirmed | "Booking confirmed. Contact details shared." | "Woohoo! You're all set! 🎉" |
| Price | "₹12,000/month" | "₹12,000 per month (negotiable!)" |
| Button — send message | "Send message" | "Reach out!" |

### Tone Adjustments by Context

- **Error messages:** Neutral, direct. No emotion. Explain what happened and how to fix it.
- **Success messages:** Warm but brief. One sentence max.
- **Empty states:** Encouraging without being cheesy.
- **Notifications:** Short. Subject: action. Body: one supporting sentence + one link.

---

## 10. Accessibility Standards

**Target:** WCAG 2.1 AA compliance.

### Contrast Ratios
- Body text on white backgrounds: minimum 4.5:1 (Inter 400 passes at neutral-600 on white).
- Large text (H2+) and UI components: minimum 3:1.
- Primary blue (#2563EB) on white: 5.9:1 ✅
- Amber (#F59E0B) on white: 2.8:1 ❌ — **never use amber as text color on white; use amber-700 (`#B45309`) instead.**

### Keyboard Navigation
- All interactive elements must have visible focus rings: `ring-2 ring-primary ring-offset-2`.
- Modal dialogs must trap focus when open.
- Dropdown menus must close on `Escape`.
- Skip-to-content link at top of every page.

### Semantic HTML Rules
- Use `<button>` for actions, `<a>` for navigation. Never use `<div onClick>`.
- Listing cards that navigate to a detail page must be wrapped in `<a>` (not a button).
- All images need `alt` text. Listing photos: descriptive. Decorative illustrations: `alt=""`.
- Form labels must be associated with inputs via `htmlFor` / `id`.
- Use `aria-label` on icon-only buttons (e.g., save/bookmark button).

### Motion
- Wrap all CSS animations in `@media (prefers-reduced-motion: no-preference)`.

---

## 11. Tailwind Config Reference

Add the following to `tailwind.config.js`:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563EB',
          dark:    '#1D4ED8',
          light:   '#DBEAFE',
        },
        accent: {
          DEFAULT: '#F59E0B',
          light:   '#FEF3C7',
          dark:    '#B45309',
        },
        success: '#16A34A',
        danger:  '#DC2626',
        warning: '#D97706',
      },
      fontFamily: {
        sans:    ['"Inter"', 'system-ui', 'sans-serif'],
        heading: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', 'monospace'],
      },
      fontSize: {
        'display': ['3.5rem',  { lineHeight: '1.1', fontWeight: '700' }],
        'h1':      ['2.25rem', { lineHeight: '1.2', fontWeight: '600' }],
        'h2':      ['1.75rem', { lineHeight: '1.3', fontWeight: '600' }],
        'h3':      ['1.375rem',{ lineHeight: '1.35',fontWeight: '600' }],
        'h4':      ['1.125rem',{ lineHeight: '1.4', fontWeight: '600' }],
      },
      borderRadius: {
        'xl':  '12px',
        '2xl': '16px',
        '3xl': '24px',
      },
      boxShadow: {
        'card':       '0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06)',
        'card-hover': '0 4px 12px rgba(0,0,0,0.12), 0 2px 4px rgba(0,0,0,0.08)',
        'modal':      '0 20px 60px rgba(0,0,0,0.15)',
      },
      maxWidth: {
        'content': '1280px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
```

**Google Fonts import (add to `index.html` or CSS):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700&display=swap" rel="stylesheet">
```

---

## 12. Page-Level Design Patterns

### Home Page
- Hero: Full-viewport-height section. Left-aligned text (not centered). Illustration on the right (desktop), hidden on mobile. Background: `neutral-50` with a very subtle blue tint band (`primary-light` at 20% opacity) bleeding from the right.
- Search bar: Prominent, white background, rounded-xl, shadow-card. Single input (city/university) + Search button. Below: 4 "popular city" quick-links.
- "How it works" section: 3 steps, NOT numbered markers — use connected icons with a horizontal dashed line connector on desktop.
- Featured listings: Left-aligned heading, horizontal scroll on mobile, 3-up grid on desktop.
- Roommate CTA band: Solid `primary-light` background, left text, right illustration. NOT a dark section.

### Search Results Page
- Filter sidebar is collapsible on mobile (slide-in drawer).
- Active filters shown as dismissible chips above the listing grid.
- Map toggle button top-right. When toggled, the map takes the right 50% of the screen and the grid shrinks to the left.
- Loading: Show 6 skeleton cards while fetching.

### Listing Detail Page
- Photo gallery: Large hero (60% viewport height), 4 thumbnail strip below. Click opens a full-screen lightbox. No carousel auto-play.
- Layout: 8-col content + 4-col sticky contact card on desktop. Content stacks on mobile with contact card at the bottom.
- Amenity section: Titled "What's included," grid of amenity tiles (icon + label). Max 3 columns.
- Lease term tags: Horizontal scrolling pill row on mobile.
- Sticky mobile footer: "Enquire Now" button stays fixed at the bottom of the viewport on mobile.

### Messaging / Inbox
- Left panel: Conversation list (like WhatsApp web). Right panel: active chat thread.
- On mobile: List view → tap → full-screen chat.
- Message bubbles: Student messages right-aligned (primary-light bg). Landlord messages left-aligned (neutral-100 bg).
- System messages: Centered, Caption size, neutral-400, no bubble.

---

## 13. Anti-Patterns

These are explicitly forbidden design decisions. If an AI or team member generates these, reject them.

### Visual Anti-Patterns
- ❌ Gradient background washes or gradient cards (e.g., `bg-gradient-to-r from-blue-500 to-purple-500`)
- ❌ Terracotta / warm clay accent color (#D97757 range) — it reads as the Claude brand
- ❌ Cream/beige page backgrounds — use neutral-50 (cool-tinted)
- ❌ ALL CAPS headings or labels
- ❌ Drop shadows on icons or text
- ❌ Border-radius inconsistency (mixing sharp and heavily rounded on the same UI)
- ❌ Emoji in UI labels, buttons, or headings (allowed only in user-generated content)
- ❌ Multiple different shadow styles on the same page
- ❌ Solid dark navy (#0B0B0B) hero backgrounds — we are a warm, approachable brand

### Copy Anti-Patterns
- ❌ "Oops!" as an error prefix
- ❌ Exclamation marks in confirmation toasts (keep them calm)
- ❌ "Submit" as a button label — use the action (e.g., "Post listing", "Send inquiry")
- ❌ "Click here" as link text
- ❌ Passive voice in error messages ("Something went wrong" → "We couldn't load listings")

### Code Anti-Patterns
- ❌ Hardcoded color values in JSX/CSS — always use Tailwind tokens
- ❌ Inline styles for anything other than dynamic values (e.g., map height)
- ❌ `div` with `onClick` for navigation — use `<Link>` or `<a>`
- ❌ Images without `alt` attributes
- ❌ Console.log statements in production code
- ❌ API keys in frontend code — use `VITE_` env vars and never expose secret keys

---

*NestMatch Brand Rules v1.0*  
*Maintained by: TM2 (Frontend Lead)*  
*Review this document at the start of every sprint.*
