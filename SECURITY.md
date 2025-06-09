# Security Policy

## Supported Versions

We actively support the following versions of Influencer News CMS:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in Influencer News CMS, please report it responsibly:

### How to Report

1. **Email**: Send details to security@infnews.com (if available)
2. **GitHub**: Use the private vulnerability reporting feature
3. **Direct Contact**: Contact maintainers directly through GitHub

### What to Include

Please include the following information in your report:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and severity assessment
- **Reproduction**: Step-by-step instructions to reproduce
- **Environment**: System information (OS, Python version, etc.)
- **Proposed Fix**: If you have suggestions for fixing the issue

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Fix Development**: Varies based on complexity
- **Patch Release**: As soon as possible after fix is ready

## Security Considerations

### Application Security

**File System Access**
- The application requires read/write access to local directories
- All file operations are limited to the project directory structure
- No external network requests are made by default (except for image URLs in content)

**Content Processing**
- Content files are processed locally without external validation
- HTML generation uses escaping to prevent XSS
- No user input is executed as code

**GUI Security**
- tkinter interface runs with user permissions only
- No elevated privileges required
- No sensitive data stored in application

### Data Security

**Local Storage**
- All data stored locally in JSON format
- No encryption of local files (content is assumed to be public)
- Database files are human-readable and editable

**Content URLs**
- External image URLs in content files are user-provided
- No validation of external URL safety
- Users responsible for content source verification

### Best Practices for Users

**File Permissions**
```bash
# Recommended permissions for project directory
chmod 755 InfNews/
chmod 644 InfNews/*.html
chmod 644 InfNews/content/**/*.txt
chmod 644 InfNews/data/*.json
```

**Content Validation**
- Verify image URLs are from trusted sources
- Review content files before integration
- Regularly backup important content and data

**Environment Security**
- Run application in isolated environment if processing untrusted content
- Keep Python installation updated
- Use virtual environments for development

## Known Security Limitations

### By Design
1. **No Authentication**: Desktop application assumes trusted local user
2. **Local File Access**: Requires write permissions to project directory
3. **External Content**: Image URLs and content are not validated for safety
4. **HTML Generation**: Generated content may include user-provided HTML

### Mitigation Strategies
- **Content Review**: Always review generated HTML before publication
- **URL Verification**: Verify external image URLs are safe and appropriate
- **Access Control**: Limit file system permissions appropriately
- **Backup Strategy**: Regular backups prevent data loss from corruption

## Security Updates

Security updates will be:
- Released as patch versions (e.g., 1.0.1)
- Documented in CHANGELOG.md with security notes
- Announced through GitHub releases
- Tagged with security labels

## Scope of Security Support

### In Scope
- Application code vulnerabilities
- File processing security issues
- HTML generation problems that could lead to XSS
- Database corruption or integrity issues

### Out of Scope
- Third-party image hosting security
- User-provided content appropriateness
- Operating system or Python runtime vulnerabilities
- Network security for generated websites

## Development Security

### Code Review
- All code changes reviewed for security implications
- Automated scanning for common vulnerability patterns
- Regular dependency updates (when dependencies are added)

### Testing
- Security testing included in development process
- File permission and access testing
- Input validation and sanitization testing

## Responsible Disclosure

We appreciate security researchers who:
- Report vulnerabilities privately before public disclosure
- Provide clear reproduction steps and impact assessment
- Allow reasonable time for fixes before public disclosure
- Work with us to verify fixes before disclosure

## Contact

For security-related questions or concerns:
- Security issues: Use GitHub's private vulnerability reporting
- General questions: Create a GitHub issue with the "security" label
- Direct contact: Reach out to project maintainers

## Acknowledgments

We thank the security research community for helping keep Influencer News CMS secure through responsible disclosure practices.