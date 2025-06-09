#!/usr/bin/env python3
"""
Author Integrator
=================
Manages author profiles and generates author pages
"""

import random
from pathlib import Path
from typing import Dict, List, Any
from .base_integrator import BaseIntegrator


class AuthorIntegrator(BaseIntegrator):
    """Integrator for managing author profiles"""
    
    def __init__(self):
        super().__init__('authors', 'authors', 'authors_db.json')
        
        # Role mappings
        self.roles = {
            'senior': ['Senior Editor', 'Senior Reporter', 'Senior Correspondent'],
            'correspondent': ['Correspondent', 'Reporter', 'Journalist'],
            'contributor': ['Contributor', 'Guest Writer', 'Freelancer']
        }
    
    def parse_content_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse an author file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Split into sections
        sections = content.split('\n---\n')
        if len(sections) < 2:
            raise ValueError(f"Invalid format in {file_path}. Missing '---' separator.")
        
        # Parse metadata
        metadata = self.parse_metadata_section(sections[0])
        bio_content = '\n---\n'.join(sections[1:]).strip()
        
        # Validate required fields
        required_fields = ['name', 'title', 'bio', 'image']
        self.validate_required_fields(metadata, required_fields, file_path)
        
        # Determine role category
        title_lower = metadata['title'].lower()
        role_category = 'contributor'  # default
        for role, titles in self.roles.items():
            if any(t.lower() in title_lower for t in titles):
                role_category = role
                break
        
        # Parse expertise list
        expertise = [e.strip() for e in metadata.get('expertise', '').split(',') if e.strip()]
        
        return {
            'name': metadata['name'],
            'title': metadata['title'],
            'bio': metadata['bio'],
            'extended_bio': bio_content,
            'image': metadata['image'],
            'location': metadata.get('location', 'Remote'),
            'expertise': expertise,
            'email': metadata.get('email', ''),
            'twitter': metadata.get('twitter', ''),
            'linkedin': metadata.get('linkedin', ''),
            'articles_written': int(metadata.get('articles_written', random.randint(10, 500))),
            'role_category': role_category,
            'rating': round(random.uniform(4.5, 5.0), 1),
            'joined_date': metadata.get('joined_date', '2020-01-01'),
            'verified': metadata.get('verified', 'true').lower() == 'true'
        }
    
    def create_content_page(self, author: Dict[str, Any]):
        """Create individual author page"""
        # Generate author page filename
        author_slug = author['name'].lower().replace(' ', '-')
        author_filename = self.integrated_dir / f"author_{author_slug}.html"
        
        # Create HTML content for author page
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{author['name']} - Author Profile | Influencer News</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        .hero-title {{ font-family: 'Playfair Display', serif; }}
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
                    <li><a href="../../authors.html" class="hover:text-indigo-200 transition font-medium text-indigo-200">Authors</a></li>
                    <li><a href="../categories.html" class="hover:text-indigo-200 transition font-medium">Categories</a></li>
                    <li><a href="../trending.html" class="hover:text-indigo-200 transition font-medium">Trending</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Author Profile Hero -->
    <section class="bg-gradient-to-br from-indigo-900 via-purple-800 to-indigo-700 text-white py-20">
        <div class="container mx-auto px-4">
            <div class="flex flex-col md:flex-row items-center gap-8">
                <img src="{author['image']}" alt="{self.escape_html(author['name'])}" 
                     class="w-48 h-48 rounded-full object-cover border-4 border-white shadow-2xl">
                <div class="text-center md:text-left">
                    <h1 class="text-5xl font-bold mb-2 hero-title">{self.escape_html(author['name'])}</h1>
                    <p class="text-2xl text-indigo-200 mb-4">{self.escape_html(author['title'])}</p>
                    <div class="flex flex-wrap gap-4 justify-center md:justify-start mb-6">
                        <span class="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
                            📍 {self.escape_html(author['location'])}
                        </span>
                        <span class="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
                            ✍️ {author['articles_written']} Articles
                        </span>
                        <span class="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
                            ⭐ {author['rating']} Rating
                        </span>
                    </div>
                    <div class="flex gap-4 justify-center md:justify-start">
                        {self._generate_social_links(author)}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Bio Section -->
            <div class="lg:col-span-2">
                <div class="bg-white rounded-2xl shadow-lg p-8">
                    <h2 class="text-3xl font-bold mb-6 hero-title">About {self.escape_html(author['name'].split()[0])}</h2>
                    <p class="text-gray-700 text-lg mb-6">{self.escape_html(author['bio'])}</p>
                    <div class="prose prose-lg max-w-none text-gray-700">
                        {self._format_extended_bio(author['extended_bio'])}
                    </div>
                </div>
                
                <!-- Recent Articles -->
                <div class="bg-white rounded-2xl shadow-lg p-8 mt-8">
                    <h2 class="text-3xl font-bold mb-6 hero-title">Recent Articles</h2>
                    <p class="text-gray-600">Articles by this author coming soon...</p>
                </div>
            </div>
            
            <!-- Sidebar -->
            <div class="lg:col-span-1">
                <!-- Expertise -->
                <div class="bg-white rounded-2xl shadow-lg p-6 mb-6">
                    <h3 class="text-xl font-bold mb-4">Areas of Expertise</h3>
                    <div class="flex flex-wrap gap-2">
                        {self._generate_expertise_tags(author['expertise'])}
                    </div>
                </div>
                
                <!-- Contact -->
                <div class="bg-white rounded-2xl shadow-lg p-6">
                    <h3 class="text-xl font-bold mb-4">Contact Information</h3>
                    {self._generate_contact_info(author)}
                </div>
            </div>
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
        
        with open(author_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.update_progress(f"Created author page: {author_filename}")
    
    def _format_extended_bio(self, bio: str) -> str:
        """Format extended bio content"""
        paragraphs = bio.split('\n\n')
        formatted = ""
        for para in paragraphs:
            if para.strip():
                formatted += f'<p class="mb-4">{self.escape_html(para.strip())}</p>\n'
        return formatted
    
    def _generate_social_links(self, author: Dict[str, Any]) -> str:
        """Generate social media links"""
        links = ""
        if author.get('twitter'):
            twitter_handle = author['twitter'].replace('@', '')
            links += f'''<a href="https://twitter.com/{twitter_handle}" class="bg-white text-indigo-900 px-4 py-2 rounded-full hover:bg-indigo-100 transition">
                Twitter
            </a>'''
        if author.get('linkedin'):
            linkedin_url = author['linkedin'] if author['linkedin'].startswith('http') else f"https://{author['linkedin']}"
            links += f'''<a href="{linkedin_url}" class="bg-white text-indigo-900 px-4 py-2 rounded-full hover:bg-indigo-100 transition">
                LinkedIn
            </a>'''
        if author.get('email'):
            links += f'''<a href="mailto:{author['email']}" class="bg-white text-indigo-900 px-4 py-2 rounded-full hover:bg-indigo-100 transition">
                Email
            </a>'''
        return links
    
    def _generate_expertise_tags(self, expertise: List[str]) -> str:
        """Generate expertise tags"""
        tags = ""
        colors = ['indigo', 'purple', 'pink', 'blue', 'green']
        for i, area in enumerate(expertise):
            color = colors[i % len(colors)]
            tags += f'<span class="bg-{color}-100 text-{color}-800 px-3 py-1 rounded-full text-sm">{self.escape_html(area)}</span>\n'
        return tags
    
    def _generate_contact_info(self, author: Dict[str, Any]) -> str:
        """Generate contact information section"""
        info = '<div class="space-y-3">'
        if author.get('email'):
            info += f'<p class="flex items-center gap-2">📧 <a href="mailto:{author["email"]}" class="text-indigo-600 hover:underline">{author["email"]}</a></p>'
        if author.get('twitter'):
            info += f'<p class="flex items-center gap-2">🐦 <a href="https://twitter.com/{author["twitter"].replace("@", "")}" class="text-indigo-600 hover:underline">{author["twitter"]}</a></p>'
        if author.get('linkedin'):
            linkedin_display = author['linkedin'].replace('https://', '').replace('linkedin.com/in/', '')
            info += f'<p class="flex items-center gap-2">💼 <a href="{author["linkedin"]}" class="text-indigo-600 hover:underline">{linkedin_display}</a></p>'
        info += '</div>'
        return info
    
    def update_listing_page(self, authors: List[Dict[str, Any]]):
        """Update authors listing page"""
        with open('authors.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate author cards HTML
        authors_html = ""
        
        if authors:
            # If there are authors, display them
            for author in authors:
                author_slug = author['name'].lower().replace(' ', '-')
                
                # Get first expertise area for badge
                expertise_badge = author['expertise'][0] if author['expertise'] else 'General'
                
                authors_html += f'''
                <div class="author-card bg-white rounded-2xl shadow-lg overflow-hidden transform transition duration-300 hover:scale-105 hover:shadow-2xl" data-category="{author['role_category']}">
                    <div class="relative">
                        <img src="{author['image']}" alt="{self.escape_html(author['name'])}" class="w-full h-64 object-cover">
                        <div class="absolute top-4 right-4">
                            <span class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-3 py-1 rounded-full text-xs font-bold uppercase animate-pulse">
                                {self.escape_html(expertise_badge)}
                            </span>
                        </div>
                        <div class="absolute bottom-4 left-4 right-4">
                            <div class="bg-white/90 backdrop-blur-sm rounded-lg p-3 flex justify-between items-center">
                                <span class="text-sm font-medium text-gray-700">📝 {author['articles_written']} Articles</span>
                                <span class="text-sm font-medium text-gray-700">⭐ {author['rating']}</span>
                            </div>
                        </div>
                    </div>
                    <div class="p-6">
                        <h3 class="text-xl font-bold mb-1">{self.escape_html(author['name'])}</h3>
                        <p class="text-gray-600 mb-3">{self.escape_html(author['title'])}</p>
                        
                        <div class="flex gap-2 mb-4">
                            {self._generate_mini_social_links(author)}
                        </div>
                        
                        <p class="text-gray-700 text-sm mb-4 line-clamp-3">{self.escape_html(author['bio'])}</p>
                        
                        <div class="flex flex-wrap gap-2 mb-4">
                            {self._generate_mini_expertise_tags(author['expertise'][:3])}
                        </div>
                        
                        <div class="flex justify-between items-center text-sm">
                            <span class="text-gray-500">📍 {self.escape_html(author['location'])}</span>
                            <a href="integrated/authors/author_{author_slug}.html" class="text-indigo-600 font-medium hover:text-indigo-800 transition">
                                View Profile →
                            </a>
                        </div>
                    </div>
                </div>
            '''
        else:
            # If no authors, show empty state
            authors_html = '''
                <div class="col-span-full text-center py-16">
                    <div class="text-gray-400 text-6xl mb-4">✍️</div>
                    <h3 class="text-xl font-semibold text-gray-600 mb-2">No Authors Yet</h3>
                    <p class="text-gray-500">Our editorial team will be featured here soon!</p>
                </div>
            '''
        
        # Replace authors grid
        start_marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8" id="authorsGrid">'
        end_marker = '</div>\n\n        <!-- Join Our Team Section -->'
        
        start_pos = content.find(start_marker)
        end_pos = content.find(end_marker)
        
        if start_pos != -1 and end_pos != -1:
            new_section = f'{start_marker}\n{authors_html}\n            </div>'
            content = content[:start_pos] + new_section + content[end_pos:]
        
        with open('authors.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        if authors:
            self.update_progress(f"Updated authors listing page with {len(authors)} authors")
        else:
            self.update_progress("Cleared authors listing page - no authors to display")
    
    def _generate_mini_social_links(self, author: Dict[str, Any]) -> str:
        """Generate mini social links for author cards"""
        links = ""
        if author.get('twitter'):
            links += '<a href="#" class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center hover:bg-gray-200 transition">🐦</a>'
        if author.get('linkedin'):
            links += '<a href="#" class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center hover:bg-gray-200 transition">💼</a>'
        if author.get('email'):
            links += '<a href="#" class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center hover:bg-gray-200 transition">📧</a>'
        return links
    
    def _generate_mini_expertise_tags(self, expertise: List[str]) -> str:
        """Generate mini expertise tags for author cards"""
        tags = ""
        for area in expertise:
            tags += f'<span class="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">{self.escape_html(area)}</span>\n'
        return tags
    
    def create_sample_file(self):
        """Create a sample author file"""
        sample_content = """Name: Sarah Chen
Title: Senior Business Reporter
Bio: Creator economy expert with 8 years experience covering the business of content creation and influencer marketing
Image: https://images.unsplash.com/photo-1494790108755-2616c395d75b?w=400&h=400&fit=crop&crop=face
Location: Los Angeles, CA
Expertise: Business, Startups, Tech, Creator Economy
Email: sarah.chen@influencernews.com
Twitter: @sarahchen
LinkedIn: linkedin.com/in/sarahchen
Articles_Written: 247

---

Sarah Chen is an award-winning business journalist specializing in the creator economy and digital entrepreneurship. With over 8 years of experience, she has become one of the leading voices in understanding how content creators are reshaping the business landscape.

Before joining Influencer News, Sarah spent five years at TechCrunch, where she launched their creator economy vertical and broke several major stories about platform changes and creator funding rounds. Her investigative series on creator burnout won the 2022 Digital Journalism Award.

Sarah holds a Master's degree in Business Journalism from Columbia University and a Bachelor's in Economics from UCLA. When she's not chasing stories, you can find her mentoring aspiring journalists or experimenting with her own YouTube channel about personal finance for creators.

Her work has been featured in The Wall Street Journal, Forbes, and Wired. She's a frequent speaker at creator economy conferences and has appeared on CNBC, Bloomberg, and NPR to discuss trends in the influencer space."""
        
        sample_file = self.content_dir / "sarah-chen.txt"
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        self.update_progress(f"Created sample author file: {sample_file}")