#!/usr/bin/env python3
"""
Influencer News - Advanced Integration Manager
=============================================
Complete desktop application for managing content integration with selective removal capabilities
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import datetime
import webbrowser
import os
import sys
import json
from pathlib import Path

# Add integrators to path
sys.path.append(str(Path(__file__).parent / "src"))

from integrators import (
    ArticleIntegrator,
    AuthorIntegrator,
    CategoryIntegrator,
    TrendingIntegrator
)
from integrators.unintegrator import ContentUnintegrator


class AdvancedIntegrationManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Influencer News - Advanced Integration Manager")
        self.root.geometry("1500x1000")
        
        # Configure colors
        self.colors = {
            'bg': '#f8fafc',
            'card': '#ffffff',
            'primary': '#667eea',
            'primary_dark': '#5a67d8',
            'success': '#48bb78',
            'success_dark': '#38a169',
            'warning': '#ed8936',
            'warning_dark': '#dd7114',
            'danger': '#e53e3e',
            'danger_dark': '#c53030',
            'text': '#2d3748',
            'text_light': '#718096',
            'border': '#e2e8f0',
            'accent': '#9f7aea'
        }
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom progressbar style
        self.style.configure(
            'Custom.Horizontal.TProgressbar',
            troughcolor=self.colors['border'],
            background=self.colors['primary'],
            lightcolor=self.colors['primary'],
            darkcolor=self.colors['primary_dark'],
            borderwidth=0,
            relief='flat'
        )
        
        # Initialize integrators
        self.integrators = {
            'articles': ArticleIntegrator(),
            'authors': AuthorIntegrator(),
            'categories': CategoryIntegrator(),
            'trending': TrendingIntegrator()
        }
        
        # Initialize unintegrator
        self.unintegrator = ContentUnintegrator()
        
        # Set progress callbacks
        for name, integrator in self.integrators.items():
            integrator.set_progress_callback(self.update_progress)
        self.unintegrator.set_progress_callback(self.update_progress)
        
        # Status tracking
        self.status = {
            'articles': {'status': '⏳', 'count': 0, 'last_run': 'Never'},
            'authors': {'status': '⏳', 'count': 0, 'last_run': 'Never'},
            'categories': {'status': '⏳', 'count': 0, 'last_run': 'Never'},
            'trending': {'status': '⏳', 'count': 0, 'last_run': 'Never'}
        }
        
        # Progress bars
        self.progress_bars = {}
        
        # Create GUI
        self.create_gui()
        
        # Load initial stats
        self.load_stats()
        
    def create_gui(self):
        """Create the main GUI layout"""
        # Main container with notebook for tabs
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title header with gradient background
        title_frame = tk.Frame(main_frame, bg=self.colors['primary'], relief=tk.FLAT, bd=0)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Inner title container
        title_inner = tk.Frame(title_frame, bg=self.colors['primary'])
        title_inner.pack(fill=tk.X, padx=20, pady=20)
        
        title_label = tk.Label(
            title_inner, 
            text="📰 Advanced Integration Manager",
            font=('Segoe UI', 28, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            title_inner,
            text="Complete content management for your news website",
            font=('Segoe UI', 12),
            bg=self.colors['primary'],
            fg='white'
        )
        subtitle_label.pack(side=tk.LEFT, padx=(20, 0), pady=(8, 0))
        
        # Button container
        btn_container = tk.Frame(title_inner, bg=self.colors['primary'])
        btn_container.pack(side=tk.RIGHT)
        
        # Help button
        help_btn = tk.Button(
            btn_container,
            text="❓ Help",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['primary'],
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.show_help,
            activebackground='#f0f0f0'
        )
        help_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Force sync button
        sync_btn = tk.Button(
            btn_container,
            text="🔄 Force Site Sync",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['warning'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.force_site_sync,
            activebackground=self.colors['warning_dark']
        )
        sync_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Integration tab
        self.create_integration_tab()
        
        # Management tab
        self.create_management_tab()
        
        # Browser tab
        self.create_browser_tab()
        
        # Selective Integration tab
        self.create_selective_integration_tab()
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Status label
        self.status_label = tk.Label(
            footer_frame,
            text="Ready",
            font=('Arial', 10),
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        )
        self.status_label.pack(side=tk.RIGHT)
        
    def create_integration_tab(self):
        """Create the integration tab"""
        integration_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(integration_frame, text="Integration")
        
        # Dashboard grid
        dashboard_frame = tk.Frame(integration_frame, bg=self.colors['bg'])
        dashboard_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create cards for each content type
        self.create_dashboard_cards(dashboard_frame)
        
        # Log panel
        log_frame = tk.LabelFrame(
            integration_frame,
            text="Integration Log",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=2
        )
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            height=10,
            font=('Consolas', 10),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Action buttons
        action_frame = tk.Frame(integration_frame, bg=self.colors['bg'])
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Run All button
        run_all_btn = tk.Button(
            action_frame,
            text="🚀 Run All Integrations",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            padx=35,
            pady=12,
            cursor='hand2',
            command=self.run_all_integrations,
            activebackground=self.colors['success_dark']
        )
        run_all_btn.pack(side=tk.LEFT)
        
        # Open Website button
        open_site_btn = tk.Button(
            action_frame,
            text="🌐 Open Website",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            relief=tk.FLAT,
            padx=35,
            pady=12,
            cursor='hand2',
            command=self.open_website,
            activebackground='#8b5a9f'
        )
        open_site_btn.pack(side=tk.LEFT, padx=(20, 0))
        
    def create_management_tab(self):
        """Create the content management tab"""
        management_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(management_frame, text="Content Management")
        
        # Content summary
        summary_frame = tk.LabelFrame(
            management_frame,
            text="Content Summary",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.summary_text = tk.Text(
            summary_frame,
            height=8,
            font=('Consolas', 10),
            bg=self.colors['card'],
            fg=self.colors['text'],
            state=tk.DISABLED
        )
        self.summary_text.pack(fill=tk.X, padx=10, pady=10)
        
        # Management actions
        actions_frame = tk.LabelFrame(
            management_frame,
            text="Content Actions",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Action buttons grid
        btn_frame = tk.Frame(actions_frame, bg=self.colors['bg'])
        btn_frame.pack(padx=10, pady=10)
        
        # Refresh summary button
        refresh_btn = tk.Button(
            btn_frame,
            text="🔄 Refresh Summary",
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.refresh_summary
        )
        refresh_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Remove by ID button
        remove_id_btn = tk.Button(
            btn_frame,
            text="🗑️ Remove by ID",
            font=('Arial', 12),
            bg=self.colors['warning'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.remove_by_id
        )
        remove_id_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Remove by filename button
        remove_file_btn = tk.Button(
            btn_frame,
            text="📄 Remove by Filename",
            font=('Arial', 12),
            bg=self.colors['warning'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.remove_by_filename
        )
        remove_file_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Clean orphaned files button
        clean_btn = tk.Button(
            btn_frame,
            text="🧹 Clean Orphaned Files",
            font=('Arial', 12),
            bg=self.colors['warning'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.clean_orphaned
        )
        clean_btn.grid(row=1, column=0, padx=5, pady=5)
        
        # Remove all content button
        remove_all_btn = tk.Button(
            btn_frame,
            text="🚨 Remove All Content",
            font=('Arial', 12),
            bg=self.colors['danger'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.remove_all_content
        )
        remove_all_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # Load initial summary
        self.refresh_summary()
        
    def create_browser_tab(self):
        """Create the content browser tab for selective removal"""
        browser_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(browser_frame, text="Content Browser")
        
        # Top controls
        controls_frame = tk.Frame(browser_frame, bg=self.colors['bg'])
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Content type selector
        tk.Label(
            controls_frame,
            text="Content Type:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.content_type_var = tk.StringVar(value="articles")
        content_type_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.content_type_var,
            values=["articles", "authors", "categories", "trending"],
            state="readonly",
            font=('Arial', 12),
            width=15
        )
        content_type_combo.pack(side=tk.LEFT, padx=(0, 20))
        content_type_combo.bind('<<ComboboxSelected>>', self.refresh_browser)
        
        # Refresh button
        refresh_browser_btn = tk.Button(
            controls_frame,
            text="🔄 Refresh",
            font=('Arial', 12),
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.refresh_browser
        )
        refresh_browser_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Select all / none buttons
        select_all_btn = tk.Button(
            controls_frame,
            text="Select All",
            font=('Arial', 10),
            bg=self.colors['text_light'],
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.select_all_items
        )
        select_all_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        select_none_btn = tk.Button(
            controls_frame,
            text="Select None",
            font=('Arial', 10),
            bg=self.colors['text_light'],
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.select_no_items
        )
        select_none_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Remove selected button
        remove_selected_btn = tk.Button(
            controls_frame,
            text="🗑️ Remove Selected",
            font=('Arial', 12, 'bold'),
            bg=self.colors['danger'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.remove_selected_items
        )
        remove_selected_btn.pack(side=tk.RIGHT)
        
        # Content list frame
        list_frame = tk.LabelFrame(
            browser_frame,
            text="Content Items",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for content items
        columns = ('ID', 'Name', 'Filename', 'Date')
        self.content_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='tree headings',
            height=20
        )
        
        # Configure columns
        self.content_tree.heading('#0', text='Selected')
        self.content_tree.column('#0', width=80, minwidth=80)
        
        for col in columns:
            self.content_tree.heading(col, text=col)
            if col == 'ID':
                self.content_tree.column(col, width=60, minwidth=60)
            elif col == 'Name':
                self.content_tree.column(col, width=300, minwidth=200)
            elif col == 'Filename':
                self.content_tree.column(col, width=200, minwidth=150)
            elif col == 'Date':
                self.content_tree.column(col, width=150, minwidth=120)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.content_tree.yview)
        self.content_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack treeview and scrollbar
        self.content_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10, padx=(0, 10))
        
        # Bind events
        self.content_tree.bind('<Button-1>', self.on_tree_click)
        
        # Initialize browser
        self.refresh_browser()
        
    def create_selective_integration_tab(self):
        """Create the selective integration tab for choosing specific files to integrate"""
        integration_browser_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(integration_browser_frame, text="Selective Integration")
        
        # Top controls
        controls_frame = tk.Frame(integration_browser_frame, bg=self.colors['bg'])
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Content type selector
        tk.Label(
            controls_frame,
            text="Content Type:",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.integration_content_type_var = tk.StringVar(value="articles")
        integration_content_type_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.integration_content_type_var,
            values=["articles", "authors", "categories", "trending"],
            state="readonly",
            font=('Segoe UI', 12),
            width=15
        )
        integration_content_type_combo.pack(side=tk.LEFT, padx=(0, 20))
        integration_content_type_combo.bind('<<ComboboxSelected>>', self.refresh_integration_browser)
        
        # Refresh button
        refresh_integration_btn = tk.Button(
            controls_frame,
            text="🔄 Refresh",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.refresh_integration_browser,
            activebackground=self.colors['primary_dark']
        )
        refresh_integration_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Select all / none buttons
        select_all_integration_btn = tk.Button(
            controls_frame,
            text="Select All",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['text_light'],
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.select_all_integration_items,
            activebackground='#5a6b7c'
        )
        select_all_integration_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        select_none_integration_btn = tk.Button(
            controls_frame,
            text="Select None",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['text_light'],
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.select_no_integration_items,
            activebackground='#5a6b7c'
        )
        select_none_integration_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Integrate selected button
        integrate_selected_btn = tk.Button(
            controls_frame,
            text="⚡ Integrate Selected",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.integrate_selected_items,
            activebackground=self.colors['success_dark']
        )
        integrate_selected_btn.pack(side=tk.RIGHT)
        
        # Content list frame
        integration_list_frame = tk.LabelFrame(
            integration_browser_frame,
            text="Available Content Files",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        integration_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for content files
        integration_columns = ('Filename', 'Status', 'Modified')
        self.integration_tree = ttk.Treeview(
            integration_list_frame,
            columns=integration_columns,
            show='tree headings',
            height=20
        )
        
        # Configure columns
        self.integration_tree.heading('#0', text='Selected')
        self.integration_tree.column('#0', width=100, minwidth=100)
        
        for col in integration_columns:
            self.integration_tree.heading(col, text=col)
            if col == 'Filename':
                self.integration_tree.column(col, width=300, minwidth=200)
            elif col == 'Status':
                self.integration_tree.column(col, width=150, minwidth=120)
            elif col == 'Modified':
                self.integration_tree.column(col, width=200, minwidth=150)
        
        # Add scrollbar
        integration_tree_scroll = ttk.Scrollbar(integration_list_frame, orient=tk.VERTICAL, command=self.integration_tree.yview)
        self.integration_tree.configure(yscrollcommand=integration_tree_scroll.set)
        
        # Pack treeview and scrollbar
        self.integration_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        integration_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10, padx=(0, 10))
        
        # Bind events
        self.integration_tree.bind('<Button-1>', self.on_integration_tree_click)
        
        # Initialize browser
        self.refresh_integration_browser()
    
    def refresh_integration_browser(self, event=None):
        """Refresh the integration browser with available content files"""
        content_type = self.integration_content_type_var.get()
        
        # Clear existing items
        for item in self.integration_tree.get_children():
            self.integration_tree.delete(item)
        
        # Get content directory
        content_dir = Path("content") / content_type
        if not content_dir.exists():
            return
        
        # Get currently integrated files
        db_file = Path("data") / f"{content_type}_db.json"
        integrated_files = set()
        if db_file.exists():
            try:
                with open(db_file, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                integrated_files = {item.get('filename', '') for item in db.get(content_type, [])}
            except:
                pass
        
        # List all .txt files in content directory
        import os
        for file_path in content_dir.glob("*.txt"):
            filename = file_path.name
            
            # Determine status
            if filename in integrated_files:
                status = "✅ Already Integrated"
                text_icon = "☐"  # Don't allow selection of already integrated files
            else:
                status = "🔄 Not Integrated"
                text_icon = "☐"
            
            # Get modification time
            try:
                mod_time = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                mod_time_str = mod_time.strftime('%Y-%m-%d %H:%M')
            except:
                mod_time_str = 'Unknown'
            
            # Insert item
            item_id = self.integration_tree.insert(
                '',
                'end',
                text=text_icon,
                values=(filename, status, mod_time_str),
                tags=('unchecked' if status.startswith('🔄') else 'disabled',)
            )
    
    def on_integration_tree_click(self, event):
        """Handle integration tree item click to toggle selection"""
        region = self.integration_tree.identify_region(event.x, event.y)
        if region == "tree":
            item = self.integration_tree.identify_row(event.y)
            if item:
                # Only allow selection of non-integrated items
                values = self.integration_tree.item(item, 'values')
                if len(values) > 1 and values[1].startswith('🔄'):  # Not integrated
                    current_text = self.integration_tree.item(item, 'text')
                    if current_text == '☐':
                        self.integration_tree.item(item, text='☑', tags=('checked',))
                    else:
                        self.integration_tree.item(item, text='☐', tags=('unchecked',))
    
    def select_all_integration_items(self):
        """Select all non-integrated items"""
        for item in self.integration_tree.get_children():
            values = self.integration_tree.item(item, 'values')
            if len(values) > 1 and values[1].startswith('🔄'):  # Not integrated
                self.integration_tree.item(item, text='☑', tags=('checked',))
    
    def select_no_integration_items(self):
        """Deselect all integration items"""
        for item in self.integration_tree.get_children():
            values = self.integration_tree.item(item, 'values')
            if len(values) > 1 and values[1].startswith('🔄'):  # Not integrated
                self.integration_tree.item(item, text='☐', tags=('unchecked',))
    
    def integrate_selected_items(self):
        """Integrate selected files"""
        selected_files = []
        
        for item in self.integration_tree.get_children():
            if self.integration_tree.item(item, 'text') == '☑':
                values = self.integration_tree.item(item, 'values')
                if len(values) > 0:
                    selected_files.append(values[0])  # filename
        
        if not selected_files:
            messagebox.showwarning("No Selection", "Please select files to integrate.")
            return
        
        content_type = self.integration_content_type_var.get()
        
        # Confirm integration
        if messagebox.askyesno(
            "Confirm Integration", 
            f"Are you sure you want to integrate {len(selected_files)} {content_type} files?"
        ):
            self._integrate_files(content_type, selected_files)
    
    def _integrate_files(self, content_type, filenames):
        """Integrate specific files"""
        def integrate():
            try:
                integrator = self.integrators[content_type]
                content_dir = Path("content") / content_type
                
                success_count = 0
                total_files = len(filenames)
                
                for i, filename in enumerate(filenames):
                    file_path = content_dir / filename
                    if file_path.exists():
                        try:
                            # Process this specific file
                            content_data = integrator.parse_content_file(file_path)
                            if content_data:
                                integrator._process_content_item(content_data, filename)
                                success_count += 1
                                
                            progress = ((i + 1) / total_files) * 100
                            self.update_progress(
                                content_type.upper(), 
                                f"Integrated {filename} ({i+1}/{total_files})", 
                                progress
                            )
                        except Exception as e:
                            self.update_progress(
                                content_type.upper(), 
                                f"Error integrating {filename}: {str(e)}"
                            )
                
                # Update listing pages and stats
                integrator.load_content_db()
                content_items = integrator.content_db.get(content_type, [])
                integrator.update_listing_page(content_items)
                
                if content_type == 'articles':
                    integrator.update_search_page(content_items)
                
                self.load_stats()
                self.refresh_summary()
                self.refresh_browser()
                self.refresh_integration_browser()
                
                messagebox.showinfo(
                    "Integration Complete", 
                    f"Successfully integrated {success_count} of {total_files} {content_type} files."
                )
                
            except Exception as e:
                messagebox.showerror("Integration Error", f"Error during integration: {str(e)}")
        
        # Run in thread
        thread = threading.Thread(target=integrate)
        thread.daemon = True
        thread.start()
        
    def create_dashboard_cards(self, parent):
        """Create dashboard cards for each content type"""
        cards_data = [
            ('articles', 'Articles', '📄', 'Manage news articles'),
            ('authors', 'Authors', '✍️', 'Manage author profiles'),
            ('categories', 'Categories', '📁', 'Manage content categories'),
            ('trending', 'Trending', '🔥', 'Manage trending topics')
        ]
        
        # Create 2x2 grid
        for i, (key, title, icon, desc) in enumerate(cards_data):
            row = i // 2
            col = i % 2
            
            card = self.create_card(parent, key, title, icon, desc)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
        # Configure grid weights
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
    def create_card(self, parent, key, title, icon, description):
        """Create a single dashboard card"""
        card = tk.Frame(parent, bg=self.colors['card'], relief=tk.FLAT, bd=2, highlightbackground=self.colors['border'], highlightthickness=1)
        
        # Card content
        content_frame = tk.Frame(card, bg=self.colors['card'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Header
        header_frame = tk.Frame(content_frame, bg=self.colors['card'])
        header_frame.pack(fill=tk.X)
        
        # Icon and title
        title_label = tk.Label(
            header_frame,
            text=f"{icon} {title}",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        title_label.pack(side=tk.LEFT)
        
        # Status indicator
        status_label = tk.Label(
            header_frame,
            text=self.status[key]['status'],
            font=('Segoe UI', 28),
            bg=self.colors['card']
        )
        status_label.pack(side=tk.RIGHT)
        self.status[key]['label'] = status_label
        
        # Description
        desc_label = tk.Label(
            content_frame,
            text=description,
            font=('Segoe UI', 11),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        )
        desc_label.pack(anchor=tk.W, pady=(8, 15))
        
        # Stats
        stats_frame = tk.Frame(content_frame, bg=self.colors['card'])
        stats_frame.pack(fill=tk.X)
        
        count_label = tk.Label(
            stats_frame,
            text=f"📄 Files: {self.status[key]['count']}",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        count_label.pack(side=tk.LEFT)
        self.status[key]['count_label'] = count_label
        
        last_run_label = tk.Label(
            stats_frame,
            text=f"🕒 Last run: {self.status[key]['last_run']}",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        )
        last_run_label.pack(side=tk.RIGHT)
        self.status[key]['last_run_label'] = last_run_label
        
        # Progress bar with custom styling
        progress_frame = tk.Frame(content_frame, bg=self.colors['card'])
        progress_frame.pack(fill=tk.X, pady=(15, 15))
        
        progress = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=250,
            style='Custom.Horizontal.TProgressbar'
        )
        progress.pack(fill=tk.X)
        self.progress_bars[key] = progress
        
        # Action buttons frame
        btn_frame = tk.Frame(content_frame, bg=self.colors['card'])
        btn_frame.pack(pady=(10, 0))
        
        # Setup/Integrate button
        if not Path(self.integrators[key].content_dir).exists():
            btn_text = "📂 Setup"
            btn_command = lambda k=key: self.setup_content_type(k)
        else:
            btn_text = "▶️ Integrate"
            btn_command = lambda k=key: self.run_integration(k)
            
        action_btn = tk.Button(
            btn_frame,
            text=btn_text,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor='hand2',
            command=btn_command,
            activebackground=self.colors['primary_dark']
        )
        action_btn.pack(side=tk.LEFT, padx=(0, 8))
        self.status[key]['button'] = action_btn
        
        # Remove all button for this type
        remove_btn = tk.Button(
            btn_frame,
            text="🗑️ Remove All",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['danger'],
            fg='white',
            relief=tk.FLAT,
            padx=12,
            pady=8,
            cursor='hand2',
            command=lambda k=key: self.remove_all_type(k),
            activebackground=self.colors['danger_dark']
        )
        remove_btn.pack(side=tk.LEFT)
        
        return card
        
    def load_stats(self):
        """Load statistics for all content types"""
        for key, integrator in self.integrators.items():
            stats = integrator.get_stats()
            self.status[key]['count'] = stats['total_count']
            self.status[key]['count_label'].config(text=f"Files: {stats['total_count']}")
            
            if stats['last_integration']:
                last_run = self.format_datetime(stats['last_integration'])
                self.status[key]['last_run'] = last_run
                self.status[key]['last_run_label'].config(text=f"Last run: {last_run}")
                
            # Update status
            if stats['total_count'] > 0:
                self.status[key]['status'] = '✅'
                self.status[key]['label'].config(text='✅')
            else:
                self.status[key]['status'] = '❌'
                self.status[key]['label'].config(text='❌')
                
    def format_datetime(self, iso_string):
        """Format ISO datetime string to readable format"""
        try:
            dt = datetime.datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return iso_string
            
    def update_progress(self, content_type, message, progress=None):
        """Update progress for a content type"""
        # Update log
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {content_type.upper()}: {message}\n")
        self.log_text.see(tk.END)
        
        # Update progress bar
        if progress is not None and content_type in self.progress_bars:
            self.progress_bars[content_type]['value'] = progress
            
        # Update GUI
        self.root.update()
        
    def run_integration(self, content_type):
        """Run integration for a specific content type"""
        def run():
            try:
                # Update status
                self.status[content_type]['status'] = '⏳'
                self.status[content_type]['label'].config(text='⏳')
                self.status[content_type]['button'].config(state=tk.DISABLED)
                
                # Run integration
                integrator = self.integrators[content_type]
                count = integrator.process_new_content()
                
                # Update stats
                self.load_stats()
                
                # Show completion message
                if count > 0:
                    messagebox.showinfo("Success", f"Successfully integrated {count} new {content_type}!")
                else:
                    messagebox.showinfo("Info", f"No new {content_type} to process.")
                    
            except Exception as e:
                self.status[content_type]['status'] = '❌'
                self.status[content_type]['label'].config(text='❌')
                messagebox.showerror("Error", f"Error processing {content_type}: {str(e)}")
                
            finally:
                self.status[content_type]['button'].config(state=tk.NORMAL)
                self.progress_bars[content_type]['value'] = 0
                
        # Run in thread
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        
    def run_all_integrations(self):
        """Run all integrations"""
        def run():
            for content_type in self.integrators:
                self.run_integration(content_type)
                # Wait for completion
                while self.status[content_type]['button']['state'] == tk.DISABLED:
                    self.root.update()
                    
        # Run in thread
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        
    def setup_content_type(self, content_type):
        """Setup a content type by creating directory and sample file"""
        try:
            integrator = self.integrators[content_type]
            integrator.content_dir.mkdir(parents=True, exist_ok=True)
            integrator.create_sample_file()
            
            # Update button
            self.status[content_type]['button'].config(
                text="▶️ Integrate",
                command=lambda: self.run_integration(content_type)
            )
            
            messagebox.showinfo("Success", f"Created {content_type} directory with sample file!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error setting up {content_type}: {str(e)}")
    
    def refresh_summary(self):
        """Refresh the content summary"""
        summary = self.unintegrator.get_content_summary()
        
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        
        summary_text = "Content Summary\n" + "="*50 + "\n\n"
        
        for content_type, data in summary.items():
            summary_text += f"{content_type.upper()}:\n"
            summary_text += f"  Total: {data['count']} items\n"
            summary_text += f"  Last Integration: {data['last_integration']}\n"
            
            if data['items']:
                summary_text += "  Items:\n"
                for item in data['items'][:5]:  # Show first 5
                    summary_text += f"    - ID {item['id']}: {item['name']} ({item['filename']})\n"
                if len(data['items']) > 5:
                    summary_text += f"    ... and {len(data['items']) - 5} more\n"
            summary_text += "\n"
        
        self.summary_text.insert(tk.END, summary_text)
        self.summary_text.config(state=tk.DISABLED)
    
    def refresh_browser(self, event=None):
        """Refresh the content browser"""
        content_type = self.content_type_var.get()
        
        # Clear existing items
        for item in self.content_tree.get_children():
            self.content_tree.delete(item)
        
        # Get content summary
        summary = self.unintegrator.get_content_summary()
        
        if content_type in summary and summary[content_type]['items']:
            for item in summary[content_type]['items']:
                # Format date
                try:
                    date_str = self.format_datetime(item.get('date', 'Unknown'))
                except:
                    date_str = 'Unknown'
                
                # Insert item with checkbox
                item_id = self.content_tree.insert(
                    '',
                    'end',
                    text='☐',
                    values=(
                        item['id'],
                        item['name'][:50] + '...' if len(item['name']) > 50 else item['name'],
                        item['filename'],
                        date_str
                    ),
                    tags=('unchecked',)
                )
        
    def on_tree_click(self, event):
        """Handle tree item click to toggle selection"""
        region = self.content_tree.identify_region(event.x, event.y)
        if region == "tree":
            item = self.content_tree.identify_row(event.y)
            if item:
                # Toggle selection
                current_text = self.content_tree.item(item, 'text')
                if current_text == '☐':
                    self.content_tree.item(item, text='☑', tags=('checked',))
                else:
                    self.content_tree.item(item, text='☐', tags=('unchecked',))
    
    def select_all_items(self):
        """Select all items in the browser"""
        for item in self.content_tree.get_children():
            self.content_tree.item(item, text='☑', tags=('checked',))
    
    def select_no_items(self):
        """Deselect all items in the browser"""
        for item in self.content_tree.get_children():
            self.content_tree.item(item, text='☐', tags=('unchecked',))
    
    def remove_selected_items(self):
        """Remove selected items from the browser"""
        selected_items = []
        
        for item in self.content_tree.get_children():
            if self.content_tree.item(item, 'text') == '☑':
                values = self.content_tree.item(item, 'values')
                selected_items.append({
                    'id': int(values[0]),
                    'name': values[1],
                    'filename': values[2]
                })
        
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select items to remove.")
            return
        
        content_type = self.content_type_var.get()
        
        # Confirm removal
        if messagebox.askyesno(
            "Confirm Removal", 
            f"Are you sure you want to remove {len(selected_items)} {content_type} items?"
        ):
            success_count = 0
            
            for item in selected_items:
                if self.unintegrator.remove_content_by_id(content_type, item['id']):
                    success_count += 1
            
            if success_count > 0:
                self.refresh_summary()
                self.refresh_browser()
                self.load_stats()
                messagebox.showinfo("Success", f"Removed {success_count} {content_type} items.")
    
    def remove_by_id(self):
        """Remove content by ID"""
        content_type = simpledialog.askstring("Remove by ID", "Enter content type (articles/authors/categories/trending):")
        if not content_type or content_type not in ['articles', 'authors', 'categories', 'trending']:
            return
            
        content_id = simpledialog.askinteger("Remove by ID", f"Enter {content_type} ID to remove:")
        if content_id is None:
            return
            
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove {content_type} ID {content_id}?"):
            success = self.unintegrator.remove_content_by_id(content_type, content_id)
            if success:
                self.refresh_summary()
                self.refresh_browser()
                self.load_stats()
                messagebox.showinfo("Success", f"Removed {content_type} ID {content_id}")
    
    def remove_by_filename(self):
        """Remove content by filename"""
        content_type = simpledialog.askstring("Remove by Filename", "Enter content type (articles/authors/categories/trending):")
        if not content_type or content_type not in ['articles', 'authors', 'categories', 'trending']:
            return
            
        filename = simpledialog.askstring("Remove by Filename", f"Enter {content_type} filename to remove:")
        if not filename:
            return
            
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove {content_type} with filename {filename}?"):
            success = self.unintegrator.remove_content_by_filename(content_type, filename)
            if success:
                self.refresh_summary()
                self.refresh_browser()
                self.load_stats()
                messagebox.showinfo("Success", f"Removed {content_type} with filename {filename}")
    
    def clean_orphaned(self):
        """Clean orphaned files"""
        if messagebox.askyesno("Confirm Cleanup", "This will remove files that don't have database entries. Continue?"):
            total_removed = 0
            for content_type in ['articles', 'authors', 'categories', 'trending']:
                removed = self.unintegrator.clean_orphaned_files(content_type)
                total_removed += removed
                
            messagebox.showinfo("Cleanup Complete", f"Removed {total_removed} orphaned files")
            self.refresh_summary()
            self.refresh_browser()
    
    def remove_all_type(self, content_type):
        """Remove all content of a specific type"""
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove ALL {content_type}? This cannot be undone!"):
            success = self.unintegrator.remove_all_content(content_type)
            if success:
                self.refresh_summary()
                self.refresh_browser()
                self.load_stats()
                messagebox.showinfo("Success", f"Removed all {content_type}")
    
    def remove_all_content(self):
        """Remove all content from all types"""
        if messagebox.askyesno("Confirm Removal", "Are you sure you want to remove ALL content? This cannot be undone!"):
            if messagebox.askyesno("Double Confirm", "This will delete everything. Are you absolutely sure?"):
                for content_type in ['articles', 'authors', 'categories', 'trending']:
                    self.unintegrator.remove_all_content(content_type)
                    
                self.refresh_summary()
                self.refresh_browser()
                self.load_stats()
                messagebox.showinfo("Success", "Removed all content")
    
    def force_site_sync(self):
        """Force site sync with database state"""
        def sync():
            try:
                self.update_progress("SYSTEM", "🔄 Force syncing site with database state...")
                
                for name, integrator in self.integrators.items():
                    self.update_progress("SYSTEM", f"📊 Syncing {name}...")
                    
                    # Load current database state
                    integrator.load_content_db()
                    content_items = integrator.content_db.get(integrator.content_type, [])
                    
                    self.update_progress("SYSTEM", f"  📄 Database contains: {len(content_items)} items")
                    
                    # Force update listing pages with current database content
                    integrator.update_listing_page(content_items)
                    
                    # For articles, also update search page
                    if name == 'articles':
                        if hasattr(integrator, 'update_search_page'):
                            integrator.update_search_page(content_items)
                            self.update_progress("SYSTEM", f"  🔍 Updated search page for {name}")
                    
                    self.update_progress("SYSTEM", f"  ✅ Site pages updated for {name}")
                
                self.update_progress("SYSTEM", "✅ Site successfully synced with database state!")
                self.load_stats()
                self.refresh_summary()
                self.refresh_browser()
                if hasattr(self, 'integration_tree'):
                    self.refresh_integration_browser()
                messagebox.showinfo("Sync Complete", "Site has been synchronized with database state.")
                
            except Exception as e:
                self.update_progress("SYSTEM", f"❌ Error syncing site: {str(e)}")
                messagebox.showerror("Sync Error", f"Error syncing site: {str(e)}")
        
        # Run in thread
        thread = threading.Thread(target=sync)
        thread.daemon = True
        thread.start()
            
    def open_website(self):
        """Open the website in default browser"""
        webbrowser.open('index.html')
        
    def show_help(self):
        """Show help dialog"""
        help_text = """Advanced Integration Manager

