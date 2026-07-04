import os
import json
import re
from bs4 import BeautifulSoup

def optimize_seo():
    root_dir = r"c:\Users\USER\Desktop\Tree Service Pocatello"
    
    pages = [
        "index.html",
        "about/index.html",
        "cabling-bracing/index.html",
        "contact/index.html",
        "emergency-tree-services/index.html",
        "privacy-policy/index.html",
        "services/index.html",
        "shrub-removal/index.html",
        "stump-removal-grinding/index.html",
        "tree-removal/index.html",
        "tree-trimming/index.html"
    ]

    # Load Organization schema template from homepage
    homepage_path = os.path.join(root_dir, "index.html")
    with open(homepage_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    homepage_schema_tag = soup.find('script', class_='rank-math-schema')
    homepage_org_schema = None
    if homepage_schema_tag:
        try:
            hp_graph = json.loads(homepage_schema_tag.string).get('@graph', [])
            for item in hp_graph:
                if any(t in item.get('@type', []) for t in ['TreeService', 'Organization']):
                    homepage_org_schema = item
                    break
        except Exception as e:
            print(f"Error loading homepage schema: {e}")

    # Optimize each page
    for rel_path in pages:
        full_path = os.path.join(root_dir, rel_path.replace('/', os.sep))
        if not os.path.exists(full_path):
            continue
            
        print(f"\nOptimizing page: {rel_path}")
        with open(full_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # 1. Enforce exact-match Pocatello keywords in meta descriptions
        descriptions = {
            "index.html": "Looking for the best tree service Pocatello? We offer expert tree removal Pocatello and 24/7 emergency tree service Pocatello. Call 208-417-7993 today!",
            "tree-removal/index.html": "Need professional tree removal Pocatello? Contact us for safe tree removal Pocatello and reliable emergency tree service Pocatello. Call 208-417-7993 today!",
            "emergency-tree-services/index.html": "Need emergency tree service Pocatello? Our 24/7 emergency tree service Pocatello crew handles safe tree removal Pocatello quickly. Call 208-417-7993 now!",
            "contact/index.html": "Get a free quote from Pocatello Tree Service. Contact us for professional tree removal Pocatello and 24/7 emergency tree service Pocatello. Call 208-417-7993 today!"
        }
        
        if rel_path in descriptions:
            new_desc = descriptions[rel_path]
            # Update meta name="description"
            desc_tag = soup.find('meta', attrs={'name': 'description'})
            if desc_tag:
                desc_tag['content'] = new_desc
            
            # Update og:description
            og_desc_tag = soup.find('meta', attrs={'property': 'og:description'})
            if og_desc_tag:
                og_desc_tag['content'] = new_desc
                
            # Update twitter:description
            twitter_desc_tag = soup.find('meta', attrs={'name': 'twitter:description'}) or soup.find('meta', attrs={'property': 'twitter:description'})
            if twitter_desc_tag:
                twitter_desc_tag['content'] = new_desc

        # 2. Add explicit dimensions and lazy-loading to images
        for idx, img in enumerate(soup.find_all('img')):
            src = img.get('src', '')
            # If it is the main navbar logo
            if "logo_-120x120.png" in src or "logo_.png" in src:
                img['width'] = "56"
                img['height'] = "56"
                # Navbar logo should load eagerly for LCP
                img['loading'] = "eager"
            else:
                # Add lazy loading
                img['loading'] = "lazy"
                # If it's a known placeholder or icon image, give it representative dimensions
                if not img.get('width') or not img.get('height'):
                    img['width'] = "600"
                    img['height'] = "400"

        # 3. Optimize Schema JSON-LD
        schema_tag = soup.find('script', class_='rank-math-schema')
        if schema_tag:
            try:
                schema_data = json.loads(schema_tag.string)
                graph = schema_data.get('@graph', [])
                
                # Check if Organization/TreeService schema exists
                org_item = None
                for item in graph:
                    item_type = item.get('@type', [])
                    if isinstance(item_type, str):
                        item_type = [item_type]
                    if 'TreeService' in item_type or 'Organization' in item_type:
                        org_item = item
                        break

                # If missing (subpages), inject the homepage Organization schema
                if not org_item and homepage_org_schema:
                    # Deep copy the homepage org schema
                    org_item = json.loads(json.dumps(homepage_org_schema))
                    graph.append(org_item)
                
                # Optimize the Organization / TreeService schema
                if org_item:
                    # Clean Chubbuck from areaServed
                    areas = org_item.get('areaServed', [])
                    new_areas = []
                    for area in areas:
                        if area.get('name') != 'Chubbuck':
                            new_areas.append(area)
                    org_item['areaServed'] = new_areas

                    # Standardize address
                    org_item['address'] = {
                        "@type": "PostalAddress",
                        "addressLocality": "Pocatello",
                        "addressRegion": "ID",
                        "postalCode": "83201",
                        "addressCountry": "US"
                    }

                    # Add geo coordinates
                    org_item['geo'] = {
                        "@type": "GeoCoordinates",
                        "latitude": 42.8713,
                        "longitude": -112.4455
                    }

                    # Ensure priceRange
                    org_item['priceRange'] = "$$"
                    org_item['telephone'] = "+1-208-417-7993"
                    org_item['email'] = "info@treeservicepocatelloidaho.com"

                # Check if there's an FAQ section to build FAQPage schema
                accordion_items = soup.find_all(class_='accordion-item')
                if accordion_items:
                    faq_entities = []
                    for item in accordion_items:
                        title_btn = item.find(class_='accordion-title') or item.find('button')
                        content_div = item.find(class_='accordion-content') or item.find(class_='elementor-tab-content')
                        if title_btn and content_div:
                            q_text = title_btn.get_text().replace('\n', ' ').strip()
                            a_text = content_div.get_text().replace('\n', ' ').strip()
                            faq_entities.append({
                                "@type": "Question",
                                "name": q_text,
                                "acceptedAnswer": {
                                    "@type": "Answer",
                                    "text": a_text
                                }
                            })
                    
                    if faq_entities:
                        # Find or create FAQPage schema in the graph
                        faq_item = None
                        for item in graph:
                            if item.get('@type') == 'FAQPage':
                                faq_item = item
                                break
                        
                        if not faq_item:
                            faq_item = {
                                "@type": "FAQPage",
                                "@id": f"https://www.treeservicepocatelloidaho.com/{rel_path if rel_path != 'index.html' else ''}#faq",
                                "mainEntity": []
                            }
                            graph.append(faq_item)
                        
                        faq_item['mainEntity'] = faq_entities
                        print(f"  -> Generated FAQPage schema with {len(faq_entities)} Q&As")

                schema_data['@graph'] = graph
                schema_tag.string = json.dumps(schema_data, separators=(',', ':'))
                print("  -> Optimized JSON-LD schema graph successfully.")

            except Exception as e:
                print(f"  -> Failed to optimize schema: {e}")

        # Save optimized HTML back to the file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    print("\nAll technical and on-page SEO assets optimized successfully!")

if __name__ == '__main__':
    optimize_seo()
