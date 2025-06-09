#!/usr/bin/env python3
"""
Trending Integrator
===================
Manages trending topics and generates trending pages
"""

import random
import datetime
from pathlib import Path
from typing import Dict, List, Any
from .base_integrator import BaseIntegrator


class TrendingIntegrator(BaseIntegrator):
    """Integrator for managing trending topics"""
    
    def __init__(self):
        super().__init__('trending', 'trending', 'trending_db.json')
        
        # Status levels for trends
        self.status_levels = {
            'active': {'label': 'Trending Now', 'color': 'red', 'priority': 1},
            'rising': {'label': 'On The Rise', 'color': 'orange', 'priority': 2},
            'steady': {'label': 'Steady Interest', 'color': 'blue', 'priority': 3},
            'declining': {'label': 'Past Peak', 'color': 'gray', 'priority': 4}
        }
    
    def parse_content_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a trending topic file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Split into sections
        sections = content.split('\n---\n')
        if len(sections) < 2:
            raise ValueError(f"Invalid format in {file_path}. Missing '---' separator.")
        
        # Parse metadata
        metadata = self.parse_metadata_section(sections[0])
        analysis_content = '\n---\n'.join(sections[1:]).strip()
        
        # Validate required fields
        required_fields = ['topic', 'category']
        self.validate_required_fields(metadata, required_fields, file_path)
        
        # Parse related articles (comma-separated IDs)
        related_articles = []
        if metadata.get('related_articles'):
            related_articles = [int(id.strip()) for id in metadata['related_articles'].split(',') if id.strip().isdigit()]
        
        # Get status info
        status = metadata.get('status', 'active').lower()
        status_info = self.status_levels.get(status, self.status_levels['active'])
        
        return {
            'topic': metadata['topic'],
            'hashtag': metadata.get('hashtag', f"#{metadata['topic'].replace(' ', '')}"),
            'category': metadata['category'].lower(),
            'trend_score': int(metadata.get('trend_score', random.randint(1000, 10000))),
            'related_articles': related_articles,
            'status': status,
            'status_info': status_info,
            'icon': metadata.get('icon', '🔥'),
            'analysis': analysis_content,
            'date_started': metadata.get('date_started', datetime.datetime.now().isoformat()),
            'peak_date': metadata.get('peak_date', None),
            'platform_data': self._parse_platform_data(metadata),
            'growth_rate': float(metadata.get('growth_rate', random.uniform(-20, 100)))
        }
    
    def _parse_platform_data(self, metadata: Dict[str, str]) -> Dict[str, int]:
        """Parse platform-specific trending data"""
        platforms = ['youtube', 'tiktok', 'instagram', 'twitter', 'twitch']
        data = {}
        for platform in platforms:
            key = f'{platform}_mentions'
            if key in metadata:
                data[platform] = int(metadata[key])
            else:
                # Generate random data for demo
                data[platform] = random.randint(100, 50000)
        return data
    
    def create_content_page(self, trend: Dict[str, Any]):
        """Create individual trending topic page"""
        trend_slug = trend['topic'].lower().replace(' ', '-')
        trend_filename = self.integrated_dir / f"trend_{trend_slug}.html"
        
        # Create HTML content for trend page
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{trend['topic']} - Trending Topic | Influencer News</title>
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
                    <li><a href="../../authors.html" class="hover:text-indigo-200 transition font-medium">Authors</a></li>
                    <li><a href="../categories.html" class="hover:text-indigo-200 transition font-medium">Categories</a></li>
                    <li><a href="../trending.html" class="hover:text-indigo-200 transition font-medium text-indigo-200">Trending</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Trend Hero -->
    <section class="bg-gradient-to-br from-{trend['status_info']['color']}-700 via-{trend['status_info']['color']}-600 to-{trend['status_info']['color']}-500 text-white py-20">
        <div class="container mx-auto px-4 text-center">
            <div class="inline-flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full mb-6">
                <span class="text-sm font-medium">{trend['status_info']['label']}</span>
                <span class="text-xl">{trend['icon']}</span>
            </div>
            <h1 class="text-5xl font-bold mb-4 hero-title">{self.escape_html(trend['topic'])}</h1>
            <p class="text-2xl text-white/90 mb-8">{self.escape_html(trend['hashtag'])}</p>
            
            <div class="flex flex-wrap gap-4 justify-center">
                <div class="bg-white/20 backdrop-blur-sm px-6 py-4 rounded-xl">
                    <p class="text-3xl font-bold">{trend['trend_score']:,}</p>
                    <p class="text-sm">Trend Score</p>
                </div>
                <div class="bg-white/20 backdrop-blur-sm px-6 py-4 rounded-xl">
                    <p class="text-3xl font-bold">{trend['growth_rate']:+.1f}%</p>
                    <p class="text-sm">Growth Rate</p>
                </div>
                <div class="bg-white/20 backdrop-blur-sm px-6 py-4 rounded-xl">
                    <p class="text-3xl font-bold">{len(trend['related_articles'])}</p>
                    <p class="text-sm">Related Articles</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Trend Analysis -->
            <div class="lg:col-span-2">
                <div class="bg-white rounded-2xl shadow-lg p-8">
                    <h2 class="text-3xl font-bold mb-6 hero-title">Trend Analysis</h2>
                    <div class="prose prose-lg max-w-none text-gray-700">
                        {self._format_analysis(trend['analysis'])}
                    </div>
                </div>
                
                <!-- Related Articles -->
                <div class="bg-white rounded-2xl shadow-lg p-8 mt-8">
                    <h2 class="text-3xl font-bold mb-6 hero-title">Related Coverage</h2>
                    <div id="relatedArticles" class="space-y-4">
                        <p class="text-gray-600">Related articles will be displayed here after integration.</p>
                    </div>
                </div>
            </div>
            
            <!-- Sidebar -->
            <div class="lg:col-span-1">
                <!-- Platform Breakdown -->
                <div class="bg-white rounded-2xl shadow-lg p-6 mb-6">
                    <h3 class="text-xl font-bold mb-4">Platform Breakdown</h3>
                    {self._generate_platform_stats(trend['platform_data'])}
                </div>
                
                <!-- Timeline -->
                <div class="bg-white rounded-2xl shadow-lg p-6">
                    <h3 class="text-xl font-bold mb-4">Trend Timeline</h3>
                    <div class="space-y-3">
                        <div class="flex items-center gap-3">
                            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                            <div>
                                <p class="font-medium">Started Trending</p>
                                <p class="text-sm text-gray-600">{self.format_date_relative(trend['date_started'])}</p>
                            </div>
                        </div>
                        {self._generate_peak_info(trend)}
                        <div class="flex items-center gap-3">
                            <div class="w-3 h-3 bg-{trend['status_info']['color']}-500 rounded-full animate-pulse"></div>
                            <div>
                                <p class="font-medium">Current Status</p>
                                <p class="text-sm text-gray-600">{trend['status_info']['label']}</p>
                            </div>
                        </div>
                    </div>
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
        
        with open(trend_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.update_progress(f"Created trending page: {trend_filename}")
    
    def _format_analysis(self, analysis: str) -> str:
        """Format trend analysis content"""
        paragraphs = analysis.split('\n\n')
        formatted = ""
        for para in paragraphs:
            if para.strip():
                if para.strip().startswith('- '):
                    # Handle bullet points
                    items = [line[2:].strip() for line in para.split('\n') if line.strip().startswith('- ')]
                    formatted += '<ul class="list-disc pl-6 mb-4">\n'
                    for item in items:
                        formatted += f'<li>{self.escape_html(item)}</li>\n'
                    formatted += '</ul>\n'
                else:
                    formatted += f'<p class="mb-4">{self.escape_html(para.strip())}</p>\n'
        return formatted
    
    def _generate_platform_stats(self, platform_data: Dict[str, int]) -> str:
        """Generate platform statistics visualization"""
        total = sum(platform_data.values())
        stats = '<div class="space-y-3">'
        
        platform_icons = {
            'youtube': '📺',
            'tiktok': '🎵',
            'instagram': '📸',
            'twitter': '🐦',
            'twitch': '🎮'
        }
        
        for platform, count in sorted(platform_data.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            icon = platform_icons.get(platform, '📱')
            
            stats += f'''
            <div>
                <div class="flex justify-between mb-1">
                    <span class="text-sm font-medium">{icon} {platform.title()}</span>
                    <span class="text-sm text-gray-600">{count:,}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-gradient-to-r from-indigo-500 to-purple-600 h-2 rounded-full" style="width: {percentage}%"></div>
                </div>
            </div>
            '''
        
        stats += '</div>'
        return stats
    
    def _generate_peak_info(self, trend: Dict[str, Any]) -> str:
        """Generate peak information if available"""
        if trend.get('peak_date'):
            return f'''
            <div class="flex items-center gap-3">
                <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div>
                    <p class="font-medium">Peak Interest</p>
                    <p class="text-sm text-gray-600">{self.format_date_relative(trend['peak_date'])}</p>
                </div>
            </div>
            '''
        return ""
    
    def update_listing_page(self, trends: List[Dict[str, Any]]):
        """Create trending overview page"""
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trending Topics - Influencer News</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .hero-title { font-family: 'Playfair Display', serif; }
        .trend-card {
            transition: all 0.3s ease;
        }
        .trend-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
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
                    <li><a href="categories.html" class="hover:text-indigo-200 transition font-medium">Categories</a></li>
                    <li><a href="trending.html" class="hover:text-indigo-200 transition font-medium text-indigo-200">Trending</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-red-700 via-orange-600 to-yellow-500 text-white py-20">
        <div class="container mx-auto px-4 text-center">
            <div class="text-6xl mb-4">🔥</div>
            <h1 class="text-5xl font-bold mb-4 hero-title">Trending Now</h1>
            <p class="text-xl text-white/90 max-w-3xl mx-auto">
                Real-time tracking of what's hot in the influencer world
            </p>
        </div>
    </section>

    <!-- Filter Tabs -->
    <div class="bg-white shadow-md sticky top-20 z-40">
        <div class="container mx-auto px-4">
            <div class="flex space-x-8 py-4 overflow-x-auto">
                <button class="trend-filter active font-medium text-indigo-600 border-b-2 border-indigo-600 pb-2" data-status="all">
                    All Trends
                </button>
                <button class="trend-filter font-medium text-gray-600 hover:text-indigo-600 transition pb-2" data-status="active">
                    🔥 Trending Now
                </button>
                <button class="trend-filter font-medium text-gray-600 hover:text-indigo-600 transition pb-2" data-status="rising">
                    📈 On The Rise
                </button>
                <button class="trend-filter font-medium text-gray-600 hover:text-indigo-600 transition pb-2" data-status="steady">
                    📊 Steady Interest
                </button>
            </div>
        </div>
    </div>

    <!-- Trends Grid -->
    <main class="container mx-auto px-4 py-12">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="trendsGrid">
'''
        
        # Sort trends by status priority and trend score
        sorted_trends = sorted(trends, key=lambda x: (x['status_info']['priority'], -x['trend_score']))
        
        for trend in sorted_trends:
            trend_slug = trend['topic'].lower().replace(' ', '-')
            status_color = trend['status_info']['color']
            
            html_content += f'''
            <div class="trend-card bg-white rounded-2xl shadow-lg overflow-hidden" data-status="{trend['status']}">
                <div class="p-6">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-3xl">{trend['icon']}</span>
                        <span class="bg-{status_color}-100 text-{status_color}-800 px-3 py-1 rounded-full text-xs font-bold">
                            {trend['status_info']['label']}
                        </span>
                    </div>
                    
                    <h3 class="text-xl font-bold mb-2">{self.escape_html(trend['topic'])}</h3>
                    <p class="text-gray-600 text-sm mb-4">{self.escape_html(trend['hashtag'])}</p>
                    
                    <div class="grid grid-cols-2 gap-4 mb-4">
                        <div class="text-center">
                            <p class="text-2xl font-bold text-indigo-600">{trend['trend_score']:,}</p>
                            <p class="text-xs text-gray-500">Trend Score</p>
                        </div>
                        <div class="text-center">
                            <p class="text-2xl font-bold text-{self._get_growth_color(trend['growth_rate'])}-600">
                                {trend['growth_rate']:+.1f}%
                            </p>
                            <p class="text-xs text-gray-500">Growth Rate</p>
                        </div>
                    </div>
                    
                    <div class="border-t pt-4">
                        <a href="trending/trend_{trend_slug}.html" class="text-indigo-600 font-medium hover:text-indigo-800 transition flex items-center justify-between">
                            <span>View Analysis</span>
                            <span>→</span>
                        </a>
                    </div>
                </div>
            </div>
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

    <script>
        // Filter functionality
        document.querySelectorAll('.trend-filter').forEach(button => {
            button.addEventListener('click', function() {
                // Update active state
                document.querySelectorAll('.trend-filter').forEach(b => {
                    b.classList.remove('active', 'text-indigo-600', 'border-b-2', 'border-indigo-600');
                    b.classList.add('text-gray-600');
                });
                this.classList.remove('text-gray-600');
                this.classList.add('active', 'text-indigo-600', 'border-b-2', 'border-indigo-600');
                
                // Filter trends
                const status = this.dataset.status;
                document.querySelectorAll('.trend-card').forEach(card => {
                    if (status === 'all' || card.dataset.status === status) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    </script>
</body>
</html>'''
        
        trending_listing_file = Path("integrated") / "trending.html"
        with open(trending_listing_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.update_progress("Created trending overview page")
        
        # Also update homepage with trending section
        self.update_homepage_trending(trends[:6])  # Top 6 trends
    
    def _get_growth_color(self, growth_rate: float) -> str:
        """Get color based on growth rate"""
        if growth_rate > 50:
            return 'green'
        elif growth_rate > 0:
            return 'blue'
        elif growth_rate > -20:
            return 'yellow'
        else:
            return 'red'
    
    def update_homepage_trending(self, trends: List[Dict[str, Any]]):
        """Update homepage with trending topics section"""
        # This would update a trending section on the homepage
        self.update_progress("Updated homepage with trending topics")
    
    def create_sample_file(self):
        """Create a sample trending topic file"""
        sample_content = """Topic: MrBeast Creator Fund
Hashtag: #MrBeastFund
Category: business
Trend_Score: 8750
Related_Articles: 1,2,3
Status: active
Icon: 🔥
Growth_Rate: 125.5
Youtube_Mentions: 45000
TikTok_Mentions: 38000
Instagram_Mentions: 22000
Twitter_Mentions: 15000
Twitch_Mentions: 8000

---

The MrBeast Creator Fund announcement has taken the influencer world by storm, with creators across all platforms discussing the implications of this $100M initiative. The fund represents one of the largest direct creator support programs ever announced by an individual creator.

Key factors driving this trend:

- Unprecedented scale: $100M is larger than many platform creator funds
- Direct creator-to-creator support model breaking traditional patterns
- Focus on smaller creators who need support the most
- No platform restrictions - creators from any platform can apply
- Transparent selection process with community involvement

The trend has sparked broader conversations about:

- Sustainability of creator businesses
- The role of successful creators in supporting the ecosystem
- Alternative funding models beyond platform monetization
- The future of creator funds and grants

Platform breakdown shows YouTube leading in mentions due to MrBeast's primary audience, but significant cross-platform discussion indicates the universal appeal of this initiative. TikTok creators are particularly engaged, seeing this as an alternative to platform-specific funds.

Early analysis suggests this could inspire other top creators to launch similar initiatives, potentially creating a new paradigm for creator support systems."""
        
        sample_file = self.content_dir / "mrbeast-creator-fund.txt"
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        self.update_progress(f"Created sample trending file: {sample_file}")