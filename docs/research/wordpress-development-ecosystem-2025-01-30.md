# WordPress Development Ecosystem Research

**Research Date:** January 30, 2025
**Focus:** WordPress 6.x Development Practices & Skills Library Architecture
**Scope:** Plugin Development, Theme Development, Modern Tooling, Testing, Security

---

## Executive Summary

WordPress continues to evolve rapidly with WordPress 6.7 (released November 12, 2024, codenamed "Rollins") representing the current stable release. The ecosystem has shifted significantly toward **Block-based development**, **Full Site Editing (FSE)**, and **modern PHP practices** (PHP 8.3 recommended). Key architectural changes include the maturation of the Block Editor (Gutenberg), theme.json for centralized styling, and enhanced REST API capabilities.

**Critical Version Requirements:**
- **WordPress:** 6.7 (current), 6.4+ recommended for FSE features
- **PHP:** 8.3 recommended (7.4 minimum, PHP 7.0-7.1 support dropped)
- **MySQL:** 5.7+ or MariaDB 10.3+
- **Node.js:** 18.x+ for modern build tooling

**Recommended Skills Library Structure:** 5 distinct skills covering (1) Plugin Fundamentals, (2) Block Editor & FSE, (3) Security & Data Validation, (4) Testing & Quality, and (5) Advanced WordPress Architecture.

---

## 1. Latest WordPress Version & PHP Requirements

### WordPress 6.7 "Rollins" (November 12, 2024)

**Major Features:**
- **Full Site Editing Maturity:** FSE is no longer beta (stabilized in 6.2, refined in 6.4-6.7)
- **Block Bindings API:** Connect block attributes to dynamic data sources
- **Improved Block Interactivity API:** Enhanced client-side interactions without React
- **Performance Improvements:** Faster asset loading, optimized query performance
- **Enhanced Site Editor:** Improved template editing workflow

**PHP Version Support:**

| PHP Version | Status | WordPress 6.7 Support |
|-------------|--------|----------------------|
| 7.0-7.1     | EOL    | ❌ Dropped Support   |
| 7.2-7.4     | EOL    | ✅ Supported (minimum: 7.4) |
| 8.0-8.2     | Security/EOL | ✅ Compatible with exceptions |
| 8.3         | Active | ✅ **Recommended** (best performance) |
| 8.4         | Candidate | ⚠️ Beta support (testing phase) |

**Key Changes in WordPress 6.x Series:**
- **6.0-6.2:** FSE foundation, block locking, template editing
- **6.3-6.4:** Style variations, design tools, pattern improvements
- **6.5-6.6:** Font library, block hooks, interactivity API refinements
- **6.7:** Performance optimizations, block bindings, developer experience improvements

**Official Documentation:**
- PHP Compatibility: https://make.wordpress.org/core/handbook/references/php-compatibility-and-wordpress-versions/
- Server Requirements: https://wordpress.org/about/requirements/

---

## 2. Plugin Development: Modern Architecture & Best Practices

### Modern Plugin Structure (2024-2025)

**Recommended Directory Structure:**
```
my-plugin/
├── my-plugin.php              # Main plugin file (metadata header)
├── composer.json               # Dependency management (REQUIRED)
├── package.json                # npm dependencies (if using build tools)
├── includes/                   # Core business logic (PSR-4 autoloaded)
│   ├── Core.php               # Plugin bootstrap/loader class
│   ├── Admin/                 # Admin-specific functionality
│   ├── Frontend/              # Public-facing functionality
│   └── API/                   # REST API endpoints
├── assets/                     # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
├── blocks/                     # Custom Gutenberg blocks
├── templates/                  # PHP template files
├── languages/                  # Translation files
├── tests/                      # PHPUnit tests
│   ├── unit/
│   ├── integration/
│   └── bootstrap.php
├── .phpcs.xml.dist            # PHP_CodeSniffer config (WPCS)
├── .editorconfig              # Editor configuration
├── .gitignore
└── README.md
```

**Main Plugin File Example:**
```php
<?php
/**
 * Plugin Name: Modern WordPress Plugin
 * Plugin URI: https://example.com/my-plugin
 * Description: Modern plugin following WordPress 6.x best practices
 * Version: 1.0.0
 * Requires at least: 6.4
 * Requires PHP: 8.1
 * Author: Your Name
 * Author URI: https://example.com
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: my-plugin
 * Domain Path: /languages
 */

// Security: Prevent direct access
if ( ! defined( 'ABSPATH' ) ) {
    exit; // Exit if accessed directly
}

// Define plugin constants
define( 'MY_PLUGIN_VERSION', '1.0.0' );
define( 'MY_PLUGIN_PATH', plugin_dir_path( __FILE__ ) );
define( 'MY_PLUGIN_URL', plugin_dir_url( __FILE__ ) );

// Composer autoloader
if ( file_exists( MY_PLUGIN_PATH . 'vendor/autoload.php' ) ) {
    require_once MY_PLUGIN_PATH . 'vendor/autoload.php';
}

// Initialize plugin on plugins_loaded hook
add_action( 'plugins_loaded', 'my_plugin_init' );

function my_plugin_init() {
    // Initialize core plugin class
    if ( class_exists( 'MyPlugin\\Core' ) ) {
        $plugin = new MyPlugin\\Core();
        $plugin->run();
    }
}

// Activation hook
register_activation_hook( __FILE__, 'my_plugin_activate' );
function my_plugin_activate() {
    // Run activation tasks (flush rewrite rules, create tables, set default options)
    if ( class_exists( 'MyPlugin\\Activation' ) ) {
        MyPlugin\\Activation::activate();
    }
}

// Deactivation hook
register_deactivation_hook( __FILE__, 'my_plugin_deactivate' );
function my_plugin_deactivate() {
    // Cleanup tasks (flush rewrite rules, clear scheduled events)
    if ( class_exists( 'MyPlugin\\Deactivation' ) ) {
        MyPlugin\\Deactivation::deactivate();
    }
}
```

**Core Plugin Class (OOP Singleton Pattern):**
```php
<?php
namespace MyPlugin;

class Core {
    private static $instance = null;

    public static function get_instance() {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->load_dependencies();
        $this->define_hooks();
    }

    private function load_dependencies() {
        // Load required classes/files
    }

    private function define_hooks() {
        // Register WordPress hooks
        add_action( 'init', [ $this, 'on_init' ] );
        add_action( 'admin_menu', [ $this, 'register_admin_menu' ] );
        add_action( 'rest_api_init', [ $this, 'register_rest_routes' ] );
    }

    public function run() {
        // Start the plugin execution
    }
}
```

### Plugin API Fundamentals

**1. Actions vs. Filters**

| Aspect | Actions | Filters |
|--------|---------|---------|
| Purpose | Execute code at specific points | Modify data before use/output |
| Return Value | Returns nothing (void) | **Must return value** |
| Example Use | Send emails, log events, register CPTs | Modify post content, filter queries |
| Common Pattern | `do_action()` / `add_action()` | `apply_filters()` / `add_filter()` |

