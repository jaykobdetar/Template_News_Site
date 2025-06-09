#!/usr/bin/env python3
"""
Base Integrator Class
====================
Shared functionality for all content integrators
"""

import os
import json
import datetime
import html
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from abc import ABC, abstractmethod


class BaseIntegrator(ABC):
    """Base class for all content integrators"""
    
    def __init__(self, content_type: str, content_dir: str, db_filename: str):
        self.content_type = content_type
        self.content_dir = Path("content") / content_dir
        self.content_dir.mkdir(parents=True, exist_ok=True)
        
        # Integrated output directory for generated content
        self.integrated_dir = Path("integrated") / content_dir
        self.integrated_dir.mkdir(parents=True, exist_ok=True)
        
        # Database file for storing processed content
        Path("data").mkdir(exist_ok=True)
        self.db_file = Path("data") / db_filename
        self.content_db = self.load_content_db()
        
        # Progress callback for GUI updates
        self.progress_callback: Optional[Callable] = None
        
        # Common category colors
        self.category_colors = {
            'business': 'green',
            'entertainment': 'orange', 
            'tech': 'blue',
            'technology': 'blue',
            'fashion': 'pink',
            'charity': 'purple',
            'beauty': 'pink',
            'lifestyle': 'indigo',
            'sports': 'red',
            'gaming': 'purple',
            'food': 'yellow',
            'travel': 'teal'
        }
        
    def load_content_db(self) -> Dict:
        """Load existing content database"""
        if self.db_file.exists():
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {self.content_type: [], 'next_id': 1, 'last_integration': None}
    
    def save_content_db(self):
        """Save content database"""
        self.content_db['last_integration'] = datetime.datetime.now().isoformat()
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.content_db, f, indent=2, ensure_ascii=False)
    
    def set_progress_callback(self, callback: Callable):
        """Set callback for progress updates"""
        self.progress_callback = callback
    
    def update_progress(self, message: str, progress: float = None):
        """Update progress via callback if set"""
        if self.progress_callback:
            self.progress_callback(self.content_type, message, progress)
    
    @abstractmethod
    def parse_content_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a content file - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def create_content_page(self, content: Dict[str, Any]):
        """Create individual content page - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def update_listing_page(self, content_list: List[Dict[str, Any]]):
        """Update the main listing page - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def create_sample_file(self):
        """Create a sample file for reference - must be implemented by subclasses"""
        pass
    
    def validate_required_fields(self, content: Dict[str, Any], required_fields: List[str], file_path: Path):
        """Validate that all required fields are present"""
        missing_fields = [field for field in required_fields if field not in content or not content[field]]
        if missing_fields:
            raise ValueError(f"Missing required fields in {file_path}: {', '.join(missing_fields)}")
    
    def format_date_relative(self, date_str: str) -> str:
        """Format date as relative time"""
        try:
            if isinstance(date_str, datetime.datetime):
                date_obj = date_str
            else:
                date_obj = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            
            now = datetime.datetime.now()
            if date_obj.tzinfo:
                now = now.replace(tzinfo=date_obj.tzinfo)
                
            diff = now - date_obj
            
            if diff.days > 365:
                years = diff.days // 365
                return f"{years} year{'s' if years > 1 else ''} ago"
            elif diff.days > 30:
                months = diff.days // 30
                return f"{months} month{'s' if months > 1 else ''} ago"
            elif diff.days > 0:
                return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            else:
                minutes = max(1, diff.seconds // 60)
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        except:
            return "Recently"
    
    def parse_metadata_section(self, metadata_text: str) -> Dict[str, str]:
        """Parse metadata section with key: value pairs"""
        metadata = {}
        for line in metadata_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().lower().replace(' ', '_')] = value.strip()
        return metadata
    
    def escape_html(self, text: str) -> str:
        """Escape HTML characters"""
        return html.escape(text)
    
    def escape_js_string(self, text: str) -> str:
        """Escape string for JavaScript"""
        return html.escape(text).replace('"', '\\"').replace('\n', '\\n').replace('\r', '')
    
    def get_category_color(self, category: str) -> str:
        """Get color for category"""
        return self.category_colors.get(category.lower(), 'gray')
    
    def process_new_content(self) -> int:
        """Process all new content files"""
        self.update_progress("Starting content processing...", 0)
        processed_count = 0
        
        # Get list of existing content files
        existing_files = {item.get('filename', '') for item in self.content_db[self.content_type]}
        
        # Get all .txt files in content directory
        txt_files = list(self.content_dir.glob("*.txt"))
        total_files = len(txt_files)
        
        if total_files == 0:
            self.update_progress("No content files found. Creating sample...", 100)
            self.create_sample_file()
            return 0
        
        # Process each .txt file
        for idx, file_path in enumerate(txt_files):
            progress = (idx / total_files) * 100
            
            if file_path.name in existing_files:
                self.update_progress(f"Skipping already processed: {file_path.name}", progress)
                continue
            
            try:
                self.update_progress(f"Processing: {file_path.name}", progress)
                content = self.parse_content_file(file_path)
                content['filename'] = file_path.name
                content['id'] = self.content_db['next_id']
                
                # Add to database
                self.content_db[self.content_type].append(content)
                self.content_db['next_id'] += 1
                
                # Create individual page
                self.create_content_page(content)
                
                processed_count += 1
                self.update_progress(f"Successfully processed: {content.get('name', content.get('title', 'Unknown'))}", progress)
                
            except Exception as e:
                self.update_progress(f"Error processing {file_path.name}: {str(e)}", progress)
                continue
        
        if processed_count > 0:
            # Sort content by date/priority
            self.sort_content()
            
            # Update listing page
            self.update_listing_page(self.content_db[self.content_type])
            
            # Update search functionality
            self.update_search_integration()
            
            # Save database
            self.save_content_db()
            
            self.update_progress(f"Successfully integrated {processed_count} new {self.content_type}!", 100)
        else:
            self.update_progress(f"No new {self.content_type} to process.", 100)
        
        return processed_count
    
    def sort_content(self):
        """Sort content by date or priority - can be overridden by subclasses"""
        if 'date' in self.content_db[self.content_type][0] if self.content_db[self.content_type] else {}:
            self.content_db[self.content_type].sort(
                key=lambda x: x.get('date', ''), 
                reverse=True
            )
        elif 'sort_order' in self.content_db[self.content_type][0] if self.content_db[self.content_type] else {}:
            self.content_db[self.content_type].sort(
                key=lambda x: x.get('sort_order', 999)
            )
    
    def update_search_integration(self):
        """Update search.html with new content - override if needed"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about integrated content"""
        return {
            'total_count': len(self.content_db[self.content_type]),
            'last_integration': self.content_db.get('last_integration', 'Never'),
            'next_id': self.content_db['next_id']
        }
    
    def clean_old_pages(self):
        """Remove pages for content that no longer exists"""
        # This can be implemented if needed
        pass