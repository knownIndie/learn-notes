# Spec: rewrite one networking topic as a QUICK page + a DETAILED page

Vault folder: /Users/ana/obsidian/learn-notes/  (Quartz site, read on a PHONE)

## The exemplar: copy its format exactly
- Quick:    /Users/ana/obsidian/learn-notes/networking/cors.md
- Detailed: /Users/ana/obsidian/learn-notes/networking/deep/cors.md
- SVG style: /Users/ana/obsidian/learn-notes/assets/diagrams/cors-flow-phone.svg, cors-preflight-phone.svg, cors-mental-map.svg
- Mental-map generator you can copy and adapt: /tmp/ln-scripts/map.py (run with python3 -I map.py OUTFILE after editing the branches list in a COPY of it, e.g. /tmp/ln-scripts/map-<topic>.py)
Read all of these first.

## Source material (old, too-long page; content is correct, use it)
/tmp/ln-old/networking/<topic>.md

## Files you write
1. /Users/ana/obsidian/learn-notes/networking/<topic>.md          (quick, overwrite the old one)
2. /Users/ana/obsidian/learn-notes/networking/deep/<topic>.md     (detailed)
3. /Users/ana/obsidian/learn-notes/assets/diagrams/<topic>-*.svg   (at least: one main picture, one mental map; add one more only if it truly helps)
Touch NO other files.

## Frontmatter
Quick:
---
title: <Topic>
tags: [networking, <topic-tag>]
---
Detailed: same, title "<Topic> (detailed)".

## Section headings: SAME headings, SAME order, in BOTH pages
1. callout `> [!abstract] What this page is for` with **Intent:**, **You'll learn:**, **Time:** lines (quick links to the detailed page; detailed says "read the quick page first" and links back)
2. `## Words you need first`
3. `## Why it exists`  (or `## Why it matters` if "exists" doesn't fit)
4. `## The picture`
5. `## How it works, with an example`
6. `## The most common mistake`  (a `> [!warning]` callout)
7. 1–3 topic-specific sections (same names in both pages)
8. `## Say it in an interview`  (quick: a ~60-second spoken answer in a quote block; detailed: "start with the quick answer" + 2–3 deeper add-ons)
9. `## Questions interviewers ask`  (collapsible callouts `> [!question]- Question?` then `> answer`; quick: 8–10 core questions, 1–2 line answers; detailed: says "the N from the quick page, plus these" and adds 8–10 harder/real-world ones)
10. `## Mental map`  (the SVG; detailed reuses the same SVG)
Quick ends with a **Want more?** line linking the detailed page.
The detailed page ONLY ADDS DEPTH under each heading (raw protocol text, exact rules, tables, commands, edge cases). It never uses a different structure or a different example. Reuse the quick page's example and pictures.

## Writing rules (the user's, strict)
- Every technical term is explained in plain words the FIRST time it appears (in "Words you need first" or inline right there). If you write TCP, say what TCP is. Abbreviations: expand + explain.
- Simple examples (shop.com / api.com style). Short sentences. Simple English.
- Quick page: 900–1400 words INCLUDING the hidden answers. Detailed: 1800–2600 words.
- NO LaTeX at all. No `$...$`, no `$$`, no \text. Write formulas in plain text or `code`, e.g. `total ≈ DNS + TCP + TLS + HTTP round trips`.
- No em dashes. Use colons, commas, or full stops.
- Wikilinks use full paths: [[networking/dns|DNS]], [[networking/deep/tcp|...]]. Topic pages that exist: http-message, request-lifecycle, dns, tcp, tls, http-caching, origin, cors.
- Images: quick page uses `../assets/diagrams/<file>.svg`, detailed uses `../../assets/diagrams/<file>.svg`. Normal markdown image syntax, never ![[...]].
- Do NOT copy the old page's series callout (`<!-- series:start -->` ... ) or nav blocks.
- Facts must be correct. If unsure, leave it out.

## SVG rules
- width="360", viewBox width 360, VERTICAL layout for a phone. Height as needed.
- Own background card: `<rect x="1" y="1" width="358" height="H-2" rx="12" fill="#faf9f5" stroke="#e3e1d9"/>` (works in dark mode).
- Same palette as the CORS SVGs (blue #E6F1FB/#185FA5, purple #EEEDFE/#534AB7, teal #E1F5EE/#0F6E56, amber #FAEEDA/#854F0B, red #FCEBEB/#A32D2D, green #EAF3DE/#3B6D11). font-family system-ui; monospace for headers/code.
- NO TEXT MAY OVERFLOW. Budget: at font-size 12, ~6.5 px per character; monospace 10px ≈ 6 px per char. A line inside a box from x=68 to x=340 fits ~40 chars at 12px. Count characters for every text line and shorten or wrap if needed. Text must stay at least 10px from any box edge.
- Every SVG has a <title>. Must be valid XML: check with `python3 -I -c "import xml.dom.minidom,sys;xml.dom.minidom.parse(sys.argv[1])" FILE`.

## Interview questions: research first
Before writing, run 2–3 WebSearch queries like "<topic> interview questions", "<topic> interview questions backend developer", "<topic> follow-up questions interview". Make sure every commonly asked question you find is answered somewhere (quick for the core ones, detailed for harder ones).

## Final check before you finish
- grep both pages for `$` (must be none outside code blocks) and for "—" (must be none).
- Both pages have the identical list of `## ` headings: compare with `grep '^## ' file`.
- Validate every SVG you wrote.
- Report back: files written, word counts, the list of interview questions covered, and the source URLs you used for questions.
