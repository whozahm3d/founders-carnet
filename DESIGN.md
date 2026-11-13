---
name: The Founder's Carnet
version: 3.8
description: Editorial design system with layered, asymmetric composition. for an AI platform that introduces founders, talent, mentors and investors in Pakistan's startup ecosystem. Warm paper canvas, ink black monoliths, one burnt orange accent. Merged from the accepted Stitch prototypes (login, register, founder dashboard) and the project rules.
colors:
  canvas: "#FAF9F7"
  fill: "#F1F0EE"
  card: "#FFFFFF"
  trough: "#E8E6E1"
  ink: "#0A0A0A"
  ink-raised: "#171717"
  ink-border: "#262626"
  accent: "#B15F2C"
  accent-deep: "#964E22"
  accent-wash: "#F8EDE5"
  accent-soft: "#D48B5D"
  text: "#0A0A0A"
  text-secondary: "#52525B"
  text-muted: "#71717A"
  hairline: "#E2DFD9"
  hairline-subtle: "#ECEAE5"
  row-line: "#E6E5E2"
  disabled: "#E3E2DF"
  input-border: "#8D8D8D"
  success: "#047857"
  success-wash: "#ECFDF5"
  warning: "#B45309"
  warning-wash: "#FFFBEB"
  error: "#B91C1C"
  error-wash: "#FEF2F2"
typography:
  font: Hanken Grotesk
  accent: Instrument Serif italic (last one or two words of headings)
  mono: JetBrains Mono (labels, nav, dates, status)
  scale: [12, 14, 16, 18, 20, 24, 30, 36, 48, 60]
theme:
  primary: "#B15F2C"
  secondary: "#52525B"
  tertiary: "#964E22"
  neutral: "#71717A"
  background: "#FAF9F7"
  font: Hanken Grotesk (headline, body and label, no other font)
rounded:
  control: 12
  card: 24
  pill: 9999
spacing: [0, 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96]
glow:
  orange-1: "rgba(177,95,44,0.28)"
  orange-2: "rgba(207,128,71,0.22)"
  wash: "rgba(248,237,229,0.9)"
glass:
  fill: "rgba(255,255,255,0.70)"
  blur: 12
  ring: "rgba(230,229,226,0.70)"
  shadow: "0 8px 24px rgba(10,10,10,0.06)"
---

# Palette lock (read first)

These are the only colors allowed in the UI: canvas #FAF9F7, fill #F1F0EE, card #FFFFFF, trough #E8E6E1, ink #0A0A0A, ink raised #171717, ink border #262626, accent #B15F2C, accent deep #964E22, accent wash #F8EDE5, text #0A0A0A, #52525B, #71717A, hairlines #E2DFD9, #E6E5E2 and #ECEAE5, disabled fill #E3E2DF, input border #8D8D8D, and the three status pairs below.

