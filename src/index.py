#!/usr/bin/env python3
"""
seo-content-brief — target keyword → full SEO content brief
Generates: search intent analysis, outline, word count, competitor gaps,
semantic keywords, FAQs, internal link suggestions, meta tags
"""
import anthropic, json, re, sys
from datetime import datetime, timezone

SYSTEM = """You are a senior SEO strategist and content director at a top digital agency.
Create a comprehensive, actionable content brief that a writer can execute to rank on page 1.

Return ONLY valid JSON — no markdown, no explanation.

{
  "keyword": "primary target keyword",
  "monthly_search_volume": "estimated range e.g. '5K-10K'",
  "keyword_difficulty": "easy|medium|hard|very_hard",
  "search_intent": "informational|navigational|transactional|commercial",
  "intent_explanation": "what the searcher actually wants",
  "recommended_content_type": "blog_post|landing_page|product_page|comparison|listicle|how_to|pillar",
  "target_word_count": number,
  "reading_level": "beginner|intermediate|advanced",
  "title_options": [
    "5 compelling title options that include the keyword naturally"
  ],
  "meta": {
    "title": "under 60 chars, includes keyword",
    "description": "under 155 chars, compelling CTA",
    "url_slug": "keyword-optimized-slug"
  },
  "outline": [
    {
      "heading": "H2 or H3",
      "level": "H2",
      "word_count": 200,
      "key_points": ["what to cover in this section"],
      "media_suggestion": "image|video|table|chart|infographic|none"
    }
  ],
  "semantic_keywords": ["LSI and related keywords to include naturally"],
  "entities_to_mention": ["people, places, brands, concepts to build topical authority"],
  "questions_to_answer": ["specific questions from People Also Ask / forums"],
  "faqs": [
    {"question":"string","answer":"1-2 sentence answer for FAQ schema"}
  ],
  "competitor_gaps": ["topics your competitors cover that you should also address"],
  "unique_angles": ["ways to differentiate from existing top-ranking content"],
  "internal_link_opportunities": ["topics or pages on your site to link to/from"],
  "external_authority_sources": ["types of authoritative sources to cite"],
  "schema_types": ["Article","FAQPage","HowTo"],
  "estimated_ranking_timeline": "3-6 months",
  "content_upgrades": ["lead magnet or downloadable asset ideas"],
  "promotion_channels": ["Reddit","LinkedIn","newsletters"],
  "brief_summary": "2-3 sentence brief for your writer"
}"""

def generate_brief(keyword: str, industry: str = "", website: str = "", competitors: list = []) -> dict:
    client = anthropic.Anthropic()
    context_parts = [
        f"Target keyword: {keyword}",
        f"Industry/niche: {industry}" if industry else "",
        f"Website/brand: {website}" if website else "",
        f"Known competitors: {', '.join(competitors)}" if competitors else "",
        f"Date: {datetime.now(timezone.utc).strftime('%B %Y')}",
    ]
    prompt = "\n".join(p for p in context_parts if p)
    prompt += "\n\nGenerate a complete SEO content brief."

    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096, system=SYSTEM,
        messages=[{"role":"user","content":prompt}]
    )
    raw = re.sub(r'^```(?:json)?\s*','',resp.content[0].text.strip(),flags=re.MULTILINE)
    raw = re.sub(r'\s*```$','',raw,flags=re.MULTILINE)
    return json.loads(raw)

