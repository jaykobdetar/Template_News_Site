# Influencer News Integration Manager

A comprehensive desktop application for managing content integration and removal for the Influencer News static website.

## Features

- **GUI Dashboard**: Visual interface showing status of all content types
- **Multiple Integrators**: Manage articles, authors, categories, and trending topics
- **Content Management**: Full removal and cleanup capabilities
- **Progress Tracking**: Real-time progress bars and logging
- **Automatic HTML Generation**: Creates individual pages and updates listing pages
- **Cross-linking**: Automatically links related content across different types
- **Organized Structure**: Clean folder organization with subfolders for each content type

## Installation

1. Ensure Python 3.7+ is installed
2. No additional dependencies required (uses tkinter, included with Python)

## Usage

### Starting the Application

**Basic Integration (recommended for beginners):**
```bash
python integration_manager.py
```

**Enhanced Management (recommended for advanced users):**
```bash
python enhanced_integration_manager.py
```

### Dashboard Overview

The dashboard shows 4 content cards:

1. **Articles** (📄) - News articles and stories
2. **Authors** (✍️) - Author profiles and bios
3. **Categories** (📁) - Content categorization
4. **Trending** (🔥) - Trending topics and analysis

Each card displays:
- Current status (✅ Ready, ❌ Not setup, ⏳ Processing)
- File count
- Last integration time
- Progress bar
- Action button (Setup/Integrate)

### First Time Setup

1. Click "Setup" on any content type to create its directory and sample file
2. Edit the sample file to understand the format
3. Add your own .txt files following the same format
4. Click "Integrate" to process the files

### File Formats

#### Articles (content/articles/article-name.txt)
```
Title: Article Title Here
Author: Author Name
Category: category-slug
Image: https://image-url.com/image.jpg
Tags: tag1, tag2, tag3
Excerpt: Brief description under 200 characters

---

Article content in markdown format...
```

#### Authors (content/authors/firstname-lastname.txt)
```
Name: Full Name
Title: Job Title
Bio: Short bio for listing pages
Image: https://image-url.com/photo.jpg
Location: City, State
Expertise: Area1, Area2, Area3
Email: email@example.com
Twitter: @handle
LinkedIn: linkedin.com/in/profile
Articles_Written: 100

---

Extended biography content...
```

#### Categories (content/categories/category-slug.txt)
```
Name: Category Name
Slug: category-slug
Icon: 🎬
Color: orange
Description: Brief category description
Featured: true
Sort_Order: 1
Keywords: keyword1, keyword2, keyword3

---

Detailed category description...
```

#### Trending (content/trending/topic-slug.txt)
```
Topic: Trending Topic Name
Hashtag: #TrendingTopic
Category: category-slug
Trend_Score: 8500
Status: active
Icon: 🔥
Growth_Rate: 125.5
Youtube_Mentions: 45000
TikTok_Mentions: 38000

---

Analysis of why this is trending...
```

### Integration Process

1. **Individual Integration**: Click "Integrate" on a specific content type
2. **Batch Integration**: Click "Run All Integrations" to process everything
3. **View Website**: Click "Open Website" to see your changes

### Output Files

The integrators create:
- **Individual HTML pages in organized folders**:
  - `integrated/articles/article_X.html` - Individual article pages
  - `integrated/authors/author_name.html` - Author profile pages
  - `integrated/categories/category_slug.html` - Category pages
  - `integrated/trending/trend_topic.html` - Trending topic pages
- **Listing pages**:
  - `integrated/categories.html` - Categories overview
  - `integrated/trending.html` - Trending topics overview
  - Updated `index.html` and `authors.html` with new content
- **JSON databases** in `data/` folder for each content type

## Enhanced Integration Manager

The enhanced manager (`enhanced_integration_manager.py`) provides additional content management features:

### Content Management Tab
- **Content Summary**: View all integrated content with IDs, names, and filenames
- **Remove by ID**: Remove specific content items by their database ID
- **Remove by Filename**: Remove content based on original source filename
- **Clean Orphaned Files**: Remove generated files that don't have database entries
- **Remove All Content**: Clear all content of a specific type or everything

### Safety Features
- Confirmation dialogs for all destructive operations
- Database integrity checks prevent corruption
- Orphaned file detection maintains clean structure

## File Structure

```
InfNews/
├── content/                    # Source content files
│   ├── articles/              # Article .txt files
│   ├── authors/               # Author .txt files
│   ├── categories/            # Category .txt files
│   └── trending/              # Trending .txt files
├── integrated/                # Generated content (organized)
│   ├── articles/              # Generated article pages
│   ├── authors/               # Generated author pages
│   ├── categories/            # Generated category pages
│   │   └── categories.html    # Categories listing page
│   ├── trending/              # Generated trending pages
│   │   └── trending.html      # Trending listing page
├── data/                      # JSON databases
│   ├── articles_db.json
│   ├── authors_db.json
│   ├── categories_db.json
│   └── trending_db.json
└── src/integrators/           # Integration logic
```

### Tips

- Files are only processed once (tracked in JSON databases)
- Use the Enhanced Manager for full content lifecycle management
- Check the log panel for detailed processing information
- Use consistent naming for cross-referencing (author names, categories)
- Regular cleanup with "Clean Orphaned Files" maintains data integrity

## Troubleshooting

**"No new files to process"**
- Ensure your .txt files are in the correct directory
- Check that files haven't been processed already (check JSON database)

**"Missing required field"**
- Review the file format requirements
- Ensure all required fields have values

**GUI doesn't start**
- Ensure tkinter is installed: `python -m tkinter`
- Try running with: `python3 integration_manager.py`

## Advanced Features

### Cross-Referencing
- Articles reference authors by name (must match author file)
- Articles and trending topics reference categories by slug
- Trending topics can reference article IDs

### Customization
- Modify color schemes in integrator files
- Adjust HTML templates by editing the generate methods
- Add new fields by updating parse methods

### Extending
To add a new content type:
1. Create a new integrator class extending BaseIntegrator
2. Add it to the IntegrationManager
3. Update the dashboard cards