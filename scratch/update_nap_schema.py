import os

# Define target directories and files to scan
root_dir = "c:\\Users\\USER\\Desktop\\Tree Service Pocatello"

target_files = []
for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".html") and "wp-content" not in dirpath and "wp-includes" not in dirpath:
            target_files.append(os.path.join(dirpath, filename))

print(f"Found {len(target_files)} HTML files to update.")

# Schema replacements
old_address = '"address":{"@type":"PostalAddress","addressLocality":"Pocatello","addressRegion":"ID","postalCode":"83201","addressCountry":"US"}'
new_address = '"address":{"@type":"PostalAddress","streetAddress":"228 Center St","addressLocality":"Pocatello","addressRegion":"ID","postalCode":"83204","addressCountry":"US"}'

old_geo = '"geo":{"@type":"GeoCoordinates","latitude":42.8713,"longitude":-112.4455}'
new_geo = '"geo":{"@type":"GeoCoordinates","latitude":42.942867,"longitude":-112.347176}'

# Footer address replacement
old_footer_addr1 = '<p><i class="fas fa-map-marker-alt"></i>Pocatello, ID</p>'
new_footer_addr1 = '<p><i class="fas fa-map-marker-alt" style="margin-right: 8px;"></i>228 Center St, Pocatello, ID 83204</p>'

# Sometimes there's a space or style in the marker icon
old_footer_addr2 = '<p><i class="fas fa-map-marker-alt" style="color: var(--color-primary); margin-right: 8px;"></i> Pocatello, ID</p>'
new_footer_addr2 = '<p><i class="fas fa-map-marker-alt" style="color: var(--color-primary); margin-right: 8px;"></i> 228 Center St, Pocatello, ID 83204</p>'

for file_path in target_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    
    # 1. Schema address
    if old_address in content:
        content = content.replace(old_address, new_address)
        modified = True
        
    # 2. Schema geo coordinates
    if old_geo in content:
        content = content.replace(old_geo, new_geo)
        modified = True
        
    # 3. Footer address variations
    if old_footer_addr1 in content:
        content = content.replace(old_footer_addr1, new_footer_addr1)
        modified = True
        
    if old_footer_addr2 in content:
        content = content.replace(old_footer_addr2, new_footer_addr2)
        modified = True

    # 4. Contact page specific replacements
    if "contact" in file_path:
        # Map iframe replacement
        old_iframe = 'src="https://maps.google.com/maps?q=Pocatello%2C%20ID&amp;t=m&amp;z=12&amp;output=embed&amp;iwloc=near"'
        new_iframe = 'src="https://maps.google.com/maps?q=228%20Center%20St%2C%20Pocatello%2C%20ID%2083204&amp;t=m&amp;z=14&amp;output=embed&amp;iwloc=near"'
        if old_iframe in content:
            content = content.replace(old_iframe, new_iframe)
            modified = True
            
        old_aria_label = 'aria-label="Pocatello, Idaho, USA"'
        new_aria_label = 'aria-label="228 Center St, Pocatello, ID 83204"'
        if old_aria_label in content:
            content = content.replace(old_aria_label, new_aria_label)
            modified = True
            
        old_title = 'title="Pocatello, Idaho, USA"'
        new_title = 'title="228 Center St, Pocatello, ID 83204"'
        if old_title in content:
            content = content.replace(old_title, new_title)
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully updated: {os.path.relpath(file_path, root_dir)}")

print("Bulk replacement complete.")
