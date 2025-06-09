#!/usr/bin/env python3
"""
Category Integrator
===================
Manages content categories and generates category pages
"""

from pathlib import Path
from typing import Dict, List, Any
from .base_integrator import BaseIntegrator


class CategoryIntegrator(BaseIntegrator):
    """Integrator for managing content categories"""
    
    def __init__(self):
        super().__init__('categories', 'categories', 'categories_db.json')
        
        # Default category icons
        self.default_icons = {
            'business': '💼',
            'entertainment': '🎬',
            'tech': '💻',
            'technology': '🚀',
            'fashion': '👗',
            'beauty': '💄',
            'charity': '❤️',
            'lifestyle': '🌟',
            'sports': '⚽',
            'gaming': '🎮',
            'food': '🍽️',
            'travel': '✈️',
            'health': '🏃',
            'education': '📚',
            'music': '🎵',
            'creator-economy': '💰'
        }
    
    def parse_content_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a category file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Split into sections
        sections = content.split('\n---\n')
        if len(sections) < 2:
            raise ValueError(f"Invalid format in {file_path}. Missing '---' separator.")
        
        # Parse metadata
        metadata = self.parse_metadata_section(sections[0])
        description_content = '\n---\n'.join(sections[1:]).strip()
        
        # Validate required fields
        required_fields = ['name', 'slug']
        self.validate_required_fields(metadata, required_fields, file_path)
        
        # Get icon or use default
        icon = metadata.get('icon', self.default_icons.get(metadata['slug'], '📁'))
        
        # Get color or use default
        color = metadata.get('color', self.get_category_color(metadata['slug']))
        
        return {
            'name': metadata['name'],
            'slug': metadata['slug'],
            'icon': icon,
            'color': color,
            'description': metadata.get('description', f"Latest {metadata['name']} news and updates"),
            'extended_description': description_content,
            'featured': metadata.get('featured', 'false').lower() == 'true',
            'sort_order': int(metadata.get('sort_order', 999)),
            'article_count': 0,  # Will be updated when articles are processed
            'parent_category': metadata.get('parent_category', None),
            'keywords': [k.strip() for k in metadata.get('keywords', '').split(',') if k.strip()]
        }
    
    def create_content_page(self, category: Dict[str, Any]):
        """Create individual category page"""
        category_filename = self.integrated_dir / f"category_{category['slug']}.html"
        
        # Create HTML content for category page
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category['name']} - Category | Influencer News</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        .hero-title {{ font-family: 'Playfair Display', serif; }}
        .category-{category['slug']} {{ color: {self._get_color_code(category['color'])}; }}
    </style>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="bg-indigo-900 text-white sticky top-0 z-50 shadow-2xl">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center">
                <div class="w-16 h-16 bg-gradient-to-br from-indigo-400 to-purple-600 rounded-full flex items-center justify-center mr-4">
                    <span class="text-2xl font-bold text-white">IN</span>
                </div>
                <div>
                    <h1 class="text-3xl font-bold hero-title">Influencer News</h1>
                    <p class="text-xs text-indigo-200">Breaking stories • Real insights</p>
                </div>
            </div>
            <nav class="hidden md:block">
                <ul class="flex space-x-8">
                    <li><a href="../../index.html" class="hover:text-indigo-200 transition font-medium">Home</a></li>
                    <li><a href="../../search.html" class="hover:text-indigo-200 transition font-medium">Search</a></li>
                    <li><a href="../../authors.html" class="hover:text-indigo-200 transition font-medium">Authors</a></li>
                    <li><a href="../categories.html" class="hover:text-indigo-200 transition font-medium text-indigo-200">Categories</a></li>
                    <li><a href="../trending.html" class="hover:text-indigo-200 transition font-medium">Trending</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Category Hero -->
    <section class="bg-gradient-to-br from-{category['color']}-700 via-{category['color']}-600 to-{category['color']}-500 text-white py-20">
        <div class="container mx-auto px-4 text-center">
            <div class="text-8xl mb-6">{category['icon']}</div>
            <h1 class="text-5xl font-bold mb-4 hero-title">{self.escape_html(category['name'])}</h1>
            <p class="text-xl text-white/90 max-w-3xl mx-auto mb-8">
                {self.escape_html(category['description'])}
            </p>
            <div class="flex gap-4 justify-center">
                <span class="bg-white/20 backdrop-blur-sm px-6 py-3 rounded-full">
                    📊 {category['article_count']} Articles
                </span>
                <span class="bg-white/20 backdrop-blur-sm px-6 py-3 rounded-full">
                    🔥 Trending Category
                </span>
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-12">
        <!-- About This Category -->
        <div class="bg-white rounded-2xl shadow-lg p-8 mb-12">
            <h2 class="text-3xl font-bold mb-6 hero-title">About {self.escape_html(category['name'])}</h2>
            <div class="prose prose-lg max-w-none text-gray-700">
                {self._format_description(category['extended_description'])}
            </div>
            
            {self._generate_keywords_section(category['keywords'])}
        </div>

        <!-- Articles in Category -->
        <section>
            <h2 class="text-3xl font-bold mb-8 hero-title">Latest in {self.escape_html(category['name'])}</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="categoryArticles">
                <!-- Articles will be dynamically loaded here -->
                <div class="bg-gray-100 rounded-xl p-8 text-center text-gray-500">
                    <p>Articles in this category will appear here after integration.</p>
                </div>
            </div>
        </section>

        <!-- Related Categories -->
        <section class="mt-16">
            <h2 class="text-3xl font-bold mb-8 hero-title">Explore More Categories</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4" id="relatedCategories">
                <!-- Related categories will be loaded here -->
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-300 py-12 mt-20">
        <div class="container mx-auto px-4 text-center">
            <p>&copy; 2024 Influencer News. All rights reserved.</p>
        </div>
    </footer>

    <script>
        // Load articles for this category
        document.addEventListener('DOMContentLoaded', function() {{
            // This would be populated by the article integrator
            console.log('Loading articles for category: {category['slug']}');
        }});
    </script>