**Action Example:**
```php
// Register custom post type on 'init' action
add_action( 'init', 'register_custom_post_type' );
function register_custom_post_type() {
    register_post_type( 'book', [
        'labels' => [
            'name' => __( 'Books', 'my-plugin' ),
            'singular_name' => __( 'Book', 'my-plugin' ),
        ],
        'public' => true,
        'has_archive' => true,
        'supports' => [ 'title', 'editor', 'thumbnail' ],
        'show_in_rest' => true, // Enable block editor
    ]);
}
```

**Filter Example:**
```php
// Modify post content with custom message
add_filter( 'the_content', 'add_reading_time' );
function add_reading_time( $content ) {
    if ( is_single() && in_the_loop() && is_main_query() ) {
        $word_count = str_word_count( strip_tags( $content ) );
        $reading_time = ceil( $word_count / 200 ); // 200 words/min

        $message = sprintf(
            '<p class="reading-time">Estimated reading time: %d min</p>',
            $reading_time
        );

        $content = $message . $content; // Prepend message
    }

    return $content; // MUST return modified content
}
```

**2. Hook Priority and Execution Order**

```php
// Priority: 1-999 (default: 10)
// Lower numbers = earlier execution, higher numbers = later execution

add_action( 'init', 'my_early_function', 5 );  // Runs first
add_action( 'init', 'my_normal_function' );     // Priority 10 (default)
add_action( 'init', 'my_late_function', 20 );   // Runs last

// Remove hooks
remove_action( 'init', 'my_normal_function', 10 );
remove_filter( 'the_content', 'wpautop' ); // Remove auto-paragraph formatting
```

**3. Creating Custom Hooks**

```php
// In your plugin code - create custom action hook
function my_plugin_process_order( $order_id ) {
    // Process order logic...

    // Allow other plugins/themes to hook into this point
    do_action( 'my_plugin_order_processed', $order_id, $order_data );
}

// Other developers can now hook into your plugin:
add_action( 'my_plugin_order_processed', 'send_order_notification', 10, 2 );
function send_order_notification( $order_id, $order_data ) {
    // Send email notification
}

// Custom filter hook
function my_plugin_get_price( $product_id ) {
    $price = get_post_meta( $product_id, '_price', true );

    // Allow price modification
    return apply_filters( 'my_plugin_product_price', $price, $product_id );
}
```

**Common Core Hooks:**
- **init:** Register post types, taxonomies, rewrite rules
- **plugins_loaded:** Initialize plugin (after all plugins loaded)
- **wp_enqueue_scripts:** Enqueue frontend CSS/JS
- **admin_enqueue_scripts:** Enqueue admin CSS/JS
- **wp_head:** Add code to <head> section
- **wp_footer:** Add code before </body>
- **save_post:** Runs when post is saved/updated
- **pre_get_posts:** Modify WP_Query before execution

### WordPress Coding Standards (WPCS)

**Installation via Composer:**
```bash
composer config allow-plugins.dealerdirect/phpcodesniffer-composer-installer true
composer require --dev wp-coding-standards/wpcs:"^3.0"
composer require --dev phpcompatibility/phpcompatibility-wp:"*"
```

**.phpcs.xml.dist Configuration:**
```xml
<?xml version="1.0"?>
<ruleset name="WordPress Coding Standards">
    <description>Custom ruleset for WordPress plugin</description>

    <!-- Check all PHP files -->
    <file>./includes</file>
    <file>./my-plugin.php</file>

    <!-- Exclude vendor and node_modules -->
    <exclude-pattern>*/vendor/*</exclude-pattern>
    <exclude-pattern>*/node_modules/*</exclude-pattern>

    <!-- Use WordPress-Extra rules -->
    <rule ref="WordPress-Extra">
        <!-- Allow short array syntax -->
        <exclude name="Generic.Arrays.DisallowShortArraySyntax"/>
    </rule>

    <!-- Check for PHP cross-version compatibility -->
    <config name="testVersion" value="8.1-"/>

    <!-- Show progress -->
    <arg value="ps"/>
    <arg name="colors"/>
    <arg name="extensions" value="php"/>
</ruleset>
```

**Key Coding Rules:**
- **Indentation:** Tabs (not spaces)
- **Braces:** Opening brace on same line for control structures
- **Yoda Conditions:** `if ( true === $value )` instead of `if ( $value === true )`
- **Naming:** Snake_case for functions/variables, PascalCase for classes
- **Documentation:** PHPDoc blocks for all functions/classes

**Running PHPCS:**
```bash
# Check coding standards
vendor/bin/phpcs

# Auto-fix fixable issues
vendor/bin/phpcbf

# Check specific file
vendor/bin/phpcs includes/Core.php
```

### Database Interactions

**1. Using $wpdb Global Object:**
```php
global $wpdb;

// Prepare queries to prevent SQL injection
$user_id = 42;
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_author = %d",
        $user_id
    )
);

// Insert data
$wpdb->insert(
    $wpdb->prefix . 'my_custom_table',
    [
        'column1' => 'value1',
        'column2' => 123,
        'created_at' => current_time( 'mysql' ),
    ],
    [ '%s', '%d', '%s' ] // Data format
);

// Update data
$wpdb->update(
    $wpdb->prefix . 'my_custom_table',
    [ 'column1' => 'new_value' ], // Data to update
    [ 'id' => 5 ],                 // WHERE condition
    [ '%s' ],                       // Data format
    [ '%d' ]                        // WHERE format
);

// Delete data
$wpdb->delete(
    $wpdb->prefix . 'my_custom_table',
    [ 'id' => 5 ],
    [ '%d' ]
);
```

**2. Creating Custom Tables:**
```php
function my_plugin_create_tables() {
    global $wpdb;

    $table_name = $wpdb->prefix . 'my_custom_table';
    $charset_collate = $wpdb->get_charset_collate();

    // IMPORTANT: Specific SQL formatting required for dbDelta()
    $sql = "CREATE TABLE $table_name (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        user_id bigint(20) unsigned NOT NULL,
        title varchar(255) NOT NULL,
        content longtext,
        status varchar(20) DEFAULT 'draft',
        created_at datetime DEFAULT CURRENT_TIMESTAMP,
        updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY  (id),
        KEY user_id (user_id),
        KEY status (status)
    ) $charset_collate;";

    // dbDelta() intelligently creates or updates tables
    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );

    // Store database version for future migrations
    add_option( 'my_plugin_db_version', '1.0.0' );
}

// Run on plugin activation
register_activation_hook( __FILE__, 'my_plugin_create_tables' );
```

**Best Practices:**
- ✅ Always use `$wpdb->prepare()` for dynamic queries
- ✅ Use `$wpdb->prefix` (never hard-code `wp_`)
- ✅ Use `$wpdb->get_charset_collate()` for correct character encoding
- ✅ Use `dbDelta()` for table creation/updates (handles schema changes)
- ✅ Store schema version in options table for migrations
- ⚠️ Consider using existing tables (post_meta, options) before creating custom tables

