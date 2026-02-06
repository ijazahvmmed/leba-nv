
import os
import re

def sync_layout():
    base_dir = r"c:\Users\ijasa\OneDrive\Desktop\nvgpapers\nvgpapers.com"
    index_path = os.path.join(base_dir, "index.html")
    
    if not os.path.exists(index_path):
        print("Error: index.html not found.")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    # Define regex patterns for extraction
    # Using non-greedy match .*? with re.DOTALL to capture multiline content
    header_pattern = re.compile(r'(<header class="site-header">[\s\S]*?</header>)', re.IGNORECASE)
    footer_pattern = re.compile(r'(<footer[\s\S]*?</footer>)', re.IGNORECASE)
    overlay_pattern = re.compile(r'(<!-- Mobile Menu Overlay -->\s*<div class="mobile-nav-overlay">[\s\S]*?</div>)', re.IGNORECASE)

    # Extract source blocks
    header_match = header_pattern.search(index_content)
    footer_match = footer_pattern.search(index_content)
    overlay_match = overlay_pattern.search(index_content)

    if not header_match or not footer_match:
        print("Error: Could not extract header or footer from index.html")
        return

    new_header = header_match.group(1)
    new_footer = footer_match.group(1)
    # Overlay might be missing in some versions, but we should try to grab it
    new_overlay = overlay_match.group(1) if overlay_match else None

    # Get all HTML files
    html_files = [f for f in os.listdir(base_dir) if f.endswith(".html") and f != "index.html"]
    
    print(f"Syncing layout to {len(html_files)} files...")

    success_count = 0
    
    for file_name in html_files:
        file_path = os.path.join(base_dir, file_name)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Replace Header
            # We use a broader pattern for target in case class names varied slightly in old files, 
            # but usually they are just <header...> </header>
            target_header_pattern = re.compile(r'<header[\s\S]*?</header>', re.IGNORECASE)
            
            if target_header_pattern.search(content):
                content = target_header_pattern.sub(new_header, content)
            else:
                # If no header found, that's weird for a site page, but we'll skip warning for now to keep output clean
                pass

            # Replace Footer
            target_footer_pattern = re.compile(r'<footer[\s\S]*?</footer>', re.IGNORECASE)
            if target_footer_pattern.search(content):
                content = target_footer_pattern.sub(new_footer, content)

            # Replace Overlay (if it exists in target, or if we want to inject it - let's replace existing Only)
            if new_overlay:
                # Targeted match for overlay
                target_overlay_pattern = re.compile(r'<!-- Mobile Menu Overlay -->\s*<div class="mobile-nav-overlay">[\s\S]*?</div>', re.IGNORECASE)
                # Fallback pattern if comment is missing
                target_overlay_fallback = re.compile(r'<div class="mobile-nav-overlay">[\s\S]*?</div>', re.IGNORECASE)
                
                if target_overlay_pattern.search(content):
                    content = target_overlay_pattern.sub(new_overlay, content)
                elif target_overlay_fallback.search(content):
                    content = target_overlay_fallback.sub(new_overlay, content)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            success_count += 1
            
        except Exception as e:
            print(f"Failed to update {file_name}: {str(e)}")

    print(f"Successfully updated {success_count} files.")

if __name__ == "__main__":
    sync_layout()
