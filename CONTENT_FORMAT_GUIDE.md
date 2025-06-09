# 📝 Influencer News - Content Format Guide

Complete guide for creating content files that integrate seamlessly with the Influencer News system.

## 🚀 Quick Start

1. **Install & Setup**: Run `python3 integration_manager.py`
2. **Create Content**: Add `.txt` files to `content/` directories
3. **Integrate**: Use the GUI or run selective integration
4. **Sync**: Run `python3 sync_site.py` to ensure everything is current

## 📁 Content Types Overview

The system supports four content types, each with its own directory structure:

```
content/
├── articles/          # News articles and stories
├── authors/           # Author profiles and bios  
├── categories/        # Content categorization
└── trending/          # Trending topics and analysis
```

---

## 📄 Articles

**Location**: `content/articles/filename.txt`
**Output**: `integrated/articles/article_X.html`

### Required Format

```
Title: Your Article Title Here
Author: Author Full Name
Category: category-slug
Image: https://images.unsplash.com/photo-123456?w=600&h=400&fit=crop
Tags: keyword1, keyword2, keyword3
Excerpt: Brief description that appears on homepage and search results. Keep under 200 characters for best display.

---

Your opening paragraph goes here. This should hook the reader and introduce the topic compellingly.

## First Section Heading

Write your content here. You can have multiple paragraphs in each section.

This is another paragraph in the same section.

### Subsection (Optional)

Use three hashtags for subsections under main sections.

## Special Formatting Options

### Information Boxes
[INFO] Use this format for important information that needs to be highlighted with a blue background.

### Bullet Lists
Create lists like this:

- First point
- Second point  
- Third point with more details

### Quotes
> This is how you create a blockquote. It will be beautifully styled. - Quote Author

## Conclusion

End with a strong conclusion that provides value to readers.
```

### Required Fields
- **Title**: The main headline (becomes page title and H1)
- **Author**: Must match an existing author name exactly
- **Category**: Must match an existing category slug
- **Image**: High-quality image URL (recommended: Unsplash with crop parameters)
- **Tags**: Comma-separated keywords for search and filtering
- **Excerpt**: Brief summary for homepage and search results

