import os
import re
from bs4 import BeautifulSoup, Comment

# Global helper to clean elements recursively
def clean_element(element):
    if isinstance(element, Comment):
        return ""
    if isinstance(element, str):
        return element
        
    classes = element.get('class', []) if not isinstance(element, str) else []
    if any('accordion' in cls for cls in classes):
        items = element.find_all(class_='elementor-accordion-item')
        if items:
            accordion_html = '<div class="accordion-wrapper">\n'
            for idx, item in enumerate(items):
                title_a = item.find(class_='elementor-accordion-title')
                if not title_a:
                    continue
                title_text = title_a.get_text().strip()
                
                content_div = item.find(class_='elementor-tab-content')
                if not content_div:
                    continue
                
                cleaned_content = ""
                for child in content_div.children:
                    cleaned_content += clean_element(child)
                cleaned_content = cleaned_content.strip()
                
                accordion_html += f'  <div class="accordion-item">\n'
                accordion_html += f'    <button class="accordion-title" aria-expanded="false" aria-controls="faq-content-{idx+1}">\n'
                accordion_html += f'      <span>{title_text}</span>\n'
                accordion_html += f'      <span class="accordion-icon"><i class="fas fa-chevron-down"></i></span>\n'
                accordion_html += f'    </button>\n'
                accordion_html += f'    <div class="accordion-content" id="faq-content-{idx+1}">\n'
                indented_content = "\n".join("      " + line for line in cleaned_content.splitlines())
                accordion_html += f'{indented_content}\n'
                accordion_html += f'    </div>\n'
                accordion_html += f'  </div>\n'
            accordion_html += '</div>\n'
            return accordion_html

    allowed_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'strong', 'em', 'a', 'br', 'img'}
    if element.name not in allowed_tags:
        content = ""
        for child in element.children:
            content += clean_element(child)
        return content
        
    new_tag = element.name
    attrs_str = ""
    if new_tag == 'a':
        href = element.get('href', '')
        attrs_str = f' href="{href}"'
    elif new_tag == 'img':
        src = element.get('src', '')
        alt = element.get('alt', '')
        width = element.get('width', '')
        height = element.get('height', '')
        attrs_list = []
        if src: attrs_list.append(f'src="{src}"')
        if alt: attrs_list.append(f'alt="{alt}"')
        if width: attrs_list.append(f'width="{width}"')
        if height: attrs_list.append(f'height="{height}"')
        attrs_str = " " + " ".join(attrs_list) if attrs_list else ""
        return f"<{new_tag}{attrs_str} />"
    elif new_tag == 'br':
        return "<br />"
        
    content = ""
    for child in element.children:
        content += clean_element(child)
        
    content = content.strip()
    if not content:
        return ""
        
    newline = "\n" if new_tag not in {'strong', 'em', 'a', 'span'} else ""
    return f"<{new_tag}{attrs_str}>{content}</{new_tag}>{newline}"

def extract_metadata(soup):
    title_tag = soup.find('title')
    title = title_tag.get_text().strip() if title_tag else ""
    title = re.sub(r'\s+', ' ', title)
    
    meta_tags = []
    for meta in soup.find_all('meta'):
        name = meta.get('name', '')
        prop = meta.get('property', '')
        content = meta.get('content', '')
        if any(k in name or k in prop for k in ['description', 'robots', 'og:', 'twitter:', 'viewport']):
            content = re.sub(r'\s+', ' ', content.strip())
            meta_tags.append((name, prop, content))
            
    canonical_link = soup.find('link', rel='canonical')
    canonical = canonical_link.get('href', '') if canonical_link else ""
    
    schema_tag = soup.find('script', class_='rank-math-schema')
    schema = schema_tag.string.strip() if schema_tag else ""
    
    return title, meta_tags, canonical, schema

def format_meta(title, meta_tags, canonical, schema):
    meta_html = ""
    for name, prop, content in meta_tags:
        if name:
            meta_html += f'  <meta name="{name}" content="{content}"/>\n'
        elif prop:
            meta_html += f'  <meta property="{prop}" content="{content}"/>\n'
            
    canonical_html = f'  <link rel="canonical" href="{canonical}"/>' if canonical else ""
    schema_html = f'  <script class="rank-math-schema" type="application/ld+json">{schema}</script>' if schema else ""
    return meta_html, canonical_html, schema_html

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

# Testimonial template
TESTIMONIAL_TEMPLATE = """
       <div class="testimonial-card">
        <div class="stars-rating">
         <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
        </div>
        <p class="testimonial-text">
         "{text}"
        </p>
        <div class="testimonial-meta">
         <div class="meta-info">
          <h4>{name}</h4>
          <p>{location}</p>
         </div>
        </div>
       </div>
"""

