---
name: wordpress-plugin-fundamentals
description: Modern WordPress plugin development with PHP 8.3+, OOP architecture, hooks system, database interactions, and Settings API
version: 1.0.0
category: development
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Modern WordPress plugin development with OOP, hooks system, database interactions, and Settings API"
    when_to_use:
      - "Building WordPress plugins with PHP 8.3+ and WP 6.7+"
      - "Need structured architecture with actions, filters, hooks"
      - "Require database operations and settings management"
    quick_start:
      - "Create plugin structure with OOP and Composer PSR-4"
      - "Register activation/deactivation hooks"
      - "Use actions and filters for core integration"
context_limit: 5500
tags:
  - wordpress
  - php
  - plugin
  - hooks
  - wpdb
  - settings-api
  - wpcs
requires_tools: []
---

# WordPress Plugin Fundamentals

## Overview

WordPress plugin development using modern PHP 8.3+ practices, OOP architecture, Composer autoloading, and WordPress 6.7+ APIs. Build secure, maintainable plugins with proper hooks integration, database management, and settings pages.

**Current Standards**:
- **WordPress**: 6.7+ (Full Site Editing stable)
- **PHP**: 8.3 recommended (7.4 minimum)
- **Architecture**: OOP with PSR-4 autoloading
- **Security**: Three-layer model (sanitize, validate, escape)
- **Testing**: PHPUnit + WPCS compliance

**Installation**:
```bash
composer require --dev wp-coding-standards/wpcs:"^3.0"
composer require --dev phpunit/phpunit:"^9.6"
```

## Plugin Architecture

### Directory Structure

Modern plugin organization with Composer autoloading:

```
my-plugin/
├── my-plugin.php              # Main plugin file (metadata header)
├── composer.json               # Dependency management (REQUIRED)
├── includes/                   # Core business logic (PSR-4 autoloaded)
│   ├── Core.php               # Plugin bootstrap/loader class
│   ├── Admin/                 # Admin-specific functionality
│   │   ├── Settings.php
│   │   └── MetaBoxes.php
│   ├── Frontend/              # Public-facing functionality
│   │   └── Shortcodes.php
│   └── API/                   # REST API endpoints
│       └── CustomEndpoint.php
├── assets/                     # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
├── languages/                  # Translation files
├── tests/                      # PHPUnit tests
│   ├── unit/
│   ├── integration/
│   └── bootstrap.php
├── .phpcs.xml.dist            # PHP_CodeSniffer config (WPCS)
└── README.md
```

### Main Plugin File

**my-plugin.php**:
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
define( 'MY_PLUGIN_BASENAME', plugin_basename( __FILE__ ) );

// Composer autoloader
if ( file_exists( MY_PLUGIN_PATH . 'vendor/autoload.php' ) ) {
    require_once MY_PLUGIN_PATH . 'vendor/autoload.php';
}

/**
 * Initialize plugin on plugins_loaded hook
 * Runs after all plugins are loaded
 */
add_action( 'plugins_loaded', 'my_plugin_init' );

function my_plugin_init() {
    // Initialize core plugin class
    if ( class_exists( 'MyPlugin\\Core' ) ) {
        $plugin = MyPlugin\Core::get_instance();
        $plugin->run();
    }
}

/**
 * Activation hook
 * Runs once when plugin is activated
 */
register_activation_hook( __FILE__, 'my_plugin_activate' );
function my_plugin_activate() {
    // Run activation tasks
    if ( class_exists( 'MyPlugin\\Activation' ) ) {
        MyPlugin\Activation::activate();
    }

    // Flush rewrite rules after plugin activation
    flush_rewrite_rules();
}

/**
 * Deactivation hook
 * Runs when plugin is deactivated
 */
register_deactivation_hook( __FILE__, 'my_plugin_deactivate' );
function my_plugin_deactivate() {
    // Cleanup tasks
    if ( class_exists( 'MyPlugin\\Deactivation' ) ) {
        MyPlugin\Deactivation::deactivate();
    }

    // Flush rewrite rules
    flush_rewrite_rules();
}
```

### Core Plugin Class (Singleton Pattern)

**includes/Core.php**:
```php
<?php
namespace MyPlugin;

