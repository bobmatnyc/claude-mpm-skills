# WordPress Testing & Quality Assurance Skill

**Version:** 1.0.0  
**Last Updated:** January 30, 2025  
**Skill Level:** Intermediate  
**Estimated Time:** 8-12 hours

## Overview

Comprehensive guide to WordPress plugin and theme testing using PHPUnit integration tests, WP_Mock unit tests, PHPCS coding standards enforcement, and GitHub Actions CI/CD pipelines.

## What You'll Learn

- **Testing Strategy**: WordPress testing pyramid (60% unit, 30% integration, 10% E2E)
- **PHPUnit Integration**: WordPress test suite with factory objects and fixtures
- **WP_Mock Unit Testing**: Isolated testing without loading WordPress
- **PHPCS Standards**: Enforcing WordPress Coding Standards
- **CI/CD Pipelines**: Automated testing with GitHub Actions
- **Coverage Requirements**: Achieving 80%+ code coverage
- **Common Patterns**: Testing CPTs, hooks, AJAX, REST API endpoints

## Quick Start

### 1. PHPUnit Setup
```bash
composer require --dev phpunit/phpunit "^9.6"
wp scaffold plugin-tests my-plugin
bash bin/install-wp-tests.sh wordpress_test root '' localhost latest
vendor/bin/phpunit
```

### 2. WP_Mock Unit Tests
```bash
composer require --dev 10up/wp_mock "^1.0"
vendor/bin/phpunit -c phpunit-wp-mock.xml.dist
```

### 3. PHPCS Standards
```bash
composer require --dev wp-coding-standards/wpcs:"^3.0"
vendor/bin/phpcs
vendor/bin/phpcbf  # Auto-fix issues
```

## Key Features

### Testing Tools
- **PHPUnit 9.6+**: WordPress integration testing
- **WP_Mock 1.0+**: Fast unit tests without WordPress
- **PHPCS 3.7+**: Coding standards enforcement
- **WPCS 3.0+**: WordPress-specific rules
- **GitHub Actions**: Automated CI/CD pipelines

### Testing Pyramid
```
       /\
      /E2E\      10% - Browser automation
     /------\
    /INTEGR \    30% - WordPress + database
   /----------\
  /UNIT TESTS \  60% - Pure logic, WP_Mock
```

### Coverage Goals
- **New Code**: 80% minimum
- **Critical Paths**: 95% (auth, payments, validation)
- **Legacy Code**: Gradual improvement
- **Public APIs**: 100% coverage

## Progressive Disclosure

**Entry Point** (~78 tokens):
- Quick summary and when to use
- Three quick start commands

**Full Content** (~5,200 tokens):
1. Testing Strategy (600 tokens)
2. PHPUnit Integration (1,200 tokens)
3. WP_Mock Unit Testing (1,000 tokens)
4. PHPCS & Standards (900 tokens)
5. GitHub Actions CI/CD (800 tokens)
6. Testing Best Practices (500 tokens)
7. Common Testing Patterns (500 tokens)

## File Structure

```
testing-qa/
├── SKILL.md           # Main skill content
├── metadata.json      # Skill metadata
└── README.md          # This file
```

## Requirements

- **WordPress**: 6.4+
- **PHP**: 8.1+ (8.3 recommended)
- **Composer**: Latest version
- **Docker**: For wp-env (optional)

## Related Skills

Related skills available in the skill library:
- **WordPress Plugin Fundamentals**: Core plugin architecture and hooks
- **WordPress Security & Validation**: Security patterns and data validation
- **WordPress Block Editor**: Modern block development and testing
- **Python pytest Testing**: Testing patterns applicable to WordPress
- **GitHub Actions**: CI/CD automation for WordPress testing pipelines

## Testing Workflow Example

```bash
# 1. Install dependencies
composer install

# 2. Run coding standards check
composer phpcs

# 3. Auto-fix PHPCS issues
composer phpcbf

# 4. Run unit tests (WP_Mock)
vendor/bin/phpunit -c phpunit-wp-mock.xml.dist

# 5. Run integration tests (PHPUnit + WordPress)
vendor/bin/phpunit

# 6. Generate coverage report
vendor/bin/phpunit --coverage-html coverage/
```

## GitHub Actions Example

```yaml
name: CI Pipeline

on: [push, pull_request]

jobs:
  phpcs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
      - run: composer install
      - run: vendor/bin/phpcs

  phpunit:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        php: ['8.1', '8.3']
        wordpress: ['6.5', 'latest']
    steps:
      - uses: actions/checkout@v4
      - run: composer install
      - run: bash bin/install-wp-tests.sh wordpress_test root root localhost ${{ matrix.wordpress }}
      - run: vendor/bin/phpunit --coverage-clover=coverage.xml
```

## Common Patterns Covered

### Custom Post Types
- Registration testing
- Supports features verification
- REST API enablement
- Meta data handling

### Hooks and Filters
- Action registration testing
- Filter callback verification
- Priority testing
- Custom hook creation

### AJAX Handlers
- Request simulation
- Response validation
- Nonce verification
- Authentication testing

### REST API Endpoints
- Route registration
- Permission callbacks
- Data validation
- Response format testing

## Best Practices

1. **Test Pyramid**: 60% unit, 30% integration, 10% E2E
2. **Isolation**: Use WP_Mock for pure logic
3. **Coverage**: 80% minimum for new code
4. **Naming**: Descriptive test names (test_method_scenario_result)
5. **AAA Pattern**: Arrange-Act-Assert structure
6. **Data Providers**: Test multiple scenarios efficiently
7. **CI/CD**: Automate testing on every push
8. **Matrix Testing**: Test across PHP/WP versions

## Token Budget Compliance

- **Entry Point**: 78 tokens (Target: 70-85) ✅
- **Full Content**: ~5,200 tokens (Target: 5,000-5,500) ✅
- **Expansion Ratio**: 66.7x

## Documentation

- [WordPress PHPUnit Handbook](https://make.wordpress.org/core/handbook/testing/automated-testing/)
- [WP_Mock GitHub](https://github.com/10up/wp_mock)
- [WordPress Coding Standards](https://github.com/WordPress/WordPress-Coding-Standards)
- [PHPUnit Documentation](https://phpunit.de/documentation.html)

## License

This skill is part of the claude-mpm-skills library and follows the same licensing as the parent project.

---

**Maintained by**: claude-mpm-skills  
**Research Date**: January 30, 2025  
**WordPress Version**: 6.7+  
**PHP Version**: 8.3 (recommended)