# Template for subpages
SUBPAGE_TEMPLATE = """<!DOCTYPE html>
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
      <li class="has-dropdown">
       <a class="nav-link" href="__PREFIX__services/">Services <i class="fas fa-chevron-down" style="margin-left: 4px; font-size: 0.75rem;"></i></a>
       <ul class="dropdown-menu">
        <li><a href="__PREFIX__tree-removal/">Tree Removal</a></li>
        <li><a href="__PREFIX__tree-trimming/">Tree Trimming</a></li>
        <li><a href="__PREFIX__stump-removal-grinding/">Stump Removal &amp; Grinding</a></li>
        <li><a href="__PREFIX__cabling-bracing/">Tree Cabling &amp; Bracing</a></li>
        <li><a href="__PREFIX__shrub-removal/">Shrub Removal</a></li>
        <li><a href="__PREFIX__emergency-tree-services/">Emergency Services</a></li>
       </ul>
      </li>
      <li><a class="nav-link" href="__PREFIX__about/">About</a></li>
      <li><a class="nav-link" href="__PREFIX__contact/">Contact</a></li>
     </ul>
    </nav>
    
    <div class="nav-cta">
     <a class="btn btn-primary" href="tel:208-417-7993">
      <i class="fas fa-phone-alt" style="margin-right: 8px;"></i>Call 208-417-7993
     </a>
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
    <div class="mobile-nav-dropdown">
     <a class="mobile-nav-link" href="#" style="display: flex; justify-content: space-between; align-items: center;">
      Services <i class="fas fa-chevron-down" style="font-size: 0.9rem;"></i>
     </a>
     <div class="mobile-dropdown-content">
      <a class="mobile-sub-link" href="__PREFIX__services/">All Services</a>
      <a class="mobile-sub-link" href="__PREFIX__tree-removal/">Tree Removal</a>
      <a class="mobile-sub-link" href="__PREFIX__tree-trimming/">Tree Trimming</a>
      <a class="mobile-sub-link" href="__PREFIX__stump-removal-grinding/">Stump Removal &amp; Grinding</a>
      <a class="mobile-sub-link" href="__PREFIX__cabling-bracing/">Tree Cabling &amp; Bracing</a>
      <a class="mobile-sub-link" href="__PREFIX__shrub-removal/">Shrub Removal</a>
      <a class="mobile-sub-link" href="__PREFIX__emergency-tree-services/">Emergency Services</a>
     </div>
    </div>
    <a class="mobile-nav-link" href="__PREFIX__about/">About</a>
    <a class="mobile-nav-link" href="__PREFIX__contact/">Contact</a>
    <div class="mobile-nav-cta">
     <a class="btn btn-primary" href="tel:208-417-7993">
      <i class="fas fa-phone-alt" style="margin-right: 8px;"></i>Call Now: 208-417-7993
     </a>
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
    <div style="display: flex; gap: var(--spacing-sm); color: var(--color-text-muted);">
     Serving all neighborhoods in Pocatello, Idaho
    </div>
   </div>
  </footer>

  <!-- Script for Mobile Navigation Menu & Accordions -->
  <script>
   document.addEventListener('DOMContentLoaded', function() {
     // Mobile Navigation Menu Toggle
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
       
       // Close menu when clicking links
       var mobileLinks = mobileMenu.querySelectorAll('a');
       mobileLinks.forEach(function(link) {
         link.addEventListener('click', function() {
           if (link.closest('.mobile-nav-dropdown') && link.getAttribute('href') === '#') {
             return;
           }
           mobileMenu.classList.remove('open');
           mobileToggle.classList.remove('open');
         });
       });
     }
     
     // Mobile Dropdown Toggle
     var mobileDropdown = document.querySelector('.mobile-nav-dropdown .mobile-nav-link');
     var mobileDropdownContent = document.querySelector('.mobile-dropdown-content');
     if (mobileDropdown && mobileDropdownContent) {
       mobileDropdown.addEventListener('click', function(e) {
         e.preventDefault();
         var isOpen = mobileDropdownContent.classList.contains('open');
         var icon = mobileDropdown.querySelector('i');
         if (isOpen) {
           mobileDropdownContent.classList.remove('open');
           if (icon) icon.style.transform = 'rotate(0deg)';
         } else {
           mobileDropdownContent.classList.add('open');
           if (icon) icon.style.transform = 'rotate(180deg)';
         }
       });
     }
     
     // Accordion Logic
     var accTitles = document.querySelectorAll('.accordion-title');
     accTitles.forEach(function(title) {
       title.addEventListener('click', function(e) {
         e.preventDefault();
         var isExpanded = title.getAttribute('aria-expanded') === 'true';
         var newState = !isExpanded;
         
         title.setAttribute('aria-expanded', newState ? 'true' : 'false');
         
         var content = title.nextElementSibling;
         if (content && content.classList.contains('accordion-content')) {
           if (newState) {
             content.style.display = 'block';
           } else {
             content.style.display = 'none';
           }
         }
       });
       
       title.addEventListener('keydown', function(e) {
         if (e.key === 'Enter' || e.key === ' ') {
           e.preventDefault();
           title.click();
         }
       });
     });
   });
  </script>
 </body>
</html>
"""

