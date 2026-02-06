
import os
import re

BASE_DIR = os.getcwd()

# Define the pattern to effectively search for the duplicates/broken duplication
# We see in the view_file that duplicates are often separated by whitespace or fragmented
# But the surest way is that `update_header_batch.py` inserted the new header,
# but likely *appended* or *didn't clean* some old artifact chunks if the regex didn't match perfectly previously.
# Or, the file `about.html` specifically (and others) has junk content "Mobile Menu Overlay (Jonite Style)" repeated.

# The junk block seems to be:
# <div class="mobile-nav-content">...</div>
# appearing AFTER the <script>...</script> of the main header.

# Our `NEW_HEADER` in `update_header_batch.py` ends with the script.
# Any "Mobile Menu Overlay" appearing *after* that script is likely a zombie fragment.

def clean_duplicates():
    count_files = 0
    
    # We will read each file
    for file_name in os.listdir(BASE_DIR):
        if file_name.endswith(".html"):
            file_path = os.path.join(BASE_DIR, file_name)
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            
            # Strategy:
            # The Valid header ends with </script>.
            # Detailed inspection of about.html in previous turn showed:
            # ... </script>
            # [whitespace]
            # <!-- Mobile Menu Overlay (Jonite Style) -->
            # ... <div class="mobile-nav-content"> ...
            # ... </div>
            #
            # We want to remove everything between `</script>` (of the active link script)
            # and `<!-- Hero Section -->` (or the first major section tag), IF it looks like junk.
            # OR simpler: Remove specifically the "Jonite Style" block which is the old menu artifact.
            
            # Regex to find the junk block:
            # It starts with <!-- Mobile Menu Overlay (Jonite Style) --> or <div class="mobile-nav-content">
            # and ends with </div>
            
            # Let's target the specifc text seen in the screenshot/file view:
            # "Custom Solutions", "Become a Distributor", "Jonite Style"
            
            # We'll construct a regex that looks for the SPECIFIC junk block that appears after the header
            junk_pattern = r'<!-- Mobile Menu Overlay \(Jonite Style\) -->[\s\S]*?<div class="mobile-nav-content">[\s\S]*?</div>\s*</div>'
            
            content = re.sub(junk_pattern, '', content)
            
            # Also clean up any lingering "Blur Wrapper Start" if it's orphaned/duplicated
            junk_pattern_2 = r'<!-- Blur Wrapper Start.*?<div class="content-blur-wrapper">\s*'
            content = re.sub(junk_pattern_2, '', content)

             # Also clean up specific duplicated text block seen in file view if regex missed
            manual_junk = r'<div class="mobile-nav-link-item"><a href="about.html">Custom Solutions</a></div>'
            if manual_junk in content and "Jonite Style" in content:
                 # If we still have this, try a broader delete of the old overlay container structure
                 pass 

            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Cleaned zombie menu from: {file_name}")
                count_files += 1

    print(f"Cleanup complete. Processed {count_files} files.")

if __name__ == "__main__":
    clean_duplicates()
