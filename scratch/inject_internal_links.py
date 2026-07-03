import os
import re
from bs4 import BeautifulSoup

def inject_links():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
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

    # Keyword rules: (keyword_pattern, subpage_target, subpage_anchor_text)
    # Target path is relative to the root directory
    LINK_RULES = [
        (r"\btree service pocatello\b", "", "tree service Pocatello"),
        (r"\btree service in pocatello\b", "", "tree service in Pocatello"),
        (r"\bpocatello tree service\b", "", "Pocatello Tree Service"),
        
        (r"\btree removal pocatello\b", "tree-removal/", "tree removal Pocatello"),
        (r"\btree removal in pocatello\b", "tree-removal/", "tree removal in Pocatello"),
        (r"\bemergency tree removal\b", "emergency-tree-services/", "emergency tree removal"),
        (r"\btree removal\b", "tree-removal/", "tree removal"),
        
        (r"\btree trimming\b", "tree-trimming/", "tree trimming"),
        (r"\btree pruning\b", "tree-trimming/", "tree pruning"),
        (r"\bpruning\b", "tree-trimming/", "tree pruning"),
        (r"\btrimming\b", "tree-trimming/", "tree trimming"),
        
        (r"\bstump grinding\b", "stump-removal-grinding/", "stump grinding"),
        (r"\bstump removal\b", "stump-removal-grinding/", "stump removal"),
        
        (r"\bcabling and bracing\b", "cabling-bracing/", "cabling and bracing"),
        (r"\bcabling & bracing\b", "cabling-bracing/", "cabling & bracing"),
        
        (r"\bshrub removal\b", "shrub-removal/", "shrub removal"),
        
        (r"\bemergency tree service\b", "emergency-tree-services/", "emergency tree service"),
        (r"\bemergency services\b", "emergency-tree-services/", "emergency services"),
        (r"\bstorm cleanup\b", "emergency-tree-services/", "storm cleanup"),
        
        (r"\babout us\b", "about/", "about us"),
        
        (r"\bcontact us\b", "contact/", "contact us"),
        (r"\bget a free quote\b", "contact/", "get a free quote"),
        (r"\bfree estimate\b", "contact/", "free estimate"),
        (r"\bfree quote\b", "contact/", "free quote")
    ]

    for rel_path in pages:
        full_path = os.path.join(root_dir, rel_path.replace('/', os.sep))
        if not os.path.exists(full_path):
            continue
            
        print(f"Injecting links in: {rel_path}")
        with open(full_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        # Determine prefix based on page depth
        is_homepage = (rel_path == "index.html")
        prefix = "" if is_homepage else "../"
        
        # Find the main content article or body area
        content_area = soup.find('article') or soup.find(class_='entry-content') or soup.find('main')
        if not content_area:
            continue
            
        paragraphs = content_area.find_all('p')
        for p in paragraphs:
            # Skip short paragraphs or those already containing a link
            if len(p.get_text().strip()) < 15:
                continue
                
            # If paragraph already has a link, let's skip to keep it natural
            if p.find('a'):
                continue
                
            p_text = p.get_text()
            linked = False
            
            # Try to match keywords
            for pattern, target_path, anchor in LINK_RULES:
                # Do not link to the page itself
                current_page_dir = rel_path.split('/')[0] + "/" if '/' in rel_path else ""
                if target_path == current_page_dir and not is_homepage:
                    continue
                if is_homepage and target_path == "":
                    continue
                    
                match = re.search(pattern, p_text, re.IGNORECASE)
                if match:
                    start, end = match.span()
                    matched_text = p_text[start:end]
                    
                    # Create the link element
                    href = f"{prefix}{target_path}"
                    if not href:
                        href = f"{prefix}index.html"
                        
                    new_link = soup.new_tag('a', href=href)
                    new_link.string = matched_text
                    
                    # Replace the text in the paragraph
                    # To do this safely without breaking other tags, we work on children strings
                    p.clear()
                    p.append(p_text[:start])
                    p.append(new_link)
                    p.append(p_text[end:])
                    linked = True
                    break
            
            # If no keyword matched, append a generic call-to-action link at the end
            if not linked:
                # Let's add a natural trailing link
                href = f"{prefix}contact/"
                # If we are on contact page, link to home or services
                if "contact/" in rel_path:
                    href = f"{prefix}services/"
                    anchor_text = "services page"
                else:
                    anchor_text = "contact us today"
                    
                new_link = soup.new_tag('a', href=href)
                new_link.string = anchor_text
                
                # Append to existing text
                p_text_stripped = p_text.rstrip(' .')
                p.clear()
                p.append(p_text_stripped)
                p.append("—feel free to ")
                p.append(new_link)
                p.append(" for more information.")
                
        # Save updated page
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    print("Link injection completed successfully!")

if __name__ == "__main__":
    inject_links()
