
import os
import re

# Directory containing the HTML files
BASE_DIR = os.getcwd()

# Define the replacements as regex patterns and their replacement strings
# We use regex to be robust against spacing variations in the inline styles
REPLACEMENTS = [
    # 1. Clean up Main Wrapper Alignment
    (
        r'<div class="main-wrapper grid-3" style="align-items: center;">',
        '<div class="main-wrapper grid-3 hero-content-grid">'
    ),
    # 2. Clean up Page Headers (About/Philosophy)
    (
        r'<div style="text-align: center; max-width: 800px; margin: 0 auto;">',
        '<div class="page-header-text">'
    ),
     # 3. Clean up Split Grids (Company Profile)
    (
        r'<div class="main-wrapper grid-3" style="grid-template-columns: 1fr 1fr; gap: 60px;">',
        '<div class="main-wrapper grid-3 product-grid">' # Reusing product-grid as it is 2-col, or generic 2-col
    ),
    # 4. Clean up Stats Grids
    (
        r'<div class="grid-3 mt-8" style="grid-template-columns: repeat\(2, 1fr\); gap: 20px;">',
        '<div class="stats-grid mt-8">'
    ),
    # 5. Clean up Gallery Grids
    (
        r'<div class="grid-3" style="grid-template-columns: repeat\(auto-fit, minmax\(250px, 1fr\)\);">',
        '<div class="gallery-grid">'
    ),
     (
        r'<div class="grid-3 mt-4" style="grid-template-columns: repeat\(auto-fit, minmax\(250px, 1fr\)\);">',
        '<div class="gallery-grid mt-4">'
    ),
    # 6. Clean up Header Flex Containers (e.g. Products Section)
    (
        r'<div class="d-flex justify-content-between align-items-end mb-8"[\s\S]*?style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 32px;">',
        '<div class="d-flex justify-content-between align-items-end mb-8 section-header-flex">'
    ),
    # 7. Clean up Product Grid Definitions
    (
        r'<div class="grid-3" style="grid-template-columns: repeat\(2, 1fr\);">',
        '<div class="grid-3 product-grid">'
    )
]

def clean_html_files():
    print("Starting global style cleanup...")
    count = 0
    for file_name in os.listdir(BASE_DIR):
        if file_name.endswith(".html"):
            file_path = os.path.join(BASE_DIR, file_name)
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            
            for pattern, replacement in REPLACEMENTS:
                # Use sub to replace; escaping regex chars in pattern is handled broadly above but specific chars like () need care in the raw string if not literal
                # Actually, simple string replacement works better if exact match, but variations exist.
                # Let's try flexible regex for the style attribute part
                
                # Simplified strategy: If the user copy-pasted, strings are exact.
                # If generated, they might vary.
                # Regex approach:
                # Match: <div [stuff] style="[specific_style]">
                
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"cleaned: {file_name}")
                count += 1
    
    print(f"Global layout standardization complete. Updated {count} files.")

if __name__ == "__main__":
    clean_html_files()