HOMEPAGE_TEMPLATE = """<!DOCTYPE html>
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
  <link rel="icon" href="wp-content/uploads/2021/04/cropped-Tree-Service-Pocatello-fav-32x32.jpg" sizes="32x32" />
  
  <!-- FontAwesome Icons -->
  <link href="wp-content/plugins/elementor/assets/lib/font-awesome/css/all.min.css" rel="stylesheet"/>
  
  <!-- Custom Redesigned Mobile-First Stylesheet -->
  <link href="index.css" rel="stylesheet"/>
 </head>
 
 <body>
  <!-- Header / Navigation -->
  <header class="header-wrapper">
   <div class="container navbar">
    <a class="logo-link" href="/">
     <img alt="Pocatello Tree Service Logo" src="wp-content/uploads/2021/04/Tree-Service-Pocatello.logo_-120x120.png" style="width: 48px; height: 48px; object-fit: contain;"/>
     <span class="logo-text">Pocatello<span> Tree</span></span>
    </a>
    
    <nav>
     <ul class="nav-menu">
      <li><a class="nav-link active" href="/">Home</a></li>
      <li class="has-dropdown">
       <a class="nav-link" href="/services/">Services <i class="fas fa-chevron-down" style="margin-left: 4px; font-size: 0.75rem;"></i></a>
       <ul class="dropdown-menu">
        <li><a href="/tree-removal/">Tree Removal</a></li>
        <li><a href="/tree-trimming/">Tree Trimming</a></li>
        <li><a href="/stump-removal-grinding/">Stump Removal &amp; Grinding</a></li>
        <li><a href="/cabling-bracing/">Tree Cabling &amp; Bracing</a></li>
        <li><a href="/shrub-removal/">Shrub Removal</a></li>
        <li><a href="/emergency-tree-services/">Emergency Services</a></li>
       </ul>
      </li>
      <li><a class="nav-link" href="/about/">About</a></li>
      <li><a class="nav-link" href="/contact/">Contact</a></li>
     </ul>
    </nav>
    
    <div class="nav-cta">
     <a class="btn btn-primary" href="tel:208-417-7993">
      <i class="fas fa-phone-alt" style="margin-right: 8px;"></i>Call 208-417-7993
     </a>
    </div>
    
    <button aria-label="Toggle Navigation" class="mobile-nav-toggle">
     <span></span>
     <span></span>
     <span></span>
    </button>
   </div>
   
   <!-- Mobile Slide-out Menu -->
   <div class="mobile-nav-menu">
    <a class="mobile-nav-link" href="/">Home</a>
    <div class="mobile-nav-dropdown">
     <a class="mobile-nav-link" href="#" style="display: flex; justify-content: space-between; align-items: center;">
      Services <i class="fas fa-chevron-down" style="font-size: 0.9rem;"></i>
     </a>
     <div class="mobile-dropdown-content">
      <a class="mobile-sub-link" href="/services/">All Services</a>
      <a class="mobile-sub-link" href="/tree-removal/">Tree Removal</a>
      <a class="mobile-sub-link" href="/tree-trimming/">Tree Trimming</a>
      <a class="mobile-sub-link" href="/stump-removal-grinding/">Stump Removal &amp; Grinding</a>
      <a class="mobile-sub-link" href="/cabling-bracing/">Tree Cabling &amp; Bracing</a>
      <a class="mobile-sub-link" href="/shrub-removal/">Shrub Removal</a>
      <a class="mobile-sub-link" href="/emergency-tree-services/">Emergency Services</a>
     </div>
    </div>
    <a class="mobile-nav-link" href="/about/">About</a>
    <a class="mobile-nav-link" href="/contact/">Contact</a>
    <div class="mobile-nav-cta">
     <a class="btn btn-primary" href="tel:208-417-7993">
      <i class="fas fa-phone-alt" style="margin-right: 8px;"></i>Call Now: 208-417-7993
     </a>
    </div>
   </div>
  </header>

  <main>
    <!-- Hero Section -->
    <section class="hero">
     <div class="hero-overlay"></div>
     <img alt="Pocatello Tree Service Hero" class="hero-bg-img" src="wp-content/uploads/2021/04/Tree-Service-Pocatello.jpg"/>
     
     <div class="container hero-container">
      <div class="hero-content">
       <span class="badge"><i class="fas fa-shield-alt"></i> Fully Licensed &amp; Insured Arborists</span>
       <h1>Tree Service in <span>Pocatello ID</span></h1>
       <p>
        __HERO_SUBTITLE__
       </p>
       <div class="hero-cta">
        <a class="btn btn-primary" href="tel:208-417-7993">
         <i class="fas fa-phone-alt" style="margin-right: 8px;"></i>Call 208-417-7993
        </a>
       </div>
       <div class="hero-trust">
        <span class="trust-item"><i class="fas fa-check-circle"></i> 10+ Years Local Experience</span>
        <span class="trust-item"><i class="fas fa-check-circle"></i> Emergency Storm Response</span>
        <span class="trust-item"><i class="fas fa-check-circle"></i> Safe Heavy Rigging Setup</span>
       </div>
      </div>
      
      <!-- Hero Side Card -->
      <div class="hero-card">
       <h3>__HERO_CARD_TITLE__</h3>
       <p style="font-size: 0.95rem; margin-bottom: var(--spacing-sm); color: var(--color-text-muted);">
        __HERO_CARD_TEXT__
       </p>
       <a class="btn btn-dark btn-block" href="tel:208-417-7993" style="text-align: center;"><i class="fas fa-phone-alt" style="margin-right: 8px;"></i>Call 208-417-7993</a>
      </div>
     </div>
    </section>

    <!-- Welcome & Intro Section -->
    <section class="section container">
     <div class="grid grid-2 align-center">
      <div>
       <span class="badge badge-gold"><i class="fas fa-star"></i> Rated #1 Local Tree Care Crew</span>
       <h2>__INTRO_TITLE__</h2>
__INTRO_PARAGRAPHS__
      </div>
      <div>
       <img alt="Tree Trimming Crew working on property in Pocatello" class="card" src="wp-content/uploads/2021/04/Pocatello-Tree-Service.jpg" style="border-radius: var(--radius-lg); width: 100%; height: 380px; object-fit: cover;"/>
      </div>
     </div>
    </section>

    <!-- Why Choose Us Grid Section -->
    <section class="section container" style="border-top: 1px solid var(--color-light-gray); padding-top: var(--spacing-lg);">
     <div class="text-center" style="max-width: 800px; margin: 0 auto var(--spacing-lg) auto;">
      <h2>__WHY_CHOOSE_US_TITLE__</h2>
     </div>
     <div class="grid grid-2" style="gap: var(--spacing-md);">
__WHY_CHOOSE_US_CARDS__
     </div>
    </section>

    <!-- Why pick quality company section -->
    <section class="section container" style="border-top: 1px solid var(--color-light-gray); padding-top: var(--spacing-lg);">
     <div class="text-center" style="max-width: 800px; margin: 0 auto var(--spacing-md) auto;">
      <h2>__QUALITY_TITLE__</h2>
     </div>
     <div style="max-width: 800px; margin: 0 auto; line-height: 1.7; font-size: 1.05rem; color: var(--color-dark-text);">
__QUALITY_PARAGRAPHS__
     </div>
    </section>

    <!-- Services Grid Section -->
    <section class="section" style="background-color: var(--color-white); border-top: 1px solid var(--color-light-gray); border-bottom: 1px solid var(--color-light-gray);">
     <div class="container">
      <div class="text-center" style="max-width: 700px; margin: 0 auto var(--spacing-lg) auto;">
       <h2>Our Professional Tree Services</h2>
       <p class="text-muted">
        We offer comprehensive residential and commercial tree services in the Bannock County area.
       </p>
      </div>
      
      <div class="grid grid-3">
__SERVICES_CARDS__
      </div>
     </div>
    </section>

    <!-- Features / Trust Section -->
    <section class="section container">
     <div class="bg-dark-section section" style="padding: var(--spacing-lg);">
      <div class="text-center" style="max-width: 700px; margin: 0 auto var(--spacing-lg) auto;">
       <h2>Why Pocatello Property Owners Trust Us</h2>
       <p style="color: rgba(255,255,255,0.85)">
        Providing Southeast Idaho with a safer, cleaner, and more reliable arborist service.
       </p>
      </div>
      
      <div class="grid grid-3">
       <div class="feature-box">
        <div class="feature-icon-wrapper"><i class="fas fa-tree"></i></div>
        <h3>Arborist Expertise</h3>
        <p style="color: rgba(255,255,255,0.75); font-size: 0.95rem;">
         We know the unique structural guidelines needed to keep local Siberian Elms, brittle Cottonwoods, and Maple trees standing strong against winter ice and windstorms.
        </p>
       </div>
       
       <div class="feature-box">
        <div class="feature-icon-wrapper"><i class="fas fa-lock"></i></div>
        <h3>$2M Insurance Cover</h3>
        <p style="color: rgba(255,255,255,0.75); font-size: 0.95rem;">
         Rest easy. Our work is fully insured and licensed for public and private property safety. We maintain absolute compliance with ban-county safety rules.
        </p>
       </div>
       
       <div class="feature-box">
        <div class="feature-icon-wrapper"><i class="fas fa-broom"></i></div>
        <h3>Impeccable Cleanup</h3>
        <p style="color: rgba(255,255,255,0.75); font-size: 0.95rem;">
         No branches, sawdust, or ruts left behind. We use protective mats for heavy machinery and clean your lawn thoroughly after every project.
        </p>
       </div>
      </div>
     </div>
    </section>

    <!-- Residential, Commercial & About Pocatello Section -->
    <section class="section container" style="border-top: 1px solid var(--color-light-gray); padding-top: var(--spacing-lg);">
     <div class="grid grid-2" style="gap: var(--spacing-lg);">
      <div>
       <h2>__RESIDENTIAL_TITLE__</h2>
__RESIDENTIAL_PARAGRAPHS__
      </div>
      <div>
       <h2>__ABOUT_POCATELLO_TITLE__</h2>
__ABOUT_POCATELLO_PARAGRAPHS__
      </div>
     </div>
    </section>

    <!-- Call CTA Section -->
    <section class="section container" id="call-cta">
     <div class="bg-primary text-center" style="padding: var(--spacing-lg) var(--spacing-md); border-radius: var(--radius-lg); color: var(--color-white); background: linear-gradient(135deg, var(--color-primary), var(--color-dark)); box-shadow: var(--shadow-md);">
      <span class="badge" style="background-color: rgba(255,255,255,0.2); color: var(--color-white); margin-bottom: var(--spacing-xs);"><i class="fas fa-phone-alt"></i> Free Estimate via Phone</span>
      <h2 style="color: var(--color-white); margin-top: 0; font-size: 2.25rem;">Get Your Free Local Tree Service Estimate</h2>
      <p style="color: rgba(255,255,255,0.9); max-width: 600px; margin: var(--spacing-sm) auto var(--spacing-md) auto; font-size: 1.1rem; line-height: 1.6;">
       Speak directly with our expert arborist. We provide free site inspections, hazard evaluations, and transparent cost breakdowns over the phone.
      </p>
      <a class="btn" href="tel:208-417-7993" style="background-color: var(--color-white); color: var(--color-dark); font-size: 1.4rem; padding: var(--spacing-sm) var(--spacing-lg); font-weight: 700; border-radius: var(--radius-md); display: inline-flex; align-items: center; gap: var(--spacing-xs); border: none; box-shadow: var(--shadow-sm); cursor: pointer; transition: transform 0.2s;">
       <i class="fas fa-phone-alt" style="color: var(--color-primary);"></i> 208-417-7993
      </a>
      <p style="font-size: 0.9rem; color: rgba(255,255,255,0.75); margin-top: var(--spacing-md); margin-bottom: 0;">
       *Serving the entire Pocatello, Idaho area.
      </p>
     </div>
    </section>

    <!-- Testimonials Section -->
    <section class="section" style="background-color: var(--color-white); border-top: 1px solid var(--color-light-gray); border-bottom: 1px solid var(--color-light-gray);">
     <div class="container">
      <div class="text-center" style="max-width: 700px; margin: 0 auto var(--spacing-lg) auto;">
       <h2>Read What Our Clients Say</h2>
       <p class="text-muted">
        Real reviews from local property owners in Southeast Idaho.
       </p>
      </div>
      
      <div class="grid grid-3">
__TESTIMONIALS__
      </div>
     </div>
    </section>

    <!-- Serving Area Section -->
    <section class="section container">
     <div class="text-center" style="max-width: 800px; margin: 0 auto var(--spacing-lg) auto;">
      <h2>Serving the Greater Pocatello Area</h2>
__SERVING_AREA_INTRO__
     </div>
     <div class="grid grid-2" style="gap: var(--spacing-md); max-width: 900px; margin: 0 auto;">
__SERVING_AREA_ITEMS__
     </div>
    </section>

    <!-- FAQ Section -->
    <section class="section container" style="border-top: 1px solid var(--color-light-gray);">
     <div class="text-center" style="max-width: 700px; margin: 0 auto var(--spacing-lg) auto;">
      <h2>Frequently Asked Questions</h2>
      <p class="text-muted">Common questions about our tree services in Pocatello.</p>
     </div>
__FAQS__
    </section>
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
      <li><a href="/">Home</a></li>
      <li><a href="/services/">Services</a></li>
      <li><a href="/about/">About Us</a></li>
      <li><a href="/contact/">Contact Us</a></li>
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
    <div style="display: flex; gap: var(--spacing-sm); color: var(--color-text-muted);">
     Serving all neighborhoods in Pocatello, Idaho
    </div>
   </div>
  </footer>

  <!-- Script for Mobile Navigation Menu & Accordions -->
  <script>
   document.addEventListener('DOMContentLoaded', function() {
     // Mobile Navigation Menu Toggle
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
       
       // Close menu when clicking links
       var mobileLinks = mobileMenu.querySelectorAll('a');
       mobileLinks.forEach(function(link) {
         link.addEventListener('click', function() {
           if (link.closest('.mobile-nav-dropdown') && link.getAttribute('href') === '#') {
             return;
           }
           mobileMenu.classList.remove('open');
           mobileToggle.classList.remove('open');
         });
       });
     }
     
     // Mobile Dropdown Toggle
     var mobileDropdown = document.querySelector('.mobile-nav-dropdown .mobile-nav-link');
     var mobileDropdownContent = document.querySelector('.mobile-dropdown-content');
     if (mobileDropdown && mobileDropdownContent) {
       mobileDropdown.addEventListener('click', function(e) {
         e.preventDefault();
         var isOpen = mobileDropdownContent.classList.contains('open');
         var icon = mobileDropdown.querySelector('i');
         if (isOpen) {
           mobileDropdownContent.classList.remove('open');
           if (icon) icon.style.transform = 'rotate(0deg)';
         } else {
           mobileDropdownContent.classList.add('open');
           if (icon) icon.style.transform = 'rotate(180deg)';
         }
       });
     }
     
     // Accordion Logic
     var accTitles = document.querySelectorAll('.accordion-title');
     accTitles.forEach(function(title) {
       title.addEventListener('click', function(e) {
         e.preventDefault();
         var isExpanded = title.getAttribute('aria-expanded') === 'true';
         var newState = !isExpanded;
         
         title.setAttribute('aria-expanded', newState ? 'true' : 'false');
         
         var content = title.nextElementSibling;
         if (content && content.classList.contains('accordion-content')) {
           if (newState) {
             content.style.display = 'block';
           } else {
             content.style.display = 'none';
           }
         }
       });
       
       title.addEventListener('keydown', function(e) {
         if (e.key === 'Enter' || e.key === ' ') {
           e.preventDefault();
           title.click();
         }
       });
     });
   });
  </script>
 </body>
</html>
"""

