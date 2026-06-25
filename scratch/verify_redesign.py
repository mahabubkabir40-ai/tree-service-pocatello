import os
from html.parser import HTMLParser

class SimpleHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)

    def handle_endtag(self, tag):
        if self.tags and self.tags[-1] == tag:
            self.tags.pop()

def verify_site():
    root_dir = r"c:\Users\USER\Desktop\Tree Service Pocatello"
    
    html_files = [
        ("index.html", "index.css"),
        ("tree-removal/index.html", "../index.css"),
        ("tree-trimming/index.html", "../index.css"),
        ("stump-removal-grinding/index.html", "../index.css"),
        ("cabling-bracing/index.html", "../index.css"),
        ("shrub-removal/index.html", "../index.css"),
        ("emergency-tree-services/index.html", "../index.css"),
        ("about/index.html", "../index.css"),
        ("services/index.html", "../index.css"),
        ("chubbuck-idaho/index.html", "../index.css"),
        ("blackfoot-idaho/index.html", "../index.css"),
        ("tree-service-caldwell-idaho/index.html", "../index.css"),
        ("tree-service-twin-falls/index.html", "../index.css"),
        ("privacy-policy/index.html", "../index.css"),
        ("contact/index.html", "../index.css")
    ]
    
    errors_found = 0
    
    for relative_path, expected_css in html_files:
        full_path = os.path.join(root_dir, relative_path.replace('/', os.sep))
        print(f"Checking {relative_path}...")
        
        if not os.path.exists(full_path):
            print(f"  [ERROR] File missing: {relative_path}")
            errors_found += 1
            continue
            
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verify index.css stylesheet linkage
        if expected_css not in content:
            print(f"  [ERROR] Missing stylesheet reference '{expected_css}' in {relative_path}")
            errors_found += 1
            
        # Verify FontAwesome is present
        if "all.min.css" not in content:
            print(f"  [ERROR] Missing FontAwesome stylesheet in {relative_path}")
            errors_found += 1
            
        # Check if Rank Math schema block is present (except for privacy-policy which didn't have one)
        if "privacy-policy" not in relative_path and "rank-math-schema" not in content:
            print(f"  [WARNING] Schema script block missing in {relative_path}")
            
        # Verify title is not empty
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if not title_match or not title_match.group(1).strip():
            print(f"  [ERROR] Empty or missing title tag in {relative_path}")
            errors_found += 1
            
        # HTML Parse Check
        parser = SimpleHTMLValidator()
        try:
            parser.feed(content)
            print(f"  [SUCCESS] parsed cleanly.")
        except Exception as e:
            print(f"  [ERROR] parsing error in {relative_path}: {e}")
            errors_found += 1
            
    # Print page weights
    homepage_size_kb = os.path.getsize(os.path.join(root_dir, "index.html")) / 1024.0
    css_size_kb = os.path.getsize(os.path.join(root_dir, "index.css")) / 1024.0
    print("\n--- Site Metrics ---")
    print(f"Homepage File Size: {homepage_size_kb:.2f} KB (Target: < 50KB)")
    print(f"Global CSS File Size: {css_size_kb:.2f} KB (Target: < 30KB)")
    print(f"Combined weight: {homepage_size_kb + css_size_kb:.2f} KB")
    
    if errors_found == 0:
        print("\nAll verification checks passed successfully!")
    else:
        print(f"\nVerification finished with {errors_found} errors.")

import re
if __name__ == '__main__':
    verify_site()
