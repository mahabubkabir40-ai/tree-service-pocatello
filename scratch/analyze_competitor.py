import os
from bs4 import BeautifulSoup

def analyze():
    filepath = r"C:\Users\USER\\.gemini\\antigravity\\brain\\00651c66-d23b-49d4-aa84-8e1e7f7e3075\\.system_generated\\steps\\1421\\content.md"
    if not os.path.exists(filepath):
        # try single backslash
        filepath = filepath.replace("\\\\", "\\")
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the HTML part
    html_start = content.find("<!DOCTYPE")
    if html_start == -1:
        html_start = content.find("<html")
    
    html_content = content[html_start:] if html_start != -1 else content

    soup = BeautifulSoup(html_content, 'html.parser')

    print("=== COMPETITOR SITE SEO AUDIT ===")
    
    # 1. Metadata
    title_tag = soup.find('title')
    print(f"Title: {title_tag.text if title_tag else 'N/A'}")
    
    meta_desc = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    print(f"Meta Description: {meta_desc.get('content') if meta_desc else 'N/A'}")

    # 2. Headings
    print("\n=== HEADINGS ===")
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        print(f"{heading.name.upper()}: {heading.text.strip()}")

    # 3. Schema
    print("\n=== SCHEMAS ===")
    schemas = soup.find_all('script', type='application/ld+json')
    print(f"Found {len(schemas)} JSON-LD schema(s).")
    for i, schema in enumerate(schemas):
        print(f"--- Schema {i+1} ---")
        print(schema.string[:1000] if schema.string else "Empty")

    # 4. Links and CTAs
    print("\n=== LINKS & CTAs ===")
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if 'tel:' in href or 'mailto:' in href or 'contact' in href or 'http' in href:
            print(f"Link: '{a.text.strip()}' -> {href}")

if __name__ == '__main__':
    analyze()
