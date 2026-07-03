import os
from bs4 import BeautifulSoup

def audit_our_site():
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

    print("=== OUR SITE SEO AUDIT ===")
    
    # Check robots.txt
    robots_path = os.path.join(root_dir, "robots.txt")
    print(f"robots.txt present: {os.path.exists(robots_path)}")
    if os.path.exists(robots_path):
        with open(robots_path, 'r') as f:
            print("--- robots.txt content ---")
            print(f.read().strip())
    
    # Check sitemap.xml
    sitemap_path = os.path.join(root_dir, "sitemap.xml")
    print(f"sitemap.xml present: {os.path.exists(sitemap_path)}")
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r') as f:
            print("--- sitemap.xml content (first 500 chars) ---")
            print(f.read(500).strip())

    print("\n=== PAGES AUDIT ===")
    for rel_path in pages:
        full_path = os.path.join(root_dir, rel_path.replace('/', os.sep))
        if not os.path.exists(full_path):
            print(f"\n[MISSING] {rel_path}")
            continue
            
        with open(full_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        print(f"\n--- Page: {rel_path} ---")
        
        # Title
        title_tag = soup.find('title')
        title_text = title_tag.text.strip() if title_tag else "N/A"
        print(f"Title ({len(title_text)} chars): {title_text}")
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        desc_text = meta_desc.get('content', 'N/A') if meta_desc else "N/A"
        print(f"Meta Desc ({len(desc_text)} chars): {desc_text}")
        
        # Headings
        h1s = soup.find_all('h1')
        print(f"H1 Count: {len(h1s)}")
        for i, h1 in enumerate(h1s):
            print(f"  H1 #{i+1}: {h1.text.strip()}")
            
        h2s = soup.find_all('h2')
        print(f"H2 Count: {len(h2s)}")
        for i, h2 in enumerate(h2s[:3]):
            print(f"  H2 #{i+1}: {h2.text.strip()}")
        if len(h2s) > 3:
            print(f"  ... and {len(h2s)-3} more H2s")

        # Schema markup
        schemas = soup.find_all('script', type='application/ld+json')
        print(f"JSON-LD schemas found: {len(schemas)}")
        for i, schema in enumerate(schemas):
            try:
                import json
                s_data = json.loads(schema.string)
                if '@graph' in s_data:
                    types = [item.get('@type') for item in s_data['@graph']]
                    print(f"  Schema #{i+1} (@graph): {types}")
                else:
                    print(f"  Schema #{i+1} (Single): {s_data.get('@type')}")
            except Exception as e:
                print(f"  Schema #{i+1} (Raw or Invalid JSON): {schema.string[:100].strip()}...")

if __name__ == '__main__':
    audit_our_site()