### Settings API and Options Framework

**1. Options API (Simple Key-Value Storage):**
```php
// Add option
add_option( 'my_plugin_setting', 'default_value' );

// Get option
$value = get_option( 'my_plugin_setting', 'default_if_not_exists' );

// Update option
update_option( 'my_plugin_setting', 'new_value' );

// Delete option
delete_option( 'my_plugin_setting' );
```

**2. Settings API (Structured Admin Pages):**
```php
// Register settings on admin_init
add_action( 'admin_init', 'my_plugin_register_settings' );
function my_plugin_register_settings() {
    // Register setting
    register_setting(
        'my_plugin_options',           // Option group
        'my_plugin_settings',           // Option name
        [
            'type' => 'array',
            'sanitize_callback' => 'my_plugin_sanitize_settings',
            'default' => [],
        ]
    );

    // Add settings section
    add_settings_section(
        'my_plugin_main_section',       // Section ID
        __( 'Main Settings', 'my-plugin' ),
        'my_plugin_section_callback',   // Callback for section description
        'my_plugin_settings_page'       // Page slug
    );

    // Add settings field
    add_settings_field(
        'api_key',                      // Field ID
        __( 'API Key', 'my-plugin' ),
        'my_plugin_api_key_callback',   // Callback to render field
        'my_plugin_settings_page',      // Page slug
        'my_plugin_main_section',       // Section ID
        [ 'label_for' => 'api_key' ]    // Extra arguments
    );
}

// Sanitize callback
function my_plugin_sanitize_settings( $input ) {
    $sanitized = [];

    if ( isset( $input['api_key'] ) ) {
        $sanitized['api_key'] = sanitize_text_field( $input['api_key'] );
    }

    return $sanitized;
}

// Field render callback
function my_plugin_api_key_callback( $args ) {
    $options = get_option( 'my_plugin_settings' );
    $value = isset( $options['api_key'] ) ? $options['api_key'] : '';
    ?>
    <input
        type="text"
        id="<?php echo esc_attr( $args['label_for'] ); ?>"
        name="my_plugin_settings[api_key]"
        value="<?php echo esc_attr( $value ); ?>"
        class="regular-text"
    />
    <?php
}

// Settings page template
function my_plugin_settings_page() {
    ?>
    <div class="wrap">
        <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
        <form action="options.php" method="post">
            <?php
            settings_fields( 'my_plugin_options' );
            do_settings_sections( 'my_plugin_settings_page' );
            submit_button();
            ?>
        </form>
    </div>
    <?php
}
```

**Modern Alternatives (2024):**
- **WordPress Settings Framework:** https://github.com/iconicwp/WordPress-Settings-Framework
- **Carbon Fields:** https://carbonfields.net/ (React-based UI)
- **REST API Approach:** Build settings UI with React/Vue, save via REST endpoints

---

## 3. Security Best Practices

### The Three-Layer Security Model

**Golden Rule:** "Sanitize on input, validate for logic, escape on output."

### 1. Nonces (Numbers Used Once)

**Purpose:** Prevent CSRF (Cross-Site Request Forgery) attacks

```php
// Create nonce for form
<form method="post">
    <?php wp_nonce_field( 'my_action', 'my_nonce_field' ); ?>
    <input type="text" name="user_data" />
    <button type="submit">Submit</button>
</form>

// Verify nonce on form submission
function handle_form_submission() {
    // Check if nonce is set and valid
    if ( ! isset( $_POST['my_nonce_field'] ) ||
         ! wp_verify_nonce( $_POST['my_nonce_field'], 'my_action' ) ) {
        wp_die( 'Security check failed' );
    }

    // Process form data
    $user_data = sanitize_text_field( $_POST['user_data'] );
    // ...
}

// Nonce for URLs
$url = wp_nonce_url(
    admin_url( 'admin.php?action=delete_item&id=5' ),
    'delete_item_5',
    'delete_nonce'
);

// Verify URL nonce
if ( ! isset( $_GET['delete_nonce'] ) ||
     ! wp_verify_nonce( $_GET['delete_nonce'], 'delete_item_5' ) ) {
    wp_die( 'Invalid security token' );
}

// Nonce for AJAX
wp_localize_script( 'my-ajax-script', 'myAjax', [
    'ajaxurl' => admin_url( 'admin-ajax.php' ),
    'nonce' => wp_create_nonce( 'my_ajax_nonce' ),
]);

// Verify AJAX nonce
add_action( 'wp_ajax_my_action', 'handle_ajax_request' );
function handle_ajax_request() {
    check_ajax_referer( 'my_ajax_nonce', 'nonce' );

    // Process AJAX request
    wp_send_json_success( [ 'message' => 'Success!' ] );
}
```

### 2. Sanitization (Input Cleaning)

**Purpose:** Remove unwanted/dangerous characters from input

```php
// Text input
$clean_text = sanitize_text_field( $_POST['username'] );

// Email
$clean_email = sanitize_email( $_POST['email'] );

// URL
$clean_url = esc_url_raw( $_POST['website'] );

// Filename
$clean_filename = sanitize_file_name( $_FILES['upload']['name'] );

// HTML content (allows safe HTML tags)
$clean_html = wp_kses_post( $_POST['content'] );

// HTML with custom allowed tags
$allowed_html = [
    'a' => [ 'href' => [], 'title' => [] ],
    'strong' => [],
    'em' => [],
];
$clean_custom_html = wp_kses( $_POST['content'], $allowed_html );

// Integer
$clean_int = absint( $_POST['user_id'] ); // Absolute integer

// Array of text fields
$clean_array = array_map( 'sanitize_text_field', $_POST['items'] );
```

### 3. Validation (Logic Checks)

**Purpose:** Ensure data meets business requirements

```php
function validate_user_registration( $data ) {
    $errors = [];

    // Validate email
    if ( empty( $data['email'] ) || ! is_email( $data['email'] ) ) {
        $errors[] = 'Invalid email address';
    }

    // Validate username length
    if ( strlen( $data['username'] ) < 3 ) {
        $errors[] = 'Username must be at least 3 characters';
    }

    // Validate age (must be integer between 18-100)
    if ( ! is_numeric( $data['age'] ) || $data['age'] < 18 || $data['age'] > 100 ) {
        $errors[] = 'Invalid age';
    }

    // Validate required field
    if ( empty( $data['terms_accepted'] ) ) {
        $errors[] = 'You must accept the terms';
    }

    return empty( $errors ) ? true : $errors;
}
```

### 4. Escaping (Output Protection)

**Purpose:** Prevent XSS (Cross-Site Scripting) attacks

