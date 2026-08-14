Design a completely new UI/UX for a web application called "DSA Practice".

IMPORTANT:
START FROM SCRATCH.

Do NOT use, imitate, reference, or improve any existing design I may have.
Do NOT use the typical AI-generated SaaS/dashboard aesthetic.
Do NOT create generic rounded cards, gradients, excessive shadows, glassmorphism, floating statistic cards, or a standard Tailwind-style dashboard.

The goal is to create a distinctive, minimalist, editorial-quality interface that feels designed by a strong human product designer.

==================================================
PRODUCT
==================================================

DSA Practice is a public platform for practicing LeetCode questions organized by:

- Company
- Topic
- Difficulty

Users do NOT need an account.

The question database is hosted on a backend, while personal progress lives entirely in browser localStorage.

Users can:

- Browse companies
- Browse topics
- Browse questions
- Filter/search questions
- Practice random question sets
- Mark questions as solved
- Bookmark questions
- Add personal notes
- Track personal progress
- Export their progress
- Import their progress
- Switch between light and dark themes

The backend currently contains approximately:

3,430 questions
737 companies
24 topics
23,748 company-question relationships

These numbers should be represented naturally in the interface, not as flashy dashboard statistics.

==================================================
DESIGN DIRECTION
==================================================

Create something that stands out from typical developer tools.

Core principles:

- Minimal
- Editorial
- Quiet
- Precise
- Functional
- Strong typography
- Excellent spacing
- Very little decoration
- Strong visual hierarchy
- Subtle interaction
- No visual clutter

Think:

"independent design publication meets developer tool"

rather than:

"AI-generated SaaS dashboard"

The interface should feel like someone spent considerable time designing the typography, spacing, proportions and interaction patterns.

==================================================
COLOR SYSTEM
==================================================

LIGHT THEME

Use a warm cream/off-white background instead of pure white.

Suggested direction:

Background:
#F4F0E6

Primary text:
#171717

Secondary text:
#6F6A60

Borders:
#D8D2C6

Accent:
Deep terracotta / burnt orange

Example:
#C65D3A

Avoid bright blue as the primary accent.

The light theme should feel warm, sophisticated and paper-like.

--------------------------------------------------

DARK THEME

Use a true near-black background.

Background:
#0A0A0A

Primary text:
#F2F0EA

Secondary text:
#92908A

Borders:
#272727

Accent:
Warm amber/orange

Example:
#F0A34A

The dark theme should feel extremely clean and understated.

Do not use neon blue/purple gradients.

==================================================
VISUAL LANGUAGE
==================================================

Explore a subtle form of editorial minimalism.

You MAY use:

- extremely subtle claymorphism
- tactile controls
- thin borders
- offset borders
- restrained shadows
- asymmetric layouts
- editorial grids
- large whitespace
- typography as the primary visual element
- small numerical labels
- subtle hover movement

But do NOT turn the entire interface into claymorphism.

Avoid:

- excessive rounded cards
- floating glass panels
- gradient backgrounds
- neon effects
- excessive shadows
- huge icons
- generic dashboard cards
- excessive pills
- unnecessary illustrations

The design should work even if all decorative elements are removed.

==================================================
TYPOGRAPHY
==================================================

Typography is extremely important.

Use a strong modern sans-serif for the interface.

Consider:

Inter
Manrope
DM Sans
Geist
or another high-quality contemporary sans-serif.

Potentially use a restrained monospace font ONLY for:

- question numbers
- statistics
- difficulty labels
- small metadata
- keyboard shortcuts

Do not use monospace everywhere.

Do not make everything uppercase.

Do not use huge marketing-style headings everywhere.

==================================================
NAVIGATION
==================================================

Create an unusual but highly usable navigation system.

Do NOT simply make:

Logo | Companies | Topics | Practice | Progress | Settings

with lots of evenly spaced links.

Explore a more editorial navigation.

For example:

DSA Practice

Companies   Topics   Practice

                    Progress · Settings

Or another layout that feels intentional.

The navigation should remain extremely simple.

On mobile, create a compact navigation system that doesn't feel like a generic hamburger menu if possible.

==================================================
HOMEPAGE
==================================================

Design the homepage from scratch.

It should NOT look like a dashboard.

The homepage should immediately communicate:

"This is a place to systematically practice interview questions."

Possible structure:

--------------------------------------------------

DSA
PRACTICE

A short one-line description.

[ Search everything... ]

--------------------------------------------------

A small editorial data line:

3,430 questions
737 companies
24 topics

--------------------------------------------------

Then introduce the actual content.

For example:

COMPANIES

The questions most associated with...

Google                         2,330
Amazon                         2,060
Microsoft                      1,466
Meta                           1,366
Bloomberg                      1,259

                 Browse all →

And:

TOPICS

Array                          1,140
String                           481
Hash Table                       427
Dynamic Programming              341
Math                             297

                 Browse all →

Do NOT make every company a card.

Consider using typography, dividers and rows instead.

The homepage should feel more like an editorial index than a SaaS dashboard.

==================================================
COMPANIES PAGE
==================================================

Create a beautiful company directory.

Think:

COMPANIES

737 companies

[ Search companies... ]

01    Google                         2,330
02    Amazon                         2,060
03    Microsoft                      1,466
04    Meta                           1,366
05    Bloomberg                      1,259

...

Use rows rather than cards.

Hovering a row should create a subtle visual response.

Possible interaction:

01     Google                 2,330
       ──────────────────────────────

Do not overdecorate it.

==================================================
COMPANY DETAIL
==================================================

Company page should feel like an index of questions.

Example:

GOOGLE

2,330 questions

