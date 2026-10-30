# Learn notes

Detailed notes on everything I learn, one page per concept, published at
**https://knownindie.github.io/learn-notes/**.

- Notes: `content/<subject>/<concept>.md` (Obsidian-flavoured markdown: wikilinks, callouts, LaTeX, Mermaid).
  `content/` can be opened as an Obsidian vault.
- Template: `content/templates/concept.md` (not published).
- Diagrams: `content/assets/diagrams/*.svg`. Interactive widgets: `quartz/static/widgets/*.html`.
- `tools/export_widget.py` turns a chat widget (or every widget in a session transcript) into those files.

Preview locally:

```bash
npm ci && npx quartz build --serve
```

Pushing to `main` builds and deploys to GitHub Pages (`.github/workflows/deploy.yml`).
Built with [Quartz](https://quartz.jzhao.xyz).
