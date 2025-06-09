# Contributing to Influencer News CMS

Thank you for your interest in contributing to the Influencer News Content Management System! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

**Before creating an issue:**
- Check if the issue already exists in [GitHub Issues](https://github.com/yourusername/InfNews/issues)
- Search closed issues to see if it was already resolved
- Ensure you're using the latest version

**When creating an issue:**
- Use a clear, descriptive title
- Provide detailed steps to reproduce the problem
- Include system information (OS, Python version)
- Add screenshots for GUI-related issues
- Include relevant log output

### Suggesting Features

We welcome feature suggestions! Please:
- Check existing issues and discussions first
- Provide a clear use case for the feature
- Explain how it would benefit users
- Consider implementation complexity

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/InfNews.git
   cd InfNews
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

4. **Test thoroughly**
   - Run the integration manager GUI
   - Test all content types
   - Verify generated HTML output
   - Check cross-linking functionality

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Coding Standards

### Python Code Style

- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type hints for function parameters and returns
- **Docstrings**: Document all classes and methods
- **Error Handling**: Include appropriate try/catch blocks
- **Logging**: Use the progress callback system for user feedback

**Example:**
```python
def parse_content_file(self, file_path: Path) -> Dict[str, Any]:
    """Parse a content file and extract metadata.
    
    Args:
        file_path: Path to the content file
        
    Returns:
        Dictionary containing parsed content data
        
    Raises:
        ValueError: If file format is invalid
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        # Implementation...
    except Exception as e:
        self.update_progress(f"Error reading {file_path}: {str(e)}")
        raise
```

### GUI Development

- **Consistent Styling**: Use the established color scheme
- **Responsive Layout**: Ensure UI works on different screen sizes
- **User Feedback**: Provide clear progress indicators and error messages
- **Accessibility**: Use readable fonts and sufficient color contrast

### HTML Generation

- **Valid HTML5**: Generate clean, semantic HTML
- **Responsive Design**: Use Tailwind CSS classes appropriately
- **SEO-Friendly**: Include proper meta tags and structure
- **Cross-Browser**: Test in multiple browsers

## 🏗️ Project Architecture

### Core Components

1. **Base Integrator** (`src/integrators/base_integrator.py`)
   - Shared functionality for all content types
   - Database management
   - Progress tracking
   - HTML generation utilities

2. **Content Integrators**
   - `article_integrator.py` - News articles
   - `author_integrator.py` - Author profiles
   - `category_integrator.py` - Content categories
   - `trending_integrator.py` - Trending topics

3. **GUI Components**
   - `integration_manager.py` - Main application
   - Tab-based interface with status cards
   - Real-time progress tracking

4. **Utilities**
   - `sync_site.py` - Site synchronization
   - `unintegrator.py` - Content removal

### Adding New Content Types

To add a new content type:

1. **Create Integrator Class**
   ```python
   class NewTypeIntegrator(BaseIntegrator):
       def __init__(self):
           super().__init__('newtype', 'newtypes', 'newtypes_db.json')
       
       def parse_content_file(self, file_path: Path) -> Dict[str, Any]:
           # Implementation
           pass
       
       def create_content_page(self, content: Dict[str, Any]):
           # Implementation
           pass
       
       def update_listing_page(self, content_list: List[Dict[str, Any]]):
           # Implementation
           pass
   ```

2. **Update Integration Manager**
   - Add to integrators dictionary
   - Create dashboard card
   - Add to GUI tabs

3. **Update Documentation**
   - Add format guide
   - Update quick start
   - Include in README

## 🧪 Testing

### Manual Testing Checklist

**Basic Functionality:**
- [ ] GUI launches without errors
- [ ] Setup creates sample files correctly
- [ ] Individual integration works for each content type
- [ ] Batch integration processes all content
- [ ] Generated HTML is valid and styled correctly

**Content Management:**
- [ ] Content browser shows all items
- [ ] Selective removal works
- [ ] Orphaned file cleanup functions
- [ ] Database consistency maintained

**Cross-Linking:**
- [ ] Articles link to correct author pages
- [ ] Categories show related articles
- [ ] Navigation between pages works
- [ ] Search functionality operates correctly

**Error Handling:**
- [ ] Invalid file formats show clear errors
- [ ] Missing required fields are reported
- [ ] File permission issues handled gracefully
- [ ] Database corruption recovery works

### Test Content

Create test files in each content directory to verify functionality:

```bash
# Test articles with various authors and categories
# Test authors with different specializations
# Test categories with different colors and icons
# Test trending topics with various metrics
```

## 📝 Documentation

When contributing, please update relevant documentation:

- **Code Comments**: Explain complex logic
- **Docstrings**: Document all public methods
- **README**: Update if adding major features
- **Format Guides**: Update for new fields or formats
- **Screenshots**: Update if changing UI

## 🐛 Debugging

### Common Issues

**Import Errors:**
```bash
# Ensure Python path includes src directory
export PYTHONPATH="${PYTHONPATH}:./src"
```

**GUI Issues:**
```bash
# Test tkinter installation
python -m tkinter
```

**File Permissions:**
```bash
# Ensure write permissions for output directories
chmod -R 755 integrated/ data/
```

### Debugging Tools

- **GUI Debug Mode**: Add print statements to progress callbacks
- **File Validation**: Use try/catch blocks around file operations
- **Database Inspection**: Check JSON files in `data/` directory
- **HTML Validation**: Use browser developer tools

## 🚀 Release Process

### Version Numbering

We use semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes to file formats or API
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, improvements

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] CHANGELOG.md updated
- [ ] Screenshots current
- [ ] README reflects new features

## 💬 Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code review and collaboration

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers get started
- Focus on the project's goals

## 🎯 Development Priorities

### Current Focus Areas

1. **Performance**: Optimize large file processing
2. **UI/UX**: Improve user experience and visual design
3. **Documentation**: Expand tutorials and examples
4. **Testing**: Add automated testing framework
5. **Features**: Additional content types and integrations

### Future Roadmap

- Web-based content editor
- Real-time preview functionality
- Template customization system
- Multi-language support
- API for external integrations
- Deployment automation

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Acknowledged in release notes
- Credited in documentation for major features

## ❓ Questions?

- Check the [FAQ](FAQ.md)
- Browse [existing issues](https://github.com/yourusername/InfNews/issues)
- Start a [discussion](https://github.com/yourusername/InfNews/discussions)

Thank you for contributing to Influencer News CMS! 🙏