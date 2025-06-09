# 🚀 Influencer News - Quick Start Guide

Get your content management system running in 5 minutes!

## 📋 Setup Checklist

1. **Start the Integration Manager**
   ```bash
   python3 integration_manager.py
   ```

2. **Create Your First Content**
   - Use the "Setup" buttons to create sample files
   - Edit the samples or create new `.txt` files
   - Follow the format examples below

3. **Integrate Content**
   - Use "Selective Integration" tab to choose files
   - Or click individual "Integrate" buttons
   - Check the integration log for status

4. **Sync & View**
   ```bash
   python3 sync_site.py    # Sync website with database
   ```
   - Open `index.html` in your browser to see results

---

## 📝 File Format Quick Reference

### Articles (`content/articles/my-article.txt`)
```
Title: Your Article Title
Author: Full Name (must match author file)
Category: category-slug (must exist)
Image: https://image-url.com/image.jpg
Tags: tag1, tag2, tag3
Excerpt: Brief description under 200 chars

---

Your article content here in markdown format.

## Section Heading

Content with **bold** and *italic* text.

- Bullet points
- Work great too

> Blockquotes look professional - Author Name

[INFO] Information boxes stand out nicely.
```

### Authors (`content/authors/firstname-lastname.txt`)
```
Name: Full Name Here
Title: Senior Reporter
Bio: Short bio for listings
Image: https://image-url.com/headshot.jpg
Location: City, State
Expertise: Area1, Area2, Area3
Email: email@example.com
Twitter: https://twitter.com/handle
LinkedIn: https://linkedin.com/in/profile
Articles_Written: 100

---

Extended biography content for the profile page.
```

### Categories (`content/categories/category-slug.txt`)
```
Name: Category Display Name
Slug: category-slug
Icon: 🎬
Color: orange
Description: Brief description for listings
Featured: true
Sort_Order: 1
Keywords: keyword1, keyword2, keyword3

---

Detailed category description for the category page.
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
Instagram_Mentions: 25000
Twitter_Mentions: 67000

---

Analysis of why this topic is trending and its impact.
```

---

## 🎯 Quick Tips

### Order of Creation
1. **Categories** - Create these first
2. **Authors** - Before writing articles
3. **Articles** - Reference existing authors/categories
4. **Trending** - Link to existing categories

### File Naming
- Use lowercase with hyphens: `my-new-article.txt`
- Author files: `firstname-lastname.txt`
- Category slugs: `creator-economy`, `tech`, `business`

### Required Field Matching
- Article `Author` = Author `Name` (exact match)
- Article/Trending `Category` = Category `Slug` (exact match)

---

## 🔧 Essential Commands

```bash
# Start the GUI
python3 integration_manager.py

# Sync website with database (run after any manual changes)
python3 sync_site.py

# Check status of all content
python3 sync_site.py status
```

---

## 📁 Folder Structure

```
InfNews/
├── content/                    # Your source files (.txt)
│   ├── articles/              # Article files
│   ├── authors/               # Author profiles  
│   ├── categories/            # Category definitions
│   └── trending/              # Trending topics
├── integrated/                # Generated HTML (don't edit)
│   ├── articles/              # Individual article pages
│   ├── authors/               # Author profile pages
│   ├── categories/            # Category pages
│   └── trending/              # Trending pages
├── data/                      # JSON databases (don't edit)
└── index.html                 # Main website page
```

---

## 🎨 Available Categories & Colors

Create these category slugs for color-coded content:

- `business` (green) - Creator economy, monetization
- `tech` (blue) - Platform updates, AI tools  
- `entertainment` (orange) - Celebrity news, drama
- `fashion` (pink) - Fashion trends, beauty
- `charity` (purple) - Social impact, causes
- `creator-economy` (green) - Business of content

---

## 🚨 Common Issues & Fixes

**Integration fails:**
- Check all required fields are present
- Verify `---` separator line exists
- Ensure referenced authors/categories exist

**Broken links:**
- Run `python3 sync_site.py` to fix
- Check author names match exactly
- Verify category slugs are correct

**GUI won't start:**
- Try `python3 integration_manager.py`
- Ensure Python 3.7+ is installed

---

## ✅ Success Indicators

You'll know it's working when:
- ✅ Integration manager shows content counts
- ✅ Individual pages appear in `integrated/` folders  
- ✅ `index.html` shows your articles
- ✅ Navigation between pages works
- ✅ No error messages in logs

---

## 📚 Need More Help?

- **Full Documentation**: See `CONTENT_FORMAT_GUIDE.md`
- **Integration Guide**: See `INTEGRATION_GUIDE.md` 
- **Help Button**: In the integration manager GUI
- **Sample Files**: Generated automatically with "Setup" buttons

**Ready to create amazing content!** 🎉