```php
// HTML content
echo esc_html( $user_input ); // Converts < > & " ' to HTML entities

// HTML attributes
<input type="text" value="<?php echo esc_attr( $value ); ?>" />

// URLs
<a href="<?php echo esc_url( $link ); ?>">Link</a>

// JavaScript strings
<script>
    var message = '<?php echo esc_js( $message ); ?>';
</script>

// Textarea content
<textarea><?php echo esc_textarea( $content ); ?></textarea>

// Internationalized text (with HTML allowed)
echo wp_kses_post( __( 'Welcome <strong>user</strong>!', 'my-plugin' ) );

// Internationalized text (no HTML)
echo esc_html__( 'Welcome user!', 'my-plugin' );

// URLs with translation
echo esc_url( __( 'https://example.com/page', 'my-plugin' ) );
```

### 5. Capability Checks (Authorization)

```php
// Check if user is logged in
if ( ! is_user_logged_in() ) {
    wp_die( 'You must be logged in' );
}

// Check user capability
if ( ! current_user_can( 'edit_posts' ) ) {
    wp_die( 'You do not have permission' );
}

// Check capability for specific post
if ( ! current_user_can( 'edit_post', $post_id ) ) {
    wp_die( 'You cannot edit this post' );
}

// Common capabilities:
// - read: Read-only access
// - edit_posts: Create/edit own posts
// - edit_published_posts: Edit published posts
// - delete_posts: Delete posts
// - manage_options: Access settings (admin)
// - upload_files: Upload media
```

**Complete Security Example:**
```php
add_action( 'admin_post_save_custom_data', 'handle_custom_form' );
function handle_custom_form() {
    // 1. Verify nonce
    if ( ! isset( $_POST['custom_nonce'] ) ||
         ! wp_verify_nonce( $_POST['custom_nonce'], 'save_custom_data' ) ) {
        wp_die( 'Security check failed' );
    }

    // 2. Check user capability
    if ( ! current_user_can( 'edit_posts' ) ) {
        wp_die( 'You do not have permission' );
    }

    // 3. Sanitize input
    $title = sanitize_text_field( $_POST['title'] );
    $email = sanitize_email( $_POST['email'] );
    $age = absint( $_POST['age'] );

    // 4. Validate data
    $errors = [];
    if ( empty( $title ) ) {
        $errors[] = 'Title is required';
    }
    if ( ! is_email( $email ) ) {
        $errors[] = 'Invalid email';
    }
    if ( $age < 18 ) {
        $errors[] = 'Must be 18 or older';
    }

    if ( ! empty( $errors ) ) {
        wp_die( implode( '<br>', $errors ) );
    }

    // 5. Process data (with escaped output if needed)
    $result = save_to_database( $title, $email, $age );

    // 6. Redirect with success message
    wp_redirect( add_query_arg( 'message', 'success', wp_get_referer() ) );
    exit;
}
```

---

## 4. Block Editor (Gutenberg) & Full Site Editing

### Current State (2024-2025)

- **FSE Status:** Production-ready (no longer beta since WordPress 6.2)
- **Block Themes:** Preferred approach for new themes (HTML templates + theme.json)
- **Classic Themes:** Still supported but considered legacy
- **Hybrid Approach:** Classic themes can add block support incrementally

### Block Theme Architecture

**File Structure:**
```
my-block-theme/
├── style.css                 # Theme metadata
├── theme.json                # Global styles and settings (REQUIRED)
├── functions.php             # Theme setup (optional)
├── templates/                # HTML block templates
│   ├── index.html           # Fallback template (REQUIRED)
│   ├── home.html
│   ├── single.html
│   ├── single-product.html  # Custom post type template
│   ├── page.html
│   └── 404.html
├── parts/                    # Template parts (header, footer, etc.)
│   ├── header.html
│   ├── footer.html
│   └── sidebar.html
├── patterns/                 # Block patterns (reusable designs)
│   ├── hero.php
│   └── call-to-action.php
├── assets/
│   ├── css/
│   └── js/
└── languages/
```

### theme.json (Global Styles)

**Purpose:** Centralized configuration for colors, typography, spacing, layouts

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "appearanceTools": true,
    "layout": {
      "contentSize": "800px",
      "wideSize": "1200px"
    },
    "color": {
      "palette": [
        {
          "slug": "primary",
          "color": "#0073aa",
          "name": "Primary"
        },
        {
          "slug": "secondary",
          "color": "#005177",
          "name": "Secondary"
        },
        {
          "slug": "black",
          "color": "#000000",
          "name": "Black"
        },
        {
          "slug": "white",
          "color": "#ffffff",
          "name": "White"
        }
      ],
      "gradients": [],
      "duotone": [],
      "defaultPalette": false,
      "defaultGradients": false
    },
    "typography": {
      "fontFamilies": [
        {
          "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
          "slug": "system",
          "name": "System Font"
        }
      ],
      "fontSizes": [
        {
          "slug": "small",
          "size": "0.875rem",
          "name": "Small"
        },
        {
          "slug": "medium",
          "size": "1rem",
          "name": "Medium"
        },
        {
          "slug": "large",
          "size": "1.5rem",
          "name": "Large"
        },
        {
          "slug": "x-large",
          "size": "2rem",
          "name": "Extra Large"
        }
      ],
      "lineHeight": true,
      "dropCap": false
    },
    "spacing": {
      "units": ["px", "em", "rem", "vh", "vw", "%"],
      "padding": true,
      "margin": true,
      "blockGap": true
    },
    "border": {
      "radius": true,
      "color": true,
      "style": true,
      "width": true
    },
    "blocks": {
      "core/button": {
        "color": {
          "palette": [
            {
              "slug": "button-primary",
              "color": "#0073aa",
              "name": "Button Primary"
            }
          ]
        }
      }
    }
  },
  "styles": {
    "color": {
      "background": "#ffffff",
      "text": "#000000"
    },
    "typography": {
      "fontFamily": "var(--wp--preset--font-family--system)",
      "fontSize": "var(--wp--preset--font-size--medium)",
      "lineHeight": "1.6"
    },
    "spacing": {
      "blockGap": "1.5rem"
    },
    "elements": {
      "link": {
        "color": {
          "text": "var(--wp--preset--color--primary)"
        },
        ":hover": {
          "color": {
            "text": "var(--wp--preset--color--secondary)"
          }
        }
      },
      "h1": {
        "typography": {
          "fontSize": "var(--wp--preset--font-size--x-large)",
          "lineHeight": "1.2"
        }
      }
    },
    "blocks": {
      "core/button": {
        "color": {
          "background": "var(--wp--preset--color--primary)",
          "text": "var(--wp--preset--color--white)"
        },
        "border": {
          "radius": "4px"
        },
        ":hover": {
          "color": {
            "background": "var(--wp--preset--color--secondary)"
          }
        }
      }
    }
  },
  "customTemplates": [
    {
      "name": "page-no-sidebar",
      "title": "Page Without Sidebar",
      "postTypes": ["page"]
    },
    {
      "name": "single-product",
      "title": "Product Template",
      "postTypes": ["product"]
    }
  ],
  "templateParts": [
    {
      "name": "header",
      "title": "Header",
      "area": "header"
    },
    {
      "name": "footer",
      "title": "Footer",
      "area": "footer"
    }
  ]
}
```

**Key theme.json Features:**
- **Version 3** (WordPress 6.6+): Latest schema version
- **Appearance Tools:** Enable border, spacing, typography controls
- **Block-Specific Settings:** Customize individual blocks
- **Custom Templates:** Register templates for specific post types
- **CSS Custom Properties:** Auto-generated CSS variables (e.g., `var(--wp--preset--color--primary)`)

### Block Template Example

**templates/single.html:**
```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
    <!-- wp:post-title {"level":1} /-->

    <!-- wp:post-featured-image /-->

    <!-- wp:post-content {"layout":{"type":"constrained"}} /-->

    <!-- wp:post-date /-->

    <!-- wp:post-author /-->

    <!-- wp:comments /-->