def to_markdown(r: dict) -> str:
    """Export brief as a Markdown document for your writer."""
    lines = [
        f"# SEO Content Brief: {r.get('keyword','')}",
        "",
        f"**Search volume:** {r.get('monthly_search_volume','?')} | "
        f"**Difficulty:** {r.get('keyword_difficulty','?')} | "
        f"**Intent:** {r.get('search_intent','?')}",
        "",
        f"**Intent:** {r.get('intent_explanation','')}",
        "",
        f"**Target word count:** {r.get('target_word_count',0):,} words | "
        f"**Content type:** {r.get('recommended_content_type','?')}",
        "",
        "---",
        "",
        "## Writer Brief",
        r.get('brief_summary',''),
        "",
        "## Title Options",
        *[f"- {t}" for t in r.get('title_options',[])],
        "",
        "## Meta Tags",
        f"**Title:** {r.get('meta',{}).get('title','')}",
        f"**Description:** {r.get('meta',{}).get('description','')}",
        f"**URL Slug:** `/{r.get('meta',{}).get('url_slug','')}`",
        "",
        "## Content Outline",
    ]
    for section in r.get("outline", []):
        indent = "###" if section.get("level") == "H3" else "##"
        lines.append(f"\n{indent} {section.get('heading','')} (~{section.get('word_count',0)} words)")
        for pt in section.get("key_points", []):
            lines.append(f"- {pt}")
        if section.get("media_suggestion") and section["media_suggestion"] != "none":
            lines.append(f"*[Include {section['media_suggestion']}]*")

    lines += [
        "",
        "## Semantic Keywords to Include",
        ", ".join(r.get("semantic_keywords",[])),
        "",
        "## Questions to Answer",
        *[f"- {q}" for q in r.get("questions_to_answer",[])],
        "",
        "## FAQ Section",
    ]
    for faq in r.get("faqs", []):
        lines.append(f"\n**Q: {faq.get('question','')}**")
        lines.append(f"A: {faq.get('answer','')}")

    lines += [
        "",
        "## Unique Angles (differentiate from competitors)",
        *[f"- {a}" for a in r.get("unique_angles",[])],
        "",
        "## Schema Types",
        ", ".join(r.get("schema_types",[])),
        "",
        "## Content Upgrades / Lead Magnets",
        *[f"- {u}" for u in r.get("content_upgrades",[])],
    ]
    return "\n".join(lines)

def print_brief(r: dict):
    print(f"\n{'═'*60}")
    print(f"  SEO BRIEF: {r.get('keyword','').upper()}")
    print(f"  {r.get('monthly_search_volume','?')} searches/mo | {r.get('keyword_difficulty','?')} difficulty | {r.get('search_intent','?')}")
    print(f"{'═'*60}")
    print(f"\n  Intent: {r.get('intent_explanation','')}")
    print(f"  Format: {r.get('recommended_content_type','?')} | {r.get('target_word_count',0):,} words")
    print(f"\n  Titles:")
    for t in r.get("title_options",[])[:3]: print(f"  • {t}")
    print(f"\n  Meta title: {r.get('meta',{}).get('title','')}")
    print(f"  Meta desc:  {r.get('meta',{}).get('description','')}")
    print(f"\n  Outline ({len(r.get('outline',[]))} sections):")
    for s in r.get("outline",[]):
        indent = "    " if s.get("level")=="H3" else "  "
        print(f"{indent}{s.get('level','H2')}: {s.get('heading','')} ({s.get('word_count',0)}w)")
    print(f"\n  Semantic keywords: {', '.join(r.get('semantic_keywords',[])[:8])}")
    print(f"\n  FAQs: {len(r.get('faqs',[]))}")
    print(f"  Schema: {', '.join(r.get('schema_types',[]))}")
    print(f"  Estimated ranking: {r.get('estimated_ranking_timeline','?')}")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Generate SEO content brief")
    p.add_argument("keyword", help="Target keyword")
    p.add_argument("--industry", "-i", default="")
    p.add_argument("--website", "-w", default="")
    p.add_argument("--competitors", "-c", nargs="+", default=[])
    p.add_argument("--json", action="store_true")
    p.add_argument("--markdown", "-m", help="Save as markdown file")
    a = p.parse_args()
    r = generate_brief(a.keyword, a.industry, a.website, a.competitors)
    if a.markdown:
        Path(a.markdown).write_text(to_markdown(r), encoding="utf-8")
        print(f"Brief saved to {a.markdown}")
    elif a.json: print(json.dumps(r, indent=2, ensure_ascii=False))
    else: print_brief(r)
