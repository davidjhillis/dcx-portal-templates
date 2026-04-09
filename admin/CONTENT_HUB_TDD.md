# Content Hub - Technical Design Document (TDD)

**Version:** 1.0  
**Date:** 2025-01-XX  
**Reference:** Based on Fluid Topics Knowledge Hub capabilities  
**Status:** Requirements Definition

---

## 1. Executive Summary

The Content Hub is the central administration interface for managing content throughout its lifecycle in the Discover CX documentation portal. It provides capabilities for publishing, processing, organizing, and managing content sources, metadata, and access controls.

### 1.1 Objectives

- **Publishing Management**: Enable administrators to publish content from various sources and formats
- **Job Processing**: Track and manage content processing jobs through a queue system
- **Content Lifecycle**: Support the full lifecycle from ingestion to deletion
- **Metadata Management**: Configure and apply metadata schemas to content
- **Source Configuration**: Manage content sources and processing pipelines
- **Access Control**: Configure content access rules and permissions
- **Content Organization**: Organize content through vocabularies, collections, and taxonomies

---

## 2. Core Modules

The Content Hub is organized into the following main modules (tabs):

1. **Publishing** - Content upload, job queue, and job history
2. **Sources** - Content source configuration and management
3. **Enrich and Clean** - Content reprocessing and enrichment
4. **Vocabularies** - Taxonomy and controlled vocabulary management
5. **Metadata Configuration** - Metadata schema and field configuration
6. **Pretty URL** - URL structure and routing configuration
7. **Access Rules** - Content access control configuration
8. **Content Packager** - Content packaging and export (premium feature)

---

## 3. Publishing Module

### 3.1 Publish Content

**Purpose**: Upload and publish content archives to the portal

**Requirements**:
- **Upload Methods**:
  - Drag-and-drop file upload
  - Browse file picker
  - API upload support (via web service)
- **File Constraints**:
  - Maximum archive size: 1.85 GB
  - Maximum individual topic size: 100 MB
  - Support for ZIP archives containing multiple files
- **Source Selection**: 
  - Must select a content source before publishing
  - Source determines processing pipeline
- **Upload Progress**:
  - Real-time progress indicator (0-100%)
  - Upload status notification
  - Cancel upload capability (0-99% only)
- **Post-Upload**: 
  - Upload moves to processing queue at 100%
  - Notification of queue placement

### 3.2 Job Queue

**Purpose**: Track active content processing jobs in real-time

**Requirements**:
- **Job Display**:
  - Card-based layout showing active jobs
  - Job name/archive name
  - Start date and time (local timezone)
  - Job status (Waiting, Running)
  - Elapsed time for running jobs
- **Job Types**:
  - **Publication**: Add or modify content
  - **Deletion**: Remove content from portal
  - **Attachments**: Process attachment files
  - **Reprocessing**: Reprocess existing content
  - **Semantic Indexation**: AI/search index updates
- **Job Details View**:
  - Click job card to open full report
  - Real-time updates during processing
  - List of all publications in job
  - Publication status filters:
    - **Done**: Successfully processed, no errors
    - **Failed**: Processing error prevented publication
    - **Warning**: Errors found but publication succeeded
    - **Waiting**: Processing pending
    - **Stopped**: Manually stopped by administrator
- **Job Actions**:
  - Stop running job (except reprocessing jobs)
  - View full report
  - Mark as stalled (after 30 minutes of inactivity)
- **Stalled Jobs**:
  - Button appears after 30 minutes of inactivity
  - Marks job as failed and removes from queue
  - Job continues in background (may still succeed)
  - Provides way to clear stuck jobs from UI

### 3.3 Job History

**Purpose**: Browse and search past publishing jobs

**Requirements**:
- **Search Tools**:
  - Search bar: Search by upload name, source, user name, or job type
  - Date picker: Filter jobs by specific date
  - Status filter: View jobs by status (Done, Failed, Warning, etc.)
- **History Table Columns**:
  - Link to full job report
  - Job status badge
  - Launch date and time (local timezone)
  - Archive name
  - Processing duration
  - Total publication time (upload to publication)
  - Number of files processed successfully
  - Source name
  - User who launched job
  - Job type
- **Time Display**:
  - Display in user's local timezone
  - Server stores times in UTC