</div>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

### Custom Block Development (PHP Registration)

**Modern Approach (block.json metadata):**

```php
// Register block in functions.php or plugin
add_action( 'init', 'register_custom_block' );
function register_custom_block() {
    register_block_type( __DIR__ . '/blocks/testimonial' );
}
```

**blocks/testimonial/block.json:**
```json
{
  "$schema": "https://schemas.wp.org/trunk/block.json",
  "apiVersion": 3,
  "name": "my-plugin/testimonial",
  "title": "Testimonial",
  "category": "widgets",
  "icon": "format-quote",
  "description": "Display a customer testimonial.",
  "keywords": ["quote", "review", "testimonial"],
  "version": "1.0.0",
  "textdomain": "my-plugin",
  "attributes": {
    "content": {
      "type": "string",
      "source": "html",
      "selector": ".testimonial-content"
    },
    "author": {
      "type": "string",
      "default": ""
    },
    "role": {
      "type": "string",
      "default": ""
    }
  },
  "supports": {
    "html": false,
    "align": true,
    "color": {
      "background": true,
      "text": true
    },
    "spacing": {
      "padding": true,
      "margin": true
    }
  },
  "editorScript": "file:./index.js",
  "editorStyle": "file:./editor.css",
  "style": "file:./style.css",
  "render": "file:./render.php"
}
```

**blocks/testimonial/render.php:**
```php
<?php
/**
 * Testimonial block template
 *
 * @var array    $attributes Block attributes
 * @var string   $content    Block content
 * @var WP_Block $block      Block instance
 */

$content = $attributes['content'] ?? '';
$author = $attributes['author'] ?? '';
$role = $attributes['role'] ?? '';

$wrapper_attributes = get_block_wrapper_attributes([
    'class' => 'testimonial-block',
]);
?>

<div <?php echo $wrapper_attributes; ?>>
    <blockquote class="testimonial-content">
        <?php echo wp_kses_post( $content ); ?>
    </blockquote>

    <?php if ( $author ) : ?>
        <cite class="testimonial-author">
            <span class="author-name"><?php echo esc_html( $author ); ?></span>
            <?php if ( $role ) : ?>
                <span class="author-role"><?php echo esc_html( $role ); ?></span>
            <?php endif; ?>
        </cite>
    <?php endif; ?>
</div>
```

### Custom Post Types & Taxonomies with Block Support

```php
// Register custom post type with block editor support
add_action( 'init', 'register_book_post_type' );
function register_book_post_type() {
    register_post_type( 'book', [
        'labels' => [
            'name' => __( 'Books', 'my-plugin' ),
            'singular_name' => __( 'Book', 'my-plugin' ),
        ],
        'public' => true,
        'has_archive' => true,
        'rewrite' => [ 'slug' => 'books' ],
        'supports' => [
            'title',
            'editor',        // Block editor
            'thumbnail',
            'custom-fields',
            'excerpt',
        ],
        'show_in_rest' => true,  // REQUIRED for block editor
        'rest_base' => 'books',
        'menu_icon' => 'dashicons-book',
        'template' => [          // Default block template
            [ 'core/paragraph', [
                'placeholder' => 'Enter book description...',
            ]],
            [ 'core/image' ],
            [ 'my-plugin/book-details' ],
        ],
        'template_lock' => 'insert', // Prevent adding/removing blocks
    ]);
}

// Register custom taxonomy
add_action( 'init', 'register_book_genre_taxonomy' );
function register_book_genre_taxonomy() {
    register_taxonomy( 'genre', 'book', [
        'labels' => [
            'name' => __( 'Genres', 'my-plugin' ),
            'singular_name' => __( 'Genre', 'my-plugin' ),
        ],
        'hierarchical' => true, // Like categories
        'show_in_rest' => true, // REQUIRED for block editor
        'rest_base' => 'genres',
        'rewrite' => [ 'slug' => 'genre' ],
    ]);
}
```

**Template Assignment in theme.json:**
```json
{
  "customTemplates": [
    {
      "name": "single-book",
      "title": "Book Template",
      "postTypes": ["book"]
    }
  ]
}
```

---

## 5. REST API Development

### Registering Custom Endpoints

```php
add_action( 'rest_api_init', 'register_custom_rest_routes' );
function register_custom_rest_routes() {
    // Route: GET /wp-json/myplugin/v1/items
    register_rest_route( 'myplugin/v1', '/items', [
        'methods'  => 'GET',
        'callback' => 'get_items_callback',
        'permission_callback' => '__return_true', // Public endpoint
    ]);

    // Route: GET /wp-json/myplugin/v1/items/(?P<id>\d+)
    register_rest_route( 'myplugin/v1', '/items/(?P<id>\d+)', [
        'methods'  => 'GET',
        'callback' => 'get_item_callback',
        'permission_callback' => '__return_true',
        'args' => [
            'id' => [
                'validate_callback' => function( $param ) {
                    return is_numeric( $param );
                },
            ],
        ],
    ]);

    // Route: POST /wp-json/myplugin/v1/items (authenticated)
    register_rest_route( 'myplugin/v1', '/items', [
        'methods'  => 'POST',
        'callback' => 'create_item_callback',
        'permission_callback' => function() {
            return current_user_can( 'edit_posts' );
        },
        'args' => [
            'title' => [
                'required' => true,
                'validate_callback' => function( $param ) {
                    return is_string( $param ) && strlen( $param ) > 0;
                },
                'sanitize_callback' => 'sanitize_text_field',
            ],
            'content' => [
                'required' => false,
                'sanitize_callback' => 'wp_kses_post',
            ],
        ],
    ]);
}

// Callback functions
function get_items_callback( $request ) {
    // Query parameters
    $per_page = $request->get_param( 'per_page' ) ?: 10;
    $page = $request->get_param( 'page' ) ?: 1;

    // Fetch data
    $items = [
        [ 'id' => 1, 'title' => 'Item 1' ],
        [ 'id' => 2, 'title' => 'Item 2' ],
    ];

    return rest_ensure_response( $items );
}

function get_item_callback( $request ) {
    $id = $request->get_param( 'id' );

    $item = [ 'id' => $id, 'title' => "Item $id" ];

    if ( ! $item ) {
        return new WP_Error( 'not_found', 'Item not found', [ 'status' => 404 ] );
    }

    return rest_ensure_response( $item );
}

function create_item_callback( $request ) {
    $title = $request->get_param( 'title' );
    $content = $request->get_param( 'content' );

    // Insert into database
    global $wpdb;
    $result = $wpdb->insert(
        $wpdb->prefix . 'my_items',
        [
            'title' => $title,
            'content' => $content,
            'created_at' => current_time( 'mysql' ),
        ],
        [ '%s', '%s', '%s' ]
    );

    if ( ! $result ) {
        return new WP_Error( 'creation_failed', 'Failed to create item', [ 'status' => 500 ] );
    }

    $item_id = $wpdb->insert_id;

    return rest_ensure_response([
        'id' => $item_id,
        'title' => $title,
        'message' => 'Item created successfully',
    ], 201 );
}
```

