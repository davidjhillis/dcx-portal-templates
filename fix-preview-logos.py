#!/usr/bin/env python3
import re

files_to_fix = [
    'admin/preview-templates/index.html',
    'admin/preview-templates/doc-page.html',
    'admin/preview-templates/user-profile.html',
    'admin/preview-templates/search-results.html',
    'admin/preview-templates/doc-page-checking-in-out.html'
]

# The correct logo implementation for preview templates (different path)
logo_html = '''<img src="../assets/discover-cx-logo.svg" alt="Discover CX" class="h-7 w-auto dark:hidden">
          <img src="../assets/discover-cx-logo-white.svg" alt="Discover CX" class="h-7 w-auto hidden dark:block">'''

for file in files_to_fix:
    with open(file, 'r') as f:
        content = f.read()
    
    # Find and replace the SVG block or img tags
    pattern = r'(<!-- Light Mode Logo -->|<(?:img|svg)[^>]*(?:discover-cx-logo\.svg|class="[^"]*dark:hidden")[^>]*>).*?(?:</svg>|/>)\s*(?:<!-- Dark Mode Logo -->)?\s*<(?:img|svg)[^>]*(?:discover-cx-logo-white\.svg|class="[^"]*dark:block")[^>]*>(?:.*?</svg>|/>)'
    
    replacement = logo_html
    content_new = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(file, 'w') as f:
        f.write(content_new)
    
    print(f'✅ Fixed {file}')

print('\n✅ All preview template files updated with correct logo!')