</body>
</html>'''
        
        with open(category_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.update_progress(f"Created category page: {category_filename}")
    
    def _get_color_code(self, color: str) -> str:
        """Get hex color code for category color"""
        color_map = {
            'green': '#10b981',
            'blue': '#3b82f6',
            'purple': '#8b5cf6',
            'pink': '#ec4899',
            'orange': '#f59e0b',
            'red': '#ef4444',
            'yellow': '#eab308',
            'indigo': '#6366f1',
            'teal': '#14b8a6',
            'gray': '#6b7280'
        }
        return color_map.get(color, '#6b7280')
    
    def _format_description(self, description: str) -> str:
        """Format extended description"""
        paragraphs = description.split('\n\n')
        formatted = ""
        for para in paragraphs:
            if para.strip():
                formatted += f'<p class="mb-4">{self.escape_html(para.strip())}</p>\n'
        return formatted
    
    def _generate_keywords_section(self, keywords: List[str]) -> str:
        """Generate keywords/topics section"""
        if not keywords:
            return ""
        
        section = '''
            <div class="mt-8 pt-8 border-t border-gray-200">
                <h3 class="text-xl font-bold mb-4">Related Topics</h3>
                <div class="flex flex-wrap gap-2">
        '''
        
        for keyword in keywords:
            section += f'<span class="bg-gray-100 text-gray-700 px-4 py-2 rounded-full text-sm hover:bg-gray-200 transition cursor-pointer">{self.escape_html(keyword)}</span>\n'
        
        section += '''
                </div>
            </div>
        '''
        return section
    
    def update_listing_page(self, categories: List[Dict[str, Any]]):
        """Update main navigation with categories"""
        # Update search page with category filters
        self.update_search_categories(categories)
        
        # Create a categories overview page
        self.create_categories_overview(categories)
    
    def update_search_categories(self, categories: List[Dict[str, Any]]):
        """Update search page with category filters"""
        # This would update the search.html with category filter options
        self.update_progress("Updated search page with category filters")
    
    def create_categories_overview(self, categories: List[Dict[str, Any]]):
        """Create categories overview page"""
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Browse Categories - Influencer News</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .hero-title { font-family: 'Playfair Display', serif; }
        .category-card {
            transition: all 0.3s ease;
        }
        .category-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="bg-indigo-900 text-white sticky top-0 z-50 shadow-2xl">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center">
                <div class="w-16 h-16 bg-gradient-to-br from-indigo-400 to-purple-600 rounded-full flex items-center justify-center mr-4">
                    <span class="text-2xl font-bold text-white">IN</span>
                </div>
                <div>
                    <h1 class="text-3xl font-bold hero-title">Influencer News</h1>
                    <p class="text-xs text-indigo-200">Breaking stories • Real insights</p>
                </div>
            </div>
            <nav class="hidden md:block">
                <ul class="flex space-x-8">
                    <li><a href="../index.html" class="hover:text-indigo-200 transition font-medium">Home</a></li>
                    <li><a href="../search.html" class="hover:text-indigo-200 transition font-medium">Search</a></li>
                    <li><a href="../authors.html" class="hover:text-indigo-200 transition font-medium">Authors</a></li>
                    <li><a href="categories.html" class="hover:text-indigo-200 transition font-medium text-indigo-200">Categories</a></li>
                    <li><a href="trending.html" class="hover:text-indigo-200 transition font-medium">Trending</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-indigo-900 via-purple-800 to-indigo-700 text-white py-20">
        <div class="container mx-auto px-4 text-center">
            <h1 class="text-5xl font-bold mb-4 hero-title">Browse Categories</h1>
            <p class="text-xl text-indigo-200 max-w-3xl mx-auto">
                Explore our diverse range of content categories covering everything in the influencer world
            </p>
        </div>
    </section>

    <!-- Categories Grid -->
    <main class="container mx-auto px-4 py-12">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
'''
        
        # Add category cards
        for category in sorted(categories, key=lambda x: x['sort_order']):
            color_code = self._get_color_code(category['color'])
            
            html_content += f'''
            <a href="categories/category_{category['slug']}.html" class="category-card block">
                <div class="bg-white rounded-2xl shadow-lg overflow-hidden h-full">
                    <div class="p-8 text-center" style="background: linear-gradient(135deg, {color_code}20 0%, {color_code}10 100%);">
                        <div class="text-6xl mb-4">{category['icon']}</div>
                        <h3 class="text-xl font-bold mb-2">{self.escape_html(category['name'])}</h3>
                        <p class="text-gray-600 text-sm mb-4">{self.escape_html(category['description'])}</p>
                        <span class="inline-block bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-xs">
                            {category['article_count']} Articles
                        </span>
                    </div>
                </div>
            </a>
            '''
        
        html_content += '''
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-300 py-12 mt-20">
        <div class="container mx-auto px-4 text-center">
            <p>&copy; 2024 Influencer News. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>'''
        
        categories_listing_file = Path("integrated") / "categories.html"
        with open(categories_listing_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.update_progress("Created categories overview page")
    
    def create_sample_file(self):
        """Create a sample category file"""
        sample_content = """Name: Creator Economy
Slug: creator-economy
Icon: 💰
Color: green
Description: Business of content creation and monetization strategies
Featured: true
Sort_Order: 1
Keywords: monetization, sponsorships, brand deals, creator funds, revenue streams

---

The Creator Economy represents the class of businesses built by over 50 million independent content creators, curators, and community builders including social media influencers, bloggers, and videographers, plus the software and finance tools designed to help them with growth and monetization.

This category covers everything from platform monetization features and creator funds to brand partnerships and alternative revenue streams. We track the latest developments in how creators are building sustainable businesses and the tools that support them.

Key areas of coverage include:
- Platform monetization updates (YouTube, TikTok, Instagram, etc.)
- Creator funds and grant programs
- Brand partnership trends and rates
- Alternative monetization strategies
- Creator-focused startups and tools
- Economic analysis and market trends

Whether you're a creator looking to grow your business or a brand wanting to understand the creator landscape, this category provides essential insights into the rapidly evolving creator economy."""
        
        sample_file = self.content_dir / "creator-economy.txt"
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        self.update_progress(f"Created sample category file: {sample_file}")