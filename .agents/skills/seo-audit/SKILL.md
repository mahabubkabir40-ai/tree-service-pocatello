---
name: seo-audit
description: Audit HTML pages for on-page SEO issues, metadata errors, headings structure, and performance problems
---

# SEO Audit Skill

This skill provides steps and automated checks to audit HTML pages on the website for on-page SEO issues, technical compliance, page metadata health, and local SEO optimizations.

## Audit Checklist

1. **Title & Meta Tags:**
   - `<title>` is under 60 characters and leads with target local keywords (e.g. `City Tree Service | Brand`).
   - `<meta name="description">` is between 120-160 characters and includes a call-to-action (CTA) and localized keywords.
   - Canonical tag is present: `<link rel="canonical" href="https://www.treeservicepocatelloidaho.com/path/">`.
   - OpenGraph and Twitter card titles/descriptions match page-specific content rather than being generic placeholders.

2. **Heading Hierarchy:**
   - Exactly one `<h1>` tag per page containing the primary local service phrase.
   - Proper nesting: `<h2>` for major sections, `<h3>` for subsections. Do not skip header levels.

3. **Images & Media:**
   - Every `<img>` tag must have a descriptive, keyword-appropriate `alt` attribute.
   - Core above-the-fold images (hero image) should use `rel="preload"` as `image` to prevent Largest Contentful Paint (LCP) delays.
   - Images should be compressed WebP or AVIF formats.

4. **Structured Data:**
   - JSON-LD script block is present and contains valid syntax (validate using the `schema` skill).

## How to Audit

Run local script checks or manual view-source inspects to extract and verify the tags of any updated pages before pushing changes live.
