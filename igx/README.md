# DCX Portal - Ingeniux CMS Implementation

Razor views and assets for implementing the Discover CX documentation portal in Ingeniux CMS.

## For the Developer

This folder contains everything you need to add to the DSS Visual Studio project. Copy these files into the corresponding locations in your `Dynamic_Site_Server_Instance.sln`.

### File Mapping

```
igx/                                    → DSS Project Root
├── Views/
│   ├── Shared/
│   │   ├── _Layout.cshtml             → /Views/Shared/_Layout.cshtml
│   │   ├── PageLayout/
│   │   │   ├── Header.cshtml          → /Views/Shared/PageLayout/Header.cshtml
│   │   │   └── Footer.cshtml          → /Views/Shared/PageLayout/Footer.cshtml
│   │   └── Editable/
│   │       ├── Trays.cshtml           → /Views/Shared/Editable/Trays.cshtml
│   │       ├── Tray.cshtml            → /Views/Shared/Editable/Tray.cshtml
│   │       ├── DCXCodeBlock_Unit.cshtml
│   │       ├── DCXCallout_Unit.cshtml
│   │       └── DCXProductCard_Unit.cshtml
│   └── CMSPageDefault/
│       ├── DCX_HomePage.cshtml        → /Views/CMSPageDefault/DCX_HomePage.cshtml
│       ├── DCX_DocPage.cshtml         → /Views/CMSPageDefault/DCX_DocPage.cshtml
│       ├── DCX_SearchResults.cshtml   → /Views/CMSPageDefault/DCX_SearchResults.cshtml
│       ├── DCX_UserProfile.cshtml     → /Views/CMSPageDefault/DCX_UserProfile.cshtml
│       └── DCX_LoginPage.cshtml       → /Views/CMSPageDefault/DCX_LoginPage.cshtml
├── Content/
│   └── css/tokens.css                 → /Content/css/tokens.css
└── Scripts/
    ├── tailwind-config.js             → /Scripts/tailwind-config.js
    ├── user-dropdown.js               → /Scripts/user-dropdown.js
    └── main.js                        → /Scripts/main.js
```

### Reference Templates

The static HTML templates in the parent repo are the source of truth for design. Compare your CMS output against these:

| View | Reference Template |
|------|--------------------|
| DCX_HomePage | `../index.html` |
| DCX_DocPage | `../doc-page.html` |
| DCX_SearchResults | `../search-results.html` |
| DCX_UserProfile | `../user-profile.html` |
| DCX_LoginPage | `../login.html` |
| Header partial | Header section in any template |
| Footer partial | Footer section in any template |

---

## Setup Steps

### 1. Add Files to VS Project

Copy the views, CSS, and JS files into the DSS project at the paths listed above. Add them to the `.csproj` so they deploy.

### 2. Create Schemas in CMS

Create these schemas in **Settings > Schema Designer**. All schema names are prefixed with `DCX_` to avoid conflicts.

#### DCX_SiteControl (SiteControl schema)

| Field | Type | Notes |
|-------|------|-------|
| SiteName | string | Site display name |
| DCXHeader | List (Component) | CompTypes: `DCXHeader` |
| DCXFooter | List (Component) | CompTypes: `DCXFooter` |
| DCXNavigationTab | List (Component) | CompTypes: `DCXNavigationTab` |
| HeadScript | dhtml | Custom head scripts |
| BodyScript | dhtml | Custom body scripts |
| FooterScript | dhtml | Custom footer scripts |

**Properties**: `IsDynamicSitePage: false`, `IsComponent: false`

#### DCXHeader (Component)

| Field | Type |
|-------|------|
| Logo | Asset |
| LogoDark | Asset |
| SearchResults | Link |
| LoginPage | Link |

#### DCXFooter (Component)

| Field | Type |
|-------|------|
| FooterLogo | Asset |
| Tagline | string |
| Copyright | string (use `{year}` placeholder) |
| FooterLinkGroup | List (Component) → DCXFooterLinkGroup |

#### DCXFooterLinkGroup (Component)

| Field | Type |
|-------|------|
| GroupTitle | string |
| FooterLink | Link (list) |

#### DCXNavigationTab (Component)

| Field | Type |
|-------|------|
| TabLink | Link |
| SubLink | Link (list) |

#### DCX_HomePage (Page schema)

| Field | Type |
|-------|------|
| Title | string |
| Subtitle | string |
| SearchPrompt | string |
| SearchResults | Link |
| ProductCards | List (Component) → DCXProductCard |
| ActionCards | List (Component) → DCXActionCard |
| Trays | List (Component) → any tray component |

