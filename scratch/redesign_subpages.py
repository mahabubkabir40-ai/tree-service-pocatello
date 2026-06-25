import os
import re
from html.parser import HTMLParser

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_head = False
        self.in_body = False
        
        self.title = ""
        self.meta_tags = []
        self.canonical = ""
        self.schema = ""
        
        self.elements = []
        self.current_tag = None
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'head':
            self.in_head = True
        elif tag == 'body':
            self.in_body = True
            
        if self.in_head:
            if tag == 'title':
                self.in_title = True
            elif tag == 'meta':
                name = attrs_dict.get('name', '')
                prop = attrs_dict.get('property', '')
                content = attrs_dict.get('content', '')
                if any(k in name or k in prop for k in ['description', 'robots', 'og:', 'twitter:', 'viewport']):
                    self.meta_tags.append((name, prop, content))
            elif tag == 'link' and attrs_dict.get('rel') == 'canonical':
                self.canonical = attrs_dict.get('href', '')
            elif tag == 'script' and attrs_dict.get('class') == 'rank-math-schema':
                self.current_tag = 'schema'
                self.current_text = []
                
        if self.in_body:
            if tag in ['h1', 'h2', 'h3', 'p']:
                cls = attrs_dict.get('class', '')
                if 'menu' not in cls and 'logo' not in cls:
                    self.current_tag = tag
                    self.current_text = []

    def handle_endtag(self, tag):
        if tag == 'head':
            self.in_head = False
        elif tag == 'body':
            self.in_body = False
        elif tag == 'title':
            self.in_title = False
            
        if self.current_tag:
            text = " ".join(self.current_text).strip()
            text = re.sub(r'\s+', ' ', text)
            if text:
                if self.current_tag == 'schema':
                    self.schema = text
                else:
                    self.elements.append((self.current_tag, text))
            self.current_tag = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.current_tag:
            self.current_text.append(data)

