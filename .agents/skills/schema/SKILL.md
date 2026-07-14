---
name: schema
description: Generate and validate JSON-LD structured data schema markup for LocalBusiness, FAQPage, BreadcrumbList, etc.
---

# Schema Structured Data Skill

This skill outlines best practices for generating, validating, and testing JSON-LD structured data schemas on pages to ensure rich search result eligibility and prevent syntax alerts in Google Search Console.

## Core Rules

1. **Syntax Escaping (CRITICAL):**
   - When placing HTML links or tags inside JSON-LD properties (like a FAQ answer's `text` property), you **MUST** escape all double quotes inside the string.
   - **Incorrect:** `"text": "Check <a href="https://site.com">link</a>"` (causes JSON parsing errors).
   - **Correct:** `"text": "Check <a href=\"https://site.com\">link</a>"`.

2. **Common Schema Types for Local SEO:**
   - **BreadcrumbList:** Define on every page to show clean breadcrumb paths in search results.
   - **TreeService / LocalBusiness:** Define on the homepage and location pages with NAP (Name, Address, Phone) details, geo-coordinates, logo, price range, and service area.
   - **FAQPage:** Generate questions and answers targeting common local queries to secure rich snippets.

3. **Validation Workflow:**
   - Run the local validator script: `python scratch/validate_schemas.py` to identify syntax errors before deploying changes.
   - Use Google's Rich Results Test tool to inspect live URLs.
