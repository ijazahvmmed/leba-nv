import os
import re

NEW_HEADER = r"""    <!-- Site Header -->
    <header class="site-header">
        <div class="header-inner">
            <div class="nav-logo">
                <a href="index.html">
                    <img src="images/logo.png" alt="Leba Trading" style="height: 50px; width: auto; display: block;">
                </a>
            </div>
            <div class="header-divider"></div>
            <nav class="nav-links">
                <a href="about.html">Company</a>
                <div class="nav-item-group">
                    <a href="#" style="cursor: default;">Graphic Speciality <i data-lucide="chevron-down" style="width: 14px; margin-left: 4px;"></i></a>
                    <div class="nav-dropdown mega-menu">
                        <div class="dropdown-col">
                            <h4>Covering</h4>
                            <ul>
                                <li><a href="covering-matt-plain.html">Matt Plain</a></li>
                                <li><a href="covering-buckram.html">Buckram</a></li>
                                <li><a href="covering-classy-covers.html">Classy Covers</a></li>
                                <li><a href="covering-glossy.html">Glossy</a></li>
                            </ul>
                            <h4 style="margin-top: 24px;">Colored Board</h4>
                            <ul>
                                <li><a href="coloredboard-burano.html">Burano</a></li>
                                <li><a href="coloredboard-sumo.html">Sumo</a></li>
                            </ul>
                        </div>
                        <div class="dropdown-col">
                            <h4>White & Cream</h4>
                            <ul>
                                <li><a href="whitecream-eco-cream.html">Eco Cream</a></li>
                                <li><a href="whitecream-ecowhite.html">Eco White</a></li>
                                <li><a href="whitecream-biancoflash.html">Biancoflash</a></li>
                            </ul>
                            <h4 style="margin-top: 24px;">Kraft & Recycled</h4>
                            <ul>
                                <li><a href="kraft-papers-boards.html">Kraft Papers</a></li>
                                <li><a href="blackpaperboard-brilliantblack.html">Brilliant Black</a></li>
                                <li><a href="blackpaperboard-shiroechorawblack.html">Raw Black</a></li>
                            </ul>
                        </div>
                        <div class="dropdown-col">
                            <h4>Textures & Art</h4>
                            <ul>
                                <li><a href="textures.html">Textured Boards</a></li>
                                <li><a href="recycledpapers-shiroecho.html">Shiro Echo</a></li>
                                <li><a href="recycledpapers-crushcorn.html">Crush Corn</a></li>
                            </ul>
                            <h4 style="margin-top: 24px;">Premium Print</h4>
                            <ul>
                                <li><a href="hiprint-vintage.html">Vintage</a></li>
                                <li><a href="hiprint-influience.html">Influience</a></li>
                                <li><a href="coated-majestic.html">Majestic</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <!-- Labels -->
                <div class="nav-item-group">
                    <a href="#" style="cursor: default;">Labels <i data-lucide="chevron-down" style="width: 14px; margin-left: 4px;"></i></a>
                    <div class="nav-dropdown mega-menu">
                        <div class="dropdown-col">
                            <h4>Paper Labels</h4>
                            <ul>
                                <li><a href="maplitho-paper-labels.html">Maplitho</a></li>
                                <li><a href="chromo-paper-labels.html">Chromo</a></li>
                                <li><a href="highgloss-paper-labels.html">High Gloss</a></li>
                                <li><a href="castcoated-paper-labels.html">Cast Coated</a></li>
                                <li><a href="fluorescent-paper-labels.html">Fluorescent</a></li>
                                <li><a href="goldpaper-paper-labels.html">Gold Paper</a></li>
                                <li><a href="metallised-paper-labels.html">Metallised Paper</a></li>
                                <li><a href="metallisedholographic-paper-labels.html">Metallised Holographic</a></li>
                            </ul>
                        </div>
                        <div class="dropdown-col">
                            <h4>Film Labels</h4>
                            <ul>
                                <li><a href="pvcclear-film-labels.html">PVC Clear</a></li>
                                <li><a href="synthetic-film-labels.html">Synthetic</a></li>
                                <li><a href="polyclear-film-labels.html">Poly Clear</a></li>
                                <li><a href="polyopaque-film-labels.html">Poly Opaque</a></li>
                                <li><a href="polymetallised-film-labels.html">Poly Metallised</a></li>
                                <li><a href="pvcmetallised-film-labels.html">PVC Metallised</a></li>
                            </ul>
                        </div>
                        <div class="dropdown-col">
                            <h4>Special Labels</h4>
                            <ul>
                                <li><a href="removable-special-labels.html">Removable</a></li>
                                <li><a href="piggyback-special-labels.html">Piggy Back</a></li>
                                <li><a href="ecofriendly-special-labels.html">Eco-friendly</a></li>
                                <li><a href="kraftpaper-special-labels.html">Kraft Paper</a></li>
                                <li><a href="blackpaper-special-labels.html">Black Paper</a></li>
                                <li><a href="sandwich-special-labels.html">Sandwich</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </nav>
            <div class="header-actions">
                <a class="btn btn-primary btn-pill-dark" href="contact.html">Get a quote</a>
            </div>
            <div class="hamburger mobile-trigger">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </header>

    <!-- Mobile Menu Overlay -->
    <div class="mobile-nav-overlay">
        <a class="mb-4 d-block" href="index.html">Home</a>
        <a class="mb-4 d-block" href="about.html">Company</a>
        <a class="mb-4 d-block" href="index.html#products">Products</a>
        <a class="mb-4 d-block" href="contact.html">Contact</a>
    </div>

    <!-- Active Link Script -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
             const currentPath = window.location.pathname.split('/').pop() || 'index.html';
             const navLinks = document.querySelectorAll('.nav-links a');
             navLinks.forEach(link => {
                 const href = link.getAttribute('href');
                 if (href === currentPath || (currentPath === 'index.html' && href === './')) {
                     link.classList.add('active');
                 }
             });
        });
    </script>
    """

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex definitions
    nav_pattern_comment = re.compile(r'<!-- Floating Nav Pill -->.*?<nav class="nav-pill">.*?</nav>', re.DOTALL)
    nav_pattern_plain = re.compile(r'<nav class="nav-pill">.*?</nav>', re.DOTALL)
    
    # New pattern to support re-running on already updated files
    site_header_pattern = re.compile(r'<!-- Site Header -->.*?<header class="site-header">.*?</header>', re.DOTALL)
    
    mobile_header_pattern = re.compile(r'(<!-- Mobile Header -->)?\s*<header class="mobile-header">.*?</header>', re.DOTALL)
    overlay_pattern = re.compile(r'(<!-- Mobile Menu Overlay -->)?\s*<div class="mobile-nav-overlay">.*?</div>', re.DOTALL)
    active_script_pattern = re.compile(r'<!-- Active Link Script -->.*?<script>.*?</script>', re.DOTALL)
    
    found_nav = False
    
    # Let's start over with content for safety.
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step A: Identify locations
    # First check if we already have the new header
    if site_header_pattern.search(content):
        # Just replace the site header with the new one
        content = site_header_pattern.sub(NEW_HEADER, content)
        # Also, check if we have multiple overlays or scripts and clean them up if needed,
        # but the NEW_HEADER includes the overlay and script.
        # So we should probably remove existing overlay/script if they are separate from the header block?
        # The NEW_HEADER string includes: Header, Overlay, Script.
        # If we replace just the Header block, we might duplicate Overlay/Script if they are outside active pattern.
        # But wait, my NEW_HEADER variable above includes everything.
        # So `site_header_pattern` should match everything from `<!-- Site Header -->` down to the end of the script?
        # No, my regex `.*?<header class="site-header">.*?</header>` only matches the header tag.
        
        # Let's adjust the regex to encompass the whole block if possible, or just replace the header and assume the rest follows.
        # IMPORTANT: The NEW_HEADER variable contains header + overlay + script.
        # So if we replace just the `<header>...</header>` part with `NEW_HEADER`, we will get:
        # <header>...</header><overlay>...</overlay><script>...</script> <overlay>...</overlay><script>...</script>
        # (duplicates).
        
        # So we must remove the old overlay and script if we are doing a full replacement.
        content = overlay_pattern.sub('', content)
        content = active_script_pattern.sub('', content)
        
        # Now replace the header part with the FULL NEW_BLOCK
        content = site_header_pattern.sub(NEW_HEADER, content)
        print(f"Updated {filepath} (Updated existing new header)")
        
    elif nav_pattern_comment.search(content) or nav_pattern_plain.search(content):
        # Old style found
        content = mobile_header_pattern.sub('', content)
        content = overlay_pattern.sub('', content)
        
        if nav_pattern_comment.search(content):
            content = nav_pattern_comment.sub(NEW_HEADER, content)
        else:
            content = nav_pattern_plain.sub(NEW_HEADER, content)
        print(f"Updated {filepath} (Converted from old header)")
        
    else:
        print(f"Skipping {filepath} - no recognized header found.")
        return

    # Clean up empty lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

# Run
root_dir = r"c:\Users\ijasa\OneDrive\Desktop\nvgpapers\nvgpapers.com"
for filename in os.listdir(root_dir):
    if filename.endswith(".html"):
        update_file(os.path.join(root_dir, filename))
