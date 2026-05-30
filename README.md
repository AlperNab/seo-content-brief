# seo-content-brief

> **Target keyword → full SEO content brief.** Search intent analysis, detailed outline, word count, semantic keywords, FAQ schema, competitor gaps, meta tags — everything a writer needs to rank on page 1.

[![PyPI](https://img.shields.io/pypi/v/seo-content-brief?style=flat)](https://pypi.org/project/seo-content-brief/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quickstart

```bash
pip install seo-content-brief

python -m seo_content_brief "best crm for small business" \
  --industry "SaaS" \
  --website "yoursite.com" \
  --markdown brief.md
```

## What's in the brief

- Search intent + content type recommendation
- 5 title options with keyword
- Meta title, meta description, URL slug
- Full H2/H3 outline with word counts per section
- Semantic/LSI keywords to include
- People Also Ask questions to answer
- FAQ section with schema markup
- Competitor gap analysis
- Internal linking opportunities
- Estimated ranking timeline
- Content upgrade / lead magnet ideas

## Export as Markdown

```bash
python -m seo_content_brief "keyword" --markdown brief.md
```

Produces a clean Markdown file you can share directly with your writer.

## License
MIT © [Alper Nabil Gabra Zakher](https://github.com/AlperNab)