- **API Integration**:
  - Support `publisher` query parameter for API uploads
  - Display publisher name and API key in user column

### 3.4 Job Report

**Purpose**: Detailed view of a specific job with full processing information

**Requirements**:
- **Job Information**:
  - Archive name or job description
  - Upload ID (with copy-to-clipboard button)
  - Job duration
  - User who uploaded/initiated
  - Job status
- **Publication Variants**:
  - List all publication variants created
  - For each variant:
    - Processing status
    - Title (clickable link to Reader/Viewer page)
    - originId (unique identifier)
    - Expandable publication log
- **Job Actions**:
  - **Stop**: Stop running job (disabled for reprocessing)
  - **Retry**: Retry stopped or finished job
    - Uses current portal configuration
    - Publication jobs: 7-day retry window (extends on retry)
    - Reprocessing jobs: No date limit
  - **Download Archive**: Download original uploaded archive
  - **Download Logs**: Download processing logs archive
- **Processing Logs**:
  - Time-stamped log messages
  - Error messages
  - Warning messages
  - Information messages
  - Expandable log sections per publication
- **Download Logs Archive Contents**:
  - `index.md`: Upload ID, status, publication list
  - `publications/` folder: Markdown files per publication
    - Upload status
    - originId
    - khubId

### 3.5 Delete Document

**Purpose**: Remove content from the portal

**Requirements**:
- **Deletion Process**:
  1. Open document in Reader page (structured) or Viewer page (unstructured)
  2. Access via Document shortcut menu or Admin reader
  3. View metadata journal to confirm document
  4. Click Delete button
  5. Confirm deletion in dialog
- **Deletion Tracking**:
  - Deletion appears as job in Queue
  - Trackable in job history
  - Permanent (no undo)
- **Pre-Deletion**:
  - Metadata journal access to verify correct document
  - Confirmation required

### 3.6 Metadata Journal

**Purpose**: View and manage document metadata throughout content lifecycle

**Requirements**:
- **Access Points**:
  - Title bar → View all metadata
  - Topic shortcut menu → Topic metadata / View all metadata
- **Metadata Information**:
  - Last processing date
  - All metadata fields and values
  - Content IDs (originId, khubId)
  - Source information
  - Publication date
  - Editorial type
  - Locale
- **Metadata History**:
  - View past values for metadata keys
  - Shows last 20 values per key
  - Highlights changed values
  - Change count indicator
- **Use Cases**:
  - Verify document before deletion
  - Check processing status
  - Retrieve content IDs
  - Identify source
  - Audit metadata changes

---

## 4. Sources Module

### 4.1 Source Management

**Purpose**: Configure and manage content sources (processing pipelines)

**Requirements**:
- **Source Operations**:
  - View source information
  - Create new source
  - Modify existing source
  - Clean source (remove all content from source)
- **Source Information Display**:
  - Source name
  - Source type/connector
  - Configuration settings
  - Processing pipeline details
- **Default Sources** (pre-installed):
  - Adobe FrameMaker
  - DITA
  - FTML (HTML)
  - MadCap Flare
  - Markdown
  - Microsoft Word
  - OpenAPI
  - Unstructured Documents
- **Source Configuration**:
  - DITA-OT configuration file upload
  - Processing options
  - Format-specific settings
- **Content Deduplication Warning**:
  - Alert when publishing same data through different sources
  - Creates duplicates

---

## 5. Content Types

### 5.1 Structured Publications

**Definition**: Content broken down into topics with metadata, organized in table-of-contents structure

**Types**:
- **Books**: Content that can be separated into individual topics
  - Each topic makes sense independently
  - Fragments are "Book topics"
- **Articles**: Content that is indivisible but may have fragments
  - Fragments are "Article topics"
  - Content forms single unit

**Structure**:
- Made of topics (textual parts)
- Associated through maps (publication structure)
- Map = publication structure without topics
- Examples: DITA, Author-it generated content

### 5.2 Unstructured Publications

**Definition**: Publications that rely on binary/textual resources

**Types**:
- **Unstructured Documents (UD)**:
  - Files intended for indexing (PDF, Word, etc.)
  - Have dedicated Viewer page
  - Can have metadata via control file
  - Self-sufficient files
