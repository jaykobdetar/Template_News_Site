#!/usr/bin/env python3
"""
Site Sync Tool
==============
Simple, reliable tool to sync the website with the current database state.
Run this whenever content appears out of sync.
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from integrators.article_integrator import ArticleIntegrator
from integrators.author_integrator import AuthorIntegrator
from integrators.category_integrator import CategoryIntegrator
from integrators.trending_integrator import TrendingIntegrator

class SiteSyncer:
    """Simple site synchronization tool"""
    
    def __init__(self):
        self.integrators = {
            'articles': ArticleIntegrator(),
            'authors': AuthorIntegrator(), 
            'categories': CategoryIntegrator(),
            'trending': TrendingIntegrator()
        }
    
    def sync_all(self):
        """Sync all content types with their databases"""
        print("🔄 Starting site synchronization...")
        print("=" * 60)
        
        total_synced = 0
        
        for name, integrator in self.integrators.items():
            print(f"\n📊 Syncing {name.upper()}...")
            
            try:
                # Load current database state
                integrator.load_content_db()
                content_items = integrator.content_db.get(integrator.content_type, [])
                
                print(f"  📄 Database contains: {len(content_items)} items")
                
                # Update listing pages to match database
                integrator.update_listing_page(content_items)
                
                # For articles, also update search page
                if name == 'articles':
                    integrator.update_search_page(content_items)
                    print(f"  🔍 Search page updated")
                
                print(f"  ✅ {name.capitalize()} pages synchronized")
                total_synced += 1
                
            except Exception as e:
                print(f"  ❌ Error syncing {name}: {str(e)}")
        
        print("\n" + "=" * 60)
        if total_synced == len(self.integrators):
            print("✅ ALL CONTENT TYPES SUCCESSFULLY SYNCHRONIZED!")
        else:
            print(f"⚠️  {total_synced}/{len(self.integrators)} content types synchronized")
        
        print("\nSynchronization Summary:")
        print("-" * 30)
        
        for name, integrator in self.integrators.items():
            try:
                integrator.load_content_db()
                count = len(integrator.content_db.get(integrator.content_type, []))
                status = "✅" if count > 0 else "🔲"
                print(f"{status} {name.capitalize()}: {count} items")
            except:
                print(f"❌ {name.capitalize()}: Error reading database")
        
        print(f"\n🌐 Website is now synchronized with database state!")
        print("📝 You can now refresh your browser to see the changes.")

    def check_status(self):
        """Check current status of all content types"""
        print("📊 Current Content Status:")
        print("=" * 50)
        
        for name, integrator in self.integrators.items():
            try:
                integrator.load_content_db()
                content_items = integrator.content_db.get(integrator.content_type, [])
                count = len(content_items)
                
                if count > 0:
                    print(f"✅ {name.capitalize()}: {count} items")
                    # Show first few items
                    for i, item in enumerate(content_items[:3]):
                        if name == 'articles':
                            title = item.get('title', 'Unknown Title')
                        elif name == 'authors':
                            title = item.get('name', 'Unknown Name')
                        elif name == 'categories':
                            title = item.get('name', 'Unknown Category')
                        elif name == 'trending':
                            title = item.get('topic', 'Unknown Topic')
                        
                        print(f"    {i+1}. {title}")
                    
                    if count > 3:
                        print(f"    ... and {count - 3} more")
                else:
                    print(f"🔲 {name.capitalize()}: No items")
                    
            except Exception as e:
                print(f"❌ {name.capitalize()}: Error reading database - {str(e)}")
        
        print("\n💡 Run 'python3 sync_site.py sync' to synchronize website with this state.")

def main():
    """Main function"""
    syncer = SiteSyncer()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        syncer.check_status()
    else:
        syncer.sync_all()

if __name__ == "__main__":
    main()