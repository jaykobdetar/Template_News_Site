# Project Structure Overview

This document provides a comprehensive overview of the Influencer News CMS project structure and file organization.

## 📁 Root Directory Structure

```
InfNews/
├── 📄 Core Application Files
│   ├── integration_manager.py          # Main GUI application
│   ├── sync_site.py                   # Site synchronization utility
│   └── test_integration_manager_sync.py # Testing utility
│
├── 🌐 Website Files
│   ├── index.html                     # Homepage
│   ├── search.html                    # Search page
│   ├── authors.html                   # Authors listing
│   ├── article.html                   # Article template (legacy)
│   ├── article_1.html                 # Sample article page
│   └── 404.html                       # Error page
│
├── 📝 Content Directories
│   └── content/
│       ├── articles/                  # Article source files (.txt)
│       ├── authors/                   # Author profile files (.txt)
│       ├── categories/                # Category definition files (.txt)
│       └── trending/                  # Trending topic files (.txt)
│
├── 🎯 Generated Content
│   └── integrated/
│       ├── articles/                  # Generated article pages
│       ├── authors/                   # Generated author profile pages
│       ├── categories/                # Generated category pages + listing
│       ├── trending/                  # Generated trending pages + listing
│       ├── categories.html            # Categories overview page
│       └── trending.html              # Trending topics overview page
│
├── 🗄️ Database Files
│   └── data/
│       ├── articles_db.json           # Article tracking database
│       ├── authors_db.json            # Author profile database
│       ├── categories_db.json         # Category definitions database
│       └── trending_db.json           # Trending topics database
│
├── ⚙️ Core Logic
│   └── src/
│       └── integrators/
│           ├── __init__.py             # Package initialization
│           ├── base_integrator.py      # Shared functionality
│           ├── article_integrator.py   # Article processing
│           ├── author_integrator.py    # Author profile processing
│           ├── category_integrator.py  # Category management
│           ├── trending_integrator.py  # Trending topics processing
│           └── unintegrator.py         # Content removal system
│
├── 📚 Documentation
│   ├── README.md                      # Main project documentation
│   ├── QUICK_START_GUIDE.md           # 5-minute setup guide
│   ├── CONTENT_FORMAT_GUIDE.md        # Complete format reference
│   ├── INTEGRATION_GUIDE.md           # Advanced usage guide
│   ├── CONTRIBUTING.md                # Contribution guidelines
│   ├── CHANGELOG.md                   # Version history
│   ├── SECURITY.md                    # Security policy
│   ├── PROJECT_STRUCTURE.md           # This file
│   └── docs/
│       ├── FAQ.md                     # Frequently asked questions
│       ├── article_format_guide.md    # Legacy format guide
│       └── sample article.txt         # Legacy sample file
│
├── 🏗️ GitHub Integration
│   ├── .github/
│   │   ├── workflows/
│   │   │   └── ci.yml                 # Continuous integration
│   │   ├── ISSUE_TEMPLATE/
│   │   │   ├── bug_report.md          # Bug report template
│   │   │   └── feature_request.md     # Feature request template
│   │   └── pull_request_template.md   # PR template
│   ├── .gitignore                     # Git ignore rules
│   ├── LICENSE                        # MIT license
│   ├── requirements.txt               # Python dependencies (none)
│   └── setup.py                       # Package setup configuration
│
├── 🖼️ Assets
│   ├── screenshots/                   # Application screenshots
│   │   ├── article.png                # Sample article page
│   │   ├── authors.png                # Authors page
│   │   ├── home.png                   # Homepage
│   │   └── search.png                 # Search page
│   └── articles/                      # Legacy article files
│       └── platform_update_news.txt   # Sample content
│
└── 🔗 Additional Files
    ├── articles_db.json               # Legacy database file
    ├── link_verification.py           # Utility script
    ├── article_integrator.py          # Legacy integrator
    ├── readme.md                      # Legacy readme
    └── SITEMAP.md                     # Site structure reference
```

## 📋 File Categories

### Core Application Files
| File | Purpose | Usage |
|------|---------|-------|
| `integration_manager.py` | Main GUI application | Primary interface for content management |
| `sync_site.py` | Site synchronization | Align website with database state |

### Content Source Files (`content/`)
| Directory | Content Type | Format | Output Location |
|-----------|--------------|--------|-----------------|
| `articles/` | News articles | `.txt` with metadata + markdown | `integrated/articles/` |
| `authors/` | Author profiles | `.txt` with profile data + bio | `integrated/authors/` |
| `categories/` | Content categories | `.txt` with category settings | `integrated/categories/` |
| `trending/` | Trending topics | `.txt` with metrics + analysis | `integrated/trending/` |

