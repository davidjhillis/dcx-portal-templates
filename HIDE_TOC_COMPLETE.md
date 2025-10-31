# "Hide Table of Contents" Feature - Complete ✅

## Added to `doc-page.html`

### **UI Components:**
1. **"Table of Contents" heading** - Added above Expand/Collapse buttons
2. **"Hide table of contents" button** - Orange button (`bg-orange-600`) positioned below Expand/Collapse buttons
3. **Visual styling** - Prominent, full-width button matches Seismic design

### **Functionality:**
- **Click to hide**: Entire left sidebar collapses
- **Main content expands**: `lg:ml-64` class is removed, allowing content to use full width
- **Button text changes**: From "Hide table of contents" → "Show table of contents"
- **Click to show**: Brings back the sidebar and restores margin

### **JavaScript:**
```javascript
const hideTocBtn = document.getElementById('hide-toc-btn');
const leftSidebar = document.querySelector('aside.lg\\:block.fixed.left-0');
const mainContent = document.querySelector('main.lg\\:ml-64');

hideTocBtn.addEventListener('click', function() {
  leftSidebar.classList.toggle('hidden');
  
  if (leftSidebar.classList.contains('hidden')) {
    mainContent.classList.remove('lg:ml-64');
    this.textContent = 'Show table of contents';
  } else {
    mainContent.classList.add('lg:ml-64');
    this.textContent = 'Hide table of contents';
  }
});
```

### **Committed to Git:**
✅ Commit: "Add 'Hide table of contents' button to doc-page"

**Hard refresh (Cmd+Shift+R) to see the feature working!**