- **Attachments**:
  - Files attached to structured publications
  - PDFs, videos, images, etc.
  - Not part of indexed content
  - Supporting resources

---

## 6. Enrich and Clean Module

### 6.1 Content Reprocessing

**Purpose**: Reprocess existing content with updated configuration

**Requirements**:
- **Reprocessing Triggers**:
  - Metadata configuration changes
  - Access rule modifications
  - Manual reprocessing request
  - Enrichment operations
- **Reprocessing Jobs**:
  - Appear in Queue
  - Cannot be stopped once started
  - No date limit for retries
- **Use Cases**:
  - Apply new metadata schema
  - Update access rules
  - Refresh content after configuration changes
  - Clean and enrich content

---

## 7. Vocabularies Module

### 7.1 Taxonomy Management

**Purpose**: Manage controlled vocabularies and taxonomies

**Requirements**:
- **Vocabulary Operations**:
  - Create vocabularies
  - Edit vocabularies
  - Delete vocabularies
  - Import/export vocabularies
- **Vocabulary Structure**:
  - Hierarchical taxonomies
  - Flat term lists
  - Controlled values for metadata fields
- **Use Cases**:
  - Product categories
  - Topic classifications
  - Tag hierarchies
  - Metadata value constraints

---

## 8. Metadata Configuration Module

### 8.1 Metadata Schema Management

**Purpose**: Configure metadata fields and schemas

**Requirements**:
- **Schema Operations**:
  - Define metadata fields
  - Configure field types
  - Set validation rules
  - Link to vocabularies
  - Set required/optional
- **Metadata Types**:
  - Text fields
  - Number fields
  - Date fields
  - Enumeration (dropdown)
  - Multi-select
  - Controlled vocabulary links
- **Field Configuration**:
  - Field name
  - Display label
  - Data type
  - Validation rules
  - Default values
  - Help text
- **Schema Application**:
  - Apply to content types
  - Source-specific metadata
  - Global metadata

---

## 9. Pretty URL Module

### 9.1 URL Structure Configuration

**Purpose**: Configure URL patterns and routing

**Requirements**:
- **URL Patterns**:
  - Define URL structure
  - Customize path segments
  - Support for SEO-friendly URLs
- **Routing Rules**:
  - Map URLs to content
  - Handle redirects
  - Support for aliases
- **Configuration Options**:
  - Base URL patterns
  - Content-specific URLs
  - Custom routing rules

---

## 10. Access Rules Module

### 10.1 Content Access Control

**Purpose**: Configure content visibility and access permissions

**Requirements**:
- **Access Rule Types**:
  - User-based access
  - Role-based access
  - Group-based access
  - IP-based access
  - Time-based access
- **Rule Configuration**:
  - Define access rules
  - Apply to content/sources
  - Set permissions (read, write, delete)
  - Configure inheritance
- **Access Control Effects**:
  - Content visibility
  - Search results filtering
  - API access control
  - Portal display filtering

---

## 11. Content Packager Module

**Purpose**: Package and export content (Premium Feature)

**Requirements**:
- **Packaging Operations**:
  - Select content for packaging
  - Configure package options
  - Generate packages
  - Export packages
- **Package Types**:
  - Full content export
  - Selective content export
  - Format-specific packages
- **Premium Feature**:
  - Requires subscription
  - Contact sales for access

---

## 12. User Roles & Permissions

### 12.1 Role Definitions

**ADMIN**:
- Full access to all Content Hub features
- All configuration capabilities
- User management

**KHUB_ADMIN** (Knowledge Hub Administrator):
- All Content Hub features
- Cannot manage users
- Source configuration
- Access rules configuration
- Pretty URL configuration

**CONTENT_PUBLISHER**:
- Publishing interface access
- Publish content
- View job queue
- View job history
- View job reports
- Cannot configure sources
- Cannot configure access rules
- Cannot configure metadata schemas

**PORTAL_ADMIN**:
- Portal configuration (outside Content Hub)
- Theme configuration
- UI configuration

**USERS_ADMIN**:
- User management
- Role assignment

### 12.2 Permission Matrix