### Generated Content (`integrated/`)
| Directory | Generated Files | Purpose |
|-----------|----------------|---------|
| `articles/` | `article_X.html` | Individual article pages |
| `authors/` | `author_slug.html` | Author profile pages |
| `categories/` | `category_slug.html` + `categories.html` | Category pages + overview |
| `trending/` | `trend_slug.html` + `trending.html` | Trending pages + overview |

### Database Files (`data/`)
| File | Purpose | Structure |
|------|---------|-----------|
| `articles_db.json` | Article tracking | Array of article objects with metadata |
| `authors_db.json` | Author profiles | Array of author objects with profile data |
| `categories_db.json` | Category definitions | Array of category objects with settings |
| `trending_db.json` | Trending topics | Array of trending objects with metrics |

### Core Logic (`src/integrators/`)
| File | Purpose | Extends |
|------|---------|---------|
| `base_integrator.py` | Shared functionality | - |
| `article_integrator.py` | Article processing | BaseIntegrator |
| `author_integrator.py` | Author processing | BaseIntegrator |
| `category_integrator.py` | Category processing | BaseIntegrator |
| `trending_integrator.py` | Trending processing | BaseIntegrator |
| `unintegrator.py` | Content removal | - |

## 🔄 Data Flow

### Content Creation Flow
```
1. User creates .txt file in content/[type]/
2. User runs integration via GUI
3. Integrator parses file and validates format
4. Content stored in data/[type]_db.json
5. HTML page generated in integrated/[type]/
6. Navigation and listing pages updated
7. Cross-links established with related content
```

### Content Management Flow
```
1. User views content via Content Browser
2. User selects content for removal
3. Unintegrator removes database entries
4. Associated HTML files deleted
5. Listing pages updated
6. Navigation links cleaned up
```

### Synchronization Flow
```
1. User runs sync_site.py
2. All databases loaded
3. Listing pages regenerated from database state
4. Navigation links updated
5. Orphaned files identified and optionally removed
```

## 🎯 Content Type Relationships

### Cross-Referencing System
```
Articles ←→ Authors (by exact name match)
    ↓
Categories (by slug match)
    ↑
Trending Topics (by category slug)
```

### File Naming Conventions
| Content Type | Source File | Generated File | ID Pattern |
|--------------|-------------|----------------|------------|
| Articles | `my-article.txt` | `article_X.html` | Sequential numbers |
| Authors | `firstname-lastname.txt` | `author_firstname-lastname.html` | Slug-based |
| Categories | `category-slug.txt` | `category_slug.html` | Slug-based |
| Trending | `topic-slug.txt` | `trend_slug.html` | Slug-based |

## 🛠️ Development Structure

### Extension Points
| Component | Purpose | Extension Method |
|-----------|---------|------------------|
| BaseIntegrator | Add new content types | Extend class and implement abstract methods |
| GUI tabs | Add new interfaces | Create new tab in integration_manager.py |
| HTML templates | Customize appearance | Modify generation methods in integrators |
| Content validation | Add new fields | Update parse_content_file methods |

### Configuration Files
| File | Purpose | Format |
|------|---------|--------|
| `.gitignore` | Git exclusions | Standard gitignore format |
| `requirements.txt` | Dependencies | pip requirements format (currently empty) |
| `setup.py` | Package configuration | Python setuptools format |

## 📊 Size and Complexity

### File Count by Category
- **Core Application**: 2 files
- **Website Templates**: 5 files  
- **Documentation**: 10+ files
- **Source Code**: 6 Python modules
- **Configuration**: 5 files
- **GitHub Integration**: 6 files

### Lines of Code (Approximate)
- **GUI Application**: 1,400 lines
- **Core Integrators**: 2,000 lines
- **Sync Utility**: 130 lines
- **Documentation**: 3,000+ lines

## 🔐 Security Considerations

### File Access Patterns
- **Read Access**: `content/` directories, `data/` JSON files
- **Write Access**: `integrated/` directories, `data/` JSON files, main HTML files
- **No Network Access**: Except for user-provided image URLs in content

### Data Sensitivity
- **Public Content**: All generated HTML is intended for public websites
- **No Authentication**: Desktop application assumes trusted local user
- **Local Storage**: All data stored in plain text/JSON format

## 🚀 Deployment Considerations

### Portable Deployment
- **No Installation Required**: Runs directly from directory
- **Self-Contained**: All dependencies are Python built-ins
- **Cross-Platform**: Works on Windows, macOS, Linux

### Production Website
- **Static Files Only**: Generated content is pure HTML/CSS/JS
- **CDN Compatible**: No server-side processing required
- **SEO Friendly**: Semantic HTML with proper meta tags

This structure provides a solid foundation for content management while maintaining simplicity and extensibility for future enhancements.