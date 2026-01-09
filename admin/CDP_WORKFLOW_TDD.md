# Enterprise Content Delivery Platform (CDP) - Workflow TDD

**Version:** 2.0  
**Date:** January 2025  
**Scope:** Enterprise content management with release management and multi-environment deployment  
**Status:** Requirements Definition

---

## 1. Executive Summary

This TDD defines a comprehensive enterprise Content Delivery Platform (CDP) that manages content from ingestion through deployment across multiple environments. Unlike simpler publishing systems, this CDP separates content **ingestion**, **organization**, **release management**, and **deployment** into distinct, controllable workflows.

### 1.1 Core Workflow Stages

```
1. INGEST → Add content to the platform (upload or automated import)
2. ORGANIZE → Define where content appears (collections, portals, routing)
3. RELEASE → Bundle content for coordinated deployment (releases)
4. DEPLOY → Publish to targets (staging, prod, domains, VectorDB)
```

---

## 2. Stage 1: Content Ingestion

### 2.1 Manual Upload

**Purpose:** Manually add content archives to the CDP

**Requirements:**
- Upload ZIP archives (max 1.85 GB)
- Select source type (DITA, Markdown, Word, etc.)
- Upload progress tracking
- Validation before processing
- Upload to staging by default (not production)

**User Stories:**
- As a Content Publisher, I want to upload a content archive so that I can add new documentation to the platform
- As a Content Publisher, I want to see upload progress so that I know when it's complete

### 2.2 Scheduled Imports

**Purpose:** Automate content ingestion from external systems

**Requirements:**
- **Import Connectors:**
  - GitHub repositories (pull on schedule/webhook)
  - GitLab repositories
  - SharePoint folders
  - Confluence spaces
  - Dropbox folders
  - S3 buckets
  - SFTP/FTP servers
  - API endpoints (custom)
  
- **Schedule Configuration:**
  - Cron-based scheduling (hourly, daily, weekly)
  - Webhook triggers (push-based)
  - Manual trigger
  - Dry-run mode (preview without importing)

- **Import Settings Per Connector:**
  - Source credentials (secure vault)
  - Path/folder to monitor
  - File filters (glob patterns)
  - Metadata extraction rules
  - Default source type
  - Target environment (staging/dev)

- **Import Jobs:**
  - Queue system (same as manual uploads)
  - Success/failure notifications
  - Error logs
  - Last import timestamp
  - Changed files detection (delta imports)

**User Stories:**
- As a KHUB_ADMIN, I want to schedule automatic imports from GitHub so that content stays synchronized
- As a KHUB_ADMIN, I want to configure a webhook from our CMS so that content publishes automatically on save
- As a KHUB_ADMIN, I want to see import job history so that I can troubleshoot failures

**Data Model:**
```typescript
interface ImportConnector {
  id: string;
  name: string;
  type: 'github' | 'gitlab' | 'sharepoint' | 'confluence' | 's3' | 'sftp' | 'api';
  enabled: boolean;
  schedule: CronSchedule | null;
  webhookUrl?: string; // If webhook-based
  credentials: {
    type: 'oauth' | 'token' | 'username_password' | 'api_key';
    vaultId: string; // Secure storage
  };
  config: {
    repository?: string; // For GitHub/GitLab
    branch?: string;
    path?: string; // Folder/path to monitor
    fileFilter?: string; // Glob pattern
    bucket?: string; // For S3
    space?: string; // For Confluence
  };
  sourceType: string; // DITA, Markdown, etc.
  targetEnvironment: 'dev' | 'staging';
  metadataRules: MetadataExtractionRule[];
  lastImport?: Date;
  lastStatus?: 'success' | 'failure';
}

interface CronSchedule {
  frequency: 'hourly' | 'daily' | 'weekly' | 'custom';
  customCron?: string; // e.g., "0 0 * * *"
  timezone: string;
}

interface MetadataExtractionRule {
  field: string; // Metadata field name
  extractFrom: 'filename' | 'frontmatter' | 'git_commit' | 'custom';
  pattern?: string; // Regex for extraction
}
```