**Properties**: `IsDynamicSitePage: true`, `ViewName: DCX_HomePage`

#### DCX_DocPage (Page schema)

| Field | Type |
|-------|------|
| Title | string |
| Body | dhtml |
| LastUpdated | string |
| ReadTime | string |
| Versions | Link (list) |
| SidebarNavigation | Navigation (configure start node + depth in UI) |
| ArticleTrays | List (Component) → DCXCodeBlock, DCXCallout |
| Trays | List (Component) → any tray component |

**Properties**: `IsDynamicSitePage: true`, `ViewName: DCX_DocPage`

#### DCXProductCard (Component)

| Field | Type |
|-------|------|
| ProductName | string |
| Subtitle | string |
| Description | string |
| Icon | Asset |
| ProductLink | Link (list) |

#### DCX_SearchResults (Page schema)

| Field | Type |
|-------|------|
| Title | string |
| AIAnswerEnabled | boolean |
| FilterGroups | List (Component) → DCXFilterGroup |

**Properties**: `IsDynamicSitePage: true`, `ViewName: DCX_SearchResults`

Note: Search results are rendered by InSite Search at runtime. The view provides the layout, filter sidebar, and AI answer container.

#### DCXFilterGroup (Component)

| Field | Type |
|-------|------|
| GroupTitle | string |
| FilterOption | List (Component) → DCXFilterOption |

#### DCXFilterOption (Component)

| Field | Type |
|-------|------|
| Label | string |
| Value | string |

#### DCX_UserProfile (Page schema)

| Field | Type |
|-------|------|
| Title | string |

**Properties**: `IsDynamicSitePage: true`, `ViewName: DCX_UserProfile`

Note: User data comes from the portal user system (`IUser`), not page fields. Bookmarks and watched pages need custom API endpoints. See `user-profile.html` for full tab HTML.

#### DCX_LoginPage (Page schema)

| Field | Type |
|-------|------|
| Heading | string |
| Subheading | string |
| SSOProviders | List (Component) → DCXSSOProvider |

**Properties**: `IsDynamicSitePage: true`, `ViewName: DCX_LoginPage`

Note: Uses its own layout (no shared `_Layout.cshtml`). Auth handled by Ingeniux SAML/CustomAccount controllers.

#### DCXSSOProvider (Component)

| Field | Type |
|-------|------|
| Name | string (e.g. "Google", "Microsoft", "Okta") |
| Icon | Asset |

#### DCXActionCard (Component)

| Field | Type |
|-------|------|
| Title | string |
| Description | string |
| ActionLink | Link |

#### DCXCodeBlock (Component)

| Field | Type |
|-------|------|
| Title | string |
| Language | string |
| Code | dhtml |

#### DCXCallout (Component)

| Field | Type |
|-------|------|
| Type | enumeration (info, warning, error, success) |
| Title | string |
| Content | dhtml |

### 3. Finalize All Schemas

Schemas created via API or UI start in Draft mode. You **must finalize** each schema in Schema Designer before pages can be created.

### 4. Create Content Units

Go to **Administration > Presentation Content Units > Mass Create from Component Schemas** and select all DCX component schemas. This enables them for ICE Page Builder drag-and-drop.

### 5. Register SiteControl

Add to `Web.config`:

```xml
<add key="SiteControlSchemas" value="DCX_SiteControl" />
```

If there's an existing SiteControl, append with semicolon:
```xml
<add key="SiteControlSchemas" value="ExistingSiteControl;DCX_SiteControl" />
```

### 6. Configure Navigation Fields

Navigation fields (SidebarNavigation on DCX_DocPage) **must be configured in Schema Designer UI**:

1. Open DCX_DocPage schema
2. Select the SidebarNavigation field
3. Set **Start Node** to the documentation section root page
4. Set **Depth** (e.g., 3 levels)
5. Save and Finalize

### 7. Create Pages

1. Create a DCX_SiteControl page at the site root
2. Populate Header (logo, dark logo) and Footer (logo, tagline, copyright, link groups)
3. Add DCXNavigationTab items for the main nav
4. Create a DCX_HomePage as the site root page
5. Create DCX_DocPage pages under a documentation section

### 8. Publish

Run a full publish to push content to the DSS.

---

## Design Token System

Colors are defined in `Content/css/tokens.css` as CSS custom properties. Tailwind maps them via `Scripts/tailwind-config.js`.