### REST API Best Practices

1. **Use Proper Namespacing:** `myplugin/v1` (allows versioning)
2. **Implement Permission Callbacks:** Always define `permission_callback`
3. **Validate & Sanitize:** Use `validate_callback` and `sanitize_callback`
4. **Return Proper HTTP Codes:** 200 (success), 201 (created), 400 (bad request), 401 (unauthorized), 404 (not found), 500 (error)
5. **Use Controller Pattern:** For complex endpoints, use dedicated controller classes
6. **Implement Pagination:** Support `?page=2&per_page=10` query parameters
7. **Enable HTTPS:** Always use HTTPS for API endpoints
8. **Use Authentication:** Application passwords, OAuth, or JWT for sensitive endpoints

**Testing REST API:**
```bash
# GET request
curl https://example.com/wp-json/myplugin/v1/items

# POST request with authentication
curl -X POST https://example.com/wp-json/myplugin/v1/items \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{"title":"New Item","content":"Item content"}'

# Using Postman or Insomnia for interactive testing
```

---

## 6. Modern Development Tools & Workflow

### Local Development Environments

**1. wp-env (Official WordPress Tool)**

**Features:**
- Docker-based (no manual configuration)
- Includes WordPress, MySQL, PHP, Composer, PHPUnit, WP-CLI
- Fast setup (one command)
- Customizable via `.wp-env.json`

**Setup:**
```bash
# Install globally
npm install -g @wordpress/env

# Start WordPress environment (in any directory)
wp-env start

# Access:
# - Frontend: http://localhost:8888
# - Admin: http://localhost:8888/wp-admin (admin/password)

# Stop environment
wp-env stop

# Clean environment (reset database)
wp-env clean
```

**.wp-env.json Configuration:**
```json
{
  "core": "WordPress/WordPress#6.7",
  "phpVersion": "8.3",
  "plugins": [
    "./my-plugin",
    "https://downloads.wordpress.org/plugin/woocommerce.latest.zip"
  ],
  "themes": [
    "./my-theme"
  ],
  "config": {
    "WP_DEBUG": true,
    "WP_DEBUG_LOG": true,
    "WP_DEBUG_DISPLAY": false
  },
  "env": {
    "development": {
      "port": 8888
    },
    "tests": {
      "port": 8889
    }
  }
}
```

**2. LocalWP (Local by Flywheel)**

**Features:**
- GUI application (no command line required)
- One-click WordPress installation
- Easy PHP/MySQL version switching
- Built-in SSL, MailHog (email testing)
- Push to Flywheel/WP Engine hosting

**Best For:** Designers, non-developers, quick prototyping

**3. Docker Compose (Custom Setup)**

**docker-compose.yml Example:**
```yaml
version: '3.8'

services:
  wordpress:
    image: wordpress:latest
    ports:
      - "8000:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_DEBUG: 1
    volumes:
      - ./wp-content:/var/www/html/wp-content
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    volumes:
      - db_data:/var/lib/mysql

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    ports:
      - "8080:80"
    environment:
      PMA_HOST: db
      PMA_USER: wordpress
      PMA_PASSWORD: wordpress

volumes:
  db_data:
```

**Usage:**
```bash
docker-compose up -d
# Access WordPress: http://localhost:8000
# Access phpMyAdmin: http://localhost:8080
```

### WP-CLI (WordPress Command-Line Interface)

**Installation:**
```bash
# Download WP-CLI
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar

# Make executable
chmod +x wp-cli.phar
sudo mv wp-cli.phar /usr/local/bin/wp

# Verify
wp --info
```

**Essential Commands:**
```bash
# Install WordPress
wp core download --locale=en_US
wp config create --dbname=wordpress --dbuser=root --dbpass=password
wp core install --url=http://localhost --title="My Site" --admin_user=admin --admin_password=password --admin_email=admin@example.com

# Plugin management
wp plugin install woocommerce --activate
wp plugin list
wp plugin update --all
wp plugin deactivate my-plugin
wp plugin delete my-plugin

# Theme management
wp theme install twentytwentyfour --activate
wp theme list
wp theme update --all

# Database operations
wp db export backup.sql
wp db import backup.sql
wp db query "SELECT * FROM wp_posts LIMIT 5"

# Search and replace (for migrations)
wp search-replace 'http://oldsite.com' 'http://newsite.com' --dry-run
wp search-replace 'http://oldsite.com' 'http://newsite.com' --all-tables

# User management
wp user create newuser user@example.com --role=editor --user_pass=password
wp user list --role=administrator
wp user update 1 --user_pass=newpassword

# Post/page operations
wp post list --post_type=page --format=table
wp post create --post_type=post --post_title="New Post" --post_status=publish
wp post delete 123 --force

# Cache operations
wp cache flush
wp transient delete --all

# Cron jobs
wp cron event list
wp cron event run wp_scheduled_delete

# Rewrite rules
wp rewrite flush
wp rewrite list
```

**Scaffolding Commands:**
```bash
# Generate plugin
wp scaffold plugin my-awesome-plugin --activate

# Generate block
wp scaffold block my-block --plugin=my-plugin

# Generate post type
wp scaffold post-type book --plugin=my-plugin --dashicon=book

# Generate taxonomy
wp scaffold taxonomy genre --post_types=book --plugin=my-plugin

# Generate plugin tests (PHPUnit)
wp scaffold plugin-tests my-plugin

# Generate package (WP-CLI command)
wp scaffold package-tests my-package
```

### Build Tools & Asset Management

**Modern WordPress Development Stack (2024):**