/**
 * Main plugin class using Singleton pattern
 *
 * Design Decision: Singleton ensures single plugin instance
 * Trade-off: Testability vs. simplicity (use DI for complex plugins)
 * Extension Point: Hook system allows third-party extensions
 */
class Core {
    /**
     * Single instance of the plugin
     * @var Core|null
     */
    private static $instance = null;

    /**
     * Get plugin instance (Singleton)
     *
     * @return Core
     */
    public static function get_instance() {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    /**
     * Private constructor prevents direct instantiation
     */
    private function __construct() {
        $this->load_dependencies();
        $this->define_hooks();
        $this->load_textdomain();
    }

    /**
     * Load required classes and dependencies
     */
    private function load_dependencies() {
        // Dependencies auto-loaded via Composer PSR-4
        // Additional manual includes if needed
    }

    /**
     * Register WordPress hooks
     */
    private function define_hooks() {
        // Core hooks
        add_action( 'init', [ $this, 'on_init' ] );
        add_action( 'admin_menu', [ $this, 'register_admin_menu' ] );
        add_action( 'admin_enqueue_scripts', [ $this, 'enqueue_admin_assets' ] );
        add_action( 'wp_enqueue_scripts', [ $this, 'enqueue_frontend_assets' ] );
        add_action( 'rest_api_init', [ $this, 'register_rest_routes' ] );
    }

    /**
     * Load plugin text domain for translations
     */
    private function load_textdomain() {
        load_plugin_textdomain(
            'my-plugin',
            false,
            dirname( MY_PLUGIN_BASENAME ) . '/languages'
        );
    }

    /**
     * Start plugin execution
     */
    public function run() {
        // Plugin is now running
        do_action( 'my_plugin_loaded' );
    }

    /**
     * Init hook callback
     * Register post types, taxonomies, etc.
     */
    public function on_init() {
        // Register custom post types
        $this->register_post_types();

        // Register taxonomies
        $this->register_taxonomies();
    }

    /**
     * Register custom post types
     */
    private function register_post_types() {
        register_post_type( 'book', [
            'labels' => [
                'name' => __( 'Books', 'my-plugin' ),
                'singular_name' => __( 'Book', 'my-plugin' ),
            ],
            'public' => true,
            'has_archive' => true,
            'supports' => [ 'title', 'editor', 'thumbnail' ],
            'show_in_rest' => true, // Enable block editor
            'menu_icon' => 'dashicons-book',
        ]);
    }

    /**
     * Register custom taxonomies
     */
    private function register_taxonomies() {
        register_taxonomy( 'genre', 'book', [
            'labels' => [
                'name' => __( 'Genres', 'my-plugin' ),
                'singular_name' => __( 'Genre', 'my-plugin' ),
            ],
            'hierarchical' => true,
            'show_in_rest' => true,
        ]);
    }

    /**
     * Register admin menu pages
     */
    public function register_admin_menu() {
        add_menu_page(
            __( 'My Plugin Settings', 'my-plugin' ),
            __( 'My Plugin', 'my-plugin' ),
            'manage_options',
            'my-plugin-settings',
            [ $this, 'render_settings_page' ],
            'dashicons-admin-generic',
            80
        );
    }

    /**
     * Render settings page
     */
    public function render_settings_page() {
        require_once MY_PLUGIN_PATH . 'includes/Admin/views/settings.php';
    }

    /**
     * Enqueue admin assets
     */
    public function enqueue_admin_assets( $hook ) {
        // Only load on our plugin pages
        if ( 'toplevel_page_my-plugin-settings' !== $hook ) {
            return;
        }

        wp_enqueue_style(
            'my-plugin-admin',
            MY_PLUGIN_URL . 'assets/css/admin.css',
            [],
            MY_PLUGIN_VERSION
        );

        wp_enqueue_script(
            'my-plugin-admin',
            MY_PLUGIN_URL . 'assets/js/admin.js',
            [ 'jquery' ],
            MY_PLUGIN_VERSION,
            true
        );

        // Localize script for AJAX
        wp_localize_script( 'my-plugin-admin', 'myPluginData', [
            'ajaxurl' => admin_url( 'admin-ajax.php' ),
            'nonce' => wp_create_nonce( 'my_plugin_nonce' ),
        ]);
    }

    /**
     * Enqueue frontend assets
     */
    public function enqueue_frontend_assets() {
        wp_enqueue_style(
            'my-plugin-frontend',
            MY_PLUGIN_URL . 'assets/css/frontend.css',
            [],
            MY_PLUGIN_VERSION
        );

        wp_enqueue_script(
            'my-plugin-frontend',
            MY_PLUGIN_URL . 'assets/js/frontend.js',
            [ 'jquery' ],
            MY_PLUGIN_VERSION,
            true
        );
    }

    /**
     * Register REST API routes
     */
    public function register_rest_routes() {
        // Delegate to API controller
        if ( class_exists( 'MyPlugin\\API\\CustomEndpoint' ) ) {
            $endpoint = new API\CustomEndpoint();
            $endpoint->register_routes();
        }
    }
}
```

### Composer Configuration

**composer.json**:
```json
{
    "name": "vendor/my-plugin",
    "description": "Modern WordPress plugin",
    "type": "wordpress-plugin",
    "require": {
        "php": ">=8.1"
    },
    "require-dev": {
        "wp-coding-standards/wpcs": "^3.0",
        "phpunit/phpunit": "^9.6",
        "yoast/phpunit-polyfills": "^2.0"
    },
    "autoload": {
        "psr-4": {
            "MyPlugin\\": "includes/"
        }
    },
    "config": {
        "allow-plugins": {
            "dealerdirect/phpcodesniffer-composer-installer": true
        }
    },
    "scripts": {
        "phpcs": "phpcs",
        "phpcbf": "phpcbf",
        "test": "phpunit"
    }
}
```

## Hooks System

### Actions vs. Filters

| Aspect | Actions | Filters |
|--------|---------|---------|
| **Purpose** | Execute code at specific points | Modify data before use/output |
| **Return Value** | Returns nothing (void) | **Must return value** |
| **Example** | Send emails, log events, register CPTs | Modify post content, filter queries |
| **Pattern** | `do_action()` / `add_action()` | `apply_filters()` / `add_filter()` |

### Common WordPress Actions

**init** - Register post types, taxonomies, rewrite rules:
```php
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

**plugins_loaded** - Initialize plugin after all plugins loaded:
```php
add_action( 'plugins_loaded', 'my_plugin_init' );
function my_plugin_init() {
    // Load translations
    load_plugin_textdomain( 'my-plugin', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );

    // Initialize plugin
    MyPlugin\Core::get_instance()->run();
}
```

**wp_enqueue_scripts** - Enqueue frontend CSS/JS:
```php
add_action( 'wp_enqueue_scripts', 'enqueue_frontend_assets' );
function enqueue_frontend_assets() {
    wp_enqueue_style( 'my-style', plugins_url( 'assets/css/style.css', __FILE__ ), [], '1.0.0' );
    wp_enqueue_script( 'my-script', plugins_url( 'assets/js/script.js', __FILE__ ), [ 'jquery' ], '1.0.0', true );
}
```

**admin_enqueue_scripts** - Enqueue admin CSS/JS:
```php
add_action( 'admin_enqueue_scripts', 'enqueue_admin_assets' );
function enqueue_admin_assets( $hook ) {
    // Only load on specific admin pages
    if ( 'toplevel_page_my-plugin' !== $hook ) {
        return;
    }

    wp_enqueue_style( 'my-admin-style', plugins_url( 'assets/css/admin.css', __FILE__ ) );
}
```

**save_post** - Runs when post is saved/updated:
```php
add_action( 'save_post', 'save_custom_meta', 10, 3 );
function save_custom_meta( $post_id, $post, $update ) {
    // Verify nonce
    if ( ! isset( $_POST['my_meta_nonce'] ) || ! wp_verify_nonce( $_POST['my_meta_nonce'], 'save_meta' ) ) {
        return;
    }

    // Check autosave
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }

    // Check permissions
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }

    // Save meta
    if ( isset( $_POST['custom_field'] ) ) {
        update_post_meta( $post_id, '_custom_field', sanitize_text_field( $_POST['custom_field'] ) );
    }
}
```

### Common WordPress Filters

**the_content** - Modify post content before output:
```php
add_filter( 'the_content', 'add_reading_time' );
function add_reading_time( $content ) {
    // Only on single posts
    if ( ! is_single() || ! in_the_loop() || ! is_main_query() ) {
        return $content;
    }

    $word_count = str_word_count( strip_tags( $content ) );
    $reading_time = ceil( $word_count / 200 ); // 200 words/min

    $message = sprintf(
        '<p class="reading-time">%s</p>',
        sprintf( __( 'Estimated reading time: %d min', 'my-plugin' ), $reading_time )
    );

    return $message . $content; // MUST return content
}
```

**pre_get_posts** - Modify WP_Query before execution:
```php
add_filter( 'pre_get_posts', 'modify_archive_query' );
function modify_archive_query( $query ) {
    // Only modify main query on archives
    if ( ! is_admin() && $query->is_main_query() && is_post_type_archive( 'book' ) ) {
        $query->set( 'posts_per_page', 20 );
        $query->set( 'orderby', 'title' );
        $query->set( 'order', 'ASC' );
    }
}
```

**excerpt_length** - Change excerpt word count:
```php
add_filter( 'excerpt_length', 'custom_excerpt_length' );
function custom_excerpt_length( $length ) {
    return 30; // 30 words instead of default 55
}
```

### Hook Priority and Execution Order

```php
// Priority: 1-999 (default: 10)
// Lower numbers = earlier execution

add_action( 'init', 'my_early_function', 5 );   // Runs first
add_action( 'init', 'my_normal_function' );      // Priority 10 (default)
add_action( 'init', 'my_late_function', 20 );    // Runs last

// Remove hooks
remove_action( 'init', 'my_normal_function', 10 );
remove_filter( 'the_content', 'wpautop' ); // Remove auto-paragraph formatting
```

### Creating Custom Hooks

**Custom action hook**:
```php
/**
 * Process order and trigger custom action
 */
function my_plugin_process_order( $order_id ) {
    // Process order logic...
    $order_data = [
        'total' => 99.99,
        'items' => [ 'item1', 'item2' ],
    ];

    // Allow other plugins/themes to hook into this point
    do_action( 'my_plugin_order_processed', $order_id, $order_data );
}

// Other developers can now hook into your plugin:
add_action( 'my_plugin_order_processed', 'send_order_notification', 10, 2 );
function send_order_notification( $order_id, $order_data ) {
    // Send email notification
    wp_mail(
        get_option( 'admin_email' ),
        'New Order: ' . $order_id,
        'Order total: $' . $order_data['total']
    );
}
```

**Custom filter hook**:
```php
/**
 * Get product price with filter for modification
 */
function my_plugin_get_price( $product_id ) {
    $price = get_post_meta( $product_id, '_price', true );

    // Allow price modification
    return apply_filters( 'my_plugin_product_price', $price, $product_id );
}

// Apply discount via filter
add_filter( 'my_plugin_product_price', 'apply_member_discount', 10, 2 );
function apply_member_discount( $price, $product_id ) {
    if ( is_user_logged_in() && current_user_can( 'member' ) ) {
        return $price * 0.9; // 10% discount
    }
    return $price;
}
```

## Database Interactions

### Using $wpdb Global Object

**Prepared statements** (prevent SQL injection):
```php
global $wpdb;

// SELECT with prepare()
$user_id = 42;
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_author = %d AND post_status = %s",
        $user_id,
        'publish'
    )
);

// Get single row
$post = $wpdb->get_row(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE ID = %d",
        $post_id
    )
);

// Get single variable
$count = $wpdb->get_var(
    $wpdb->prepare(
        "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = %s",
        'book'
    )
);

// Get single column
$post_ids = $wpdb->get_col(
    "SELECT ID FROM {$wpdb->posts} WHERE post_type = 'book' ORDER BY post_date DESC LIMIT 10"
);
```

**Insert data**:
```php
global $wpdb;

$wpdb->insert(
    $wpdb->prefix . 'my_custom_table',
    [
        'column1' => 'value1',
        'column2' => 123,
        'created_at' => current_time( 'mysql' ),
    ],
    [ '%s', '%d', '%s' ] // Data format: %s (string), %d (integer), %f (float)
);

$inserted_id = $wpdb->insert_id; // Get last inserted ID
```

**Update data**:
```php
global $wpdb;

$wpdb->update(
    $wpdb->prefix . 'my_custom_table',
    [ 'column1' => 'new_value', 'updated_at' => current_time( 'mysql' ) ], // Data
    [ 'id' => 5 ],                                                          // WHERE
    [ '%s', '%s' ],                                                         // Data format
    [ '%d' ]                                                                // WHERE format
);
```

**Delete data**:
```php
global $wpdb;

$wpdb->delete(
    $wpdb->prefix . 'my_custom_table',
    [ 'id' => 5 ],
    [ '%d' ]
);
```

### Creating Custom Tables

**Activation hook with dbDelta()**:
```php
/**
 * Create custom database tables on activation
 *
 * Design Decision: Custom table for performance (vs. post meta)
 * Trade-off: Custom queries needed, but 10x faster for large datasets
 * Migration Strategy: Store schema version for future updates
 */
function my_plugin_create_tables() {
    global $wpdb;

    $table_name = $wpdb->prefix . 'my_custom_table';
    $charset_collate = $wpdb->get_charset_collate();

    // CRITICAL: Specific SQL formatting required for dbDelta()
    // - Two spaces after PRIMARY KEY
    // - No spaces in data type definitions
    // - KEY definitions must be on separate lines
    $sql = "CREATE TABLE $table_name (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        user_id bigint(20) unsigned NOT NULL,
        title varchar(255) NOT NULL,
        content longtext,
        status varchar(20) DEFAULT 'draft',
        priority int(11) DEFAULT 0,
        created_at datetime DEFAULT CURRENT_TIMESTAMP,
        updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY  (id),
        KEY user_id (user_id),
        KEY status (status),
        KEY priority (priority)
    ) $charset_collate;";

    // dbDelta() intelligently creates or updates tables
    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );

    // Store database version for future migrations
    add_option( 'my_plugin_db_version', '1.0.0' );
}

register_activation_hook( __FILE__, 'my_plugin_create_tables' );
```

**Database migrations**:
```php
/**
 * Run database migrations on plugin updates
 */
function my_plugin_check_db_version() {
    $current_version = get_option( 'my_plugin_db_version', '0.0.0' );
    $required_version = '1.1.0';

    if ( version_compare( $current_version, $required_version, '<' ) ) {
        my_plugin_upgrade_database( $current_version );
    }
}
add_action( 'plugins_loaded', 'my_plugin_check_db_version' );

function my_plugin_upgrade_database( $from_version ) {
    global $wpdb;

    if ( version_compare( $from_version, '1.1.0', '<' ) ) {
        // Add new column
        $table_name = $wpdb->prefix . 'my_custom_table';
        $wpdb->query( "ALTER TABLE $table_name ADD COLUMN email varchar(255) AFTER user_id" );
    }

    // Update version
    update_option( 'my_plugin_db_version', '1.1.0' );
}
```

### Best Practices

✅ **Always use `$wpdb->prepare()` for dynamic queries**
✅ **Use `$wpdb->prefix` (never hard-code `wp_`)**
✅ **Use `$wpdb->get_charset_collate()` for correct encoding**
✅ **Use `dbDelta()` for table creation/updates**
✅ **Store schema version for migrations**
⚠️ **Consider using post_meta/options before custom tables**

## Settings API

### Options API (Simple Storage)

```php
// Add option (only if doesn't exist)
add_option( 'my_plugin_setting', 'default_value' );

// Get option with default
$value = get_option( 'my_plugin_setting', 'default_if_not_exists' );

// Update option (creates if doesn't exist)
update_option( 'my_plugin_setting', 'new_value' );

// Delete option
delete_option( 'my_plugin_setting' );

// Store arrays/objects (automatically serialized)
update_option( 'my_plugin_settings', [
    'api_key' => 'abc123',
    'enabled' => true,
    'threshold' => 50,
]);

$settings = get_option( 'my_plugin_settings', [] );
```

### Settings API (Admin Pages)

**Register settings**:
```php
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
        'my_plugin_main_section',                    // Section ID
        __( 'Main Settings', 'my-plugin' ),          // Title
        'my_plugin_section_callback',                // Callback
        'my_plugin_settings_page'                    // Page slug
    );

    // Add settings fields
    add_settings_field(
        'api_key',                                   // Field ID
        __( 'API Key', 'my-plugin' ),                // Label
        'my_plugin_api_key_callback',                // Render callback
        'my_plugin_settings_page',                   // Page slug
        'my_plugin_main_section',                    // Section ID
        [ 'label_for' => 'api_key' ]                 // Extra args
    );

    add_settings_field(
        'enable_feature',
        __( 'Enable Feature', 'my-plugin' ),
        'my_plugin_enable_feature_callback',
        'my_plugin_settings_page',
        'my_plugin_main_section',
        [ 'label_for' => 'enable_feature' ]
    );
}

// Section description callback
function my_plugin_section_callback() {
    echo '<p>' . esc_html__( 'Configure plugin settings below:', 'my-plugin' ) . '</p>';
}

// Field render callbacks
function my_plugin_api_key_callback( $args ) {
    $options = get_option( 'my_plugin_settings', [] );
    $value = isset( $options['api_key'] ) ? $options['api_key'] : '';
    ?>
    <input
        type="text"
        id="<?php echo esc_attr( $args['label_for'] ); ?>"
        name="my_plugin_settings[api_key]"
        value="<?php echo esc_attr( $value ); ?>"
        class="regular-text"
    />
    <p class="description">
        <?php esc_html_e( 'Enter your API key from the service provider.', 'my-plugin' ); ?>
    </p>
    <?php
}

function my_plugin_enable_feature_callback( $args ) {
    $options = get_option( 'my_plugin_settings', [] );
    $checked = isset( $options['enable_feature'] ) && $options['enable_feature'];
    ?>
    <label>
        <input
            type="checkbox"
            id="<?php echo esc_attr( $args['label_for'] ); ?>"
            name="my_plugin_settings[enable_feature]"
            value="1"
            <?php checked( $checked, true ); ?>
        />
        <?php esc_html_e( 'Enable this feature', 'my-plugin' ); ?>
    </label>
    <?php
}

// Sanitize callback
function my_plugin_sanitize_settings( $input ) {
    $sanitized = [];

    if ( isset( $input['api_key'] ) ) {
        $sanitized['api_key'] = sanitize_text_field( $input['api_key'] );
    }

    if ( isset( $input['enable_feature'] ) ) {
        $sanitized['enable_feature'] = (bool) $input['enable_feature'];
    }

    return $sanitized;
}
```

**Settings page template**:
```php
function my_plugin_settings_page() {
    // Check user capabilities
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( __( 'You do not have sufficient permissions to access this page.', 'my-plugin' ) );
    }
    ?>
    <div class="wrap">
        <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>

        <?php settings_errors( 'my_plugin_settings' ); ?>

        <form action="options.php" method="post">
            <?php
            // Output security fields
            settings_fields( 'my_plugin_options' );

            // Output settings sections
            do_settings_sections( 'my_plugin_settings_page' );

            // Submit button
            submit_button( __( 'Save Settings', 'my-plugin' ) );
            ?>
        </form>
    </div>
    <?php
}
```

## WordPress Coding Standards (WPCS)

### Installation and Configuration

**.phpcs.xml.dist**:
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
    <exclude-pattern>*/tests/*</exclude-pattern>

    <!-- Use WordPress-Extra rules (includes WordPress-Core + WordPress-Docs) -->
    <rule ref="WordPress-Extra">
        <!-- Allow short array syntax [] instead of array() -->
        <exclude name="Generic.Arrays.DisallowShortArraySyntax"/>

        <!-- Allow multiple assignments in one line for simple cases -->
        <exclude name="Squiz.PHP.DisallowMultipleAssignments"/>
    </rule>

    <!-- Check PHP cross-version compatibility -->
    <config name="testVersion" value="8.1-"/>
    <rule ref="PHPCompatibilityWP"/>

    <!-- Text domain verification -->
    <rule ref="WordPress.WP.I18n">
        <properties>
            <property name="text_domain" type="array">
                <element value="my-plugin"/>
            </property>
        </properties>
    </rule>

    <!-- Prefix all global functions/classes/variables -->
    <rule ref="WordPress.NamingConventions.PrefixAllGlobals">
        <properties>
            <property name="prefixes" type="array">
                <element value="my_plugin"/>
                <element value="MyPlugin"/>
            </property>
        </properties>
    </rule>

    <!-- Show progress and use colors -->
    <arg value="ps"/>
    <arg name="colors"/>
    <arg name="extensions" value="php"/>
</ruleset>
```

### Running PHPCS

```bash
# Check coding standards
vendor/bin/phpcs

# Auto-fix fixable issues
vendor/bin/phpcbf

# Check specific file
vendor/bin/phpcs includes/Core.php

# Show progress and sniff codes
vendor/bin/phpcs -ps

# Generate report
vendor/bin/phpcs --report=summary
```

### Key Coding Rules

**Indentation**: Tabs (not spaces)
```php
// CORRECT
function my_function() {
	if ( true ) {
		echo 'Hello';
	}
}

// WRONG (spaces)
function my_function() {
    if ( true ) {
        echo 'Hello';
    }
}
```

**Yoda Conditions**: Constant on left side
```php
// CORRECT (Yoda)
if ( true === $value ) {
    // ...
}

if ( 'active' === $status ) {
    // ...
}

// WRONG
if ( $value === true ) {
    // ...
}
```

**Naming Conventions**:
```php
// Functions and variables: snake_case
function my_plugin_process_data() { }
$user_name = 'John';

// Classes: PascalCase
class MyPlugin_Database { }

// Constants: UPPERCASE with underscores
define( 'MY_PLUGIN_VERSION', '1.0.0' );
```

**Documentation**: PHPDoc blocks required
```php
/**
 * Process user registration
 *
 * @param string $username User's username
 * @param string $email User's email address
 * @return int|WP_Error User ID on success, WP_Error on failure
 */
function my_plugin_register_user( $username, $email ) {
    // ...
}
```

## Best Practices

### Security Considerations

**Cross-reference**: See `../security-validation/SKILL.md` for comprehensive security patterns.

**Three-layer security model**:
1. **Sanitize on input** - Remove dangerous characters
2. **Validate for logic** - Check business rules
3. **Escape on output** - Prevent XSS

```php
// 1. Sanitize input
$title = sanitize_text_field( $_POST['title'] );
$email = sanitize_email( $_POST['email'] );

// 2. Validate
if ( empty( $title ) || strlen( $title ) < 3 ) {
    wp_die( 'Invalid title' );
}

if ( ! is_email( $email ) ) {
    wp_die( 'Invalid email' );
}

// 3. Escape output
echo '<h1>' . esc_html( $title ) . '</h1>';
echo '<a href="mailto:' . esc_attr( $email ) . '">' . esc_html( $email ) . '</a>';
```

### Prefix Everything

```php
// Prefix functions
function my_plugin_init() { }

// Prefix classes
class MyPlugin_Settings { }

// Prefix constants
define( 'MY_PLUGIN_VERSION', '1.0.0' );

// Prefix hooks
do_action( 'my_plugin_loaded' );
apply_filters( 'my_plugin_content', $content );

// Prefix database tables
$wpdb->prefix . 'my_plugin_data';

// Prefix options
update_option( 'my_plugin_settings', $data );
```

### Translation-Ready (i18n)

```php
// Simple string
__( 'Hello World', 'my-plugin' );

// Output translation
esc_html__( 'Hello World', 'my-plugin' );
esc_attr__( 'Hello World', 'my-plugin' );

// Echo translation
esc_html_e( 'Hello World', 'my-plugin' );

// Plural forms
_n( 'One item', '%d items', $count, 'my-plugin' );

// Contextual translation (same word, different meanings)
_x( 'Post', 'noun', 'my-plugin' );
_x( 'Post', 'verb', 'my-plugin' );

// With sprintf
sprintf( __( 'Hello %s', 'my-plugin' ), $name );

// Load text domain
load_plugin_textdomain( 'my-plugin', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );
```

### Use WordPress Functions Over PHP

```php
// ✅ WordPress functions (preferred)
$url = esc_url( $link );
$current_time = current_time( 'mysql' );
$user_ip = $_SERVER['REMOTE_ADDR']; // Sanitized by WP

// ❌ Native PHP (avoid when WP alternative exists)
$url = htmlspecialchars( $link ); // Use esc_url() instead
$current_time = date( 'Y-m-d H:i:s' ); // Use current_time() instead
```

### Performance Considerations

**Object caching**:
```php
// Set cache
wp_cache_set( 'my_key', $data, 'my_plugin', 3600 );

// Get cache
$data = wp_cache_get( 'my_key', 'my_plugin' );
if ( false === $data ) {
    // Cache miss, fetch data
    $data = expensive_operation();
    wp_cache_set( 'my_key', $data, 'my_plugin', 3600 );
}
```

**Transients** (database-backed cache):
```php
// Set transient (12 hours)
set_transient( 'my_plugin_data', $data, 12 * HOUR_IN_SECONDS );

// Get transient
$data = get_transient( 'my_plugin_data' );
if ( false === $data ) {
    $data = expensive_api_call();
    set_transient( 'my_plugin_data', $data, 12 * HOUR_IN_SECONDS );
}

// Delete transient
delete_transient( 'my_plugin_data' );
```

## Common Patterns

### Singleton Pattern

```php
class MyPlugin_Service {
    private static $instance = null;

