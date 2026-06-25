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

def verify_files():
    root_dir = r"c:\Users\USER\Desktop\Tree Service Pocatello"
    modified_files = [
        "index.html",
        "blackfoot-idaho/index.html",
        "chubbuck-idaho/index.html",
        "tree-removal/index.html",
        "tree-service-caldwell-idaho/index.html",
        "tree-service-twin-falls/index.html"
    ]
    
    for relative_path in modified_files:
        full_path = os.path.join(root_dir, relative_path.replace('/', os.sep))
        print(f"Verifying {relative_path}...")
        
        if not os.path.exists(full_path):
            print(f"Error: File does not exist at {full_path}")
            continue
            
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verify script presence
        if 'Accordion Logic' not in content:
            print(f"Error: Script missing in {relative_path}")
            continue
            
        # Basic HTML parsing check
        parser = SimpleHTMLValidator()
        try:
            parser.feed(content)
            print(f"Success: {relative_path} parses cleanly as HTML.")
        except Exception as e:
            print(f"Error parsing {relative_path}: {e}")

if __name__ == '__main__':
    verify_files()