**package.json Example:**
```json
{
  "name": "my-wordpress-plugin",
  "version": "1.0.0",
  "scripts": {
    "start": "wp-scripts start",
    "build": "wp-scripts build",
    "format": "wp-scripts format",
    "lint:css": "wp-scripts lint-style",
    "lint:js": "wp-scripts lint-js",
    "test:e2e": "wp-scripts test-e2e",
    "test:unit": "wp-scripts test-unit-js"
  },
  "devDependencies": {
    "@wordpress/scripts": "^27.0.0",
    "@wordpress/env": "^9.0.0"
  },
  "dependencies": {
    "@wordpress/block-editor": "^13.0.0",
    "@wordpress/blocks": "^13.0.0",
    "@wordpress/components": "^27.0.0",
    "@wordpress/data": "^10.0.0",
    "@wordpress/element": "^6.0.0",
    "@wordpress/i18n": "^5.0.0"
  }
}
```

**@wordpress/scripts Features:**
- Webpack bundling (pre-configured)
- Babel transpilation (ES6+ to ES5)
- SASS/SCSS compilation
- ESLint (JavaScript linting)
- Stylelint (CSS linting)
- Playwright (E2E testing)
- Jest (unit testing)

**Usage:**
```bash
# Install dependencies
npm install

# Development mode (watch for changes)
npm run start

# Production build (minified)
npm run build

# Lint JavaScript
npm run lint:js

# Format code
npm run format
```

---

## 7. Testing & Quality Assurance

### PHPUnit for WordPress

**Setup:**
```bash
# Install PHPUnit via Composer
composer require --dev phpunit/phpunit ^9.6
composer require --dev yoast/phpunit-polyfills

# Generate test scaffold
wp scaffold plugin-tests my-plugin

# Install WordPress test suite
bash bin/install-wp-tests.sh wordpress_test root '' localhost latest
```

**Test Structure:**
```
my-plugin/
├── tests/
│   ├── bootstrap.php          # Test suite bootstrap
│   ├── test-sample.php        # Example test
│   └── phpunit.xml.dist       # PHPUnit configuration
└── bin/
    └── install-wp-tests.sh    # Test DB setup script
```

**phpunit.xml.dist:**
```xml
<?xml version="1.0"?>
<phpunit
    bootstrap="tests/bootstrap.php"
    backupGlobals="false"
    colors="true"
    convertErrorsToExceptions="true"
    convertNoticesToExceptions="true"
    convertWarningsToExceptions="true"
>
    <testsuites>
        <testsuite name="unit">
            <directory prefix="test-" suffix=".php">./tests/</directory>
        </testsuite>
    </testsuites>
    <coverage includeUncoveredFiles="true">
        <include>
            <directory suffix=".php">./includes/</directory>
        </include>
    </coverage>
</phpunit>
```

**Example Test:**
```php
<?php
/**
 * Tests for MyPlugin\Helper class
 */
class Test_Helper extends WP_UnitTestCase {

    public function setUp(): void {
        parent::setUp();
        // Setup code runs before each test
    }

    public function tearDown(): void {
        parent::tearDown();
        // Cleanup code runs after each test
    }

    public function test_sanitize_phone_number() {
        $helper = new MyPlugin\Helper();

        $input = '(555) 123-4567';
        $expected = '5551234567';
        $actual = $helper->sanitize_phone_number( $input );

        $this->assertEquals( $expected, $actual );
    }

    public function test_create_post() {
        $post_id = $this->factory->post->create([
            'post_title' => 'Test Post',
            'post_content' => 'Test content',
        ]);

        $this->assertIsInt( $post_id );
        $this->assertGreaterThan( 0, $post_id );

        $post = get_post( $post_id );
        $this->assertEquals( 'Test Post', $post->post_title );
    }

    public function test_user_permission() {
        $user_id = $this->factory->user->create([
            'role' => 'editor',
        ]);

        wp_set_current_user( $user_id );

        $this->assertTrue( current_user_can( 'edit_posts' ) );
        $this->assertFalse( current_user_can( 'manage_options' ) );
    }
}
```

**Run Tests:**
```bash
# Run all tests
vendor/bin/phpunit

# Run specific test file
vendor/bin/phpunit tests/test-helper.php

# Run with coverage report
vendor/bin/phpunit --coverage-html coverage/
```

### WP_Mock for Unit Testing

**Purpose:** Mock WordPress functions without loading WordPress core (faster tests)

**Installation:**
```bash
composer require --dev mockery/mockery
composer require --dev 10up/wp_mock
```

**Example Test with WP_Mock:**
```php
<?php
use WP_Mock\Tools\TestCase;

class Test_Email_Service extends TestCase {

    public function setUp(): void {
        \WP_Mock::setUp();
    }

    public function tearDown(): void {
        \WP_Mock::tearDown();
    }

    public function test_send_notification_email() {
        // Mock wp_mail function
        \WP_Mock::userFunction( 'wp_mail', [
            'times' => 1,
            'args' => [
                'user@example.com',
                'Test Subject',
                'Test message',
                \WP_Mock\Functions::type( 'array' ),
            ],
            'return' => true,
        ]);

        // Mock get_option
        \WP_Mock::userFunction( 'get_option', [
            'args' => 'admin_email',
            'return' => 'admin@example.com',
        ]);

        $service = new MyPlugin\EmailService();
        $result = $service->send_notification( 'user@example.com', 'Test message' );

        $this->assertTrue( $result );
    }

    public function test_action_hook_fired() {
        \WP_Mock::expectActionAdded( 'init', 'my_plugin_init', 10 );

        my_plugin_register_hooks();

        // Assert action was added
        $this->assertConditionsMet();
    }
}
```

### WordPress Coding Standards Enforcement

**GitHub Actions Workflow (.github/workflows/phpcs.yml):**
```yaml
name: PHPCS

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  phpcs:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: '8.3'
        tools: composer

    - name: Install dependencies
      run: composer install --prefer-dist --no-progress

    - name: Run PHPCS
      run: vendor/bin/phpcs

    - name: Run PHPUnit
      run: vendor/bin/phpunit
```

---

## 8. Recommended Skills Library Structure

Based on the research findings, here's the recommended breakdown for a WordPress development skills library:

### **Skill 1: WordPress Plugin Fundamentals**
**Path:** `toolchains/php/frameworks/wordpress/plugin-development/`

**Focus Areas:**
- Modern plugin architecture (OOP, Composer, PSR-4)
- Hooks system (actions, filters, priorities, custom hooks)
- Plugin lifecycle (activation, deactivation, uninstall)
- Database interactions (wpdb, custom tables, dbDelta)
- Settings API and options management
- WordPress Coding Standards (WPCS)

**Code Examples:**
- Complete plugin structure template
- Hook priority examples
- Custom table creation with versioning
- Settings API implementation
- Sanitization/validation patterns

**SKILL.md Sections:**
- Plugin architecture patterns
- Hook system deep dive
- Database best practices
- Settings page creation
- WPCS integration

---

### **Skill 2: Block Editor & Full Site Editing**
**Path:** `toolchains/php/frameworks/wordpress/block-development/`

**Focus Areas:**
- Block theme architecture
- theme.json configuration
- Custom block development (block.json, render.php)
- Template hierarchy (HTML templates)
- Custom post types with block support
- Block patterns and template parts

