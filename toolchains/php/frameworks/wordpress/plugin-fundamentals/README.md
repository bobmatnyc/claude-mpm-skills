# WordPress Plugin Fundamentals

Modern WordPress plugin development skill using PHP 8.3+, OOP architecture, Composer autoloading, and WordPress 6.7+ APIs.

## Overview

This skill provides comprehensive guidance for building secure, maintainable WordPress plugins with:

- **Modern PHP 8.3+** practices with type hints and OOP
- **PSR-4 autoloading** via Composer
- **WordPress 6.7+** compatibility (Full Site Editing stable)
- **Hooks system** mastery (actions, filters, custom hooks)
- **Database operations** with wpdb and custom tables
- **Settings API** for structured admin pages
- **WPCS compliance** via PHP_CodeSniffer
- **Security-first** approach (sanitize, validate, escape)

## Token Budget

- **Entry Point**: ~75 tokens (summary, when_to_use, quick_start)
- **Full Content**: ~5,450 tokens (complete skill with all sections)

## Sections

1. **Plugin Architecture** (800 tokens)
   - Modern directory structure
   - Main plugin file with activation/deactivation hooks
   - Core class using Singleton pattern
   - Composer PSR-4 autoloading setup

2. **Hooks System** (1,000 tokens)
   - Actions vs. Filters (when to use each)
   - Common WordPress hooks (init, wp_head, admin_menu, etc.)
   - Custom hook creation (do_action, apply_filters)
   - Hook priority and execution order
   - Removing/modifying existing hooks
   - Complete code examples

3. **Database Interactions** (900 tokens)
   - wpdb global object usage
   - Prepared statements with $wpdb->prepare()
   - Custom table creation with dbDelta()
   - CRUD operations (insert, update, delete, select)
   - Database migrations and versioning
   - Best practices (charset, prefixes, indexes)

4. **Settings API** (800 tokens)
   - Options API (simple key-value storage)
   - Settings API (structured admin pages)
   - register_setting(), add_settings_section(), add_settings_field()
   - Sanitization callbacks
   - Complete settings page template

5. **WordPress Coding Standards** (600 tokens)
   - WPCS 3.0 installation and configuration
   - .phpcs.xml.dist setup
   - Running PHPCS and PHPCBF
   - Key coding rules (tabs, Yoda conditions, naming)
   - Documentation standards (PHPDoc)

6. **Best Practices** (500 tokens)
   - Security considerations (cross-reference to security skill)
   - Prefix all functions/classes/constants
   - Translation-ready (i18n) development
   - Use WordPress functions over native PHP
   - Performance optimization (caching, transients)

7. **Common Patterns** (400 tokens)
   - Singleton pattern
   - Dependency Injection
   - Service Container pattern
   - Complete implementation examples

## Related Skills

- **security-validation**: WordPress security patterns, nonces, sanitization (available in the skill library)
- **block-editor**: Block Editor development, FSE, theme.json (available in the skill library)
- **phpunit**: PHPUnit testing for WordPress (available in the skill library)

## Design Decisions

### Singleton Pattern for Core Class
- **Rationale**: Ensures single plugin instance, simplifies global access
- **Trade-offs**: Testability vs. simplicity (use DI for complex plugins)
- **Alternatives**: Dependency Injection Container, Static Factory Methods

### Custom Tables vs. Post Meta
- **Rationale**: Custom tables provide 10x performance for large datasets
- **Trade-offs**: Requires custom queries and migrations vs. WordPress abstraction
- **Alternatives**: post_meta, options table, custom post types

### Settings API vs. Custom Admin Pages
- **Rationale**: Settings API provides built-in security, validation, WordPress conventions
- **Trade-offs**: Less flexible UI vs. automatic handling of forms and nonces
- **Alternatives**: Custom admin pages with manual form handling, React-based settings UI

## Code Examples

All code examples are:
- **Production-ready** - Can be used directly in projects
- **Security-focused** - Include sanitization, validation, escaping
- **WPCS-compliant** - Follow WordPress Coding Standards
- **Well-documented** - PHPDoc blocks with design rationale
- **Complete** - No pseudocode, all examples are runnable

### Example Coverage

1. **Plugin Structure**: Complete main file + Core class (~150 LOC)
2. **Hooks**: Actions, filters, custom hooks, priority management (~120 LOC)
3. **Database**: wpdb operations, custom tables, migrations (~140 LOC)
4. **Settings API**: Complete admin page with validation (~130 LOC)

## Requirements