Use no color outside this list anywhere, including buttons, chips, icons, outlines, selected states and focus rings. The design system theme in the tool must use these values (primary #B15F2C, secondary #52525B, tertiary #964E22, neutral #71717A, background #FAF9F7) and Hanken Grotesk for headline, body and label. If the tool proposes its own theme colors, override them with these.

# Typography lock (same as the current screens)

Keep the typography exactly as it appears on the current Founder, Investor, Mentor, Talent and Admin screens. Use these fonts and nothing else (no Inter, no Plus Jakarta Sans, no other serif or mono):
- Hanken Grotesk, weights 400 to 700, for headlines, body text, buttons and card titles.
- Instrument Serif italic for the last words of a heading, as on the current screens: the name in "Welcome back, Bilal", and the last one or two words of page and card titles ("Verification & Moderation Console", "Recommended founders", "Pending advisory requests", "Profile completeness", "Resume insights", "Recent pitch feedback"). The italic words are the same size as the heading, in #F5C842 on the gradient and #B15F2C on white cards. Every page title and card title has its last one or two words in italic. Never in body text, buttons, chips, tables or nav.
- JetBrains Mono, weight 500 or 600, for small labels, navigation items, dates and times, status chips and counters. It is uppercase with 0.05em letter spacing at 12 to 13 px. Minimum size 12 px.

Every role uses the same navigation style (JetBrains Mono, uppercase, 13 px, active item in an ink pill). The labels themselves must still be real content: no invented IDs, cohort names or codes.

# Icon and tint lock

Icons are thin line icons, 16 to 20 px, bare (the same family on every screen). Surface tints come from the palette only: no other tints on chips, tags or buttons. Chips and tags are #F1F0EE or #F8EDE5.

# Page background (every screen, no exceptions)

Every screen, desktop and mobile, uses this warm gradient as its page background, fixed behind the content (the same look as the current Founder, Investor and Admin dashboards): bright yellow glow at the top right, orange across the middle, red orange, then deep brown at the bottom left. Use this exact CSS and nothing else, with the same values on every screen:

background: radial-gradient(circle at 85% 15%, #F5C842 0%, #FF8A2B 30%, #C4451A 55%, #3A1206 100%) fixed; min-height: 100vh;

Do not substitute white, off white, peach, brown, tinted or lighter versions. Do not use photos or illustrations as the background. On mobile use the same gradient. Do not use a different size, position or color stops on any screen (no white highlight, no 120% size, no 90% 70% ellipse).

Content never sits directly on the gradient except the greeting, a short subline, the nav pill, and the footer line, which are white text over the darker area. Everything else sits on white cards (#FFFFFF, radius 24, 1px #E6E5E2) or ink cards (#0A0A0A). Modals and drawers open over the blurred page. The nav pill and Karachi time chip are glass (white at 70 percent, blur 12). Accent #B15F2C is used on white and ink surfaces only, never on the gradient.

This replaces the earlier "flat canvas" page background. #FAF9F7 is now used only for sections of the landing page between the hero and the closing section.

# Editing rule for design tools

Edit the existing screens in place, one by one. Keep each screen's name, position and layout. Do not create new screens, copies or variations. When a screen is done, move to the next.

# Composition (what makes it look designed, not generated)

Style reference: a calm studio landing page with a near white page, deep ink areas, soft orange light and floating glass cards. Borrow the visual language only. Never its name, copy, imagery or its four point star.

- One dramatic hero element per screen: an oversized headline or the score numeral. Headlines 48 to 60 px, weight 600, tracking -2 percent, with small muted supporting text. Hero numerals (the readiness "3.1 / 5") may go to 72 or 96 px, on that numeral only.
- Plain and specific beats decorated. When a layout choice here conflicts with the Mentor dashboard reference, the reference wins.
- Asymmetric layouts: one wide block beside one narrow, mixed card sizes, deliberate empty space. No centered single card on a plain background. No equal three column grids. No icon in a circle repeated in rows.
- Layered depth: a glass card overlapping a glow, an ink panel beside white cards, glass cards at different sizes and offsets that slightly overlap. Keep overlap away from text.
- Soft orange glow blobs sit behind the hero zone only, one or two per screen, using the glow tokens. They are blurred shapes (blur 80 to 120), never a hard gradient bar, and only the glow colors.
- Glass card: fill rgba(255,255,255,0.70), backdrop blur 12, 1px ring rgba(230,229,226,0.70), shadow 0 8px 24px rgba(10,10,10,0.06), radius 24. Use for the top nav, floating info cards and the login form card. Text on glass stays #0A0A0A (4.5:1 minimum).
- Rows fill #F1F0EE on hover and show a 36 px ink circular arrow badge at the right (hover only). The one main action per screen keeps its permanent badge.
- Small meta line (12 px, muted) is allowed at the top of ink cards and glass cards. It follows the Typography lock.
- Believable Pakistani data: Karachi, Lahore, Islamabad, Faisalabad, PKR amounts, real sector names. No lorem ipsum, no emoji, no stock illustrations. Do not mention SECP, PSEB or FBR as endorsement or compliance.

# Reference screen: Mentor dashboard (the baseline for every app screen)

The Mentor dashboard is the accepted reference for simplicity. Every app screen follows its structure and restraint. Sign-in and the Founder dashboard hero may add glow and glass from Composition. All other screens stay flat like this one.

Structure to copy:
- Floating white pill nav: logo and wordmark, a small role chip, centered nav pill with the active item in ink, a time chip and initials avatar on the right.
- Greeting at 36 to 48 px weight 600 with a one or two line muted subline under it.
- One ink card: a short headline on the left with a hairline divider and three plain stats under it (number 30 to 36 px, label 14 px, one muted line), and on the right a darker inner panel with the user's own tags and one white pill button.
- Below, two columns. Left (wide): one white card with a title, one muted line, then rows divided by hairlines. Each row has a mono index (01, 02), the name in 18 px weight 600, small muted meta (founder, sector, stage, city), a "Profile similarity" line with the percentage, one sentence of context, 2 to 3 plain tags (squarish, #F1F0EE), and two buttons at the bottom right: a neutral pill ("View founder carnet") and an ink pill ("Review advisory request" with a small inline arrow glyph, no circle).
- Right (narrow): white cards with lists. Each item has a name, a muted time, one sentence, then an ink pill "Accept request" and an outlined pill "Decline".
- One plain footer line under a hairline: logo and name on the left, Privacy, Terms, Contact on the right.

What makes it work: plain text buttons with no decoration, no icons in circles, hairline rows, tags that describe the data, small numbers, lots of white space, and only the ink card for contrast.

Rules that override the reference where it broke our rules (remove these from any screen that has them):
- No "SECP", "PECA", "Compliant", "Registered", "Attested", "Exemption" or "Charter" text, no advisory or legal notice card, no "Sovereign" wording, no cohort label ("Cohort 2026.Q1 Active"), no "Active & Matching" status chips.
- No invented stat such as "94% Rubric elevation". Stats are plain counts that exist in the data (inbound requests, active mentees, and similar).
- No green dots, no "Strict Sovereign Screening" chip.
- Small inline arrow glyphs inside ink pills are fine. The circular arrow badge is used on one main action per screen only.
- Keep the honesty lines: "Profile similarity, not a funding probability" and "Contact details after mutual acceptance" as one muted line, not a chip.

# Overview

The Founder's Carnet is a role based web app (founder, talent, mentor, investor, admin) with one AI engine behind it. It must feel like a serious, calm professional tool in a trust sensitive domain. Visual voice: editorial and print like, warm paper background, big confident headlines, ink black anchors, one burnt orange accent, lots of whitespace.

This file replaces the earlier DESIGN.md and the Stitch exported "Editorial Sovereign" file. Layout, shapes and components follow the accepted Stitch prototypes. Content and claims rules follow the project docs. Where the Stitch export contradicted the project (compliance claims, sidebar, AI badge, invented statistics), this file wins.

Do not copy Lumora's name, logo, copy or imagery. Only the visual language is borrowed.

Existing wireframe PNGs are the source of truth for content, fields and information hierarchy. Restyle them. Do not add, remove or rename screens, sections, fields or nav items. Do not invent features.

# Product context

AI introductions for Pakistani startups. The platform only makes introductions. Contact details are revealed only after both sides accept.

Nav per role:
- Founder: Dashboard, Profile, Readiness score, Pitch practice, Session feedback, Matches
- Talent: Dashboard, Profile, Resume, Jobs, Matches
- Mentor: Dashboard, Profile, Requests
- Investor: Dashboard, Profile, Founders, Requests
- Admin: Console

Honesty rules the UI must show:
- Readiness score is a rubric guide on a 1 to 5 scale. Caption: "A rubric guide, not a funding probability".
- Match percentages are labeled "Profile similarity", never likelihood of success.
- Contact details stay hidden until mutual acceptance. Caption: "Contact details after mutual acceptance".
- Verification is automated checks plus a human reviewer. Rejection is final after one appeal.

Claims that must never appear: regulatory compliance or certification (no "SECP compliant", "PSEB certified", "PECA compliant"), security or encryption claims, "NFR" or any requirement IDs, "AI-generated" badges, invented statistics (cohort medians, deltas, funding figures, admission cohorts, registry status), jargon like "telemetry", "frontier", "syndicate", "sovereign", "dossier", "rig", and fake identifiers such as session IDs, hashes, NTN, CNIC, CUIN, case or batch numbers. No payments, brokerage, equity, legal or tax advice anywhere.

# Colors

Light theme is the default. Cards are flat or glass. Allowed light effects: the sign-in artwork, soft orange glow blobs behind the hero zone (glow tokens only), and glass cards. No gradient fills on buttons, chips or the page background. The ink card is flat.

- Canvas #FAF9F7 is the page. Fill #F1F0EE is for chips, inputs on canvas, track backgrounds. Card #FFFFFF with a 1px hairline #E2DFD9.
- Ink #0A0A0A is for primary buttons, the featured monolith card, the mobile menu overlay and the logo tile. Text on ink is white. Ink border #262626.
- Accent #B15F2C is the only accent. It marks focus, progress fills, active states, key numbers and links. Hover and pressed #964E22. Wash #F8EDE5 for tag backings and focus rings.
- Text: primary #0A0A0A, secondary #52525B, muted #71717A (minimum 4.5:1 on canvas and cards). Small accent text on #F1F0EE uses #964E22.
- Status text and fills: success #047857 on #ECFDF5, warning #B45309 on #FFFBEB, error #B91C1C on #FEF2F2. Always pair color with an icon or label.
- Input borders need 3:1, so use #8D8D8D for inputs. Hairlines #E2DFD9 and #ECEAE5 are decorative only.

Dark mode (optional later): backgrounds only #000000, #181818, #1F1F1F, #272727, #313131. Accent becomes #CF8047.

Sign-in artwork palette (artwork only, never UI color): #3A1206, #C4451A, #FF8A2B, #F5C842, highlight #FFF6E2. Warm light falling from the top right into deep shade at the bottom left, soft and grainless.

# Typography

See the Typography lock above: Hanken Grotesk for text, Instrument Serif italic for the last words of headings, JetBrains Mono for small labels and navigation. Numbers use tabular figures.

Sizes follow the Tailwind scale only (12, 14, 16, 18, 20, 24, 30, 36, 48, 60).

| Style | Size / line | Weight | Tracking | Use |
|---|---|---|---|---|
| Display 1 | 60 / 60 (mobile 36 / 40) | 700 | -2.5% | Sign-in headline |
| Display 2 | 48 / 48 (mobile 36 / 40) | 700 | -2% | Page greeting, big score number |
| Heading 1 | 30 / 36 (mobile 24 / 32) | 700 | -2% | Page and section titles |
| Heading 2 | 24 / 32 | 600 | -1.5% | Card titles, form titles |
| Title | 18 / 28 | 600 | -1% | List titles, match names |
| Body | 16 / 24 | 400 and 500 | 0 | Running text |
| Body small | 14 / 20 | 400 | 0 | Secondary text, table cells |
| Label | 14 / 20 | 600 | +1% | Buttons, nav, field labels |
| Caption | 12 / 16 | 500 | +2% | Honesty captions, metadata, chips |

Headings and body text are sentence case. Mono labels are uppercase. Headings have no trailing period except the sign-in headline. Page subtitle capped at 680 px. Honesty captions never drop below 12 px or 4.5:1 contrast. Chips and badges use 12 px, not 11.

# Spacing, radius and layout

Spacing tokens only: 0, 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96. Card padding 24 (32 for the featured card). Gap between cards 24. Section gap 48.

Radius: cards and major containers 24, inputs and small containers 12, buttons, chips, avatars, nav pill full. Nested rule: inner radius = outer radius minus gap when the gap is under 32.

Layout:
- Max content width 1280, centered. Margins 32 desktop, 24 tablet, 16 mobile.
- Frames: 1440 desktop, 768 tablet, 390 mobile.
- Dashboard: nav, greeting headline, one ink monolith card, a two column row, then an asymmetric card row (one featured, two smaller). No equal three card rows.
- Do not use boxes inside boxes. Use hairline divided lists inside cards, not grey pill rows.

# Navigation (no sidebar)

A floating pill top nav replaces the sidebar on every app screen.
- Desktop: white at 90 percent with a 1px hairline and slight blur, full radius, 24 px from the top. Left: logo tile and "The Founder's Carnet". Center: nav items for the role, active item is an ink pill with white text. Right: a glass "Local time" chip with Karachi time and date (for example "3:55pm, 9 November 2026") and avatar with initials. The nav itself is a glass pill.
- The nav sits in normal flow with 24 px of space below it so it never covers the headline.
- Tablet: nav items collapse to icons or fewer labels. Mobile: logo and a Menu button that opens a full screen ink overlay with large numbered links (01, 02 ...), staggered in, close button top right, Escape closes.

# Logo

One mark everywhere, drawn as a single inline SVG (no raster files), used exactly as below and never redrawn:

<svg viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0A0A0A"/><path d="M45 0H52V22L48.5 18L45 22Z" fill="#B15F2C"/><path d="M14 14H40V23H24V28.5H36V37.5H24V50H14Z" fill="#fff"/></svg>

This logo is final and replaces any earlier brief (continuous stroke monogram, star, other marks). An ink rounded tile, a white F, and a small burnt orange ribbon hanging from the top edge like a bookmark. The wordmark "The Founder's Carnet" sits beside it in Hanken Grotesk 600. Reuse the same SVG in the nav, sign-in, footer and favicon. Never an "E", a lowercase c, or a placeholder image.

# Elevation

Tonal planes and hairlines, not stacked shadows.
1. Canvas.
2. Cards: white, 1px hairline, no shadow at rest.
3. Interactive card hover: lift 4 px and shadow 0 4px 12px rgba(0,0,0,0.04).
4. Modals and drawers: white, shadow 0 16px 36px -8px rgba(10,10,10,0.12), ink backdrop at 30 percent with blur.
5. Ink monolith: flat #0A0A0A, 1px #262626, flush on the canvas, sitting next to or under a glass card. No gradient fill.
6. Glass card: see Composition. Only over a glow or the ink panel, never on a plain white page where it would look like a white card.

# Icons

Phosphor, Regular weight, one stroke weight across the product, 20 px in nav, 16 px inline.

# Components

Buttons: full pill, min height 44 (48 on mobile), label style. Only the main action on a screen has the inset circular arrow badge: 36 px circle on the right, with 6 px padding on the right and 24 px on the left, so the badge sits snug inside the pill. All other buttons are plain pills with 24 to 28 px side padding and no badge. Hover scales to 1.03 and the arrow moves 3 px right.
- Primary: ink fill, white label, white 36 px badge with an ink arrow. On hover the badge turns accent with a white arrow.
- Accent: #B15F2C fill, white label (large or bold only). Hover #964E22. Badge only if it is the main action.
- Secondary: transparent or white fill, 1px #E6E5E2 border (#8D8D8D when it needs 3:1), ink label, no badge.
- Neutral: #F1F0EE fill, ink label, no badge.
- Tertiary: text with underline on hover.
- States for every type: Default, Hover, Pressed, Focus (2px accent ring, 2px offset), Disabled (#E3E2DF fill, #8D8D8D label). Use the pill with badge for the main action only. Secondary actions can be plain pills or text.

Inputs: height 44 (48 mobile), radius 12, white, 1px #8D8D8D border, label above. Focus shows an accent border with a 3px #F8EDE5 ring. States: Default, Hover, Focus, Filled, Error (red border, icon and message), Disabled.

ConsentBox: radius 12, #F1F0EE fill, 20 px checkbox, bold title, disclosure in caption style. Checkbox checked fills accent with a white check. The Create account button stays disabled until it is checked.

Ink card (featured block): flat #0A0A0A, 1px #262626, radius 24, padding 24 (32 on desktop). A small muted meta line at the top (sentence case, 12 px, white at 45 percent), the large title or number in the middle or bottom, and one muted line under it (white at 55 percent). Use it for the score card and at most one featured item per screen. Text on it is white at 100, 55 and 45 percent only.

Stat group (ink card only): numbers at 48 to 60 px, weight 600, tracking -2 percent, a 14 px muted label under each, 2 to 4 columns with 32 px between. Elsewhere, counts are one plain line of text.

Row list (replaces card walls): rows separated by 1px #E6E5E2 hairlines, no row backgrounds at rest. Each row has a mono index (01, 02), a title at 18 to 24 px weight 500, one muted line, and a trailing arrow or value. Row padding 24 vertical. On hover the row fills #F1F0EE, horizontal padding grows from 24 to 32 and content moves right over 500 ms.

Page heading block: a small eyebrow only when it adds meaning (a 6 px dot plus a short real label such as "Investor workspace"), a heading at 30 to 48 px weight 600 with -2 percent tracking, and a subline capped at 680 px.

Modal: white, radius 24, max width 512, padding 24 to 32, close button 36 px circle in #F1F0EE top right, backdrop ink at 30 percent with 16 px blur. Fields use the input spec above, labels in sentence case 14 px. On mobile the modal sits at the bottom of the screen.

Chips and badges: pill, 24 px high, caption style. Status chips use the wash colors with an icon. Entity tags use #F8EDE5 with #964E22 text. Squarer chips (8 px radius) are allowed for tags to avoid a wall of pills.

Readiness score card (flat ink monolith): greeting-sized number (Display 2 or larger) with "/ 5", a 1 to 5 ruler with tick marks and a marker pill reading the current value, the caption "A rubric guide, not a funding probability", and one pill button "Inspect rubric breakdown". Never show a probability, percentile or matrix.

Lists (next actions, pitch feedback, requests): hairline divided rows with a mono index (01, 02, 03), title, one muted line, trailing value or arrow. Hover fills the row with #F1F0EE and shifts content 8 px in over 300 ms.

Match card: white card, name, role and organization, "Profile similarity" with the percentage in accent, 2 to 3 tags, lock line "Contact details after mutual acceptance", primary pill "Request match". The featured match card is larger and fills its height (put the button at the bottom with a short "Why this match" line, no empty gap).

Chat (pitch practice): AI bubble #F1F0EE with ink text, user bubble ink with white text, radius 16, max width 70 percent, live rubric panel beside it as a white card with 1 to 5 progress rows.

Progress bars: 6 px, full radius, trough #E8E6E1, fill accent or success.

Drawers and modals: radius 24, white, shadow tier 4, focus trapped, Escape closes. Admin review drawer slides from the right with Approve and Reject, and states that rejection is final after one appeal. Request match modal confirms and states that contact details are shared only if the other side accepts.

Data views have Loading (skeleton shaped like the layout), Empty (one composed message and one action) and Error (message and retry) states.

# Motion

Easing cubic-bezier(0.22, 1, 0.36, 1). 500 ms layout changes, 300 ms color and opacity. Entrance: 12 to 24 px rise with fade, staggered 80 ms. Card hover lifts 4 px. Pill buttons scale to 1.03 and the badge arrow shifts 2 to 3 px. Mobile menu links stagger in. Honor prefers-reduced-motion.

# Sign in and Register

One screen with two states (Login and Register tabs). Full bleed warm gradient artwork behind everything. The form is a glass card that overlaps the artwork on the right, and the note card floats at a different height on the left. Left: top row with logo and name, a Display 1 headline "Introductions for Pakistan's startup ecosystem", a muted subline, and a frosted glass note card with three short product notes and prev and next arrows (for example mutual consent introductions, profile similarity not success odds, human review of unclear profiles). Right: a white form card 480 px wide, radius 24.
- Login: Welcome back, email, password, remember me, forgot password, Sign in pill, "Continue with LinkedIn", link to Register. No role picker, no consent box, no step counter. (Role picker and consent box belong to Register only.)
- Register: Create account, email, password, role select, LinkedIn option, ConsentBox, Create account pill (disabled until consent is checked).
- Footer: "The Founder's Carnet", 2026, Privacy, Terms, Contact. No status, compliance or security claims. Mobile: the artwork shrinks to a header band above the form.

# Landing page (public, route /)

A full public page that explains the product and converts visitors to Create account or Sign in. It matches the sign-in screen and adds no features. The message it must carry: "The Founder's Carnet introduces founders, talent, mentors and investors in Pakistan's startup ecosystem. Introductions are based on profile similarity, both sides must accept before contact details are shared, and nothing here is a funding promise."

Look: the hero and the closing section use the exact sign-in artwork (full bleed warm gradient, light from the top right into deep shade at the bottom left, #3A1206, #C4451A, #FF8A2B, #F5C842, #FFF6E2). The sections between sit on #FAF9F7 with white cards, hairline lists and one ink panel, like the Mentor dashboard reference. No photos, no stock images, no illustrations. Use the exact logo SVG (see Logo) in the nav and footer, never an "FC" tile, book icon or any other mark.

Sections in order:
1. Glass pill nav: logo and wordmark, links (What it is, How it works, Roles, Principles, FAQ, Contact), Karachi time chip, "Sign in" plain pill, "Create account" as the one main action with the circular arrow badge. Mobile: Menu button and the ink overlay.
2. Hero on the sign-in artwork: Display 1 headline "Introductions for Pakistan's startup ecosystem.", a two line subline ("A network that introduces founders, talent, mentors and investors across Karachi, Lahore and Islamabad. Contact details stay private until both sides accept."), buttons "Create account" and "Sign in". A glass card cycles three product notes with prev and next arrows, and a smaller glass card at a different offset says "Contact details after mutual acceptance". Asymmetric: headline left, cards floating right and lower.
3. What it is: a large statement on the left ("Finding the right people should not depend on who you already know.") and three short plain paragraphs on the right: the problem (early stage teams rely on personal networks), what the platform does (builds profiles, gives a readiness guide, suggests matches by profile similarity, sends introduction requests), and what it does not do (no payments, no brokerage, no equity dealing, no legal or tax advice, no cold outreach).
4. How it works: a hairline list of four rows, each with a mono index, a title, two sentences of explanation and an arrow badge on hover. 01 Create your account and choose a role. 02 Build your profile; automated checks and a human reviewer verify it. 03 See your readiness guide (founders) and matches by profile similarity. 04 Request an introduction; contact details appear only after both sides accept.
5. Roles: four hairline rows (Founders, Talent, Mentors, Investors), wide text column and a narrow "what you get" column. Founders: readiness guide on a 1 to 5 rubric, pitch practice with feedback, matches. Talent: profile, resume, job listings, matches with startups. Mentors: profile, advisory requests to accept or decline. Investors: thesis profile, founder matches, introduction requests. Use only features that exist in the app navigation.
6. Product preview: one large glass framed image of the Founder dashboard screen overlapping a soft orange glow, with a short caption. Use the real screen from the project, not a drawing.
7. Principles: one flat ink panel with four commitments, each with a title and one or two plain sentences: A rubric guide, not a funding probability. Profile similarity, not likelihood of success. Contact details after mutual acceptance. Human review for unclear profiles; a rejection is final after one appeal.
8. FAQ: five hairline rows that open on click: Who can join? How are profiles verified? When do I see contact details? Does the platform help raise money or hire? (It only makes introductions.) What happens if my profile is rejected? Answers are two sentences, plain, with no pricing or regulatory claims.
9. Contact: a two column section on #FAF9F7. Left: heading "Get in touch" and one sentence. Right: a white card form with Name, Email and Message fields and a "Send message" ink pill. Do not invent an email address, phone number, office address or response time.
10. Closing on the sign-in artwork: large headline "Ready for an introduction?" and one "Create account" button. Under it a flat #0A0A0A footer with rounded top corners: logo and wordmark, links (What it is, How it works, Roles, Contact), Privacy, Terms, "© 2026 The Founder's Carnet".

Never on the landing page: client or partner logos, "Trusted by", testimonials, ratings, user or startup counts, funding amounts, pricing, regulatory, security or compliance claims, statistics, photos of people, the words equity, syndicate, archetype, topological, curator, signal, calibration, methodology, and no small uppercase tracked labels. Section titles are sentence case at 36 to 48 px. Each section has real explanatory copy, not just a title and a list.

# Screens

Keep content, fields, copy, navigation items and functionality of all 12 prototypes. Redesign composition, hierarchy and style with this file. Work in place, one screen at a time, starting with Sign in and Register, then Founder dashboard, then the rest.
1. Sign in and Register
2. Founder profile: single column form in cards, two columns on desktop
3. Readiness score: ink hero card, then one hairline list of 7 rows (name, score, thin bar, one sentence, one text link)
4. Founder dashboard: oversized greeting row, ink score panel with "3.1 / 5" at hero size and the caption "A rubric guide, not a funding probability", then asymmetric cards (next actions, recent pitch feedback, match preview with one featured and two smaller, one glass card overlapping the ink panel edge)
5. Pitch practice: chat and live rubric panel
6. Pitch feedback: session header with "Investor persona: Seed-stage fintech investor" and "Session 3 of 3", score and gaps
7. Match feed: ranked match cards, filters as chips
8. Talent dashboard and job board: job rows with hover fill and tags
9. Mentor dashboard: verification banner and request rows
10. Investor dashboard: thesis summary, founder matches, request rows
11. Admin console: one line of plain counts, review queue with status chips, review drawer
12. Shared shell: top nav, mobile menu overlay
13. Landing page (public, route /), see Landing page above. Sign in has no step counter and offers LinkedIn only.

# Content

Realistic Pakistani context: names, cities (Karachi, Lahore, Islamabad, Faisalabad, Peshawar), sectors (fintech, agritech, healthtech, logistics, edtech), PKR amounts. Believable specifics, no placeholder text, no stock names like Acme. Use only content that exists in the wireframes or this file.

Banned phrases: revolutionize, supercharge, cutting edge, effortless, transform your workflow, take it to the next level, harness the power, world class.

# Hand made feel

Borrowed from the reference studio site (visual language only, never its name, copy or imagery): big confident headlines with tight tracking, generous whitespace, one ink block per screen as an anchor, hairline lists in place of card grids, round pill buttons with a snug arrow badge on the main action only, and hover that fills a row instead of adding a shadow. Vary card widths (one wide, one narrow) and keep one clear focal point. Nothing is centered by default; align to the left edge and let the right side breathe.

# Do and don't

Do
- One accent, ink anchors, flat cards, hairlines, real copy, one clear focal point per screen.
- Vary scale and card size. Make the greeting and the score big.
- Show every state: hover, focus, disabled, error, loading, empty.

Don't
- No sidebar, no boxes inside boxes, no wall of identical pills or cards.
- No gradient fills. Glows only as blurred blobs behind the hero zone. No eyebrow tags above headings.
- No colors outside the palette lock.
- No single side borders.
- No compliance, security or certification claims, no requirement IDs, no invented numbers.
- No probability, prediction or guarantee language about funding, matching or hiring.

# Anti template rules (what makes a screen look generated)

These override any default a tool would choose.
- One main action per screen gets the pill with the circular arrow badge. Every other button is a plain pill or a text link with no badge.
- No icon inside a circle on cards or list rows. Use an icon only when it adds meaning, bare and 16 px. The only circles are the arrow badges.
- No wall of identical cards. If seven items share a structure (such as the 7 readiness dimensions), show them as one list with hairline rows, not seven boxes. Use at most one card grid per screen.
- Chips only for real status (verified, pending, rejected) or a tag the user chose. No decorative chips, no stacks of check marks.
- Small uppercase mono labels are allowed (see Typography lock), but their text must be real and plain, never an invented code, ID, cohort or version.
- No fake system text: no "terminal", "BATCH_RUN", "200 OK", version strings, ledger or sync status.
- No invented analytics: no percentiles, cohort medians, benchmark matrices, sentiment analysis, deltas or "calibration" panels. Only data that exists in the wireframes.
- Footer is only: logo, "© 2026 The Founder's Carnet", Privacy, Terms, Contact. No "Sovereign", "Institutional", "Regulatory" or "Compliance" links. No duplicated logo or nav on a screen.
- Four stats in a row is allowed only on the ink score card, and only when the wireframe has them. Elsewhere show counts as one line of text.
- Each screen has one focal point (the score, the greeting, the active chat) and a clear order of importance. Vary card sizes and let whitespace do the work.
- Copy is plain and specific. No invented jargon (telemetry, frontier, syndicate, vector, dossier, docket).

# Accessibility

Body text 4.5:1, large text and UI parts 3:1. Touch targets at least 44 by 44 on mobile. Visible focus ring on everything interactive. Never rely on color alone for state. Logical heading order, labeled fields, aria-current on the active nav item, keyboard closable drawers and overlays.