**Code Examples:**
- Complete block theme structure
- theme.json with comprehensive settings
- Custom block registration (PHP + React)
- CPT registration with block editor support
- Template customization

**SKILL.md Sections:**
- FSE architecture overview
- theme.json schema reference
- Block development workflow
- Template system guide
- Migration from classic themes

---

### **Skill 3: WordPress Security & Data Validation**
**Path:** `toolchains/php/frameworks/wordpress/security/`

**Focus Areas:**
- Three-layer security model (sanitize, validate, escape)
- Nonce implementation (forms, URLs, AJAX)
- Capability checks and user permissions
- SQL injection prevention
- XSS protection
- CSRF mitigation

**Code Examples:**
- Nonce verification patterns
- Sanitization function reference
- Validation logic examples
- Escaping output templates
- Capability check patterns

**SKILL.md Sections:**
- Security fundamentals
- Nonce system guide
- Sanitization reference
- Validation strategies
- Output escaping reference

---

### **Skill 4: WordPress Testing & Quality Assurance**
**Path:** `toolchains/php/frameworks/wordpress/testing/`

**Focus Areas:**
- PHPUnit integration testing
- WP_Mock unit testing
- WordPress Coding Standards (PHPCS)
- Automated testing workflows
- Test factories and fixtures
- CI/CD integration

**Code Examples:**
- PHPUnit test suite setup
- WP_Mock test examples
- PHPCS configuration
- GitHub Actions workflow
- Test factory usage

**SKILL.md Sections:**
- Testing strategy guide
- PHPUnit setup and usage
- WP_Mock patterns
- PHPCS enforcement
- CI/CD workflows

---

### **Skill 5: Advanced WordPress Architecture**
**Path:** `toolchains/php/frameworks/wordpress/advanced/`

**Focus Areas:**
- REST API custom endpoints
- WP-CLI command development
- Custom admin pages and meta boxes
- Multisite development
- Performance optimization
- Caching strategies

**Code Examples:**
- REST API controller pattern
- WP-CLI command registration
- Custom admin UI components
- Query optimization techniques
- Object caching implementation

**SKILL.md Sections:**
- REST API development guide
- WP-CLI integration
- Admin customization
- Performance best practices
- Multisite considerations

---

## 9. Key Documentation References

### Official WordPress Resources

**Core Documentation:**
- Plugin Handbook: https://developer.wordpress.org/plugins/
- Theme Handbook: https://developer.wordpress.org/themes/
- Block Editor Handbook: https://developer.wordpress.org/block-editor/
- REST API Handbook: https://developer.wordpress.org/rest-api/
- Code Reference: https://developer.wordpress.org/reference/

**Coding Standards:**
- WordPress Coding Standards: https://developer.wordpress.org/coding-standards/
- WPCS GitHub: https://github.com/WordPress/WordPress-Coding-Standards
- PHP Compatibility: https://make.wordpress.org/core/handbook/references/php-compatibility-and-wordpress-versions/

**Testing:**
- Automated Testing: https://make.wordpress.org/core/handbook/testing/automated-testing/
- PHPUnit Tests: https://make.wordpress.org/core/handbook/testing/automated-testing/writing-phpunit-tests/
- WP_Mock GitHub: https://github.com/10up/wp_mock

**Tools:**
- WP-CLI: https://wp-cli.org/
- wp-env: https://developer.wordpress.org/block-editor/reference-guides/packages/packages-env/
- @wordpress/scripts: https://developer.wordpress.org/block-editor/reference-guides/packages/packages-scripts/

### Community Resources

**Learning Platforms:**
- Learn WordPress: https://learn.wordpress.org/
- Full Site Editing: https://fullsiteediting.com/
- WordPress TV: https://wordpress.tv/

**Development Tools:**
- LocalWP: https://localwp.com/
- Query Monitor Plugin: https://querymonitor.com/
- Debug Bar Plugin: https://wordpress.org/plugins/debug-bar/

---

## 10. Implementation Recommendations

### Priority 1: Essential Skills (Immediate Implementation)
1. **Plugin Fundamentals** - Core foundation for all WordPress PHP development
2. **Security & Data Validation** - Critical for secure plugin development

### Priority 2: Modern Workflow (Week 2-3)
3. **Block Editor & FSE** - Modern WordPress development approach
4. **Testing & Quality** - Ensure code reliability and maintainability

### Priority 3: Advanced Features (Week 4+)
5. **Advanced Architecture** - REST API, WP-CLI, performance optimization

### Skill Dependencies

```
Plugin Fundamentals (Base)
    ├── Security & Data Validation (Extends fundamentals)
    ├── Block Editor & FSE (Applies fundamentals to modern WP)
    └── Testing & Quality (Tests fundamental concepts)
            └── Advanced Architecture (Requires testing foundation)
```

### Code Example Template Structure

Each skill should include:
- **Basic Examples:** Simple, copy-paste ready code
- **Intermediate Patterns:** Real-world implementations
- **Advanced Techniques:** Performance, security, scalability
- **Anti-Patterns:** Common mistakes to avoid
- **Migration Guides:** Classic to modern approaches

### metadata.json Recommendations

```json
{
  "name": "wordpress-plugin-development",
  "version": "1.0.0",
  "description": "Modern WordPress plugin development with PHP 8.3, hooks system, WPCS compliance, and security best practices",
  "tags": ["wordpress", "php", "plugin", "hooks", "wpcs", "security"],
  "requirements": {
    "wordpress": ">=6.4",
    "php": ">=8.1",
    "tools": ["composer", "wp-cli"]
  },
  "dependencies": [
    "php-fundamentals",
    "composer-package-management"
  ],
  "learning_path": [
    "Plugin architecture and structure",
    "Hooks system (actions and filters)",
    "Database interactions with wpdb",
    "Settings API implementation",
    "Security and data validation"
  ]
}
```

---

## Summary: Key Findings for Skills Library

**WordPress 6.7 Ecosystem (2024-2025):**
- PHP 8.3 is the recommended version (7.4 minimum)
- Full Site Editing is production-ready (no longer beta)
- Block-based development is the modern standard
- Security remains paramount (sanitize, validate, escape)
- Testing is essential (PHPUnit + WP_Mock)
- Modern tooling includes wp-env, WP-CLI, @wordpress/scripts

**Skills Library Structure:**
5 comprehensive skills covering the full WordPress development spectrum from plugin fundamentals to advanced architecture, with emphasis on modern PHP 8.3 practices, block editor integration, and security-first development.

**Implementation Priority:**
Start with Plugin Fundamentals and Security, then expand to Block Editor and Testing, finally adding Advanced Architecture capabilities.

This research provides the foundation for creating a robust, modern WordPress development skills library aligned with 2024-2025 best practices and industry standards.

---

**Research Completed:** January 30, 2025
**Next Steps:** Begin skill implementation starting with Plugin Fundamentals (Priority 1)