---

## 3. Stage 2: Content Organization

### 3.1 Portal Structure

**Purpose:** Define where content appears on the portal(s)

**Concept:** Content doesn't automatically appear anywhere after ingestion. Admins must explicitly map content to portal locations using metadata-based rules.

**Requirements:**

#### 3.1.1 Portal Destinations

Define **Portal Sections** where content can appear:

- **Home Page Sections:**
  - Featured content cards
  - Getting started section
  - Popular topics
  - Recent updates
  - Quick links

- **Navigation Structure:**
  - Top-level categories (Product Docs, API Reference, Tutorials, etc.)
  - Sub-categories
  - Custom portal pages

- **Search Scopes:**
  - Which content appears in which search contexts
  - Faceted search categories

**Data Model:**
```typescript
interface PortalDestination {
  id: string;
  name: string; // e.g., "Home - Featured Content", "Product Docs - Portal v10"
  type: 'homepage_section' | 'nav_category' | 'search_scope' | 'custom_page';
  path: string; // URL path where this appears
  displayOrder: number;
  parent?: string; // For hierarchical navigation
  rules: ContentMappingRule[];
}

interface ContentMappingRule {
  id: string;
  name: string;
  description: string;
  conditions: MetadataCondition[]; // AND/OR logic
  actions: {
    addToDestination: string[]; // Portal destination IDs
    setURL?: string; // Pretty URL template: {product}/{version}/{title}
    setVisibility?: 'public' | 'authenticated' | 'group'; // Access control
    setPriority?: number; // Display order
  };
  enabled: boolean;
}

interface MetadataCondition {
  field: string; // e.g., "product", "version", "type"
  operator: 'equals' | 'contains' | 'startsWith' | 'matches' | 'exists';
  value: string | string[];
  logic?: 'AND' | 'OR'; // How to combine with next condition
}
```

#### 3.1.2 Auto-Organization (Smart Collections)

**Purpose:** Automatically organize content based on metadata

**Requirements:**
- Define rules based on metadata
- Content automatically added/removed as metadata changes
- Rules evaluated on every import/publish
- Multiple rules can apply to same content

**Examples:**
- Rule: `product=Portal v10` AND `type=tutorial` → Add to "Portal v10 Tutorials" section
- Rule: `audience=developer` → Include in developer portal search
- Rule: `featured=true` → Show on home page

**User Stories:**
- As a KHUB_ADMIN, I want to create a rule that automatically adds Portal v10 docs to the Portal v10 navigation section
- As a KHUB_ADMIN, I want featured content to automatically appear on the home page without manual curation

#### 3.1.3 Manual Collections

**Purpose:** Manually curate content groupings

**Requirements:**
- Create named collections
- Manually add/remove documents
- Set collection metadata (description, icon, color)
- Map collections to portal destinations
- Order documents within collection

**User Stories:**
- As a Content Publisher, I want to create a "New in January 2025" collection so that I can manually curate release highlights
- As a Content Publisher, I want to reorder documents in a collection so that the most important appear first

### 3.2 URL Routing & Pretty URLs

**Purpose:** Define how content is accessed via URLs

**Requirements:**
- **URL Templates:** Based on metadata patterns
  - Example: `/{product}/{version}/{category}/{title}`
  - Example: `/api/{version}/{endpoint-name}`
  - Example: `/tutorials/{topic}/{title}`

- **Template Priority:** Rules evaluated in order
- **Fallback:** Default URL if no template matches
- **Validation:** Ensure URL uniqueness
- **Redirects:** Manage old URLs when content moves

**User Stories:**
- As a KHUB_ADMIN, I want to define URL patterns based on product and version so that URLs are SEO-friendly and predictable
- As a KHUB_ADMIN, I want to set up redirects for old URLs so that links don't break when we reorganize

---

## 4. Stage 3: Release Management

### 4.1 Release Concept

**Purpose:** Bundle content updates for coordinated deployment

**Key Insight:** Releases allow you to:
- Stage multiple content items together
- Review all changes before deployment
- Deploy everything at once (atomic release)
- Schedule releases for specific dates/times
- Rollback entire releases if needed

