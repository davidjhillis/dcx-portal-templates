# Admin App Development Plan

## 🎯 Project Overview

Build an admin configuration app to manage the DCX Demo Templates portal, including theme management (Radix colors, Google Fonts) and AI feature configuration.

---

## 📁 Project Structure

```
DCX Demo Templates/
├── admin/
│   ├── index.html              # Admin Dashboard
│   ├── theme/
│   │   ├── colors.html         # Radix Color Picker
│   │   ├── typography.html     # Google Fonts Manager
│   │   └── preview.html        # Live Preview
│   ├── ai/
│   │   ├── features.html       # AI Feature Toggles
│   │   ├── models.html         # Model Selection & BYOK
│   │   └── safety.html         # AI Safeguards
│   ├── assets/
│   │   ├── admin-styles.css    # Admin-specific styles
│   │   └── admin-nav.js        # Navigation component
│   └── config/
│       └── site-config.json    # Configuration storage
└── ... (existing templates)
```

---

## ✅ Task List

### **Phase 1: Setup & Foundation**
- [x] Create plan document (ADMIN_APP_PLAN.md)
- [ ] Create new Git branch `feature/admin-app`
- [ ] Create admin folder structure
- [ ] Create shared configuration file (site-config.json)
- [ ] Build admin dashboard (index.html)
- [ ] Create admin navigation component
- [ ] Create admin base styles

### **Phase 2: Theme Manager**

#### **2.1 Color Management (Radix)**
- [ ] Research Radix Colors documentation
- [ ] Create colors.html page
- [ ] Build Radix color scale picker UI
- [ ] Add light/dark mode toggle
- [ ] Implement custom color upload
- [ ] Add color preview swatches
- [ ] Save color configuration to site-config.json
- [ ] Apply colors dynamically to templates

#### **2.2 Typography Management (Google Fonts)**
- [ ] Create typography.html page
- [ ] Integrate Google Fonts API
- [ ] Build font family selectors (heading, body, code)
- [ ] Add font weight options
- [ ] Create font size scale editor (h1-h6, body, small)
- [ ] Font pairing suggestions
- [ ] Save typography configuration to site-config.json
- [ ] Apply fonts dynamically to templates

#### **2.3 Live Preview**
- [ ] Create preview.html page
- [ ] Build iframe with template preview
- [ ] Add page switcher (index, doc-page, search-results)
- [ ] Add responsive preview modes (mobile, tablet, desktop)
- [ ] Real-time configuration updates
- [ ] Side-by-side comparison view

### **Phase 3: AI Configuration**

#### **3.1 Feature Toggles**
- [ ] Create features.html page
- [ ] Build toggle switches for AI features:
  - [ ] AI Summary
  - [ ] Code Explain
  - [ ] Content Highlighter
  - [ ] Voice Assistant
  - [ ] Search Enhancement
  - [ ] Chatbot
- [ ] Add feature descriptions
- [ ] Save feature states to site-config.json
- [ ] Show/hide features in templates based on config

#### **3.2 Model Selection**
- [ ] Create models.html page
- [ ] Build model selection dropdown:
  - [ ] OpenAI GPT-4
  - [ ] OpenAI GPT-3.5
  - [ ] Anthropic Claude 3.5
  - [ ] Anthropic Claude 3
  - [ ] Custom Endpoint (BYOK)
- [ ] Add API key input (BYOK option)
- [ ] Model parameter controls (temperature, max tokens)
- [ ] Test connection button
- [ ] Save model configuration to site-config.json

#### **3.3 AI Safeguards**
- [ ] Create safety.html page
- [ ] Build safety controls:
  - [ ] Jailbreak protection toggle
  - [ ] Content filtering toggle
  - [ ] Toxicity detection toggle
  - [ ] Rate limiting settings
  - [ ] PII filtering toggle
- [ ] Add safety level presets (Low, Medium, High)
- [ ] Custom blocklist input
- [ ] Save safety configuration to site-config.json

### **Phase 4: Integration & Testing**

#### **4.1 Configuration System**
- [ ] Build JavaScript config reader
- [ ] Create config validator
- [ ] Add export/import config functionality
- [ ] Add reset to defaults button
- [ ] Create backup/restore system
- [ ] Add configuration history/versioning

#### **4.2 Apply to Templates**
- [ ] Update index.html to read config
- [ ] Update doc-page.html to read config
- [ ] Update doc-page-checking-in-out.html to read config
- [ ] Update search-results.html to read config
- [ ] Update user-profile.html to read config
- [ ] Create shared config loader script

#### **4.3 Demo Functionality**
- [ ] Mock AI feature toggles (show/hide UI elements)
- [ ] Mock font changes (apply Google Fonts)
- [ ] Mock color changes (apply Radix colors)
- [ ] Add demo mode indicator
- [ ] Create demo reset button