This tool provides complete content management for your static news website.

INTEGRATION TAB:
- Use 'Setup' to create directories and sample files
- Use 'Integrate' to process new content files
- Use 'Run All Integrations' to process everything at once
- Use 'Force Site Sync' to align site with database state

CONTENT MANAGEMENT TAB:
- View summary of all integrated content
- Remove content by ID or filename
- Clean up orphaned files
- Remove all content of a specific type

CONTENT BROWSER TAB:
- Browse all content by type
- Select individual items for removal
- Visual interface for selective content management

SELECTIVE INTEGRATION TAB:
- Browse content files in content/ directories
- See which files are already integrated vs. not integrated
- Select specific files to integrate individually
- Skip files you don't want to process yet

FILE STRUCTURE:
- content/articles/ - Source article .txt files
- content/authors/ - Source author .txt files  
- content/categories/ - Source category .txt files
- content/trending/ - Source trending .txt files
- integrated/articles/ - Generated article pages
- integrated/authors/ - Generated author pages
- integrated/categories/ - Generated category pages
- integrated/trending/ - Generated trending pages
- data/ - JSON databases

SAFETY FEATURES:
- Confirmation dialogs for destructive operations
- Database tracking prevents duplicate processing
- Orphaned file cleanup maintains data integrity
- Force sync ensures site reflects database state

For detailed file formats, see INTEGRATION_GUIDE.md"""
        
        messagebox.showinfo("Help", help_text)


def main():
    """Main function"""
    root = tk.Tk()
    app = AdvancedIntegrationManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()