    public static function get_instance() {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        // Initialization
    }

    // Prevent cloning
    private function __clone() { }

    // Prevent unserialization
    private function __wakeup() { }
}
```

### Dependency Injection

```php
/**
 * Better testability than Singleton
 */
class MyPlugin_Controller {
    private $database;
    private $settings;

    public function __construct( MyPlugin_Database $database, MyPlugin_Settings $settings ) {
        $this->database = $database;
        $this->settings = $settings;
    }

    public function process() {
        $data = $this->database->get_data();
        $config = $this->settings->get_config();
        // Process...
    }
}

// Usage
$database = new MyPlugin_Database();
$settings = new MyPlugin_Settings();
$controller = new MyPlugin_Controller( $database, $settings );
```

### Service Container Pattern

```php
class MyPlugin_Container {
    private $services = [];

    public function register( $name, $callback ) {
        $this->services[ $name ] = $callback;
    }

    public function get( $name ) {
        if ( ! isset( $this->services[ $name ] ) ) {
            throw new Exception( "Service not found: $name" );
        }

        $callback = $this->services[ $name ];
        return $callback( $this );
    }
}

// Usage
$container = new MyPlugin_Container();

$container->register( 'database', function( $c ) {
    return new MyPlugin_Database();
});

$container->register( 'settings', function( $c ) {
    return new MyPlugin_Settings();
});

$container->register( 'controller', function( $c ) {
    return new MyPlugin_Controller(
        $c->get( 'database' ),
        $c->get( 'settings' )
    );
});

$controller = $container->get( 'controller' );
```

## Related Skills

When developing WordPress plugins, consider these complementary skills (available in the skill library):

- **security-validation**: WordPress security, nonces, sanitization, validation, escaping - critical for securing plugin functionality
- **block-editor**: Block Editor development, FSE, theme.json, custom blocks - extend plugins with modern block-based interfaces
- **phpunit**: PHPUnit testing for WordPress plugins - comprehensive testing strategies for WordPress plugin development

## Resources

**Official Documentation**:
- Plugin Handbook: https://developer.wordpress.org/plugins/
- Code Reference: https://developer.wordpress.org/reference/
- Coding Standards: https://developer.wordpress.org/coding-standards/

**Tools**:
- WP-CLI: https://wp-cli.org/
- WPCS: https://github.com/WordPress/WordPress-Coding-Standards
- PHPUnit: https://make.wordpress.org/core/handbook/testing/automated-testing/

## Summary

- **Modern architecture**: OOP with PSR-4 autoloading, Composer dependencies
- **Hooks system**: Actions for execution, filters for modification
- **Database**: Use $wpdb with prepared statements, custom tables via dbDelta()
- **Settings API**: Structured admin pages with sanitization callbacks
- **WPCS compliance**: WordPress coding standards via PHPCS
- **Security-first**: Sanitize input, validate logic, escape output
- **Translation-ready**: Use i18n functions for all user-facing text
- **Performance**: Object caching, transients, query optimization