def redesign_homepage(original_path, output_path):
    print(f"Redesigning Homepage: {original_path} -> {output_path}")
    with open(original_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    title, meta_tags, canonical, schema = extract_metadata(soup)
    meta_html, canonical_html, schema_html = format_meta(title, meta_tags, canonical, schema)
    
    content_area = soup.find(class_='entry-content') or soup.find(class_='elementor') or soup.find('main')
    
    # Hero Subtitle
    hero_h4 = content_area.find('h4')
    hero_subtitle = clean_text(hero_h4.text) if hero_h4 else "Safe Tree Removal, Trimming, and 24/7 Emergency Care. Locally Owned & Fully Insured."
    
    # Hero Card
    hero_card_title = "Call For A Free Quote!"
    hero_card_text = "Speak directly with our local arborist for transparent phone pricing."
    
    # Intro
    h2_intro = content_area.find(lambda t: t.name == 'h2' and 'Tree Service Near You' in t.text)
    intro_title = clean_text(h2_intro.text) if h2_intro else "Tree Service Near You !"
    
    intro_paragraphs_html = ""
    if h2_intro:
        for p in h2_intro.find_all_next('p')[:4]:
            intro_paragraphs_html += f"       <p>{clean_text(p.text)}</p>\n"
            
    # Why Choose Us
    why_heading = content_area.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4'] and "Why choose Pocatello" in tag.get_text())
    why_choose_us_title = clean_text(why_heading.text) if why_heading else "Why choose Pocatello Tree Service?"
    
    why_cards_html = ""
    why_terms = [
        ("Professional Experienced Staff", "Professional Experienced Staff:"),
        ("Customer Satisfaction", "Customer Satisfaction:"),
        ("Affordable Price", "Affordable Price:"),
        ("Residential & Commercial Tree Service", "Residential & Commercial Tree Service:")
    ]
    for n_title, term in why_terms:
        li = content_area.find(lambda tag: tag.name == 'li' and term in tag.get_text())
        if li:
            paragraphs = []
            all_after = li.find_all_next()
            for el in all_after:
                if el.name in ['li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section']:
                    break
                if el.name == 'p':
                    txt = clean_text(el.text)
                    if txt and txt not in paragraphs:
                        paragraphs.append(txt)
            p_html = "".join(f"<p>{p}</p>\n        " for p in paragraphs)
            why_cards_html += f"""
      <div class="card" style="padding: var(--spacing-md);">
       <h3 style="color: var(--color-primary); margin-bottom: var(--spacing-xs);"><i class="fas fa-check-circle"></i> {n_title}</h3>
       {p_html}
      </div>
"""
            
    # Quality Section
    quality_heading = content_area.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4'] and "pick a quality tree service" in tag.get_text().lower())
    quality_title = clean_text(quality_heading.text) if quality_heading else "Why is it necessary to pick a quality tree service company?"
    
    quality_paragraphs_html = ""
    if quality_heading:
        for p in quality_heading.find_all_next('p')[:2]:
            quality_paragraphs_html += f"      <p>{clean_text(p.text)}</p>\n"
            
    services_list = [
        ("Tree Removal", "tree-removal/", "wp-content/uploads/2021/04/Tree-Removal-Pocatello-1.jpg",
         "Professional tree removal services in Pocatello, ID. Our licensed arborists safely extract dead, diseased, or hazardous trees using precision rigging systems to protect your home and yard."),
         
        ("Tree Trimming", "tree-trimming/", "wp-content/uploads/2021/04/Tree-Trimming-Pocatello-1.jpg",
         "Precision tree trimming and pruning in Pocatello, ID. Thin crowns, remove dangerous deadwood, and shape limbs to boost high-desert wind resistance and protect your roof from storm damage."),
         
        ("Stump Grinding", "stump-removal-grinding/", "wp-content/uploads/2021/04/Tree-Service-company-1.jpg",
         "Fast stump grinding and root removal in Bannock County. We grind stumps deep below ground grade to prevent pests like carpenter ants, clear your lawn, and prepare the site for fresh sod."),
         
        ("Cabling & Bracing", "cabling-bracing/", "wp-content/uploads/2021/04/Pocatello-Tree-Service.jpg",
         "Arborist cabling and structural bracing in Pocatello, Idaho. We install premium support systems to secure weak branch unions and protect storm-threatened trees from splitting or failing."),
         
        ("Shrub Removal", "shrub-removal/", "wp-content/uploads/2021/04/Tree-Service-Pocatello.jpg",
         "Complete shrub removal and land clearing services. We excavate overgrown bushes and invasive roots to restore pedestrian access, improve curb appeal, and prep your landscaping for new designs."),
         
        ("Emergency Services", "emergency-tree-services/", "wp-content/uploads/2021/04/Tree-Removal-Pocatello-1.jpg",
         "24/7 emergency tree service and rapid storm cleanup in Pocatello, ID. Call 208-417-7993 for urgent hazard removal of fallen trees, split limbs, and power line clearance.")
    ]
    services_cards_html = ""
    for s_name, s_link, s_img, s_desc in services_list:
        services_cards_html += f"""
       <div class="card">
        <div class="card-img-wrapper">
         <img alt="{s_name} Service in Pocatello" class="card-img" src="{s_img}"/>
        </div>
        <div class="card-content">
         <h3>{s_name}</h3>
         <p>{s_desc}</p>
         <a class="card-link" href="{s_link}">Learn More <i class="fas fa-arrow-right"></i></a>
        </div>
       </div>
"""
    

    # Residential And Commercial
    res_heading = content_area.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4'] and "Residential And Commercial Tree Service" in tag.get_text())
    residential_title = clean_text(res_heading.text) if res_heading else "Residential And Commercial Tree Service:"
    residential_paragraphs_html = ""
    if res_heading:
        res_p = res_heading.find_next('p')
        if res_p:
            residential_paragraphs_html += f"       <p>{clean_text(res_p.text)}</p>\n"
            
    # About Pocatello Idaho
    about_poc_p = content_area.find(lambda tag: tag.name == 'p' and "About Pocatello, Idaho :" in tag.get_text())
    about_pocatello_title = clean_text(about_poc_p.text) if about_poc_p else "About Pocatello, Idaho :"
    about_pocatello_paragraphs_html = ""
    if about_poc_p:
        desc_p = about_poc_p.find_next('p')
        if desc_p:
            about_pocatello_paragraphs_html += f"       <p>{clean_text(desc_p.text)}</p>\n"
            
    # Testimonials
    testimonials_html = ""
    testimonials = [
        ("Clara", "In our yard, we have a huge elm tree", "Pocatello, ID"),
        ("Amelia", "devastated by the removal of a very large tree", "Chubbuck, ID"),
        ("Ryan", "My business will always be with this tree service company", "Blackfoot, ID")
    ]
    for name, content_part, loc in testimonials:
        test_el = content_area.find(lambda t: t.name == 'div' and 'elementor-testimonial-content' in t.get('class', []) and content_part in t.text)
        text = clean_text(test_el.text) if test_el else ""
        if not text:
            # Hardcoded fallbacks of original texts if bs4 lookup fails
            if "Clara" in name:
                text = "In our yard, we have a huge elm tree, and in our backyard, we have a giant cottonwood that is trimmed by this company. I found them to be extremely knowledgeable and friendly. It was wonderful to watch the clean-up! I think it looked better than when the first group arrived! This tree service is certainly one we would recommend."
            elif "Amelia" in name:
                text = "This Tree Service company has awesome service. I was devastated by the removal of a very large tree, which was located right next to my house. It was an extremely competitive and fair bid. Their arrival was on time and as planned (even early!). I was impressed by the whole crew. Very hard workers and very safe as well."
            elif "Ryan" in name:
                text = "My business will always be with this tree service company. It was hired to trim a number of large trees in my backyard. The extremely large trees on my property needed a lot of attention. To make my trees healthy and safe, I asked them to do whatever was needed.  It was discovered there were several dead limbs that had a lot of potential for damage come winter. Just as I wanted, I received perfectly trimmed trees that were safe and healthy."
        testimonials_html += TESTIMONIAL_TEMPLATE.format(name=name, text=text, location=loc)
        
    # Serving Area Section
    h_serve = content_area.find(lambda t: t.name in ['h1','h2','h3','h4'] and 'Serving the Greater Pocatello' in t.text)
    serving_area_intro_html = ""
    if h_serve:
        intro_p = h_serve.find_next('p')
        if intro_p:
            serving_area_intro_html += f"      <p class=\"text-muted\">{clean_text(intro_p.text)}</p>\n"
            
    serving_area_items_html = ""
    neighborhoods = [
        ("Highland", "Highland:"),
        ("University Area", "University Area:"),
        ("Indian Hills", "Indian Hills:"),
        ("Johnny Creek", "Johnny Creek:")
    ]
    for n_name, n_term in neighborhoods:
        n_p = content_area.find(lambda t: t.name == 'p' and n_term in t.text)
        if n_p:
            n_text = clean_text(n_p.text)
            n_desc = n_text.replace(n_term, "").strip().lstrip(':- ')
            serving_area_items_html += f"""
       <div class="card" style="padding: var(--spacing-sm) var(--spacing-md); border-left: 4px solid var(--color-primary);">
        <h4 style="margin: 0 0 4px 0; color: var(--color-dark);">{n_name}</h4>
        <p style="margin: 0; font-size: 0.95rem; color: var(--color-text-muted);">{n_desc}</p>
       </div>
"""
            
    # FAQs
    faq_acc = content_area.find(class_='elementor-accordion')
    faqs_html = ""
    if faq_acc:
        faqs_html = clean_element(faq_acc)
        
    # Build final page
    new_html = HOMEPAGE_TEMPLATE.replace("__TITLE__", title)\
                                .replace("__META__", meta_html)\
                                .replace("__CANONICAL__", canonical_html)\
                                .replace("__SCHEMA__", schema_html)\
                                .replace("__HERO_SUBTITLE__", hero_subtitle)\
                                .replace("__HERO_CARD_TITLE__", hero_card_title)\
                                .replace("__HERO_CARD_TEXT__", hero_card_text)\
                                .replace("__INTRO_TITLE__", intro_title)\
                                .replace("__INTRO_PARAGRAPHS__", intro_paragraphs_html)\
                                .replace("__WHY_CHOOSE_US_TITLE__", why_choose_us_title)\
                                .replace("__WHY_CHOOSE_US_CARDS__", why_cards_html)\
                                .replace("__QUALITY_TITLE__", quality_title)\
                                .replace("__QUALITY_PARAGRAPHS__", quality_paragraphs_html)\
                                .replace("__SERVICES_CARDS__", services_cards_html)\
                                .replace("__RESIDENTIAL_TITLE__", residential_title)\
                                .replace("__RESIDENTIAL_PARAGRAPHS__", residential_paragraphs_html)\
                                .replace("__ABOUT_POCATELLO_TITLE__", about_pocatello_title)\
                                .replace("__ABOUT_POCATELLO_PARAGRAPHS__", about_pocatello_paragraphs_html)\
                                .replace("__TESTIMONIALS__", testimonials_html)\
                                .replace("__SERVING_AREA_INTRO__", serving_area_intro_html)\
                                .replace("__SERVING_AREA_ITEMS__", serving_area_items_html)\
                                .replace("__FAQS__", faqs_html)
                                
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Redesigned Homepage saved: {output_path}")

def redesign_subpage(original_path, prefix, is_contact=False, is_privacy=False):
    print(f"Redesigning Subpage: {original_path}")
    # Restore original file first from git to extract the content
    # Note: we need to run git checkout 925a513 on the file before opening it, but we already did checkout
    with open(original_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    title, meta_tags, canonical, schema = extract_metadata(soup)
    meta_html, canonical_html, schema_html = format_meta(title, meta_tags, canonical, schema)
    
    header_h1 = title.split('|')[0].strip()
    
    # Extract cleaned content
    entry_content = soup.find(class_='entry-content')
    if not entry_content:
        entry_content = soup.find(class_='elementor')
    if not entry_content:
        entry_content = soup.find('main')
        
    cleaned_content = ""
    if entry_content:
        for child in entry_content.children:
            cleaned_content += clean_element(child)
        cleaned_content = re.sub(r'\n\s*\n', '\n', cleaned_content).strip()
    else:
        cleaned_content = "<p>Content not found.</p>"
        
    # Choose Layout
    main_section_content = ""
    
    if is_contact:
        main_section_content = f"""
   <!-- Contact Page Layout -->
   <div class="container section">
    <div class="grid grid-2">
     <!-- Contact Info & Map -->
     <div>
      <h2>Get In Touch</h2>
      <p>We are a fully mobile tree service business serving Pocatello, Idaho.</p>
      
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
     
     <!-- Direct Call Widget -->
     <div>
      <div class="card text-center" style="padding: var(--spacing-lg); display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: var(--color-white); border: 1px solid var(--color-light-gray); height: 100%;">
       <div class="feature-icon-wrapper" style="background-color: var(--color-primary); color: var(--color-white); width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-bottom: var(--spacing-sm);">
        <i class="fas fa-phone-alt"></i>
       </div>
       <h3 style="color: var(--color-dark); margin-bottom: var(--spacing-xs);">Call Our Arborist Team</h3>
       <p style="color: var(--color-text-muted); margin-bottom: var(--spacing-md); font-size: 1.05rem; line-height: 1.6;">
        We handle all scheduling and estimate requests directly over the phone. Speak with a local tree expert in seconds.
       </p>
       <a class="btn btn-primary" href="tel:208-417-7993" style="font-size: 1.2rem; padding: var(--spacing-sm) var(--spacing-md); width: 100%; justify-content: center; display: inline-flex; align-items: center; gap: 8px;">
        <i class="fas fa-phone-alt"></i> Call 208-417-7993
       </a>
       <p style="font-size: 0.9rem; color: var(--color-text-muted); margin-top: var(--spacing-sm); margin-bottom: 0;">
        Available for emergencies 24/7.
       </p>
      </div>
     </div>
    </div>
   </div>
"""
    elif is_privacy:
        main_section_content = f"""
   <!-- Privacy Page Layout -->
   <div class="container section" style="max-width: 800px;">
    <article class="content-area">
{cleaned_content}
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
{cleaned_content}
     </article>
     
     <!-- Sidebar Area -->
     <aside class="sidebar-area">
      <!-- Call Widget -->
      <div class="sidebar-widget text-center" style="background-color: var(--color-dark); color: var(--color-white); border-radius: var(--radius-md);">
       <h4 style="color: var(--color-white); border-color: var(--color-primary);">Need Fast Service?</h4>
       <p style="font-size: 0.95rem; color: rgba(255,255,255,0.85); margin-bottom: var(--spacing-sm);">
        Contact our arborist team now for a free, no-obligation quote.
       </p>
       <a class="btn btn-primary" href="tel:208-417-7993" style="margin-bottom: var(--spacing-xs);">
        <i class="fas fa-phone-alt" style="margin-right: 8px;"></i>208-417-7993
       </a>
       <a class="btn btn-secondary" href="{prefix}contact/" style="border-color: var(--color-white); color: var(--color-white);">
        Contact Form
       </a>
      </div>
      
      <!-- Services Menu Widget -->
      <div class="sidebar-widget">
       <h4>Our Tree Services</h4>
       <ul class="footer-links" style="color: var(--color-dark-text);">
        <li><a href="{prefix}tree-removal/">Tree Removal</a></li>
        <li><a href="{prefix}tree-trimming/">Tree Trimming</a></li>
        <li><a href="{prefix}stump-removal-grinding/">Stump Grinding</a></li>
        <li><a href="{prefix}cabling-bracing/">Cabling &amp; Bracing</a></li>
        <li><a href="{prefix}shrub-removal/">Shrub Removal</a></li>
        <li><a href="{prefix}emergency-tree-services/">Emergency Services</a></li>
       </ul>
      </div>
     </aside>
    </div>
   </div>
"""

    new_html = SUBPAGE_TEMPLATE.replace("__TITLE__", title)\
                              .replace("__META__", meta_html)\
                              .replace("__CANONICAL__", canonical_html)\
                              .replace("__SCHEMA__", schema_html)\
                              .replace("__PREFIX__", prefix)\
                              .replace("__HEADER_H1__", header_h1)\
                              .replace("__MAIN_CONTENT__", main_section_content)
                              
    with open(original_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Redesigned Subpage saved: {original_path}")

def run_redesign():
    root_dir = r"c:\Users\USER\Desktop\Tree Service Pocatello"
    
    # 1. Homepage
    homepage_path = os.path.join(root_dir, "index.html")
    redesign_homepage(homepage_path, homepage_path)
    
    # 2. Subpages
    subpages = [
        ("tree-removal/index.html", "../", False, False),
        ("tree-trimming/index.html", "../", False, False),
        ("stump-removal-grinding/index.html", "../", False, False),
        ("cabling-bracing/index.html", "../", False, False),
        ("shrub-removal/index.html", "../", False, False),
        ("emergency-tree-services/index.html", "../", False, False),
        ("about/index.html", "../", False, False),
        ("services/index.html", "../", False, False),
        ("privacy-policy/index.html", "../", False, True),
        ("contact/index.html", "../", True, False)
    ]
    
    for rel_path, prefix, is_contact, is_privacy in subpages:
        full_path = os.path.join(root_dir, rel_path.replace('/', os.sep))
        if os.path.exists(full_path):
            redesign_subpage(full_path, prefix, is_contact, is_privacy)
        else:
            print(f"Error: {full_path} not found.")

if __name__ == '__main__':
    run_redesign()
