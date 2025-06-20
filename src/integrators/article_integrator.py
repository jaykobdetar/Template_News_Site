#!/usr/bin/env python3
"""
Enhanced Article Integrator
===========================
Integrates articles with progress callbacks for GUI
"""

import datetime
import json
from pathlib import Path
from typing import Dict, List, Any
from .base_integrator import BaseIntegrator
from ..models.article import Article
from ..models.author import Author
from ..models.category import Category


class ArticleIntegrator(BaseIntegrator):
    """Enhanced article integrator with GUI support"""
    
    def __init__(self):
        super().__init__('articles', 'articles')
        # Authors will be loaded from database dynamically
        self._authors_cache = None
    
    def get_author_info(self, author_name: str, author_slug: str = '') -> Dict[str, Any]:
        """Get author information from database"""
        if not self._authors_cache:
            # Load all authors from database and cache them
            try:
                authors = Author.find_all()
                self._authors_cache = {}
                for author in authors:
                    author_key = author.name.lower()
                    expertise_list = []
                    if author.expertise:
                        # Split comma-separated expertise
                        expertise_list = [e.strip() for e in author.expertise.split(',')]
                    
                    # Use image handler for proper image processing
                    from ..utils.image_handler import ImageHandler
                    image_handler = ImageHandler()
                    
                    author_data = {
                        'id': author.id,
                        'name': author.name,
                        'image_url': author.image_url
                    }
                    
                    self._authors_cache[author_key] = {
                        'name': author.name,
                        'title': author.title or 'Contributor',
                        'image': image_handler.process_author_image(author_data),
                        'bio': author.bio or 'Contributing writer for Influencer News.',
                        'expertise': expertise_list or ['General']
                    }
            except Exception as e:
                self.update_progress(f"Warning: Could not load authors from database: {e}")
                self._authors_cache = {}
        
        # Look up author by name
        author_key = author_name.lower()
        author_info = self._authors_cache.get(author_key)
        
        if not author_info:
            # Return default info for unknown authors
            from ..utils.image_handler import ImageHandler
            image_handler = ImageHandler()
            
            default_author_data = {
                'name': author_name,
                'image_url': ''
            }
            
            author_info = {
                'name': author_name,
                'title': 'Contributor',
                'image': image_handler.process_author_image(default_author_data),
                'bio': 'Contributing writer for Influencer News.',
                'expertise': ['General']
            }
        
        return author_info
    
    def sync_all(self):
        """Sync all articles from database"""
        self.update_progress("Starting article sync...")
        
        try:
            # Get articles from database with pagination (default limit)
            articles = Article.find_all(limit=50)  # Reasonable default limit
            
            if not articles:
                self.update_progress("No articles found in database")
                return
                
            # Convert to dictionaries for compatibility
            article_dicts = []
            for article in articles:
                # Get author and category from database using relationships
                author = article.get_author()
                category = article.get_category()
                
                author_name = author.name if author else 'Unknown Author'
                author_slug = author.slug if author else 'unknown-author'
                category_name = category.name if category else 'Uncategorized'
                category_slug = category.slug if category else 'uncategorized'
                
                author_info = self.get_author_info(author_name, author_slug)
                
                article_dict = {
                    'id': article.id,
                    'title': article.title,
                    'slug': article.slug,
                    'author': author_name,
                    'author_info': author_info,
                    'author_slug': author_slug,
                    'category': category_name,
                    'category_slug': category_slug,
                    'date': article.publish_date,
                    'content': article.content,
                    'excerpt': article.excerpt or '',
                    'image': f'assets/images/articles/article_{article.id}_hero.jpg',
                    'views': str(article.views),
                    'comments': str(article.comments),
                    'read_time': f'{article.read_time_minutes} min',
                    'tags': article.tags if isinstance(article.tags, list) else [],
                    'trending': article.trending
                }
                article_dicts.append(article_dict)
                
            # Create individual article pages
            for article_dict in article_dicts:
                self.create_content_page(article_dict)
                
            # Update listing pages (homepage, search)
            self.update_listing_page(article_dicts)
            
            self.update_progress(f"Synced {len(articles)} articles successfully")
            
        except Exception as e:
            self.update_progress(f"Error syncing articles: {e}")
            raise
    
    def parse_content_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse an article file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Split into sections
        sections = content.split('\n---\n')
        if len(sections) < 2:
            raise ValueError(f"Invalid format in {file_path}. Missing '---' separator.")
        
        # Parse metadata
        metadata = self.parse_metadata_section(sections[0])
        article_content = '\n---\n'.join(sections[1:]).strip()
        
        # Validate required fields
        required_fields = ['title', 'author', 'category', 'image', 'excerpt']
        self.validate_required_fields(metadata, required_fields, file_path)
        
        # Process content sections
        processed_content = self.format_article_content(article_content)
        
        # Get author info using database lookup
        author_info = self.get_author_info(metadata['author'])
        
        return {
            'title': metadata['title'],
            'author': author_info['name'],
            'author_info': author_info,
            'category': metadata['category'].lower(),
            'tags': [tag.strip() for tag in metadata.get('tags', '').split(',') if tag.strip()],
            'image': metadata['image'],
            'excerpt': metadata['excerpt'],
            'content': processed_content,
            'date': datetime.datetime.now().isoformat(),
            'views': str(self.generate_realistic_views()),
            'comments': str(self.generate_realistic_comments()),
            'read_time': self.calculate_read_time(article_content),
            'trending': metadata.get('trending', 'false').lower() == 'true'
        }
    
    def format_article_content(self, content: str) -> str:
        """Format article content with HTML"""
        html_content = ""
        
        # Process content sections
        content_sections = content.split('\n## ')
        
        for i, section in enumerate(content_sections):
            if i == 0 and not section.startswith('## '):
                # First section without heading
                html_content += self.format_content_section('', section)
            else:
                lines = section.split('\n', 1)
                heading = lines[0].strip()
                body = lines[1].strip() if len(lines) > 1 else ''
                html_content += self.format_content_section(heading, body)
        
        return html_content
    
    def format_content_section(self, heading: str, content: str) -> str:
        """Format a content section with proper HTML"""
        html_content = ""
        
        if heading:
            html_content += f'<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">{self.sanitize_text(heading)}</h2>\n'
        
        # Process paragraphs and special formatting
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # Handle special formatting
            if para.startswith('> '):
                # Blockquote
                quote_text = para[2:].strip()
                if ' - ' in quote_text:
                    quote, author = quote_text.rsplit(' - ', 1)
                    html_content += f'''<blockquote class="border-l-4 border-gray-300 pl-6 italic text-gray-700 my-8 text-lg">
                        {self.sanitize_text(quote)}
                        <footer class="text-sm text-gray-500 mt-2">— {self.sanitize_text(author)}</footer>
                    </blockquote>\n'''
                else:
                    html_content += f'<blockquote class="border-l-4 border-gray-300 pl-6 italic text-gray-700 my-8 text-lg">{self.sanitize_text(quote_text)}</blockquote>\n'
            elif para.startswith('- '):
                # Bullet list
                items = [line[2:].strip() for line in para.split('\n') if line.strip().startswith('- ')]
                html_content += '<ul class="list-disc pl-6 text-gray-700 mb-6 space-y-2">\n'
                for item in items:
                    html_content += f'    <li>{self.sanitize_text(item)}</li>\n'
                html_content += '</ul>\n'
            elif para.startswith('[INFO]'):
                # Info box
                info_text = para[6:].strip()
                html_content += f'''<div class="bg-indigo-50 border-l-4 border-indigo-400 p-6 my-8">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <svg class="h-5 w-5 text-indigo-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                            </svg>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm text-indigo-700">{self.sanitize_text(info_text)}</p>
                        </div>
                    </div>
                </div>\n'''
            else:
                # Regular paragraph
                html_content += f'<p class="text-gray-700 mb-6">{self.sanitize_text(para)}</p>\n'
        
        return html_content
    
    def generate_realistic_views(self) -> int:
        """Return actual view count from database"""
        return 0  # Return real view count or 0 if not tracked
    
    def generate_realistic_comments(self) -> int:
        """Return actual comment count from database"""
        return 0  # Return real comment count or 0 if not tracked
    
    def calculate_read_time(self, content: str) -> str:
        """Calculate estimated read time"""
        word_count = len(content.split())
        minutes = max(1, round(word_count / 200))  # Average 200 WPM
        return f"{minutes} min"
    
    def create_content_page(self, article: Dict[str, Any]):
        """Create individual article page"""
        # Get path manager for this location (using slug-based naming)
        article_filename = f"article_{article['slug']}.html"
        path_manager = self.get_path_manager(f"integrated/articles/{article_filename}")
        base_path = path_manager.get_base_path()
        
        # Use template engine for cleaner rendering
        from ..utils.template_engine import ArticleTemplate
        import os
        
        template_engine = ArticleTemplate()
        
        # Try to use new template engine first
        template_path = None
        use_template_engine = False
        
        # Look for new template
        new_template_paths = [
            os.path.join(os.getcwd(), 'templates', 'article.html'),
            os.path.join(os.path.dirname(os.getcwd()), 'templates', 'article.html')
        ]
        
        for path in new_template_paths:
            if os.path.exists(path):
                template_path = path
                use_template_engine = True
                break
        
        # Fall back to old template if new one not found
        if not template_path:
            old_template_paths = [
                os.path.join(os.getcwd(), 'article.html'),
                os.path.join(os.path.dirname(os.getcwd()), 'article.html')
            ]
            
            for path in old_template_paths:
                if os.path.exists(path):
                    template_path = path
                    break
        
        if not template_path:
            raise FileNotFoundError("Article template not found")
        
        # Load template
        if use_template_engine:
            template_engine.load_article_template(template_path)
        else:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
        
        # If using template engine, render with context
        if use_template_engine:
            # Prepare article data for template engine
            article_data = {
                'title': article['title'],
                'slug': article['slug'],
                'excerpt': article.get('excerpt', ''),
                'content': article['content'],
                'author_name': article['author_info']['name'],
                'author_slug': article['author_info']['name'].lower().replace(' ', '-'),
                'author_title': article['author_info']['title'],
                'author_bio': article['author_info']['bio'],
                'author_image': article['author_info']['image'],
                'author_location': article['author_info'].get('location', 'Unknown'),
                'author_article_count': article['author_info'].get('article_count', 0),
                'category_name': article['category'],
                'category_slug': article['category'].lower().replace(' ', '-'),
                'category_color': 'indigo',  # Default color
                'category_icon': article.get('category_icon', '📁'),
                'image_url': article['image'],
                'views': int(article['views']),
                'likes': int(article['views']) // 50,
                'comments': int(article['comments']),
                'shares': int(article['comments']) * 2,
                'read_time': article['read_time'],
                'publish_date': article['date'],
                'publish_date_relative': self.format_date_relative(article['date']),
                'is_breaking': article.get('is_breaking', False),
                'tags': article.get('tags', []),
                'related_articles': []
            }
            
            # Render with template engine
            output_html = template_engine.render_article(article_data, base_path)
            
        else:
            # Fall back to old replacement method
            # Replace {base_path} placeholders with actual base path
            template = template.replace('{base_path}', base_path)
            
            # Format numbers with commas
            views_formatted = f"{int(article['views']):,}"
            likes_formatted = f"{int(article['views']) // 50:,}"
            comments_formatted = f"{int(article['comments']):,}"
            
            # Apply site branding before other replacements
            template = self._apply_site_branding(template)
            
            # Replace placeholders
            replacements = {
            'MrBeast Announces Revolutionary $100M Creator Support Fund to Transform YouTube Landscape': article['title'],
            'Sarah Chen': article['author_info']['name'],
            'Senior Business Reporter': article['author_info']['title'],
            'https://images.unsplash.com/photo-1494790108755-2616c395d75b?w=50&h=50&fit=crop&crop=face': article['author_info']['image'],
            'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=400&fit=crop': article['image'],
            'Published 2 hours ago': f"Published {self.format_date_relative(article['date'])}",
            '5 minute read': f"{article['read_time']} read",
            '1,247,892': views_formatted,
            '24,156': likes_formatted,
            '2,847': comments_formatted,
            # Fix breadcrumb replacements - add proper category links
            'search.html?q=business': f"../categories/category_{article['category'].lower().replace(' ', '-')}.html",
            '>Business<': f">{article['category'].title()}<",
            '>MrBeast Creator Fund<': f">{article['title'][:50] + '...' if len(article['title']) > 50 else article['title']}<",
            # Fix sidebar author references - add proper author links
            'Jessica Kim': article['author_info']['name'],
            'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=80&h=80&fit=crop&crop=face': article['author_info']['image'].replace('w=50&h=50', 'w=80&h=80'),
            'Follow Sarah': f"Follow {article['author_info']['name'].split()[0]}",
            # Fix share functionality
            '"MrBeast Announces Revolutionary $100M Creator Support Fund"': f'"{article["title"]}"',
            'alt="MrBeast Creator Fund Announcement"': f'alt="{article["title"]}"',
        }
        
            # Apply replacements
            for old, new in replacements.items():
                template = template.replace(old, new)
            
            # Add clickable author links - wrap author names with links
            author_slug = article['author_info']['name'].lower().replace(' ', '-')
            author_link = f'../authors/author_{author_slug}.html'
            
            # Replace author name instances with clickable links
            template = template.replace(
                f'<h3 class="text-xl font-bold text-gray-900">{article["author_info"]["name"]}</h3>',
                f'<h3 class="text-xl font-bold text-gray-900"><a href="{author_link}" class="hover:text-indigo-600 transition">{article["author_info"]["name"]}</a></h3>'
            )
            
            # Also add link in the article header area where author name appears
            template = template.replace(
                f'<span class="text-gray-600 font-medium">{article["author_info"]["name"]}</span>',
                f'<span class="text-gray-600 font-medium"><a href="{author_link}" class="hover:text-indigo-600 transition">{article["author_info"]["name"]}</a></span>'
            )
            
            # Replace content
            content_start = template.find('<div class="prose prose-lg max-w-none" id="articleContent">')
            content_end = template.find('</div>', content_start) + 6
            
            if content_start != -1 and content_end != -1:
                new_content = f'''<div class="prose prose-lg max-w-none" id="articleContent">
                    <p class="text-xl text-gray-700 font-medium mb-6 leading-relaxed">
                        {self.sanitize_text(article['excerpt'])}
                    </p>
                    {article['content']}
                </div>'''
                template = template[:content_start] + new_content + template[content_end:]
            
            # End of old replacement method - assign to output_html
            output_html = template
            
            # Add CSP nonces to output HTML for fallback method
            nonce = self.get_current_nonce()
            output_html = self._add_nonces_to_html(output_html, nonce)
        
        # Save the article page (using slug-based naming)
        article_filename = self.integrated_dir / f"article_{article['slug']}.html"
        with open(article_filename, 'w', encoding='utf-8') as f:
            f.write(output_html)
        
        self.update_progress(f"Created article page: {article_filename}")
    
    def _apply_site_branding(self, html_content: str) -> str:
        """Apply site configuration to HTML content"""
        try:
            site_integrator = self.get_site_integrator()
            branding = site_integrator.get_config_section('branding')
            contact = site_integrator.get_config_section('contact')
            
            # Create replacements dictionary - use site config dynamically
            replacements = {
                # Site name replacements
                'Influencer News': branding.get('site_name'),
                # Title tag replacements
                ' - Influencer News': f" - {branding.get('site_name')}",
                # Header logo text
                '>IN<': f">{branding.get('logo_text')}<",
                # Header tagline
                'Breaking stories • Real insights': branding.get('site_tagline'),
                # Theme color replacements - comprehensive
                '#4f46e5': branding.get('theme_color'),  # indigo-500
                '#6366f1': branding.get('theme_color'),  # indigo-500 variant
                '#312e81': branding.get('theme_color'),  # indigo-900
                '#4338ca': branding.get('theme_color'),  # indigo-700
                '#3730a3': branding.get('theme_color'),  # indigo-800
                '#1e1b4b': branding.get('theme_color'),  # indigo-950
                '#667eea': branding.get('theme_color'),  # custom indigo
                # Specific Tailwind class replacements
                'bg-indigo-900': f"bg-{self._get_theme_class_name(branding.get('theme_color'))}900",
                'bg-indigo-800': f"bg-{self._get_theme_class_name(branding.get('theme_color'))}800",
                'bg-indigo-700': f"bg-{self._get_theme_class_name(branding.get('theme_color'))}700",
                'bg-indigo-600': f"bg-{self._get_theme_class_name(branding.get('theme_color'))}600",
                'bg-indigo-500': f"bg-{self._get_theme_class_name(branding.get('theme_color'))}500",
                'bg-indigo-400': f"bg-{self._get_theme_class_name(branding.get('theme_color'))}400",
                'text-indigo-900': f"text-{self._get_theme_class_name(branding.get('theme_color'))}900",
                'text-indigo-800': f"text-{self._get_theme_class_name(branding.get('theme_color'))}800",
                'text-indigo-700': f"text-{self._get_theme_class_name(branding.get('theme_color'))}700",
                'text-indigo-600': f"text-{self._get_theme_class_name(branding.get('theme_color'))}600",
                'text-indigo-500': f"text-{self._get_theme_class_name(branding.get('theme_color'))}500",
                'text-indigo-400': f"text-{self._get_theme_class_name(branding.get('theme_color'))}400",
                'text-indigo-300': f"text-{self._get_theme_class_name(branding.get('theme_color'))}300",
                'text-indigo-200': f"text-{self._get_theme_class_name(branding.get('theme_color'))}200",
                'text-indigo-100': f"text-{self._get_theme_class_name(branding.get('theme_color'))}100",
                'border-indigo-700': f"border-{self._get_theme_class_name(branding.get('theme_color'))}700",
                'border-indigo-600': f"border-{self._get_theme_class_name(branding.get('theme_color'))}600",
                'border-indigo-500': f"border-{self._get_theme_class_name(branding.get('theme_color'))}500",
                'border-indigo-400': f"border-{self._get_theme_class_name(branding.get('theme_color'))}400",
                'hover:bg-indigo-700': f"hover:bg-{self._get_theme_class_name(branding.get('theme_color'))}700",
                'hover:bg-indigo-600': f"hover:bg-{self._get_theme_class_name(branding.get('theme_color'))}600",
                'hover:text-indigo-600': f"hover:text-{self._get_theme_class_name(branding.get('theme_color'))}600",
                'hover:text-indigo-200': f"hover:text-{self._get_theme_class_name(branding.get('theme_color'))}200",
                'focus:ring-indigo-400': f"focus:ring-{self._get_theme_class_name(branding.get('theme_color'))}400",
                'from-indigo-400': f"from-{self._get_theme_class_name(branding.get('theme_color'))}400",
                'from-indigo-500': f"from-{self._get_theme_class_name(branding.get('theme_color'))}500",
                'to-purple-600': f"to-{self._get_theme_class_name(branding.get('theme_color'))}600",
                'bg-indigo-50': f"bg-{self._get_theme_class_name(branding.get('theme_color'))}50",
                'border-indigo-400': f"border-{self._get_theme_class_name(branding.get('theme_color'))}400",
                # Footer copyright
                '© 2025 Influencer News': f"© 2025 {branding.get('site_name')}",
                # Contact info in footer
                'news@influencernews.com': contact.get('contact_email'),
                '(555) 123-NEWS': contact.get('contact_phone'),
                '123 Creator Avenue': contact.get('business_address'),
                'Los Angeles, CA 90210': f"{contact.get('city', 'New York')}, {contact.get('state', 'NY')} {contact.get('zip_code', '10001')}"
            }
            
            # Apply all replacements
            for old_value, new_value in replacements.items():
                if old_value and new_value:  # Only replace if both values exist and are not None
                    html_content = html_content.replace(old_value, str(new_value))
            
            return html_content
            
        except Exception as e:
            self.update_progress(f"Warning: Could not apply site branding to article: {e}")
            return html_content
    
    def _get_theme_class_name(self, theme_color: str) -> str:
        """Convert theme color to appropriate Tailwind class name"""
        if not theme_color:
            return 'emerald-'
        
        # Map common colors to Tailwind classes
        color_map = {
            '#059669': 'emerald-',
            '#10b981': 'emerald-',
            '#3b82f6': 'blue-',
            '#8b5cf6': 'violet-',
            '#f59e0b': 'amber-',
            '#ef4444': 'red-',
            '#6b7280': 'gray-'
        }
        
        return color_map.get(theme_color.lower(), 'emerald-')
    
    def _add_nonces_to_html(self, html: str, nonce: str) -> str:
        """Add nonces to inline scripts and styles"""
        import re
        
        # Add nonce to inline script tags that don't have it
        script_pattern = re.compile(r'<script(?![^>]*\bnonce=)([^>]*)>', re.IGNORECASE)
        
        def add_nonce_to_script(match):
            attrs = match.group(1)
            # Skip external scripts (those with src attribute)
            if 'src=' in attrs:
                return match.group(0)
            return f'<script nonce="{nonce}"{attrs}>'
        
        html = script_pattern.sub(add_nonce_to_script, html)
        
        # Add nonce to inline style tags that don't have it
        style_pattern = re.compile(r'<style(?![^>]*\bnonce=)([^>]*)>', re.IGNORECASE)
        
        def add_nonce_to_style(match):
            attrs = match.group(1)
            return f'<style nonce="{nonce}"{attrs}>'
        
        html = style_pattern.sub(add_nonce_to_style, html)
        
        # Update CSP meta tag with current nonce
        csp_meta_pattern = re.compile(
            r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]*)"[^>]*>',
            re.IGNORECASE
        )
        
        def update_csp_meta(match):
            # Get new CSP with nonce
            new_csp = self.security_middleware.csp_generator.get_strict_csp(nonce)
            return f'<meta http-equiv="Content-Security-Policy" content="{new_csp}">'
        
        html = csp_meta_pattern.sub(update_csp_meta, html)
        
        return html
    
    def update_listing_page(self, articles: List[Dict[str, Any]]):
        """Update homepage with latest articles"""
        self.update_homepage(articles)
        self.update_search_page(articles)
    
    def update_homepage(self, articles: List[Dict[str, Any]]):
        """Update homepage with latest articles"""
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate article cards HTML
        articles_html = ""
        
        if articles:
            # If there are articles, display them
            for i, article in enumerate(articles[:12]):  # Show latest 12 articles for pagination
                card_class = "md:col-span-2 lg:col-span-1" if i == 0 else ""  # Featured article
                
                # Format views
                views_formatted = f"{article['views']:,}" if isinstance(article['views'], int) else str(article['views'])
                
                articles_html += f'''
                <div class="article-card bg-white rounded-xl shadow-lg overflow-hidden {card_class}">
                    <div class="relative">
                        <img src="{article['image']}" alt="{self.sanitize_text(article['title'])}" class="w-full h-48 object-cover">
                        <div class="absolute top-4 right-4">
                            <span class="category-{article['category']} bg-white/90 px-2 py-1 rounded text-xs font-bold uppercase">{article['category']}</span>
                        </div>
                    </div>
                    <div class="p-6">
                        <div class="flex items-center gap-2 mb-3">
                            <span class="text-gray-500 text-sm">{article['author']} • {self.format_date_relative(article['date'])}</span>
                        </div>
                        <h3 class="text-lg font-bold mb-3 hover:text-emerald-600 transition cursor-pointer">
                            {self.sanitize_text(article['title'])}
                        </h3>
                        <p class="text-gray-700 mb-4 text-sm">
                            {self.sanitize_text(article['excerpt'])}
                        </p>
                        <div class="flex items-center justify-between text-sm">
                            <span class="text-gray-500">👁 {views_formatted} views</span>
                            <a href="integrated/articles/article_{article['slug']}.html" class="text-indigo-600 font-medium cursor-pointer">Read →</a>
                        </div>
                    </div>
                </div>
            '''
        else:
            # If no articles, show empty state
            articles_html = '''
                <div class="col-span-full text-center py-16">
                    <div class="text-gray-400 text-6xl mb-4">📰</div>
                    <h3 class="text-xl font-semibold text-gray-600 mb-2">No Articles Yet</h3>
                    <p class="text-gray-500">Check back soon for the latest news and updates!</p>
                </div>
            '''
        
        # Replace articles section
        start_marker = '<div id="articlesGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">'
        end_marker = '</div>\n\n            <!-- Load More Button -->'
        
        start_pos = content.find(start_marker)
        end_pos = content.find(end_marker)
        
        if start_pos != -1 and end_pos != -1:
            new_section = f'{start_marker}\n{articles_html}\n            </div>'
            content = content[:start_pos] + new_section + content[end_pos:]
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        if articles:
            self.update_progress(f"Updated homepage with {len(articles)} articles")
        else:
            self.update_progress("Cleared homepage - no articles to display")
    
    def update_search_page(self, articles: List[Dict[str, Any]]):
        """Update search page JavaScript with new articles"""
        with open('search.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate JavaScript articles array
        if articles:
            js_articles = "const articles = [\n"
            for article in articles:
                js_articles += f'''            {{
                id: {article['id']},
                title: "{self.escape_js_string(article['title'])}",
                author: "{self.escape_js_string(article['author'])}",
                date: "{self.format_date_relative(article['date'])}",
                category: "{article['category']}",
                views: "{article['views']}",
                image: "{article['image']}",
                excerpt: "{self.escape_js_string(article['excerpt'])}",
                readTime: "{article['read_time']}",
                trending: {str(article.get('trending', False)).lower()}
            }},
'''
            js_articles += "        ];"
        else:
            # Empty articles array when no articles
            js_articles = "const articles = [];"
        
        # Replace articles array in JavaScript
        start_marker = "const articles = ["
        end_marker = "        ];"
        
        start_pos = content.find(start_marker)
        if start_pos != -1:
            end_pos = content.find(end_marker, start_pos) + len(end_marker)
            content = content[:start_pos] + js_articles + content[end_pos:]
        
        with open('search.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        if articles:
            self.update_progress(f"Updated search page with {len(articles)} articles")
        else:
            self.update_progress("Cleared search page - no articles to display")
    
    def create_sample_file(self):
        """Create a sample article file"""
        sample_content = """Title: Sample Article Title Here
Author: Sarah Chen
Category: business
Image: https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=600&h=300&fit=crop
Tags: sample, demo, tutorial
Excerpt: This is a brief excerpt that will appear on the homepage and in search results. Keep it under 200 characters for best display.

---

This is the opening paragraph of your article. It should hook the reader and provide a compelling introduction to your topic.

## First Section Heading

This is the content under the first section. You can write multiple paragraphs here.

This is a second paragraph in the same section.

## Important Information Box

[INFO] This is an information box that will be highlighted with a special blue background. Use this for key facts or important details.

## Lists and Special Formatting

Here's how to create a bullet list:

- First item in the list
- Second item in the list  
- Third item with more details

## Quotes and Citations

You can include blockquotes like this:

> This is a quote from someone important. It will be styled nicely with proper formatting. - Quote Author

## Final Section

End your article with a strong conclusion that ties everything together and provides value to the reader.
"""
        
        sample_file = self.content_dir / "sample_article.txt"
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        self.update_progress(f"Created sample article: {sample_file}")
    
    def process_article(self, content_data: Dict[str, Any]) -> bool:
        """Process article content and add to database"""
        try:
            # Find author by name
            author_name = content_data.get('author', '').lower()
            author = Author.find_by_slug(author_name.replace(' ', '-'))
            if not author:
                # Try by exact name match
                all_authors = Author.find_all()
                author = next((a for a in all_authors if a.name.lower() == author_name), None)
                
            if not author:
                self.update_progress(f"Warning: Author '{content_data.get('author')}' not found, using default")
                # Use first available author as fallback
                all_authors = Author.find_all()
                author = all_authors[0] if all_authors else None
                if not author:
                    self.update_progress("Error: No authors found in database")
                    return False
            
            # Find category by name
            category_name = content_data.get('category', '').lower()
            category = Category.find_by_slug(category_name)
            if not category:
                # Try by exact name match  
                all_categories = Category.find_all()
                category = next((c for c in all_categories if c.name.lower() == category_name), None)
                
            if not category:
                self.update_progress(f"Warning: Category '{content_data.get('category')}' not found, using default")
                # Use first available category as fallback
                all_categories = Category.find_all()
                category = all_categories[0] if all_categories else None
                if not category:
                    self.update_progress("Error: No categories found in database")
                    return False
            
            # Generate slug from title
            title = content_data.get('title', '')
            slug = title.lower().replace(' ', '-').replace(',', '').replace(':', '').replace('?', '').replace('!', '')
            slug = ''.join(c for c in slug if c.isalnum() or c == '-')
            
            # Check if article already exists
            existing = Article.find_by_slug(slug)
            if existing:
                self.update_progress(f"Article '{title}' already exists, skipping")
                return False
            
            # Create article
            article = Article(
                title=title,
                slug=slug,
                author_id=author.id,
                category_id=category.id,
                publish_date=content_data.get('date', datetime.datetime.now().isoformat()),
                content=content_data.get('content', ''),
                excerpt=content_data.get('excerpt', ''),
                read_time_minutes=content_data.get('read_time', 5),
                tags_json=json.dumps(content_data.get('tags', [])),
                seo_description=content_data.get('excerpt', '')
            )
            
            # Save to database
            article.save()
            
            # Handle image if provided
            if content_data.get('image'):
                self.convert_image_urls(
                    content={'image': content_data['image'], 'title': title},
                    content_type='article',
                    content_id=article.id,
                    slug=slug
                )
            
            self.update_progress(f"Successfully added article: {title}")
            return True
            
        except Exception as e:
            self.update_progress(f"Error processing article: {str(e)}")
            return False
    
    def update_article(self, article, content_data: Dict[str, Any]) -> bool:
        """Update existing article with new data from file"""
        try:
            
            # Update article fields with new data
            updated_fields = []
            
            if article.title != content_data.get('title', ''):
                article.title = content_data['title']
                updated_fields.append('title')
            
            if article.content != content_data.get('content', ''):
                article.content = content_data['content']
                updated_fields.append('content')
            
            if article.subtitle != content_data.get('excerpt', ''):
                article.subtitle = content_data['excerpt']
                updated_fields.append('excerpt')
            
            # Update author if needed
            author_name = content_data.get('author', '')
            if article.author_name != author_name:
                article.author_name = author_name
                # Update author reference if possible
                from ..models.author import Author
                author = Author.find_by_name(author_name)
                if author:
                    article.author_id = author.id
                    article.author_slug = author.slug
                updated_fields.append('author')
            
            # Update category if needed
            category_name = content_data.get('category', '')
            if article.category_name != category_name:
                article.category_name = category_name
                # Update category reference if possible
                from ..models.category import Category
                category = Category.find_by_name(category_name)
                if category:
                    article.category_id = category.id
                    article.category_slug = category.slug
                updated_fields.append('category')
            
            # Update image URL if provided
            if 'image' in content_data and content_data['image']:
                if article.image_url != content_data['image']:
                    article.image_url = content_data['image']
                    updated_fields.append('image')
            
            # Update tags if provided
            if 'tags' in content_data and content_data['tags']:
                new_tags = content_data['tags'] if isinstance(content_data['tags'], str) else ', '.join(content_data['tags'])
                if article.tags != new_tags:
                    article.tags = new_tags
                    updated_fields.append('tags')
            
            # Update last modified timestamp
            article.updated_at = datetime.datetime.now().isoformat()
            
            # Save changes to database
            if updated_fields:
                success = article.save()
                if success:
                    self.update_progress(f"Updated article '{article.title}' - fields: {', '.join(updated_fields)}")
                    return True
                else:
                    self.update_progress(f"Failed to save article '{article.title}' to database")
                    return False
            else:
                self.update_progress(f"No changes detected for article '{article.title}'")
                return False
                
        except Exception as e:
            self.update_progress(f"Error updating article: {str(e)}")
            return False
    
    def update_all_listing_pages(self):
        """Update all listing pages with current articles from database"""
        self.update_progress("Updating listing pages...")
        
        # Get all articles from database
        articles = Article.find_all()
        
        # Convert to dictionaries for compatibility
        article_dicts = []
        for article in articles:
            author_name = article.author_name or 'Unknown Author'
            author_info = self.get_author_info(author_name, article.author_slug or '')
            
            article_dict = {
                'id': article.id,
                'title': article.title,
                'slug': article.slug,
                'author': author_name,
                'author_info': author_info,
                'author_slug': article.author_slug or '',
                'category': article.category_name or 'Uncategorized',
                'category_slug': article.category_slug or '',
                'date': article.publication_date,
                'content': article.content,
                'excerpt': article.subtitle or '',
                'views': article.views or 0,
                'read_time': article.read_time_minutes or 3,
                'image': f'assets/images/articles/article_{article.id}_hero.jpg',
                'trending': False
            }
            article_dicts.append(article_dict)
        
        # Update homepage and search page
        self.update_homepage(article_dicts)
        self.update_search_page(article_dicts)
        
        self.update_progress(f"Updated listing pages with {len(article_dicts)} articles")


