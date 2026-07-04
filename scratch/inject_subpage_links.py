import os
import re

def inject_subpage_links():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define the replacements per file
    # Format: { relative_file_path: [ (target_string_to_find, replacement_string_with_links) ] }
    REPLACEMENTS = {
        "tree-removal/index.html": [
            (
                "<p>Pocatello Tree Service is a company dedicated to fast and efficient responses to any tree related services such as tree removal, tree trimming, stump removal and grinding, tree cabling and bracing, emergency tree removal services either for residential areas or commercial establishments.</p>",
                "<p>At <a href=\"../\">Pocatello Tree Service</a>, we are dedicated to fast and efficient responses to any tree related services such as tree removal, <a href=\"../tree-trimming/\">tree trimming</a>, <a href=\"../stump-removal-grinding/\">stump removal and grinding</a>, tree cabling and bracing, emergency tree removal services either for residential areas or commercial establishments.</p>"
            ),
            (
                "emergency tree removal services either for residential areas or commercial establishments.</p>",
                "emergency tree removal, and <a href=\"../shrub-removal/\">shrub removal</a> services for both residential and commercial properties.</p>"
            ),
            (
                "climate of Bannock County, weather",
                "climate of <a href=\"https://en.wikipedia.org/wiki/Bannock_County,_Idaho\" target=\"_blank\" rel=\"noopener noreferrer\">Bannock County</a>, weather"
            )
        ],
        "tree-trimming/index.html": [
            (
                "<p>Proper tree trimming and pruning are essential for maintaining the health, beauty, and safety of your property's canopy.",
                "<p>At <a href=\"../\">Pocatello Tree Service</a>, we believe proper tree trimming and pruning are essential for maintaining the health, beauty, and safety of your property's canopy."
            ),
            (
                "<p>Deciding whether to trim a tree or remove it entirely depends on its health, structure, and position.",
                "<p>Deciding whether to trim a tree or perform a complete <a href=\"../tree-removal/\">tree removal</a> depends on its health, structure, and position."
            ),
            (
                "keeping your trees healthy, safe, and looking their best year-round.</p>",
                "keeping your trees healthy, safe, and looking their best year-round. If a tree has structural splits but is otherwise healthy, we may also recommend a <a href=\"../cabling-bracing/\">tree cabling and bracing</a> support system.</p>"
            ),
            (
                "clean, professional pruning cuts",
                "clean, professional <a href=\"https://en.wikipedia.org/wiki/Pruning\" target=\"_blank\" rel=\"noopener noreferrer\">pruning</a> cuts"
            )
        ],
        "stump-removal-grinding/index.html": [
            (
                "At Pocatello Tree Service, we offer professional, efficient mobile stump grinding and complete stump removal services throughout Pocatello",
                "At <a href=\"../\">Pocatello Tree Service</a>, we offer professional, efficient mobile stump grinding and complete stump removal services throughout Pocatello"
            ),
            (
                "or build structures directly over the former tree site.</li>",
                "or build structures directly over the former tree site after a <a href=\"../tree-removal/\">tree removal</a>.</li>"
            ),
            (
                "protecting your yard's landscape value.</p>",
                "protecting your yard's landscape value. To keep the rest of your canopy healthy, we also provide expert <a href=\"../tree-trimming/\">tree trimming</a> and pruning services.</p>"
            ),
            (
                "protecting your yard's landscape value",
                "protecting your yard's <a href=\"https://en.wikipedia.org/wiki/Landscaping\" target=\"_blank\" rel=\"noopener noreferrer\">landscape value</a>"
            )
        ],
        "cabling-bracing/index.html": [
            (
                "At Pocatello Tree Service, we offer professional tree cabling and bracing services in the Pocatello and Chubbuck areas.",
                "At <a href=\"../\">Pocatello Tree Service</a>, we offer professional tree cabling and bracing services in the Pocatello and Chubbuck areas."
            ),
            (
                "Don’t worry, we offer not only tree cabling and bracing in Pocatello but also tree trimming and removal services.",
                "Don’t worry, we offer not only tree cabling and bracing in Pocatello but also professional <a href=\"../tree-trimming/\">tree trimming</a> and removal services."
            ),
            (
                "trim the tree, brace or cable it, or just remove it entirely.",
                "trim the tree, brace or cable it, or perform a complete <a href=\"../tree-removal/\">tree removal</a>."
            ),
            (
                "co-dominant stems",
                "<a href=\"https://en.wikipedia.org/wiki/Co-dominant_stem\" target=\"_blank\" rel=\"noopener noreferrer\">co-dominant stems</a>"
            )
        ],
        "shrub-removal/index.html": [
            (
                "At Pocatello Tree Service, we provide professional shrub removal, hedge clearing, and land prep services",
                "At <a href=\"../\">Pocatello Tree Service</a>, we provide professional shrub removal, hedge clearing, and land prep services"
            ),
            (
                "removing mature shrubs is a labor-intensive task that requires the right equipment",
                "just like a full <a href=\"../tree-removal/\">tree removal</a>, removing mature shrubs is a labor-intensive task that requires the right equipment"
            ),
            (
                "grind down or excavate root balls, and ensure the site is left clean and safe.",
                "perform any needed <a href=\"../stump-removal-grinding/\">stump grinding</a> or root ball excavation, and ensure the site is left clean and safe."
            ),
            (
                "decrease your property's curb appeal",
                "decrease your property's <a href=\"https://en.wikipedia.org/wiki/Curb_appeal\" target=\"_blank\" rel=\"noopener noreferrer\">curb appeal</a>"
            )
        ],
        "emergency-tree-services/index.html": [
            (
                "At Pocatello Tree Service, we provide 24/7 rapid mobilization emergency tree services throughout Pocatello",
                "At <a href=\"../\">Pocatello Tree Service</a>, we provide 24/7 rapid mobilization emergency tree services throughout Pocatello"
            ),
            (
                "Usually, with emergency tree removal services, time is of the essence.",
                "Usually, with emergency <a href=\"../tree-removal/\">tree removal</a> services, time is of the essence."
            ),
            (
                "preventative measures like cabling and bracing trees.",
                "preventative measures like <a href=\"../cabling-bracing/\">cabling and bracing</a> trees."
            ),
            (
                "lightning strikes, heavy",
                "<a href=\"https://en.wikipedia.org/wiki/Lightning\" target=\"_blank\" rel=\"noopener noreferrer\">lightning strikes</a>, heavy"
            )
        ]
    }
    
    for rel_path, reps in REPLACEMENTS.items():
        file_path = os.path.join(root_dir, rel_path.replace('/', os.sep))
        if not os.path.exists(file_path):
            print(f"Skipping (not found): {rel_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        for target, replacement in reps:
            # Try exact replacement
            if target in content:
                content = content.replace(target, replacement)
            else:
                # Try normalized whitespace replacement in case of spacing differences
                normalized_target = re.sub(r'\s+', ' ', target).strip().lower()
                # Find matching block in content
                found = False
                for block in re.split(r'(<[^>]+>)', content):
                    normalized_block = re.sub(r'\s+', ' ', block).strip().lower()
                    if normalized_target in normalized_block:
                        # Direct replacement might fail on multi-line blocks, let's warning
                        pass
                
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully injected links in: {rel_path}")
        else:
            print(f"Warning: No links injected in {rel_path} (could not find target content strings)")

if __name__ == "__main__":
    inject_subpage_links()
