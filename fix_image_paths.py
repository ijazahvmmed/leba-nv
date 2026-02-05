
import os
import glob
import re

# Map of common product names to their correct folder and file structure
# Structure: images/{Folder}/{big|thumb}/{File}
# We need to find the correct casing for {Folder} and {File}

def find_correct_path(search_name):
    """
    Search for a file in images/ that matches search_name case-insensitively.
    Returns (big_path, thumb_path) if found.
    """
    img_dir = "images"
    # Search all folders in images/
    for folder in os.listdir(img_dir):
        folder_path = os.path.join(img_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        
        # Check subfolders big and thumb
        big_dir = os.path.join(folder_path, "big")
        thumb_dir = os.path.join(folder_path, "thumb")
        
        if os.path.isdir(big_dir) and os.path.isdir(thumb_dir):
            for filename in os.listdir(big_dir):
                if search_name.lower() in filename.lower():
                    # Check if thumb has the same file
                    if filename in os.listdir(thumb_dir):
                        return (
                            f"images/{folder}/big/{filename}",
                            f"images/{folder}/thumb/{filename}"
                        )
    return None, None

def fix_html_images():
    html_files = glob.glob("*.html")
    
    # Common gallery patterns
    # href="images/..." and img src="images/..."
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # Find all gallery-like links
        # Pattern: <a href="(images/[^"]+)" ...> <img src="(images/[^"]+)" ...>
        # We'll look for card-modern blocks
        
        # Manual overrides for the ones we know are broken
        replacements = {
            "images/BiancoflashMaster.jpg": "images/Biancoflash/big/Biancoflashmaster.jpg",
            "images/thumb/BiancoflashMaster.jpg": "images/Biancoflash/thumb/Biancoflashmaster.jpg",
            "images/BiancoflashNatural.jpg": "images/Biancoflash/big/Biancoflashnatural.jpg",
            "images/thumb/BiancoflashNatural.jpg": "images/Biancoflash/thumb/Biancoflashnatural.jpg",
            "images/BiancoflashIvory.jpg": "images/Biancoflash/big/Biancoflashivory.jpg",
            "images/thumb/BiancoflashIvory.jpg": "images/Biancoflash/thumb/Biancoflashivory.jpg",
            
            "images/hi-print/vintage/VintageWhite.jpg": "images/Vintage/big/VintageWhite.jpg",
            "images/hi-print/vintage/thumb/VintageWhite.jpg": "images/Vintage/thumb/VintageWhite.jpg",
            "images/hi-print/vintage/VintageIvory.jpg": "images/Vintage/big/VintageIvory.jpg",
            "images/hi-print/vintage/thumb/VintageIvory.jpg": "images/Vintage/thumb/VintageIvory.jpg",
            
            "images/hi-print/influience/Influiencewhite.jpg": "images/Influience/big/Influiencewhite.jpg",
            "images/hi-print/influience/thumb/Influiencewhite.jpg": "images/Influience/thumb/Influiencewhite.jpg",
            "images/hi-print/influience/Influienceivory.jpg": "images/Influience/big/Influienceivory.jpg",
            "images/hi-print/influience/thumb/Influienceivory.jpg": "images/Influience/thumb/Influienceivory.jpg",
            
            # Additional discovered during browse
            "images/Vintage/VintageWhite.jpg": "images/Vintage/big/VintageWhite.jpg",
            "images/Vintage/thumb/VintageWhite.jpg": "images/Vintage/thumb/VintageWhite.jpg",
            "images/Vintage/VintageIvory.jpg": "images/Vintage/big/VintageIvory.jpg",
            "images/Vintage/thumb/VintageIvory.jpg": "images/Vintage/thumb/VintageIvory.jpg",
            
            "images/Influience/Influiencewhite.jpg": "images/Influience/big/Influiencewhite.jpg",
            "images/Influience/thumb/Influiencewhite.jpg": "images/Influience/thumb/Influiencewhite.jpg",
            "images/Influience/Influienceivory.jpg": "images/Influience/big/Influienceivory.jpg",
            "images/Influience/thumb/Influienceivory.jpg": "images/Influience/thumb/Influienceivory.jpg",
            
            "images/Biancoflash/BiancoflashMaster.jpg": "images/Biancoflash/big/Biancoflashmaster.jpg",
            "images/Biancoflash/thumb/BiancoflashMaster.jpg": "images/Biancoflash/thumb/Biancoflashmaster.jpg",
            "images/Biancoflash/BiancoflashNatural.jpg": "images/Biancoflash/big/Biancoflashnatural.jpg",
            "images/Biancoflash/thumb/BiancoflashNatural.jpg": "images/Biancoflash/thumb/Biancoflashnatural.jpg",
            "images/Biancoflash/BiancoflashIvory.jpg": "images/Biancoflash/big/Biancoflashivory.jpg",
            "images/Biancoflash/thumb/BiancoflashIvory.jpg": "images/Biancoflash/thumb/Biancoflashivory.jpg",
        }
        
        for old, new in replacements.items():
            if old in content:
                content = content.replace(old, new)
                modified = True
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filepath}")

if __name__ == "__main__":
    fix_html_images()