| Feature | ADMIN | KHUB_ADMIN | CONTENT_PUBLISHER |
|---------|-------|------------|-------------------|
| Publish Content | ✅ | ✅ | ✅ |
| View Queue | ✅ | ✅ | ✅ |
| View History | ✅ | ✅ | ✅ |
| View Reports | ✅ | ✅ | ✅ |
| Stop Jobs | ✅ | ✅ | ✅ |
| Retry Jobs | ✅ | ✅ | ✅ |
| Configure Sources | ✅ | ✅ | ❌ |
| Configure Metadata | ✅ | ✅ | ❌ |
| Configure Access Rules | ✅ | ✅ | ❌ |
| Configure Pretty URLs | ✅ | ✅ | ❌ |
| Manage Vocabularies | ✅ | ✅ | ❌ |
| Delete Documents | ✅ | ✅ | ✅ |
| Content Packager | ✅ | ✅ | ❌ |

---

## 13. Technical Requirements

### 13.1 File Upload

- **Maximum Archive Size**: 1.85 GB
- **Maximum Topic Size**: 100 MB
- **Supported Formats**: ZIP archives containing content files
- **Upload Methods**: 
  - Browser drag-and-drop
  - File picker
  - API (multipart/form-data)
- **Progress Tracking**: Real-time percentage (0-100%)
- **Cancellation**: Support for upload cancellation (0-99%)

### 13.2 Job Processing

- **Queue System**: Asynchronous job queue
- **Job Types**: Publication, Deletion, Attachments, Reprocessing, Indexation
- **Status Tracking**: Real-time status updates
- **Job Persistence**: Jobs stored in database
- **Retry Logic**: Configurable retry windows
- **Stalled Detection**: 30-minute inactivity threshold

### 13.3 Time Zone Handling

- **Display**: User's local timezone
- **Storage**: UTC in database
- **Conversion**: Automatic timezone conversion for display

### 13.4 Logging

- **Log Levels**: Error, Warning, Info
- **Log Format**: Time-stamped messages
- **Log Storage**: Per-job log files
- **Log Export**: Downloadable archive format
- **Log Contents**: Processing messages, errors, warnings

### 13.5 API Integration

- **Web Services**: RESTful API for all operations
- **Authentication**: API key or OAuth
- **Upload Endpoint**: Multipart file upload
- **Publisher Parameter**: Support for API publisher identification

---

## 14. Data Models

### 14.1 Job Model

```typescript
interface Job {
  id: string;
  uploadId: string;
  name: string;
  type: 'Publication' | 'Deletion' | 'Attachments' | 'Reprocessing' | 'Indexation';
  status: 'Waiting' | 'Running' | 'Done' | 'Failed' | 'Warning' | 'Stopped';
  startTime: Date; // UTC
  endTime?: Date; // UTC
  duration?: number; // milliseconds
  totalDuration?: number; // milliseconds (upload to publication)
  source: string;
  userId: string;
  userName: string;
  archiveName?: string;
  filesProcessed?: number;
  publications?: Publication[];
  logs?: LogEntry[];
  canStop: boolean;
  canRetry: boolean;
  retryWindow?: Date; // 7 days for publications
  isStalled: boolean; // 30+ minutes inactive
}
```

### 14.2 Publication Model

```typescript
interface Publication {
  id: string;
  originId: string;
  khubId: string;
  title: string;
  status: 'Done' | 'Failed' | 'Warning' | 'Waiting' | 'Stopped';
  variant?: string;
  type: 'Book' | 'Article' | 'UnstructuredDocument' | 'Attachment';
  log?: LogEntry[];
  url?: string; // Link to Reader/Viewer page
}
```

### 14.3 Source Model

```typescript
interface Source {
  id: string;
  name: string;
  type: 'DITA' | 'Markdown' | 'Word' | 'Flare' | 'FrameMaker' | 'OpenAPI' | 'FTML' | 'Unstructured';
  isDefault: boolean;
  configuration: SourceConfiguration;
  ditaOtConfig?: File;
}
```

### 14.4 Metadata Model

```typescript
interface Metadata {
  originId: string;
  khubId: string;
  fields: Record<string, MetadataValue>;
  source: string;
  lastProcessed: Date;
  publicationDate: Date;
  editorialType: 'Book' | 'Article';
  locale: string;
  history: MetadataHistory[];
}

interface MetadataValue {
  key: string;
  value: string | number | Date | string[];
  lastUpdated: Date;
}

interface MetadataHistory {
  key: string;
  values: Array<{
    value: string | number | Date | string[];
    timestamp: Date;
  }>;
}
```

