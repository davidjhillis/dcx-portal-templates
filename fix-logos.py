#!/usr/bin/env python3
import re

files_to_fix = [
    'index.html',
    'doc-page.html',
    'user-profile.html',
    'search-results.html',
    'doc-page-checking-in-out.html'
]

# The correct logo implementation
logo_html = '''<img src="admin/assets/discover-cx-logo.svg" alt="Discover CX" class="h-7 w-auto dark:hidden">
          <img src="admin/assets/discover-cx-logo-white.svg" alt="Discover CX" class="h-7 w-auto hidden dark:block">'''

for file in files_to_fix:
    with open(file, 'r') as f:
        content = f.read()
    
    # Find and replace the SVG block (both light and dark logos together)
    # Pattern matches from "<!-- Light Mode Logo -->" or first <svg to the closing </svg> of dark logo
    pattern = r'(<!-- Light Mode Logo -->|<svg[^>]*class="[^"]*dark:hidden"[^>]*>).*?</svg>\s*(?:<!-- Dark Mode Logo -->)?\s*<svg[^>]*class="[^"]*dark:block"[^>]*>.*?</svg>'
    
    replacement = logo_html
    content_new = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(file, 'w') as f:
        f.write(content_new)
    
    print(f'✅ Fixed {file}')

print('\n✅ All portal files updated with correct logo!')

