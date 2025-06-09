# Influencer News - Content Management System

A comprehensive desktop application for managing content integration for a static news website focused on the influencer and creator economy.

## 🚀 Features

- **Desktop GUI Application**: User-friendly Tkinter interface for content management
- **Multiple Content Types**: Articles, Authors, Categories, and Trending Topics
- **Automated HTML Generation**: Creates individual pages and updates listing pages
- **Cross-Linking**: Automatically links related content across different types
- **Progress Tracking**: Real-time progress bars and detailed logging
- **File-Based Content**: Simple .txt file format for all content types

## 📁 Project Structure

```
InfNews/
├── integration_manager.py          # Main GUI application
├── PROJECT_README.md               # This file
├── INTEGRATION_GUIDE.md           # Detailed usage guide
├── 
├── src/
│   └── integrators/               # Core integration modules
│       ├── __init__.py
│       ├── base_integrator.py     # Shared functionality
│       ├── article_integrator.py  # Article processing
│       ├── author_integrator.py   # Author profile processing
│       ├── category_integrator.py # Category management
│       └── trending_integrator.py # Trending topics
│
├── content/                       # Source content files
│   ├── articles/                 # Article .txt files
│   ├── authors/                  # Author profile .txt files
│   ├── categories/               # Category definition .txt files
│   └── trending/                 # Trending topic .txt files
│
├── generated/                     # Generated HTML pages
│   ├── article_*.html            # Individual article pages
│   ├── author_*.html             # Author profile pages
│   ├── category_*.html           # Category pages
│   └── trend_*.html              # Trending topic pages
│
├── data/                         # JSON databases
│   ├── articles_db.json         # Article metadata
│   ├── authors_db.json          # Author metadata
│   ├── categories_db.json       # Category metadata
│   └── trending_db.json         # Trending metadata
│
├── assets/
│   └── images/
│       └── screenshots/          # Application screenshots
│
├── docs/                         # Documentation
└── *.html                       # Main website pages (index, search, etc.)
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- No additional dependencies required (uses built-in tkinter)

### Quick Start

1. **Run the integration manager**
```bash
python integration_manager.py
```

2. **Setup content types**
   - Click "Setup" for each content type to create directories and sample files
   - Edit sample files to understand the format
   - Add your own content files following the same format

3. **Integrate content**
   - Click "Integrate" for individual content types
   - Or use "Run All Integrations" to process everything at once

4. **View your website**
   - Click "Open Website" to view the generated site in your browser

## 📝 Content File Formats

### Articles (`content/articles/article-name.txt`)
```
Title: Your Article Title
Author: Author Name
Category: category-slug
Image: https://example.com/image.jpg
Tags: tag1, tag2, tag3
Excerpt: Brief description under 200 characters

---

Your article content in markdown format...

## Section Heading

Content with proper formatting support.

> Blockquotes with attribution - Author Name

[INFO] Information boxes for important details

- Bullet point lists
- Are also supported
```

### Authors (`content/authors/firstname-lastname.txt`)
```
Name: Full Name
Title: Job Title
Bio: Short bio for listing pages
Image: https://example.com/photo.jpg
Location: City, State
Expertise: Area1, Area2, Area3
Email: email@example.com
Twitter: @handle
LinkedIn: linkedin.com/in/profile
Articles_Written: 100

---

Extended biography content with full details...
```

### Categories (`content/categories/category-slug.txt`)
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

Detailed category description and coverage areas...
```

### Trending (`content/trending/topic-slug.txt`)
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

Analysis of why this topic is trending...
```

## 🎯 Key Features

### Integration Manager GUI
- **Dashboard View**: Status cards for each content type
- **Progress Tracking**: Real-time progress bars during integration
- **Logging**: Detailed integration log with timestamps
- **Batch Processing**: Run all integrations with one click

### Content Processing
- **Automatic HTML Generation**: Creates responsive, modern HTML pages
- **Cross-Referencing**: Links articles to authors, categories, and trends
- **Search Integration**: Updates search functionality with new content
- **Database Management**: Maintains JSON databases for all content

### Generated Output
- **Individual Pages**: Unique pages for each piece of content
- **Listing Pages**: Updated index pages for browsing content
- **Category Pages**: Dedicated pages for each content category
- **Trending Pages**: Dynamic trending topic analysis pages

## 🔧 Advanced Usage

### Customization
- **Colors & Styling**: Modify category colors in base_integrator.py
- **HTML Templates**: Customize generated HTML in individual integrator files
- **File Processing**: Add new fields by updating parse methods

### Integration
- **API Integration**: Extend integrators to pull from external APIs
- **Automation**: Set up scheduled runs using cron jobs or Task Scheduler
- **Deployment**: Integrate with static site generators or CDNs

### Monitoring
- **Database Inspection**: View JSON databases to understand content structure
- **Log Analysis**: Review integration logs for troubleshooting
- **File Tracking**: Monitor which files have been processed

## 🐛 Troubleshooting

### Common Issues

**"No new files to process"**
- Ensure .txt files are in the correct content directory
- Check that files haven't been processed already (check JSON database)
- Verify file naming follows the expected pattern

**"Missing required field"**
- Review the file format requirements in sample files
- Ensure all required fields have values
- Check for proper field naming (case-sensitive)

**GUI doesn't start**
- Verify Python installation includes tkinter: `python -m tkinter`
- Try running with Python 3 explicitly: `python3 integration_manager.py`
- Check for permission issues in the project directory

**Generated pages missing**
- Ensure the `generated/` directory exists and is writable
- Check the integration log for error messages
- Verify template files (like article.html) exist in the root directory

### Getting Help
- Check the detailed INTEGRATION_GUIDE.md
- Review sample files for proper formatting
- Use the built-in Help button in the GUI

## 🚀 Next Steps

### Enhancements
1. **Real-time Preview**: Add preview functionality before integration
2. **Content Validation**: Implement more robust validation rules
3. **Template System**: Add customizable HTML templates
4. **Analytics Integration**: Add view tracking and analytics
5. **Multi-language Support**: Internationalization features

### Deployment
1. **Static Site Integration**: Connect with Jekyll, Hugo, or Gatsby
2. **CDN Deployment**: Automated deployment to Netlify, Vercel, etc.
3. **CI/CD Pipeline**: Automated content processing on file changes
4. **Content API**: REST API for programmatic content management

## 📄 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

Built with ❤️ for the creator economy community.