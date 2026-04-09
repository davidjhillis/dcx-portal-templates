# Discover CX Documentation Portal Templates

Static HTML/Tailwind CSS templates for the Discover CX documentation portal. Designed for implementation in Ingeniux CMS.

## Live Pages

| Page | File | Description |
|------|------|-------------|
| Home | `index.html` | Product documentation landing with search, product cards, support |
| Doc Page | `doc-page.html` | Article reader with sidebar nav, TOC, code blocks, AI features |
| Doc Page (alt) | `doc-page-checking-in-out.html` | Second article demonstrating the same layout |
| Search Results | `search-results.html` | Search results with filters and AI answers |
| User Profile | `user-profile.html` | Settings, subscriptions, bookmarks, watched pages |
| Login | `login.html` | SSO login with Aurora animation |

## Architecture

### Design Tokens

All colors are defined as CSS custom properties in `css/tokens.css` (default: Indigo). Tailwind maps these via `js/tailwind-config.js`. The admin theme editor overrides tokens at runtime via `admin/assets/theme-loader.js`.

```
css/tokens.css          <- color token values (single source of truth)
js/tailwind-config.js   <- maps CSS vars to Tailwind classes
admin/assets/theme-loader.js <- runtime theme override from admin editor
```

### Shared Components

- **`js/user-dropdown.js`** - User menu dropdown + notification bell panel. Injected on every page. Contains theme switcher, profile links, notification feed.
- **`js/main.js`** - Core JS: mobile menu, search modal, navigation tree, dark mode persistence.
- **`assets/js/chatbot-widget.js`** - Floating support chat widget.

### Page Head (standard include order)

```html
<link rel="stylesheet" href="css/tokens.css">
<script src="https://cdn.tailwindcss.com"></script>
<script src="js/tailwind-config.js"></script>
<script src="admin/assets/theme-loader.js"></script>
<script src="https://unpkg.com/lucide@latest"></script>
```

### Dependencies

- **Tailwind CSS** (CDN) - utility classes
- **Lucide Icons** (CDN) - SVG icons via `data-lucide` attributes
- **Inter** (Google Fonts) - typography

No build pipeline. No npm. No framework.

## User Profile Features

- **Settings** - personal info, language/timezone, photo upload
- **Subscriptions** - notification toggles (documentation, product, email) with green/gray states
- **Bookmarks** - saved articles with search, type badges, remove on hover
- **Watched Pages** - page-level subscriptions with update badges and "View changes" links
- **Notification Bell** - dropdown panel on all pages with read/unread states

## Doc Page Features

- **Bookmark & Watch buttons** in article toolbar with toggle states
- **Sidebar navigation** with collapsible sections
- **Table of contents** (right sidebar)
- **Code blocks** with copy and AI explain actions
- **Dark mode** toggle in user menu
- **Command K** search modal (Cmd/Ctrl+K)

## Admin Suite

Located in `admin/`. Not part of the public portal - internal tooling for theme editing, content management, and configuration.

- `admin/theme.html` - Visual theme editor with live preview
- `admin/content-hub.html` - Content source management
- `admin/content-tables.html` - Metadata orchestration
- `admin/ai.html` - AI model configuration
- `admin/users.html` - User and role management
- `admin/integrations.html` - External API connections
- `admin/validator.html` - WCAG compliance checker
- `admin/page-builder.html` - No-code page composition

## Directory Structure

```
/
├── index.html                  Main landing page
├── doc-page.html               Article reader
├── doc-page-checking-in-out.html  Second article
├── search-results.html         Search results
├── user-profile.html           User profile & settings
├── login.html                  Login page
├── css/
│   └── tokens.css              Design token values
├── js/
│   ├── main.js                 Core functionality
│   ├── tailwind-config.js      Shared Tailwind config
│   └── user-dropdown.js        Shared user menu + notifications
├── assets/
│   └── js/chatbot-widget.js    Support chat widget
├── admin/                      Admin suite (internal)
├── components/                 Component reference files
├── themes/                     Customer theme JSON configs
├── presets/                    Color preset configs
├── theme.json                  Design token schema
├── docs/                       Reference documentation
├── tests/                      Playwright test specs
└── archive/                    Archived variants and unused CSS
```

## Quick Start

```bash
python3 -m http.server 8080
# Open http://localhost:8080
```

## Ingeniux CMS Mapping

| Template Element | Ingeniux Component |
|-----------------|-------------------|
| Header + nav + user menu | SiteControl (Header partial) |
| Footer | SiteControl (Footer partial) |
| Sidebar nav | Navigation field (dynamic from page tree) |
| Article content | Page schema (doc page) |
| Code blocks, callouts | Content Unit tray components |
| Bookmark/Watch buttons | Custom JS + API integration |
| Theme tokens | CSS file per customer deployment |

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile Safari, Chrome Mobile