---

## 15. UX Requirements

### 15.1 Navigation

- **Tab-based Navigation**: Clear tab structure for main modules
- **Breadcrumbs**: Context-aware breadcrumbs for deep navigation
- **Back Navigation**: Consistent back button/links
- **Quick Actions**: Contextual action buttons

### 15.2 Real-time Updates

- **Queue Refresh**: Auto-refresh or manual refresh for job queue
- **Progress Indicators**: Real-time progress for active jobs
- **Status Badges**: Color-coded status indicators
- **Notifications**: Toast notifications for job completion

### 15.3 Search & Filter

- **Global Search**: Search across jobs, content, sources
- **Filter Sidebar**: Collapsible filter panels
- **Date Range Picker**: Calendar-based date selection
- **Multi-select Filters**: Multiple filter criteria

### 15.4 Responsive Design

- **Desktop First**: Optimized for desktop (768px+ minimum)
- **Mobile Support**: Limited functionality on mobile
- **Tablet Support**: Full functionality on tablets
- **Touch-friendly**: Adequate touch targets

### 15.5 Error Handling

- **Error Messages**: Clear, actionable error messages
- **Validation**: Inline form validation
- **Confirmation Dialogs**: Destructive action confirmations
- **Error Logs**: Accessible error logs in reports

### 15.6 Accessibility

- **Keyboard Navigation**: Full keyboard support
- **Screen Readers**: ARIA labels and roles
- **Color Contrast**: WCAG AA compliance
- **Focus Indicators**: Visible focus states

---

## 16. Implementation Priorities

### Phase 1: Core Publishing (MVP)
1. Publish Content (upload, source selection)
2. Job Queue (view active jobs)
3. Job History (browse past jobs)
4. Basic Job Report (view job details)

### Phase 2: Job Management
1. Stop/Retry jobs
2. Stalled job detection
3. Download archive/logs
4. Real-time queue updates

### Phase 3: Source Management
1. View sources
2. Configure sources
3. Create/modify sources

### Phase 4: Advanced Features
1. Metadata configuration
2. Access rules
3. Vocabularies
4. Pretty URLs
5. Enrich and Clean

### Phase 5: Premium Features
1. Content Packager

---

## 17. Success Metrics

- **Upload Success Rate**: Percentage of successful uploads
- **Processing Time**: Average time from upload to publication
- **Error Rate**: Percentage of failed jobs
- **User Adoption**: Percentage of admins using Content Hub
- **Job Retry Rate**: Frequency of job retries
- **Stalled Job Frequency**: How often jobs stall

---

## 18. References

- [Fluid Topics Knowledge Hub Documentation](https://docs.fluidtopics.com/r/Fluid-Topics-Configuration-and-Administration-Guide/Configure-a-Fluid-Topics-tenant/Knowledge-Hub)
- [Fluid Topics Publishing Guide](https://docs.fluidtopics.com/r/Fluid-Topics-Configuration-and-Administration-Guide/Configure-a-Fluid-Topics-tenant/Knowledge-Hub/Publishing)
- [Fluid Topics API Reference](https://docs.fluidtopics.com/r/Fluid-Topics-API-Reference-Guide)

---

## 19. Appendix

### 19.1 Glossary

- **Archive**: Compressed file (ZIP) containing content to publish
- **Publication**: Content item created from an archive
- **Source**: Processing pipeline/connector for specific content format
- **Topic**: Individual content fragment within a structured publication
- **Map**: Structure/organization of topics in a publication
- **originId**: Unique identifier for content source
- **khubId**: Knowledge Hub unique identifier
- **Reprocessing**: Re-running content through processing pipeline
- **Stalled Job**: Job inactive for 30+ minutes

### 19.2 Content Format Support

**Structured Formats**:
- DITA
- Author-it
- Markdown
- MadCap Flare
- Adobe FrameMaker

**Unstructured Formats**:
- PDF
- Microsoft Word
- HTML
- Images
- Videos
- Archives (ZIP)

---

**Document Status**: Ready for UX Design and Development Planning


