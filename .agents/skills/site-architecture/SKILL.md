---
name: site-architecture
description: Plan and optimize website URL structures, page hierarchy, and internal linking for SEO
---

# Site Architecture Skill

This skill provides comprehensive instructions for designing, auditing, and optimizing website directory structure, URL paths, and internal linking to maximize search engine crawlability, indexation, and PageRank distribution.

## Core Principles

1. **Logical Hierarchy:**
   - Maintain a flat structure where possible (no page should be more than 3-4 clicks away from the homepage).
   - Use folder structures to represent service areas and sub-services:
     - `/` (Homepage)
     - `/tree-trimming/` (Core Service)
     - `/chubbuck-idaho/` (Location Landing Page)

2. **Clean URLs:**
   - lowercase letters only.
   - Use hyphens `-` instead of underscores `_` or spaces.
   - Avoid trailing parameters where possible.
   - Keep URLs short, descriptive, and keyword-focused.

3. **Internal Linking Strategy:**
   - **Contextual Body Links:** Link to relevant sub-pages within the main body paragraphs using high-weight anchor text. Google passes more PageRank to links in the body than in the footer.
   - **Breadcrumbs:** Implement schema-valid breadcrumb navigation on every subpage to establish parent-child relationships for search engines.
   - **Footer Navigation:** Provide clean links to all core pages and location landing pages for redundancy and crawlability.

4. **Redundancy & Redirects:**
   - Configure 301 redirects for any deleted or renamed pages in `vercel.json` or server config to preserve link juice.
   - Maintain a synchronized `sitemap.xml` file.

## Execution Checklist

- [ ] Draw/document the current sitemap hierarchy.
- [ ] Identify isolated pages (orphan pages) that have no incoming links.
- [ ] Add 2-3 body links from high-authority parent pages to new child pages.
- [ ] Audit URLs for uppercase letters, underscores, or trailing parameter issues.