### Content Features
- **Markdown Support**: Headers (##, ###), lists, quotes, bold, italic
- **Information Boxes**: `[INFO] Your message here`
- **Automatic Metrics**: View counts, read time, engagement stats
- **Author Linking**: Automatic links to author profiles
- **Category Tagging**: Automatic categorization and filtering

---

## ✍️ Authors

**Location**: `content/authors/firstname-lastname.txt`
**Output**: `integrated/authors/author_firstname-lastname.html`

### Required Format

```
Name: Full Name Here
Title: Senior Business Reporter
Bio: Short bio that appears on listing pages and article bylines
Image: https://images.unsplash.com/photo-123456?w=400&h=400&fit=crop&crop=face
Location: Los Angeles, CA
Expertise: Business, Creator Economy, Market Analysis
Email: author@email.com
Twitter: https://twitter.com/handle
LinkedIn: https://linkedin.com/in/profile
Articles_Written: 150

---

Extended biography content goes here. This appears on the author's individual profile page.

You can write multiple paragraphs about their background, experience, and expertise.

## Career Highlights

- Notable achievement 1
- Notable achievement 2
- Notable achievement 3

## Coverage Areas

This author specializes in covering topics related to their expertise areas. They bring years of experience and industry connections to provide readers with insider perspectives and breaking news.

## Contact Information

For story tips, interview requests, or collaboration opportunities, readers can reach out through the provided contact methods.
```

### Required Fields
- **Name**: Full name used in article bylines
- **Title**: Professional title/role
- **Bio**: Short description for listing pages
- **Image**: Professional headshot URL
- **Location**: City, State/Country
- **Expertise**: Comma-separated specialization areas
- **Email**: Contact email
- **Twitter**: Full Twitter profile URL
- **LinkedIn**: Full LinkedIn profile URL  
- **Articles_Written**: Number for credibility metrics

### Features
- **Author Profile Pages**: Individual pages with full bio and stats
- **Article Linking**: Automatically shows all articles by this author
- **Social Integration**: Links to social profiles
- **Expertise Tags**: Visual tags showing specialization areas

---

## 📁 Categories

**Location**: `content/categories/category-slug.txt`
**Output**: `integrated/categories/category_slug.html` + listing updates

### Required Format

```
Name: Category Display Name
Slug: category-slug
Icon: 🎬
Color: orange
Description: Brief category description that appears in listings
Featured: true
Sort_Order: 1
Keywords: keyword1, keyword2, keyword3

---

Detailed category description goes here. This content appears on the individual category page.

You can explain what type of content falls under this category and why it's important to your audience.

## Coverage Areas

This category includes:
- Specific topic area 1
- Specific topic area 2  
- Specific topic area 3

## Why This Matters

Explain the relevance and importance of this category to the influencer and creator economy.

## Key Topics

- Main subtopic 1
- Main subtopic 2
- Main subtopic 3
```

### Required Fields
- **Name**: Display name shown on website
- **Slug**: URL-friendly identifier (lowercase, hyphens only)
- **Icon**: Single emoji representing the category
- **Color**: Color theme (green, blue, orange, pink, purple, red, yellow, teal)
- **Description**: Brief summary for listings
- **Featured**: true/false - whether to highlight prominently
- **Sort_Order**: Number for ordering (lower = first)
- **Keywords**: Related terms for search and filtering

### Available Colors
- `green` (#10b981) - Business, economy, money
- `blue` (#3b82f6) - Technology, innovation  
- `orange` (#f59e0b) - Entertainment, media
- `pink` (#ec4899) - Fashion, beauty, lifestyle
- `purple` (#8b5cf6) - Social impact, charity
- `red` (#ef4444) - Breaking news, alerts
- `yellow` (#eab308) - Creator tools, tips
- `teal` (#14b8a6) - Health, wellness

### Features
- **Category Pages**: Individual pages with descriptions and article listings
- **Article Filtering**: Automatic article grouping by category
- **Color Coding**: Consistent visual theming throughout site
- **Search Integration**: Category-based filtering on search page

---

## 🔥 Trending Topics

**Location**: `content/trending/topic-slug.txt`
**Output**: `integrated/trending/trend_topic-slug.html` + listing updates

### Required Format

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
Instagram_Mentions: 25000
Twitter_Mentions: 67000

---

Analysis of why this topic is trending and its significance to the creator economy.

## Current Status

Detailed analysis of where this trend stands right now, including key metrics and developments.

## Key Players

- Notable creator/influencer 1
- Notable creator/influencer 2
- Major brand involvement

## Platform Breakdown

### YouTube
Specific details about how this trend is performing on YouTube.

### TikTok  
How the trend manifests on TikTok and key viral moments.

### Instagram
Instagram-specific aspects and engagement patterns.

## Future Outlook

Predictions about where this trend is heading and its potential longevity.
```

### Required Fields
- **Topic**: Display name of the trending topic
- **Hashtag**: Primary hashtag (with #)
- **Category**: Must match existing category slug
- **Trend_Score**: Numerical trending strength (1-10000)
- **Status**: active, declining, emerging, stable
- **Icon**: Emoji representing the trend
- **Growth_Rate**: Percentage growth over time period
- **Youtube_Mentions**: Number of mentions on YouTube
- **TikTok_Mentions**: Number of mentions on TikTok
- **Instagram_Mentions**: Number of mentions on Instagram
- **Twitter_Mentions**: Number of mentions on Twitter

### Status Options
- `active` - Currently trending strongly
- `emerging` - Just starting to gain traction
- `declining` - Past peak but still relevant
- `stable` - Consistent long-term trend

### Features
- **Trend Analysis Pages**: Individual pages with detailed breakdowns
- **Platform Metrics**: Visual representation of cross-platform performance
- **Category Integration**: Linked to relevant content categories
- **Real-time Scoring**: Trend strength visualization

---

## 🎯 Integration Workflow

### 1. File Creation
- Create `.txt` files in appropriate `content/` subdirectories
- Follow exact format requirements
- Use consistent naming and referencing

### 2. Content Integration
**Option A - GUI Integration:**
```bash
python3 integration_manager.py
```
- Use "Selective Integration" tab to choose specific files
- Or use individual "Integrate" buttons per content type

**Option B - Command Line:**
```bash
# Sync all content with current database state
python3 sync_site.py
```

### 3. Verification
- Check individual content pages in `integrated/` folders
- Verify navigation links work correctly
- Confirm cross-references (author names, categories) are functioning

---

## 🔗 Cross-Referencing System

### Author Linking
- Article `Author` field must **exactly match** author `Name` field
- Creates automatic bidirectional linking between articles and author profiles

### Category Linking  
- Article and Trending `Category` field must match category `Slug`
- Enables automatic filtering and categorization

### Naming Conventions
- **Files**: Use lowercase, hyphens for spaces (`my-article.txt`)
- **Category Slugs**: Lowercase, hyphens only (`creator-economy`)
- **Author Names**: Exact case matching required (`Sarah Chen`)

---

## 📊 Generated Features

### Automatic Metrics
- **Articles**: View counts, read time, engagement stats, social shares
- **Authors**: Article counts, expertise display, social links
- **Categories**: Article counts, color theming, search filtering
- **Trending**: Platform-specific metrics, growth visualization

### Navigation
- **Breadcrumbs**: Automatic navigation paths
- **Related Content**: Cross-links between related articles, authors, categories
- **Search Integration**: All content automatically indexed

### Visual Elements
- **Responsive Design**: Mobile-optimized layouts
- **Color Theming**: Consistent category-based color schemes
- **Image Optimization**: Automatic sizing and cropping
- **Interactive Elements**: Hover effects, smooth transitions

---

## 🛠️ Advanced Tips

### Content Quality
- **Headlines**: Use compelling, specific titles
- **Images**: High-resolution photos with proper aspect ratios
- **Structure**: Break content into scannable sections
- **SEO**: Include relevant keywords naturally

### Performance
- **File Sizes**: Keep text files under 50KB for optimal processing
- **Image URLs**: Use CDN-hosted images (Unsplash recommended)
- **Batch Processing**: Use selective integration for large content sets

### Maintenance
- **Regular Syncing**: Run `python3 sync_site.py` after bulk changes
- **Content Auditing**: Use integration manager's content browser
- **Cleanup**: Remove orphaned files periodically

---

## 🚨 Troubleshooting

### Common Errors

**"Missing required field"**
```
Solution: Check field names match exactly (case-sensitive)
Verify all required fields have values
```

**"Invalid format"**
```
Solution: Ensure `---` separator line exists
Check for special characters in field values
```

**"Author not found"**
```
Solution: Author name in article must exactly match author file name
Create author profile first, then reference in articles
```

**"Category not found"**
```
Solution: Category slug must exist as a category file
Check spelling and hyphens in category references
```

### File Validation
Before integrating, verify:
- [ ] All required fields present
- [ ] Separator line (`---`) included
- [ ] Referenced authors/categories exist
- [ ] Image URLs are accessible
- [ ] File saved with `.txt` extension

---

## 📈 Best Practices

### Content Strategy
1. **Authors First**: Create author profiles before their articles
2. **Categories**: Establish category structure early
3. **Consistency**: Use standardized naming and formatting
4. **Quality**: Focus on well-written, valuable content

### Technical Workflow
1. **Batch Creation**: Prepare multiple files before integration
2. **Testing**: Use sample content to verify formatting
3. **Backup**: Keep source files in version control
4. **Monitoring**: Check generated output regularly

### SEO Optimization
- Use descriptive, keyword-rich titles
- Write compelling excerpts under 200 characters
- Include relevant tags for discoverability
- Optimize images with descriptive alt text

---

## 🎉 Ready to Create!

You're now equipped to create professional content for the Influencer News system. Start with a few sample files to get comfortable with the format, then scale up your content creation process.

For additional help:
- Use the integration manager's help system
- Check sample files created by the setup process
- Reference existing content in the `integrated/` directories

**Happy content creating!** 📝✨