Easy       588
Medium   1,094
Hard       459

[ Search questions... ]

All    Easy    Medium    Hard

Then a beautiful question list.

01   Two Sum                         Easy
02   Add Two Numbers                Medium
03   Trapping Rain Water            Hard

Each row should contain:

- question number
- title
- difficulty
- solved indicator
- bookmark indicator
- frequency

No giant cards.

==================================================
QUESTION BROWSER
==================================================

Create a sophisticated question table/list.

Desktop:

#     Question                         Difficulty    Frequency    Status

01    Two Sum                          Easy          100           ✓
02    Add Two Numbers                 Medium         65
03    Trapping Rain Water             Hard           62

Mobile:

Convert each row into a compact stacked layout.

Never create horizontal overflow.

==================================================
QUESTION DETAIL
==================================================

Design a focused question page.

Example:

Two Sum

Easy · Array · Hash Table

A clean primary action:

Open on LeetCode ↗

Then:

[ Mark solved ]     [ Bookmark ]

Personal notes

------------------------------------------------

A generous but minimalist textarea.

The page should feel like a workspace rather than a profile page.

==================================================
PRACTICE MODE
==================================================

Practice should feel like a focused mode.

Create a configuration interface:

Practice

Build a session.

Company
[ All companies                    ↓ ]

Topic
[ All topics                       ↓ ]

Difficulty
[ Any difficulty                   ↓ ]

Questions
[ 10 ]

                 Start session →

Use custom searchable dropdowns.

Do NOT use native browser select elements.

During practice:

Question 04 / 10

Two Sum

Easy

[ Open on LeetCode ↗ ]

[ Solved ]

[ Next question → ]

Keep distractions minimal.

==================================================
MY PROGRESS
==================================================

Do not create a generic analytics dashboard.

Instead create an elegant personal index.

MY PROGRESS

37 solved

12 bookmarked

4 notes

Then:

Recently solved

01  Two Sum
02  Binary Search
03  Merge Intervals

Progress by difficulty:

Easy      ███████████
Medium    █████
Hard      ██

Keep it subtle.

==================================================
SETTINGS
==================================================

Minimal settings page.

Appearance

○ Light
○ Dark
○ System

Data

Export progress
Import progress
Reset progress

Explain clearly that progress is stored locally in the browser.

==================================================
LOCAL STORAGE
==================================================

The design must account for the fact that progress is local.

There is no login/profile system.

Make this feel intentional rather than like a limitation.

Potential small message:

"Your progress stays on this device."

Do not repeatedly show this message everywhere.

==================================================
RESPONSIVENESS
==================================================

This is extremely important.

Design for:

320px mobile
375px mobile
430px mobile
768px tablet
1024px tablet/laptop
1440px desktop
1920px desktop

Mobile should NOT simply be the desktop layout compressed.

Create intentional mobile compositions.

On mobile:

- navigation becomes compact
- tables become stacked lists
- filters become drawers/sheets
- search takes full width
- buttons remain thumb-friendly
- typography scales appropriately
- no horizontal scrolling
- no tiny text
- no giant empty spaces

Tablet should feel equally intentional.

==================================================
INTERACTION
==================================================

Keep animations extremely subtle.

Use:

- 120–200ms transitions
- slight translation
- opacity changes
- underline animations
- border changes
- subtle background shifts

No:

- excessive bouncing
- parallax
- huge page transitions
- animated gradients
- flashy loading effects

==================================================
IMPORTANT DESIGN CONSTRAINTS
==================================================

DO NOT create:

❌ Generic SaaS dashboard
❌ Typical AI-generated landing page
❌ Gradient hero
❌ Blue/purple startup aesthetic
❌ Huge rounded cards
❌ Glassmorphism
❌ Excessive pill buttons
❌ Floating statistic cards
❌ Giant icons
❌ Terminal aesthetic
❌ Excessive uppercase typography
❌ Dense Tailwind-looking UI
❌ Generic "Welcome back" dashboard
❌ Stock illustrations

Instead create:

✓ Editorial
✓ Minimal
✓ Warm
✓ Distinctive
✓ Typography-driven
✓ Data-driven
✓ Functional
✓ Quiet
✓ Human-designed
✓ Memorable

==================================================
FIGMA DELIVERABLE
==================================================

Create a complete Figma design system and high-fidelity screens for:

1. Homepage — Light
2. Homepage — Dark
3. Companies — Light
4. Companies — Dark
5. Company Detail — Light
6. Company Detail — Dark
7. Topics — Light
8. Topics — Dark
9. Topic Detail — Light
10. Topic Detail — Dark
11. Question Browser — Light
12. Question Browser — Dark
13. Question Detail — Light
14. Question Detail — Dark
15. Practice Setup — Light
16. Practice Setup — Dark
17. Practice Session — Light
18. Practice Session — Dark
19. My Progress — Light
20. My Progress — Dark
21. Settings — Light
22. Settings — Dark

Also create:

- desktop versions
- mobile versions
- tablet considerations
- reusable components
- typography system
- color variables
- spacing system
- buttons
- inputs
- searchable dropdown
- question rows
- difficulty indicators
- solved/bookmarked states
- empty states
- loading states
- error states

==================================================
FINAL DESIGN TEST
==================================================

Before finalizing, ask:

"If I removed the logo and product name, would this still look like a generic AI-generated developer dashboard?"

If YES → redesign it.

The final result should be immediately recognizable as a carefully designed minimalist product, not another Tailwind/AI-generated website.

START COMPLETELY FROM SCRATCH.
DO NOT USE THE EXISTING WEBSITE'S VISUAL DESIGN AS INSPIRATION.