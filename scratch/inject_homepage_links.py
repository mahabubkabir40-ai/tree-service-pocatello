import os
import re
from bs4 import BeautifulSoup

def inject_homepage_links():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    homepage_path = os.path.join(root_dir, "index.html")
    
    with open(homepage_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    # Match rules: (keyword, target_path)
    # We match in order of priority (more specific first)
    RULES = [
        ("tree service in Pocatello, Idaho", "services/"),
        ("tree service in Pocatello, ID", "services/"),
        ("tree service companies", "services/"),
        ("tree service company", "services/"),
        ("tree service", "services/"),
        
        ("emergency tree removal", "emergency-tree-services/"),
        ("emergency arbor care", "emergency-tree-services/"),
        
        ("tree stump removal or grinding", "stump-removal-grinding/"),
        ("tree stump removal", "stump-removal-grinding/"),
        ("stump grinding", "stump-removal-grinding/"),
        ("stump removal", "stump-removal-grinding/"),
        
        ("cabling and bracing", "cabling-bracing/"),
        ("cabling & bracing", "cabling-bracing/"),
        
        ("shrub removal", "shrub-removal/"),
        
        ("tree removal", "tree-removal/"),
        ("tree trimming", "tree-trimming/"),
        ("trim or remove", "services/"),
        ("remove or trim", "services/"),
        
        ("contact us", "contact/"),
        ("contact our team", "contact/"),
    ]
    
    sections = soup.find_all('section')
    for sec in sections:
        sec_text = sec.get_text().lower()
        # Skip sections where we don't want to inject paragraph links
        if "frequently asked questions" in sec_text or "what our clients say" in sec_text or "serving the greater" in sec_text or "contact our arborist team" in sec_text or "call cta" in sec.get('id', ''):
            continue
            
        paragraphs = sec.find_all('p')
        for p in paragraphs:
            # Skip if paragraph is inside hero card, trust badge, or hero layout
            parent_classes = []
            for parent in p.parents:
                parent_classes.extend(parent.get('class', []))
            if 'hero-card' in parent_classes or 'hero-content' in parent_classes or 'hero-trust' in parent_classes:
                continue
                
            # Skip if it already has a link
            if p.find('a'):
                continue
                
            p_text = p.get_text()
            
            # Find first matching keyword
            for kw, target in RULES:
                pattern = re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE)
                match = pattern.search(p_text)
                if match:
                    start, end = match.span()
                    matched_text = p_text[start:end]
                    
                    new_link = soup.new_tag('a', href=target)
                    new_link.string = matched_text
                    
                    p.clear()
                    p.append(p_text[:start])
                    p.append(new_link)
                    p.append(p_text[end:])
                    break
                    
    with open(homepage_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print("Homepage link injection completed successfully!")

if __name__ == "__main__":
    inject_homepage_links()