# Rebuild Template using simple placeholders
TEMPLATE = """<!DOCTYPE html>
<html lang="en-US" prefix="og: https://ogp.me/ns#">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <link href="https://gmpg.org/xfn/11" rel="profile"/>
  
  <title>__TITLE__</title>
__META__
__CANONICAL__
__SCHEMA__
  
  <!-- Favicon -->
  <link rel="icon" href="__PREFIX__wp-content/uploads/2021/04/cropped-Tree-Service-Pocatello-fav-32x32.jpg" sizes="32x32" />
  
  <!-- FontAwesome Icons -->
  <link href="__PREFIX__wp-content/plugins/elementor/assets/lib/font-awesome/css/all.min.css" rel="stylesheet"/>
  
  <!-- Custom Redesigned Mobile-First Stylesheet -->
  <link href="__PREFIX__index.css" rel="stylesheet"/>
 </head>
 
 <body>
  <!-- Header / Navigation -->
  <header class="header-wrapper">
   <div class="container navbar">
    <a class="logo-link" href="__PREFIX__">
     <img alt="Pocatello Tree Service Logo" src="__PREFIX__wp-content/uploads/2021/04/Tree-Service-Pocatello.logo_-120x120.png" style="width: 48px; height: 48px; object-fit: contain;"/>
     <span class="logo-text">Pocatello<span> Tree</span></span>
    </a>
    
    <nav>
     <ul class="nav-menu">
      <li><a class="nav-link" href="__PREFIX__">Home</a></li>
      <li><a class="nav-link" href="__PREFIX__services/">Services</a></li>
      <li><a class="nav-link" href="__PREFIX__about/">About</a></li>
      <li><a class="nav-link" href="__PREFIX__contact/">Contact</a></li>
     </ul>
    </nav>
    
    <div class="nav-cta">
     <a class="btn btn-secondary" href="tel:208-417-7993">
      <i class="fas fa-phone-alt" style="margin-right: 8px; color: var(--color-primary);"></i>208-417-7993
     </a>
     <a class="btn btn-primary" href="__PREFIX__#estimate-form">Free Estimate</a>
    </div>
    
    <button aria-label="Toggle Navigation" class="mobile-nav-toggle">
     <span></span>
     <span></span>
     <span></span>
    </button>
   </div>
   
   <!-- Mobile Slide-out Menu -->
   <div class="mobile-nav-menu">
    <a class="mobile-nav-link" href="__PREFIX__">Home</a>
    <a class="mobile-nav-link" href="__PREFIX__services/">Services</a>
    <a class="mobile-nav-link" href="__PREFIX__about/">About</a>
    <a class="mobile-nav-link" href="__PREFIX__contact/">Contact</a>
    <div class="mobile-nav-cta">
     <a class="btn btn-primary" href="tel:208-417-7993">
      <i class="fas fa-phone-alt" style="margin-right: 8px;"></i>Call Now: 208-417-7993
     </a>
     <a class="btn btn-secondary" href="__PREFIX__#estimate-form">Get Free Estimate</a>
    </div>
   </div>
  </header>

  <main>
   <!-- Page Header -->
   <section class="page-header text-center">
    <div class="container" style="position: relative; z-index: 2;">
     <span class="badge" style="background-color: rgba(255,255,255,0.1); color: var(--color-primary);"><i class="fas fa-tree"></i> Pocatello Tree Service</span>
     <h1 style="color: var(--color-white); margin-top: var(--spacing-xs);">__HEADER_H1__</h1>
    </div>
   </section>
__MAIN_CONTENT__
  </main>

  <!-- Footer -->
  <footer class="footer">
   <div class="container footer-top">
    <div class="footer-about">
     <h3>Pocatello Tree Service</h3>
     <p>
      Providing top-tier tree care, safe crane removals, hazard trimming, and emergency cleanup in Bannock County. Fully licensed, insured, and committed to local safety protocols.
     </p>
    </div>
    <div>
     <h4>Quick Links</h4>
     <ul class="footer-links">
      <li><a href="__PREFIX__">Home</a></li>
      <li><a href="__PREFIX__services/">Services</a></li>
      <li><a href="__PREFIX__about/">About Us</a></li>
      <li><a href="__PREFIX__contact/">Contact Us</a></li>
     </ul>
    </div>
    <div class="footer-contact">
     <h4>Contact Us</h4>
     <p><i class="fas fa-phone-alt"></i>208-417-7993</p>
     <p><i class="fas fa-envelope"></i>info@treeservicepocatelloidaho.com</p>
     <p><i class="fas fa-map-marker-alt"></i>Pocatello, ID</p>
    </div>
   </div>
   
   <div class="container footer-bottom">
    <p>&copy; 2026 Pocatello Tree Service. All Rights Reserved.</p>
    <div style="display: flex; gap: var(--spacing-sm);">
     <a href="__PREFIX__chubbuck-idaho/">Chubbuck</a> | 
     <a href="__PREFIX__blackfoot-idaho/">Blackfoot</a> | 
     <a href="__PREFIX__tree-service-caldwell-idaho/">Caldwell</a> | 
     <a href="__PREFIX__tree-service-twin-falls/">Tree Service Twin Falls</a>
    </div>
   </div>
  </footer>

  <!-- Script for Mobile Navigation Menu -->
  <script>
   document.addEventListener('DOMContentLoaded', function() {
     var mobileToggle = document.querySelector('.mobile-nav-toggle');
     var mobileMenu = document.querySelector('.mobile-nav-menu');
     
     if (mobileToggle && mobileMenu) {
       mobileToggle.addEventListener('click', function() {
         var isOpen = mobileMenu.classList.contains('open');
         if (isOpen) {
           mobileMenu.classList.remove('open');
           mobileToggle.classList.remove('open');
         } else {
           mobileMenu.classList.add('open');
           mobileToggle.classList.add('open');
         }
       });
     }
   });
  </script>
 </body>
</html>
"""