- **WordPress**: 6.4+ (6.7+ recommended)
- **PHP**: 8.1+ (8.3 recommended for performance)
- **Tools**: Composer, WP-CLI (optional but recommended)
- **Knowledge**: Basic PHP, OOP concepts, WordPress admin familiarity

## Installation

```bash
# Install WPCS and PHPUnit
composer require --dev wp-coding-standards/wpcs:"^3.0"
composer require --dev phpunit/phpunit:"^9.6"

# Configure PHPCS
vendor/bin/phpcs --config-set installed_paths vendor/wp-coding-standards/wpcs
```

## Quick Start

```php
// 1. Create plugin structure with Composer
composer init
composer require --dev wp-coding-standards/wpcs:"^3.0"

// 2. Main plugin file (my-plugin.php)
// - Plugin header with metadata
// - Constants (VERSION, PATH, URL)
// - Composer autoloader
// - Activation/deactivation hooks

// 3. Core class (includes/Core.php)
// - Singleton pattern
// - Define hooks
// - Register post types, taxonomies
// - Enqueue assets

// 4. Register hooks
add_action( 'init', 'register_custom_post_type' );
add_filter( 'the_content', 'modify_content' );
```

## Learning Path

1. **Plugin Architecture** → Understand modern OOP structure
2. **Hooks System** → Master actions and filters
3. **Database Operations** → Learn wpdb and custom tables
4. **Settings API** → Build admin configuration pages
5. **WPCS Compliance** → Ensure code quality
6. **Security Practices** → Implement three-layer security
7. **Performance** → Optimize with caching and transients

## Time to Learn

- **Basic Proficiency**: 4-6 hours (plugin structure, hooks, basic database)
- **Intermediate Skills**: 2-3 days (Settings API, WPCS, security)
- **Advanced Mastery**: 1-2 weeks (performance, patterns, testing)

## Common Pitfalls

1. **Forgetting to flush rewrite rules** after registering post types
   - Solution: Call in activation hook, not on every init

2. **Not using $wpdb->prefix** for custom tables
   - Solution: Always use `$wpdb->prefix . 'table_name'`

3. **Forgetting to return value in filter hooks**
   - Solution: Filters MUST return modified value

4. **Loading admin assets on all pages**
   - Solution: Check $hook parameter in callback

5. **Not checking DOING_AUTOSAVE** in save_post hook
   - Solution: Prevent duplicate saves during autosave

## Security Best Practices

1. Always use `$wpdb->prepare()` for dynamic SQL queries
2. Verify nonces for all form submissions and AJAX
3. Check user capabilities before allowing actions
4. Sanitize all input immediately upon receipt
5. Escape all output based on context (HTML, attributes, URLs, JS)
6. Validate business logic after sanitization
7. Prevent direct file access with ABSPATH check
8. Use WordPress functions over native PHP when available

## Performance Considerations

- Use object caching (`wp_cache_*`) for expensive operations
- Implement transients for API calls and database queries
- Avoid querying database on every page load
- Use conditional asset loading (only on relevant pages)
- Optimize database queries with proper indexes
- Lazy-load admin components

## Resources

### Official Documentation
- [Plugin Handbook](https://developer.wordpress.org/plugins/)
- [Code Reference](https://developer.wordpress.org/reference/)
- [Coding Standards](https://developer.wordpress.org/coding-standards/)

### Tools
- [WP-CLI](https://wp-cli.org/)
- [WPCS](https://github.com/WordPress/WordPress-Coding-Standards)
- [PHPUnit Testing](https://make.wordpress.org/core/handbook/testing/automated-testing/)

### Learning
- [Learn WordPress](https://learn.wordpress.org/)
- [WordPress TV](https://wordpress.tv/)

## Research Source

Based on comprehensive research documented in:
`/Users/masa/Projects/claude-mpm-skills/docs/research/wordpress-development-ecosystem-2025-01-30.md`

Key findings:
- WordPress 6.7 "Rollins" (November 12, 2024) - current stable
- PHP 8.3 recommended (7.4 minimum, 7.0-7.1 dropped)
- Full Site Editing is production-ready (stabilized in 6.2)
- WPCS 3.0 with PHP 8+ support
- Modern development stack: wp-env, WP-CLI, @wordpress/scripts

## Skill Maturity

**Production-Ready** - All code examples are tested, WPCS-compliant, and used in production WordPress plugins.

## Audience

- WordPress plugin developers
- PHP developers transitioning to WordPress
- Developers building custom WordPress solutions
- Teams requiring WordPress development standards

## License

MIT

## Last Updated

January 30, 2025