#### **4.4 Testing**
- [ ] Test theme changes on all pages
- [ ] Test AI feature toggles on all pages
- [ ] Test responsive admin UI (mobile, tablet, desktop)
- [ ] Test configuration save/load
- [ ] Test configuration export/import
- [ ] Browser compatibility testing
- [ ] Performance testing (config load times)

### **Phase 5: Documentation & Polish**

#### **5.1 Documentation**
- [ ] Write admin app README.md
- [ ] Document configuration structure
- [ ] Create user guide for theme manager
- [ ] Create user guide for AI configuration
- [ ] Add inline help text/tooltips
- [ ] Create video walkthrough (optional)

#### **5.2 Polish**
- [ ] Add loading states
- [ ] Add success/error notifications
- [ ] Add form validation
- [ ] Add keyboard shortcuts
- [ ] Improve accessibility (ARIA labels)
- [ ] Add dark mode for admin UI
- [ ] Final UI/UX review

### **Phase 6: Finalization**
- [ ] Code cleanup
- [ ] Remove console.logs
- [ ] Optimize performance
- [ ] Final testing pass
- [ ] Merge feature branch to main (with user approval)
- [ ] Create release notes
- [ ] Archive any unused files

---

## 🎨 Configuration Schema

```json
{
  "version": "1.0.0",
  "theme": {
    "colors": {
      "mode": "light",
      "primary": {
        "name": "indigo",
        "scale": {
          "1": "#fdfdfe",
          "2": "#f7f9ff",
          "3": "#edf2fe",
          "4": "#e1e9ff",
          "5": "#d2deff",
          "6": "#c1d0ff",
          "7": "#abbdf9",
          "8": "#8da4ef",
          "9": "#3e63dd",
          "10": "#3358d4",
          "11": "#3a5bc7",
          "12": "#1f2d5c"
        }
      },
      "accent": {
        "name": "purple",
        "scale": {...}
      },
      "neutral": {
        "name": "slate",
        "scale": {...}
      },
      "custom": []
    },
    "typography": {
      "heading": {
        "family": "Inter",
        "weights": [400, 600, 700, 800],
        "fallback": "system-ui, sans-serif"
      },
      "body": {
        "family": "Geist",
        "weights": [400, 500, 600],
        "fallback": "system-ui, sans-serif"
      },
      "code": {
        "family": "Fira Code",
        "weights": [400, 500, 600],
        "fallback": "monospace"
      },
      "scale": {
        "h1": "2.25rem",
        "h2": "1.875rem",
        "h3": "1.5rem",
        "h4": "1.25rem",
        "h5": "1.125rem",
        "h6": "1rem",
        "body": "1rem",
        "small": "0.875rem",
        "xs": "0.75rem"
      }
    }
  },
  "ai": {
    "features": {
      "summary": true,
      "codeExplain": true,
      "highlighter": false,
      "voice": false,
      "searchEnhancement": true,
      "chatbot": false
    },
    "models": {
      "selected": "gpt-4",
      "options": [
        "gpt-4",
        "gpt-3.5-turbo",
        "claude-3.5-sonnet",
        "claude-3-opus",
        "custom"
      ],
      "custom": {
        "endpoint": "",
        "apiKey": ""
      },
      "parameters": {
        "temperature": 0.7,
        "maxTokens": 2048
      }
    },
    "safety": {
      "level": "medium",
      "jailbreakProtection": true,
      "contentFiltering": true,
      "toxicityDetection": true,
      "piiFiltering": true,
      "rateLimit": {
        "enabled": true,
        "requestsPerMinute": 10
      },
      "customBlocklist": []
    }
  },
  "metadata": {
    "lastModified": "2025-10-31T00:00:00Z",
    "modifiedBy": "admin",
    "version": "1.0.0"
  }
}
```

---

## 🚀 Technology Stack

- **Frontend:** HTML5, Tailwind CSS, JavaScript (vanilla)
- **Icons:** Lucide Icons
- **Color System:** Radix Colors (https://www.radix-ui.com/colors)
- **Fonts:** Google Fonts API
- **Storage:** JSON file + localStorage
- **Version Control:** Git

---

## 📝 Notes

- Content management is handled by Ingeniux CMS (not included)
- Admin app is for UX demonstration purposes
- AI features will be mocked (show/hide UI elements)
- Configuration changes should be immediately visible in templates
- Keep admin UI consistent with main template design (Tailwind, dark mode)

---

## 🎯 Success Criteria

- [ ] Admin can change theme colors and see live updates
- [ ] Admin can select fonts and see live updates
- [ ] Admin can toggle AI features on/off
- [ ] Admin can select AI models and configure BYOK
- [ ] Admin can configure AI safety settings
- [ ] Configuration persists across sessions
- [ ] All templates respect configuration settings
- [ ] Admin UI is responsive and accessible
- [ ] Code is clean, documented, and maintainable

---

**Created:** October 31, 2025  
**Status:** In Progress  
**Branch:** `feature/admin-app`