def redesign_file(file_path, rel_path_prefix, is_contact=False, is_privacy=False):
    print(f"Parsing: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    parser = ContentExtractor()
    parser.feed(html_content)
    
    title = parser.title.strip()
    title = re.sub(r'\s+', ' ', title)
    
    # Build head meta tags
    head_meta_html = ""
    for name, prop, content in parser.meta_tags:
        if name:
            head_meta_html += f'  <meta name="{name}" content="{content}"/>\n'
        elif prop:
            head_meta_html += f'  <meta property="{prop}" content="{content}"/>\n'
            
    canonical_html = f'  <link rel="canonical" href="{parser.canonical}"/>' if parser.canonical else ""
    schema_html = f'  <script class="rank-math-schema" type="application/ld+json">{parser.schema}</script>' if parser.schema else ""
    
    # Extract main content
    content_html = ""
    has_h1 = False
    
    for tag, text in parser.elements:
        # Filter out common boilerplate
        if any(nav_term in text.lower() for nav_term in ['home', 'services', 'about us', 'contact us', 'call us', 'get a free', 'rated #1', 'copy &copy;', 'all rights reserved']):
            continue
            
        if tag == 'h1':
            content_html += f'      <h1>{text}</h1>\n'
            has_h1 = True
        elif tag == 'h2':
            content_html += f'      <h2>{text}</h2>\n'
        elif tag == 'h3':
            content_html += f'      <h3>{text}</h3>\n'
        elif tag == 'p':
            content_html += f'      <p>{text}</p>\n'
            
    header_h1 = title.split('|')[0].strip()
    if not has_h1:
        content_html = f'      <h1>{header_h1}</h1>\n' + content_html
        
    # Choose Template Layout
    main_section_content = ""
    
    if is_contact:
        main_section_content = """
   <!-- Contact Page Layout -->
   <div class="container section">
    <div class="grid grid-2">
     <!-- Contact Info & Map -->
     <div>
      <h2>Get In Touch</h2>
      <p>We are a fully mobile tree service business serving Pocatello, Chubbuck, Blackfoot, and surrounding Southeast Idaho communities.</p>
      
      <div style="margin: var(--spacing-md) 0;">
       <p style="font-weight: 600;"><i class="fas fa-phone-alt" style="color: var(--color-primary); margin-right: 8px;"></i> 208-417-7993</p>
       <p style="font-weight: 600;"><i class="fas fa-envelope" style="color: var(--color-primary); margin-right: 8px;"></i> info@treeservicepocatelloidaho.com</p>
       <p style="font-weight: 600;"><i class="fas fa-map-marker-alt" style="color: var(--color-primary); margin-right: 8px;"></i> Pocatello, ID</p>
       <p style="font-weight: 600;"><i class="fas fa-clock" style="color: var(--color-primary); margin-right: 8px;"></i> Mon - Sat: 9:00 AM - 8:00 PM</p>
      </div>
      
      <div class="location-map-wrapper">
       <iframe aria-label="Pocatello, Idaho, USA" loading="lazy" src="https://maps.google.com/maps?q=Pocatello%2C%20ID&amp;t=m&amp;z=12&amp;output=embed&amp;iwloc=near" title="Pocatello, Idaho, USA"></iframe>
      </div>
     </div>
     
     <!-- Contact Form -->
     <div>
      <form class="form-card" data-netlify="true" method="POST" name="contact-form">
       <input name="form-name" type="hidden" value="contact-form"/>
       <div class="form-row">
        <div class="form-group">
         <label for="contact-name">Your Name</label>
         <input class="form-control" id="contact-name" name="name" required="" type="text"/>
        </div>
        <div class="form-group">
         <label for="contact-phone">Phone Number</label>
         <input class="form-control" id="contact-phone" name="phone" required="" type="tel"/>
        </div>
       </div>
       
       <div class="form-group">
        <label for="contact-email">Email Address</label>
        <input class="form-control" id="contact-email" name="email" required="" type="email"/>
       </div>
       
       <div class="form-group">
        <label for="contact-subject">Subject</label>
        <input class="form-control" id="contact-subject" name="subject" required="" type="text"/>
       </div>
       
       <div class="form-group">
        <label for="contact-message">Message</label>
        <textarea class="form-control" id="contact-message" name="message" required="" placeholder="How can we help you?"></textarea>
       </div>
       
       <button class="btn btn-primary btn-block" type="submit">Send Message</button>
      </form>
     </div>
    </div>
   </div>
"""
    elif is_privacy:
        main_section_content = f"""
   <!-- Privacy Page Layout -->
   <div class="container section" style="max-width: 800px;">
    <article class="content-area">
{content_html}
    </article>
   </div>
"""
    else:
        # Standard Sidebar Layout for service & location landing pages
        main_section_content = f"""
   <!-- Sidebar & Content Layout -->
   <div class="container section">
    <div class="sidebar-layout">
     <!-- Main Content Area -->
     <article class="content-area">
{content_html}
     </article>
     
     <!-- Sidebar Area -->
     <aside class="sidebar-area">
      <!-- Call Widget -->
      <div class="sidebar-widget text-center" style="background-color: var(--color-dark); color: var(--color-white); border-radius: var(--radius-md);">
       <h4 style="color: var(--color-white); border-color: var(--color-primary);">Need Fast Service?</h4>
       <p style="font-size: 0.95rem; color: rgba(255,255,255,0.85); margin-bottom: var(--spacing-sm);">
        Contact our arborist team now for a free, no-obligation quote.
       </p>
       <a class="btn btn-primary btn-block" href="tel:208-417-7993" style="margin-bottom: var(--spacing-xs);">
        <i class="fas fa-phone-alt" style="margin-right: 8px;"></i>208-417-7993
       </a>
       <a class="btn btn-secondary btn-block" href="{rel_path_prefix}contact/" style="border-color: var(--color-white); color: var(--color-white);">
        Contact Form
       </a>
      </div>
      
      <!-- Services Menu Widget -->
      <div class="sidebar-widget">
       <h4>Our Tree Services</h4>
       <ul class="footer-links" style="color: var(--color-dark-text);">
        <li><a href="{rel_path_prefix}tree-removal/">Tree Removal</a></li>
        <li><a href="{rel_path_prefix}tree-trimming/">Tree Trimming</a></li>
        <li><a href="{rel_path_prefix}stump-removal-grinding/">Stump Grinding</a></li>
        <li><a href="{rel_path_prefix}cabling-bracing/">Cabling &amp; Bracing</a></li>
        <li><a href="{rel_path_prefix}shrub-removal/">Shrub Removal</a></li>
        <li><a href="{rel_path_prefix}emergency-tree-services/">Emergency Services</a></li>
       </ul>
      </div>
     </aside>
    </div>
   </div>
"""

    new_html = TEMPLATE.replace("__TITLE__", title)\
                       .replace("__META__", head_meta_html)\
                       .replace("__CANONICAL__", canonical_html)\
                       .replace("__SCHEMA__", schema_html)\
                       .replace("__PREFIX__", rel_path_prefix)\
                       .replace("__HEADER_H1__", header_h1)\
                       .replace("__MAIN_CONTENT__", main_section_content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Redesigned and saved: {file_path}")

def run_redesign():
    subpages = [
        ("tree-removal/index.html", "../", False, False),
        ("tree-trimming/index.html", "../", False, False),
        ("stump-removal-grinding/index.html", "../", False, False),
        ("cabling-bracing/index.html", "../", False, False),
        ("shrub-removal/index.html", "../", False, False),
        ("emergency-tree-services/index.html", "../", False, False),
        ("about/index.html", "../", False, False),
        ("services/index.html", "../", False, False),
        ("chubbuck-idaho/index.html", "../", False, False),
        ("blackfoot-idaho/index.html", "../", False, False),
        ("tree-service-caldwell-idaho/index.html", "../", False, False),
        ("tree-service-twin-falls/index.html", "../", False, False),
        ("privacy-policy/index.html", "../", False, True),
        ("contact/index.html", "../", True, False)
    ]
    
    root_dir = r"c:\Users\USER\Desktop\Tree Service Pocatello"
    for relative_file, prefix, is_contact, is_privacy in subpages:
        full_path = os.path.join(root_dir, relative_file.replace('/', os.sep))
        if os.path.exists(full_path):
            redesign_file(full_path, prefix, is_contact, is_privacy)
        else:
            print(f"Error: {full_path} not found.")

if __name__ == '__main__':
    run_redesign()