### 4.2 Release Types

#### 4.2.1 Incremental Update
**Scope:** Small, ongoing updates  
**Frequency:** Continuous/daily  
**Examples:** Bug fixes, minor edits, new KB articles  
**Deployment:** Can auto-deploy to production

#### 4.2.2 Major Update
**Scope:** Significant content additions/changes  
**Frequency:** Weekly/monthly  
**Examples:** New feature documentation, major reorganization  
**Deployment:** Requires review before production

#### 4.2.3 Product Release
**Scope:** Coordinated multi-document release tied to product launch  
**Frequency:** Quarterly/as needed  
**Examples:** New product version, major feature launch  
**Deployment:** Scheduled for specific date/time, all-or-nothing

### 4.3 Release Workflow

**Requirements:**

1. **Create Release:**
   - Name (e.g., "Portal v10.5 Launch")
   - Description
   - Type (Incremental, Major, Product)
   - Target date (for product releases)
   - Status: Draft, Ready, Scheduled, Deployed, Rolled Back

2. **Add Content to Release:**
   - Automatically include all content since last release (for incremental)
   - Manually select documents for release
   - Tag content with release ID during import
   - View all content in release (grouped by source/type)
   - Preview changes (what's new, modified, deleted)

3. **Release Review:**
   - See diff of all changes
   - Validate all content processed successfully
   - Check for broken links
   - Review metadata completeness
   - Approve/reject individual items
   - Approve release for deployment

4. **Schedule Deployment:**
   - Immediate deployment
   - Scheduled deployment (date/time)
   - Manual trigger
   - Deployment to specific environment(s)

5. **Deploy Release:**
   - Atomic deployment (all content goes live together)
   - Progress tracking
   - Rollback capability if errors
   - Notification on completion

6. **Post-Deployment:**
   - Mark release as deployed
   - Archive release
   - Create next release automatically

**Data Model:**
```typescript
interface Release {
  id: string;
  name: string;
  description: string;
  type: 'incremental' | 'major' | 'product';
  status: 'draft' | 'ready' | 'scheduled' | 'deploying' | 'deployed' | 'failed' | 'rolled_back';
  
  createdAt: Date;
  createdBy: string;
  
  targetDate?: Date; // For product releases
  deploymentDate?: Date;
  deployedBy?: string;
  
  content: ReleaseContent[];
  
  targets: DeploymentTarget[]; // Which environments
  
  approvals: {
    requiredApprovers: string[];
    approvedBy: string[];
    approvedAt?: Date;
    status: 'pending' | 'approved' | 'rejected';
  };
  
  deployment?: {
    startTime: Date;
    endTime?: Date;
    status: 'running' | 'complete' | 'failed';
    logs: DeploymentLog[];
  };
}

interface ReleaseContent {
  documentId: string;
  changeType: 'new' | 'modified' | 'deleted';
  sourcePath: string;
  title: string;
  metadata: Record<string, any>;
  validationStatus: 'pending' | 'passed' | 'failed';
  validationErrors?: string[];
  includedInRelease: boolean; // Can exclude items from release
}
```

**User Stories:**
- As a Content Publisher, I want to create a release for Portal v10.5 so that I can deploy all related documentation together
- As a KHUB_ADMIN, I want to review all content in a release before deployment so that I can ensure quality
- As a KHUB_ADMIN, I want to schedule a release for January 15 at 9 AM so that it goes live with the product launch
- As a KHUB_ADMIN, I want to rollback a release if issues are found so that I can quickly revert to the previous state

---

## 5. Stage 4: Deployment & Targets

### 5.1 Deployment Targets

**Purpose:** Deploy content to multiple environments and endpoints

**Target Types:**

#### 5.1.1 Environments
- **Development** - For testing and preview
- **Staging** - Pre-production validation
- **Production** - Live portal

#### 5.1.2 Portals/Domains
- **Primary Portal** - Main documentation site (docs.example.com)
- **Customer Portal** - Customer-only docs (customers.example.com)
- **Partner Portal** - Partner documentation (partners.example.com)
- **Internal Portal** - Internal wiki (internal.example.com)
- **Regional Portals** - Language/region specific (docs.eu.example.com)

#### 5.1.3 Vector Databases
- **Production VectorDB** - For AI features (search, chatbot, recommendations)
- **Staging VectorDB** - Testing AI before production
- **Analytics VectorDB** - For semantic analytics

#### 5.1.4 CDN/Edge Locations
- Content distribution networks
- Edge caching
- Geographic distribution

### 5.2 Deployment Configuration

**Requirements:**

**Per-Target Configuration:**
```typescript
interface DeploymentTarget {
  id: string;
  name: string;
  type: 'environment' | 'portal' | 'vectordb' | 'cdn';
  
  environment?: 'dev' | 'staging' | 'production';
  
  // For portal targets
  domain?: string;
  baseUrl?: string;
  
  // For VectorDB targets
  vectorDBConfig?: {
    provider: 'pinecone' | 'weaviate' | 'qdrant' | 'milvus';
    apiKey: string;
    index: string;
    namespace?: string;
    chunkSize?: number;
    embeddingModel?: string;
  };
  
  // For CDN targets
  cdnConfig?: {
    provider: 'cloudflare' | 'fastly' | 'akamai';
    purgeCache: boolean;
  };
  
  accessControl: {
    enabled: boolean;
    defaultGroup: 'public' | 'authenticated' | 'none';
    rules: AccessRule[];
  };
  
  contentFilters?: ContentFilter[]; // Only deploy matching content
  
  enabled: boolean;
  lastDeployment?: Date;
  deploymentStatus?: 'idle' | 'deploying' | 'error';
}

interface ContentFilter {
  field: string; // e.g., "audience", "product"
  operator: 'equals' | 'not_equals' | 'contains';
  value: string | string[];
}
```

**User Stories:**
- As an ADMIN, I want to configure deployment targets for dev, staging, and production so that I can control where content goes
- As an ADMIN, I want to deploy Portal v10 docs only to the public portal and Portal v9 docs to the customer portal
- As an ADMIN, I want to sync all content to the VectorDB for AI features so that search and chatbot work correctly

### 5.3 Deployment Workflow

**Requirements:**

1. **Select Release** - Choose which release to deploy
2. **Select Targets** - Choose one or more deployment targets
3. **Preview Deployment:**
   - Show what content will be deployed to each target
   - Show what will be added, modified, removed
   - Estimate deployment time
   - Check for conflicts
4. **Confirm Deployment** - Review and confirm
5. **Deploy:**
   - Deploy to all targets in parallel
   - Real-time progress per target
   - Stop deployment on error (or continue)
6. **Post-Deployment:**
   - Verify deployment success
   - Run smoke tests
   - Purge CDN caches
   - Update VectorDB indexes
   - Send notifications

**Deployment Strategies:**
- **Atomic:** All-or-nothing deployment
- **Progressive:** Deploy to targets sequentially (dev → staging → prod)
- **Blue-Green:** Deploy to alternate environment, then switch
- **Canary:** Deploy to subset of users first

**User Stories:**
- As an ADMIN, I want to deploy a release to staging first so that I can test before production
- As an ADMIN, I want to see deployment progress for each target so that I know when it's complete
- As an ADMIN, I want to rollback a deployment if errors occur so that the portal doesn't break

---

## 6. Content Organization Deep Dive

### 6.1 Organization Mechanisms

Fluid Topics uses **metadata + access rules** to organize content. We'll enhance this with explicit **portal mapping**.

#### 6.1.1 Metadata-Based Organization

**How Fluid Topics Does It:**
- Content has metadata (product, version, audience, type, etc.)
- Access rules bind metadata values to user groups
- Pretty URL templates use metadata for routing
- Search facets based on metadata

**What We'll Add:**
- **Portal Mapping Rules:** Explicitly define which content appears where
- **Multi-Portal Support:** Same content can appear on multiple portals
- **Portal-Specific Presentation:** Same doc, different styling/context per portal

#### 6.1.2 Portal Mapping Rules

**Concept:** Rules that say "Content with metadata X appears in portal location Y"

**Example Rules:**
```yaml
Rule: "Portal v10 Documentation"
Conditions:
  - product = "Portal v10"
  - type IN ["documentation", "tutorial", "guide"]
Actions:
  - Add to navigation: "Product Docs > Portal v10"
  - Include in search scope: "Portal v10"
  - Set URL template: "/docs/portal-v10/{category}/{title}"
  - Show on home page if: featured = true

Rule: "API Reference"
Conditions:
  - type = "api-reference"
Actions:
  - Add to navigation: "API > {version}"
  - Set URL template: "/api/{version}/{endpoint}"
  - Exclude from home page

Rule: "Customer-Only Content"
Conditions:
  - audience = "customer"
Actions:
  - Deploy to: Customer Portal (customers.example.com)
  - Restrict access to: Customer group
  - Exclude from public portal
```

**User Stories:**
- As a KHUB_ADMIN, I want to create a rule that puts all Portal v10 docs under "Product Docs > Portal v10" in navigation
- As a KHUB_ADMIN, I want customer-only content to only appear on the customer portal domain
- As a KHUB_ADMIN, I want to set featured=true to make content appear on the home page

### 6.2 Collections

**Purpose:** Manual content curation and grouping

**Types:**
- **Manual Collections:** Hand-picked document lists
- **Smart Collections:** Rule-based (auto-updating)

**Use Cases:**
- "What's New in v10.5" (manual, curated for release)
- "Getting Started Path" (manual, ordered learning path)
- "All API Docs" (smart collection, auto-updates)
- "Troubleshooting Guides" (smart collection)

**User Stories:**
- As a Content Publisher, I want to create a "Getting Started" collection with 5 key docs in a specific order
- As a Content Publisher, I want to create a smart collection for all tutorial content so it stays up to date automatically

---

## 7. Revised Tab Structure

Based on the 4-stage workflow, here's the new Content Hub structure:

### Tab 1: **Content**
**Purpose:** Ingest and view all content in the platform

**Sub-tabs:**
- **Upload** - Manual upload interface
- **Imports** - Scheduled/automated import connectors
- **Library** - Browse all ingested content (regardless of publication status)
- **Jobs** - View processing jobs (upload, import, reprocess)

### Tab 2: **Organization**
**Purpose:** Define where content appears on portals

**Sub-tabs:**
- **Portal Map** - Define portal destinations and mapping rules
- **Collections** - Manual and smart collections
- **URLs** - Pretty URL templates and routing
- **Access** - Access control rules per content/portal

### Tab 3: **Releases**
**Purpose:** Bundle and manage content releases

**Sub-tabs:**
- **Active Releases** - Releases in progress (draft, ready, scheduled)
- **Deployed** - Release history
- **Create Release** - New release wizard

### Tab 4: **Deployment**
**Purpose:** Manage deployment targets and deploy releases

**Sub-tabs:**
- **Targets** - Configure deployment targets (environments, portals, VectorDB)
- **Deploy** - Deploy a release to targets
- **History** - Deployment history and logs

### Tab 5: **Sources**
**Purpose:** Manage content sources (same as before)

---

## 8. Key User Workflows

### Workflow 1: Quick Content Update (Incremental)
1. Upload content → **Content > Upload**
2. Content auto-organized by existing rules
3. Goes into "Continuous Deployment" release (auto-created)
4. Auto-deploys to staging
5. Manual deploy to production when ready

### Workflow 2: Product Release (Major)
1. Over several weeks:
   - Import content from GitHub (scheduled)
   - Upload additional docs manually
   - Tag all with metadata: `release=v10.5`
2. Week before launch:
   - Create release: "Portal v10.5 Launch" → **Releases > Create**
   - Add all content with `release=v10.5` tag
   - Create collection: "What's New in v10.5"
   - Configure portal mapping for new features
3. Day before launch:
   - Deploy release to staging → **Deployment > Deploy**
   - Review and test
4. Launch day:
   - Schedule deployment to production for 9 AM
   - Deploy to VectorDB
   - Deploy executes automatically
5. Post-launch:
   - Monitor deployment logs
   - View deployed release in history

### Workflow 3: Multi-Portal Deployment
1. Upload customer-specific docs
2. Set metadata: `audience=customer`
3. Create mapping rule:
   - Condition: `audience=customer`
   - Action: Deploy to Customer Portal only
4. Create release: "Customer Q1 Updates"
5. Deploy to:
   - ✅ Staging (customers-staging.example.com)
   - ✅ Customer VectorDB
   - ❌ Public Portal (excluded by rule)
6. After review, deploy to production Customer Portal

---

## 9. UI/UX Requirements

### 9.1 Content Tab

**Upload Sub-tab:**
- Large dropzone
- Source selector
- Progress tracking
- Success → "Add to Release" prompt

**Imports Sub-tab:**
- List of import connectors (cards)
- Status (active, paused, error)
- Last import time
- Configure connector button
- Trigger manual import button
- View import history

**Library Sub-tab:**
- All content (published and unpublished)
- Filters: source, metadata, release, deployment status
- Deployment status badges:
  - ⚪ Not deployed
  - 🟡 Staging only
  - 🟢 Production
  - 🔵 Multi-portal
- Click document → view metadata, releases, deployment history

**Jobs Sub-tab:**
- Queue (active jobs)
- History (completed jobs)
- Same as current implementation

### 9.2 Organization Tab

**Portal Map Sub-tab:**
- Visual tree of portal structure
- Each node shows:
  - Portal destination (navigation category, home section, etc.)
  - Mapping rules
  - Document count
- Add/edit mapping rules
- Preview which content goes where

**Collections Sub-tab:**
- Grid of collections (manual + smart)
- Create collection button
- Edit collection (add/remove docs, reorder)

**URLs Sub-tab:**
- List of URL templates
- Priority ordering (drag to reorder)
- Test URL generator (enter metadata, see resulting URL)
- Redirects management

**Access Sub-tab:**
- Access rules table
- Default access setting
- Create/edit rules
- Preview affected content

### 9.3 Releases Tab

**Active Releases Sub-tab:**
- Cards for each non-deployed release
- Status, date, content count
- Click to expand:
  - Content list (with add/remove)
  - Deployment targets
  - Schedule
  - Approve/deploy buttons

**Deployed Sub-tab:**
- Table of past releases
- Filters: date range, type, status
- Click to view details and deployment logs

**Create Release:**
- Wizard:
  1. Basic info (name, type, date)
  2. Add content (search/filter to find)
  3. Select targets
  4. Schedule (immediate, scheduled, manual)
  5. Review and create

### 9.4 Deployment Tab

**Targets Sub-tab:**
- Cards for each target
- Status (configured, deploying, error)
- Last deployment time
- Health check status
- Edit configuration button
- Test connection button

**Deploy Sub-tab:**
- Select release (dropdown)
- Select targets (checkboxes)
- Preview deployment (what will change)
- Deployment options (atomic, progressive, etc.)
- Deploy button
- Real-time progress for each target
- Logs

**History Sub-tab:**
- Table of all deployments
- Columns: release, targets, date, duration, status, deployed by
- Click to view logs
- Rollback button (for recent deployments)

---

## 10. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTENT INGESTION                        │
│  Upload Manual  │  Scheduled Imports  │  Webhook Triggers   │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                   PROCESSING QUEUE                          │
│  Convert → Index → Extract Metadata → Validate             │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                   CONTENT LIBRARY                           │
│  All Content (Published + Unpublished) with Metadata       │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│              ORGANIZATION (Mapping Rules)                   │
│  Portal Map → Collections → URLs → Access Control          │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                  RELEASE MANAGEMENT                         │
│  Bundle Content → Review → Schedule → Approve              │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT                              │
│  Dev → Staging → Production → Portals → VectorDB          │
└─────────────────────────────────────────────────────────────┘
```

---

## 11. Key Differences from Fluid Topics

| Aspect | Fluid Topics | Our CDP |
|--------|--------------|---------|
| **Publishing Model** | Upload = immediate processing | Upload = ingestion only |
| **Organization** | Metadata + access rules | Explicit portal mapping + metadata |
| **Release Management** | No concept of releases | Full release workflow |
| **Deployment** | Single portal/environment | Multi-environment, multi-portal |
| **VectorDB** | Not mentioned | First-class deployment target |
| **Scheduling** | No scheduled imports | Automated import connectors |
| **Approval Workflow** | No approvals | Release approvals required |

---

## 12. API Endpoints Required

### Content Ingestion
- `POST /api/content/upload` - Manual upload
- `GET /api/content/imports` - List import connectors
- `POST /api/content/imports` - Create import connector
- `PUT /api/content/imports/{id}` - Update connector
- `POST /api/content/imports/{id}/trigger` - Manual trigger
- `GET /api/content/imports/{id}/history` - Import history

### Organization
- `GET /api/organization/portal-map` - Get portal structure
- `POST /api/organization/mapping-rules` - Create mapping rule
- `GET /api/organization/collections` - List collections
- `POST /api/organization/collections` - Create collection
- `GET /api/organization/url-templates` - List URL templates
- `POST /api/organization/access-rules` - Create access rule

### Releases
- `GET /api/releases` - List releases
- `POST /api/releases` - Create release
- `PUT /api/releases/{id}` - Update release
- `POST /api/releases/{id}/content` - Add content to release
- `DELETE /api/releases/{id}/content/{docId}` - Remove content
- `POST /api/releases/{id}/approve` - Approve release
- `POST /api/releases/{id}/schedule` - Schedule deployment

### Deployment
- `GET /api/deployment/targets` - List targets
- `POST /api/deployment/targets` - Create target
- `POST /api/deployment/deploy` - Deploy release to targets
- `GET /api/deployment/history` - Deployment history
- `POST /api/deployment/{id}/rollback` - Rollback deployment
- `GET /api/deployment/{id}/logs` - Deployment logs
- `GET /api/deployment/targets/{id}/health` - Health check

---

## 13. Implementation Priority

### Phase 1: Basic Ingestion & Library (Week 1-2)
- Upload content
- Processing jobs
- Content library
- Basic metadata

### Phase 2: Organization & Mapping (Week 3-4)
- Portal mapping rules
- Collections
- URL templates
- Access rules

### Phase 3: Release Management (Week 5-6)
- Create releases
- Add content to releases
- Release approval workflow
- Basic deployment (staging only)

### Phase 4: Multi-Environment Deployment (Week 7-8)
- Deployment targets configuration
- Deploy to multiple environments
- Deployment history and rollback

### Phase 5: Automated Imports (Week 9-10)
- Import connectors (GitHub, GitLab)
- Scheduled imports
- Webhook integrations

### Phase 6: Advanced Deployment (Week 11-12)
- VectorDB deployment
- Multi-portal deployment
- Progressive deployment strategies
- Blue-green deployments

---

## 14. Success Metrics

**Content Ingestion:**
- Time to import content: <5 minutes for 100MB archive
- Import success rate: >95%
- Scheduled imports: 99% uptime

**Organization:**
- Time to configure mapping rule: <3 minutes
- Content auto-organized: 80%+ (only 20% manual)
- URL template coverage: 100% of content has pretty URLs

**Release Management:**
- Time to create release: <10 minutes
- Release approval time: <24 hours
- Deployment success rate: >99%

**Deployment:**
- Staging deployment time: <5 minutes
- Production deployment time: <15 minutes
- Rollback time: <2 minutes
- VectorDB sync time: <30 minutes for full index

---

## 15. Next Steps

1. **Review this TDD** - Validate workflow with stakeholders
2. **Create detailed mockups** - For all 5 tabs and key workflows
3. **Define API contracts** - Detailed endpoint specifications
4. **Build Phase 1** - Content ingestion and library
5. **Iterate** - Test with real content and refine

---

**Document Status:** Ready for review and UX design sprint