To change the default theme, edit `tokens.css`. For per-customer theming, deploy a different `tokens.css` per DSS instance.

## Dark Mode

Dark mode is controlled by the `dark` class on `<html>`. The theme switcher in the user dropdown (injected by `user-dropdown.js`) toggles this class and persists to localStorage.

## ICE Support

All Content Unit views include `@_Helpers.RenderICEAttribute()` calls on editable elements. When ICE is enabled in CMS Settings, content editors can click directly on rendered text to edit it.

## AI Assists Integration

The doc pages include AI-powered features: article summary, code explanation with Q&A, and AI-enhanced search. The UI for these features is already built in the page views (thinking states, streaming text, feedback buttons). The `ai-assists.js` module provides the API abstraction layer.

### Architecture

```
Page JS (existing UI code in doc-page views)
    │  calls AIAssists.summary(), AIAssists.explainCode(), etc.
    ▼
ai-assists.js (API abstraction layer)
    │  POST /api/ai-assists/summary, /explain, /chat
    ▼
AIAssistsController.cs (.NET MVC controller)
    │  HttpClient call to LLM API
    ▼
LLM Service (Claude API, OpenRouter, or Ingeniux AI service)
```

### Files

| File | Purpose |
|------|---------|
| `Scripts/ai-assists.js` | Client-side API abstraction — mock responses until backend connected |
| `Controllers/AIAssistsController.cs` | .NET controller with endpoints for summary, explain, chat, status |

### Configuration (Web.config)

```xml
<appSettings>
  <add key="AIAssists.Enabled" value="true" />
  <add key="AIAssists.ApiEndpoint" value="https://api.anthropic.com/v1/messages" />
  <add key="AIAssists.ApiKey" value="sk-..." />
  <add key="AIAssists.Model" value="claude-sonnet-4-20250514" />
  <add key="AIAssists.CacheDuration" value="3600" />
</appSettings>
```

### API Endpoints

| Endpoint | Method | Input | Output |
|----------|--------|-------|--------|
| `/api/ai-assists/summary` | POST | `pageId`, `content` | `{ summary, cached }` |
| `/api/ai-assists/explain` | POST | `code`, `language` | `{ overview, breakdowns[] }` |
| `/api/ai-assists/chat` | POST | `message`, `pageContent`, `pageTitle` | `{ response }` |
| `/api/ai-assists/status` | GET | — | `{ enabled, hasApiKey, model }` |

### Connecting to a Real LLM

1. Set `AIAssists.Enabled` to `true` in Web.config
2. Add your API key and endpoint
3. Uncomment the `CallLLM()` method in `AIAssistsController.cs`
4. Replace the TODO mock responses with the `CallLLM()` calls
5. Set `AIAssists.config.useMocks = false` in the client JS (or remove mock fallbacks)

Responses are cached by page ID / content hash. The cache duration is configurable.

### Integrating with Ingeniux AI Services

If Ingeniux provides native AI summary or search services:

1. Replace the `CallLLM()` method in the controller with calls to the Ingeniux AI API
2. For search, the AI answer section in `DCX_SearchResults.cshtml` can be populated by InSite Search's AI features directly — no need to route through this controller

### Mock Mode

By default, `ai-assists.js` returns mock responses so the UI works for demos without a backend. The page views handle these identically to real responses — same streaming, same UI states. When ready to go live, flip `useMocks` to `false`.

### Client API

```javascript
// Initialize with custom endpoint
AIAssists.init({ endpoint: '/api/ai-assists', useMocks: false });

// Summary
var result = await AIAssists.summary(articleText, pageId);
// → { summary: "...", cached: true/false }

// Code explanation
var result = await AIAssists.explainCode(codeText, 'javascript');
// → { overview: "...", breakdowns: [{ lines, code, explanation }] }

// Code Q&A follow-up
var result = await AIAssists.answerCodeQuestion("Why use async?", codeText, 'javascript');
// → { answer: "..." }

// Chat with page context
var result = await AIAssists.chat("How do I configure this?", pageText, pageTitle);
// → { response: "..." }

// Check backend status
var status = await AIAssists.checkStatus();
// → { enabled: true, hasApiKey: true, model: "claude-sonnet-4-20250514" }
```

## Tailwind CDN Note

These templates use Tailwind via CDN (`cdn.tailwindcss.com`). This is fine for development and moderate traffic. For high-traffic production, consider compiling Tailwind with a build step to reduce page weight.
