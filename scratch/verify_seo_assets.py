import os
import json
from bs4 import BeautifulSoup

def verify_seo_assets():
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

    print("=== VERIFYING SEO ASSETS ===")
    errors = 0

    # 1. robots.txt Verification
    robots_path = os.path.join(root_dir, "robots.txt")
    if not os.path.exists(robots_path):
        print("[ERROR] robots.txt is missing!")
        errors += 1
    else:
        with open(robots_path, 'r') as f:
            content = f.read()
            if "Sitemap:" not in content:
                print("[ERROR] robots.txt does not link to sitemap.xml!")
                errors += 1
            else:
                print("[SUCCESS] robots.txt is valid and points to the sitemap.")

    # 2. sitemap.xml Verification
    sitemap_path = os.path.join(root_dir, "sitemap.xml")
    if not os.path.exists(sitemap_path):
        print("[ERROR] sitemap.xml is missing!")
        errors += 1
    else:
        with open(sitemap_path, 'r') as f:
            content = f.read()
            # simple check for standard sitemap tags
            if "<urlset" not in content or "</urlset>" not in content:
                print("[ERROR] sitemap.xml is invalid!")
                errors += 1
            else:
                for page in pages:
                    url_loc = f"https://www.treeservicepocatelloidaho.com/{page.replace('index.html', '')}"
                    if url_loc not in content:
                        print(f"[ERROR] sitemap.xml is missing page URL: {url_loc}")
                        errors += 1
                if errors == 0:
                    print("[SUCCESS] sitemap.xml contains all 11 page URLs.")

    # 3. HTML Pages Checks
    for rel_path in pages:
        full_path = os.path.join(root_dir, rel_path.replace('/', os.sep))
        if not os.path.exists(full_path):
            print(f"[ERROR] Missing HTML page: {rel_path}")
            errors += 1
            continue

        with open(full_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Check H1 Count
        h1s = soup.find_all('h1')
        if len(h1s) != 1:
            print(f"[ERROR] {rel_path} has {len(h1s)} H1 tags instead of 1!")
            errors += 1
        
        # Check Schema JSON Validity and Coordinates
        schema_tag = soup.find('script', class_='rank-math-schema')
        if not schema_tag:
            print(f"[ERROR] {rel_path} is missing class='rank-math-schema'!")
            errors += 1
        else:
            try:
                schema_data = json.loads(schema_tag.string)
                graph = schema_data.get('@graph', [])
                
                # Check for Chubbuck in AreaServed and verify GeoCoordinates
                has_org = False
                for item in graph:
                    item_type = item.get('@type', [])
                    if isinstance(item_type, str):
                        item_type = [item_type]
                    if 'TreeService' in item_type or 'Organization' in item_type:
                        has_org = True
                        # Verify coordinate presence
                        geo = item.get('geo', {})
                        if geo.get('latitude') != 42.8713 or geo.get('longitude') != -112.4455:
                            print(f"[ERROR] {rel_path} organization schema has invalid geo coordinates: {geo}")
                            errors += 1
                        # Verify Chubbuck is removed
                        areas = item.get('areaServed', [])
                        for area in areas:
                            if area.get('name') == 'Chubbuck':
                                print(f"[ERROR] {rel_path} organization schema still serves Chubbuck!")
                                errors += 1
                if not has_org:
                    print(f"[ERROR] {rel_path} schema does not contain TreeService/Organization block!")
                    errors += 1
            except Exception as e:
                print(f"[ERROR] {rel_path} schema JSON-LD is syntactically invalid: {e}")
                errors += 1

    if errors == 0:
        print("\n[SUCCESS] All SEO verification checks passed successfully!")
    else:
        print(f"\n[FAILURE] Verification failed with {errors} error(s).")

if __name__ == '__main__':
    verify_seo_assets()
