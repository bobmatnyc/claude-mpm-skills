---
name: wordpress-testing-qa
description: WordPress plugin and theme testing with PHPUnit integration tests, WP_Mock unit tests, PHPCS coding standards, and CI/CD workflows. Use when testing WordPress plugins, enforcing coding standards, or implementing quality assurance processes.
---

# WordPress Testing & Quality Assurance

---
progressive_disclosure:
  entry_point:
    summary: "WordPress plugin and theme testing with PHPUnit, WP_Mock, PHPCS, and CI/CD for quality assurance"
    when_to_use:
      - "Testing WordPress plugins with PHPUnit integration tests"
      - "Unit testing without loading WordPress core (WP_Mock)"
      - "Enforcing coding standards with PHPCS"
    quick_start:
      - "Set up PHPUnit with WordPress test suite"
      - "Write unit tests with WP_Mock"
      - "Configure PHPCS with WPCS ruleset"
---

## Testing Strategy

### Testing Pyramid for WordPress

**The WordPress Testing Hierarchy:**

```
       /\
      /  \     E2E Tests (Playwright)
     /    \    - Full user workflows
    /------\   - Browser automation
   /        \
  /  INTEG  \  Integration Tests (PHPUnit + WordPress)
 /    TESTS  \ - Database operations
/            \ - Hook interactions
--------------
 UNIT TESTS    Unit Tests (WP_Mock)
               - Pure logic
               - No WordPress dependency
```

**Test Distribution Guidelines:**
- **Unit Tests (60%):** Fast, isolated, no WordPress
  - Pure PHP functions
  - Class methods with clear inputs/outputs
  - Business logic without side effects
- **Integration Tests (30%):** WordPress-loaded tests
  - Database operations
  - Hook/filter interactions
  - Custom post type registration
  - Settings API functionality
- **E2E Tests (10%):** Browser automation
  - Critical user workflows
  - Admin panel interactions
  - Frontend form submissions

### When to Use PHPUnit vs WP_Mock

**Use PHPUnit (Integration Tests) when:**
- ✅ Testing database operations (`$wpdb`, post creation, meta data)
- ✅ Testing WordPress hooks (actions/filters actually firing)
- ✅ Testing template rendering and output
- ✅ Testing plugin activation/deactivation logic
- ✅ Testing with actual WordPress functions

**Use WP_Mock (Unit Tests) when:**
- ✅ Testing pure business logic
- ✅ Testing functions that call WordPress functions but logic is independent
- ✅ Need fast test execution (no database setup)
- ✅ Testing in isolation without side effects
- ✅ Mocking external API calls

### Test Coverage Goals

**Minimum Coverage Requirements:**
- **New Code:** 80% minimum coverage
- **Critical Paths:** 95% coverage (payment processing, authentication, data validation)
- **Legacy Code:** Gradual improvement, prioritize high-risk areas
- **Public APIs:** 100% coverage for all public methods

**What to Test (Priority Order):**
1. **Security Functions:** Nonce verification, sanitization, capability checks
2. **Data Operations:** Database CRUD, data validation, transformation
3. **Business Logic:** Calculations, workflows, state transitions
4. **Hook Callbacks:** Action/filter handlers
5. **Public APIs:** REST endpoints, WP-CLI commands

**What NOT to Test:**
- ❌ WordPress core functions (assume they work)
- ❌ Third-party library internals
- ❌ Simple getters/setters with no logic
- ❌ Configuration files (theme.json, block.json)

---

## PHPUnit Integration Testing

### WordPress Test Suite Setup

**Step 1: Install Dependencies**

```bash
# Install PHPUnit and WordPress polyfills
composer require --dev phpunit/phpunit "^9.6"
composer require --dev yoast/phpunit-polyfills "^2.0"

# Generate test scaffold with WP-CLI
wp scaffold plugin-tests my-plugin

# This creates:
# - tests/bootstrap.php
# - tests/test-sample.php
# - phpunit.xml.dist
# - bin/install-wp-tests.sh
```

**Step 2: Install WordPress Test Library**

```bash
# Install WordPress test suite and test database
# Syntax: bash bin/install-wp-tests.sh <db-name> <db-user> <db-pass> <db-host> <wp-version>
bash bin/install-wp-tests.sh wordpress_test root '' localhost latest

# For specific WordPress version:
bash bin/install-wp-tests.sh wordpress_test root '' localhost 6.7
```

**Step 3: Configure phpunit.xml.dist**

```xml
<?xml version="1.0"?>
<phpunit
    bootstrap="tests/bootstrap.php"
    backupGlobals="false"
    colors="true"
    convertErrorsToExceptions="true"
    convertNoticesToExceptions="true"
    convertWarningsToExceptions="true"
    stopOnFailure="false"
>
    <testsuites>
        <testsuite name="plugin">
            <directory prefix="test-" suffix=".php">./tests/</directory>
            <exclude>./tests/bootstrap.php</exclude>
        </testsuite>
    </testsuites>

    <coverage includeUncoveredFiles="true">
        <include>
            <directory suffix=".php">./includes/</directory>
        </include>
        <exclude>
            <directory>./vendor/</directory>
            <directory>./tests/</directory>
        </exclude>
        <report>
            <html outputDirectory="coverage-html"/>
            <text outputFile="php://stdout" showOnlySummary="true"/>
        </report>
    </coverage>

    <php>
        <const name="WP_TESTS_PHPUNIT_POLYFILLS_PATH" value="vendor/yoast/phpunit-polyfills"/>
    </php>
</phpunit>
```

### WP_UnitTestCase Base Class

**tests/bootstrap.php:**

```php
<?php
/**
 * PHPUnit bootstrap file
 */

// Composer autoloader
require_once dirname(__DIR__) . '/vendor/autoload.php';

// WordPress tests directory
$_tests_dir = getenv('WP_TESTS_DIR');
if (!$_tests_dir) {
    $_tests_dir = rtrim(sys_get_temp_dir(), '/\\') . '/wordpress-tests-lib';
}

if (!file_exists("{$_tests_dir}/includes/functions.php")) {
    throw new Exception("Could not find {$_tests_dir}/includes/functions.php");
}

// Give access to tests_add_filter() function
require_once "{$_tests_dir}/includes/functions.php";

/**
 * Manually load the plugin being tested
 */
function _manually_load_plugin() {
    require dirname(__DIR__) . '/my-plugin.php';
}
tests_add_filter('muplugins_loaded', '_manually_load_plugin');

// Start up the WordPress testing environment
require "{$_tests_dir}/includes/bootstrap.php";
```

### Factory Objects for Test Data

**Using Built-in Factories:**

```php
<?php
class Test_Plugin_Integration extends WP_UnitTestCase {

    /**
     * Test creating posts with factory
     */
    public function test_create_post_with_meta() {
        // Create a post using factory
        $post_id = $this->factory->post->create([
            'post_title'   => 'Test Post',
            'post_content' => 'Test content for integration test',
            'post_status'  => 'publish',
            'post_type'    => 'post',
        ]);

        $this->assertIsInt($post_id);
        $this->assertGreaterThan(0, $post_id);

        // Add post meta
        add_post_meta($post_id, '_custom_field', 'custom_value');

        // Verify meta was saved
        $meta_value = get_post_meta($post_id, '_custom_field', true);
        $this->assertEquals('custom_value', $meta_value);
    }

    /**
     * Test creating users
     */
    public function test_user_can_edit_post() {
        // Create editor user
        $editor_id = $this->factory->user->create([
            'role' => 'editor',
            'user_login' => 'test_editor',
            'user_email' => 'editor@example.com',
        ]);

        // Set as current user
        wp_set_current_user($editor_id);

        // Create post
        $post_id = $this->factory->post->create([
            'post_author' => $editor_id,
        ]);

        // Test capabilities
        $this->assertTrue(current_user_can('edit_post', $post_id));
        $this->assertTrue(current_user_can('edit_posts'));
        $this->assertFalse(current_user_can('manage_options'));
    }

    /**
     * Test creating terms and taxonomy
     */
    public function test_assign_categories() {
        // Create category
        $category_id = $this->factory->category->create([
            'name' => 'Test Category',
            'slug' => 'test-category',
        ]);

        // Create post
        $post_id = $this->factory->post->create();

        // Assign category
        wp_set_post_categories($post_id, [$category_id]);

        // Verify assignment
        $categories = wp_get_post_categories($post_id);
        $this->assertContains($category_id, $categories);
    }

    /**
     * Test creating comments
     */
    public function test_post_has_comments() {
        $post_id = $this->factory->post->create();

        // Create multiple comments
        $comment_ids = $this->factory->comment->create_many(3, [
            'comment_post_ID' => $post_id,
            'comment_approved' => 1,
        ]);

        $this->assertCount(3, $comment_ids);

        // Get comments for post
        $comments = get_comments(['post_id' => $post_id]);
        $this->assertCount(3, $comments);
    }
}
```

**Available Factory Objects:**
- `$this->factory->post` - Posts, pages, custom post types
- `$this->factory->user` - Users with roles
- `$this->factory->term` - Terms (categories, tags, custom taxonomies)
- `$this->factory->category` - Categories specifically
- `$this->factory->tag` - Tags specifically
- `$this->factory->comment` - Comments
- `$this->factory->blog` - Multisite blogs

### Database Fixtures and Teardown

**setUp() and tearDown() Methods:**

```php
<?php
class Test_Custom_Post_Type extends WP_UnitTestCase {

    protected $post_ids = [];

    /**
     * Setup runs before EACH test method
     */
    public function setUp(): void {
        parent::setUp();

        // Register custom post type
        register_post_type('book', [
            'public' => true,
            'supports' => ['title', 'editor'],
        ]);

        // Create test data
        $this->post_ids = $this->factory->post->create_many(5, [
            'post_type' => 'book',
        ]);
    }

    /**
     * Teardown runs after EACH test method
     */
    public function tearDown(): void {
        // Clean up test data
        foreach ($this->post_ids as $post_id) {
            wp_delete_post($post_id, true); // Force delete
        }

        // Unregister post type
        unregister_post_type('book');

        parent::tearDown();
    }

    /**
     * Test that books are created
     */
    public function test_books_created() {
        $this->assertCount(5, $this->post_ids);

        $query = new WP_Query([
            'post_type' => 'book',
            'posts_per_page' => -1,
        ]);

        $this->assertEquals(5, $query->found_posts);
    }
}
```

**setUpBeforeClass() and tearDownAfterClass():**

```php
<?php
class Test_Plugin_Database extends WP_UnitTestCase {

    protected static $table_name;

    /**
     * Runs ONCE before all tests in class
     */
    public static function setUpBeforeClass(): void {
        parent::setUpBeforeClass();

        global $wpdb;
        self::$table_name = $wpdb->prefix . 'plugin_data';

        // Create custom table
        $charset_collate = $wpdb->get_charset_collate();
        $sql = "CREATE TABLE " . self::$table_name . " (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            user_id bigint(20) unsigned NOT NULL,
            data_value varchar(255) NOT NULL,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY  (id),
            KEY user_id (user_id)
        ) $charset_collate;";

        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        dbDelta($sql);
    }

    /**
     * Runs ONCE after all tests in class
     */
    public static function tearDownAfterClass(): void {
        global $wpdb;
        $wpdb->query("DROP TABLE IF EXISTS " . self::$table_name);

        parent::tearDownAfterClass();
    }

    /**
     * Test table exists
     */
    public function test_custom_table_exists() {
        global $wpdb;
        $table_exists = $wpdb->get_var(
            "SHOW TABLES LIKE '" . self::$table_name . "'"
        );
        $this->assertEquals(self::$table_name, $table_exists);
    }

    /**
     * Test insert data
     */
    public function test_insert_data() {
        global $wpdb;

        $result = $wpdb->insert(
            self::$table_name,
            [
                'user_id' => 1,
                'data_value' => 'test_value',
            ],
            ['%d', '%s']
        );

        $this->assertEquals(1, $result);
        $this->assertGreaterThan(0, $wpdb->insert_id);
    }
}
```

### Complete Plugin Test Example

**tests/test-plugin-functionality.php:**

```php
<?php
/**
 * Test plugin core functionality
 */
class Test_Plugin_Functionality extends WP_UnitTestCase {

    /**
     * Test plugin registers custom post type
     */
    public function test_custom_post_type_registered() {
        $this->assertTrue(post_type_exists('book'));

        $post_type = get_post_type_object('book');
        $this->assertTrue($post_type->public);
        $this->assertTrue($post_type->show_in_rest);
    }

    /**
     * Test custom taxonomy registration
     */
    public function test_custom_taxonomy_registered() {
        $this->assertTrue(taxonomy_exists('genre'));

        $taxonomy = get_taxonomy('genre');
        $this->assertTrue($taxonomy->hierarchical);
        $this->assertContains('book', $taxonomy->object_type);
    }

    /**
     * Test saving custom meta data
     */
    public function test_save_book_metadata() {
        $book_id = $this->factory->post->create([
            'post_type' => 'book',
            'post_title' => 'Test Book',
        ]);

        // Simulate saving meta (as would happen in save_post hook)
        update_post_meta($book_id, '_isbn', '978-3-16-148410-0');
        update_post_meta($book_id, '_author', 'John Doe');
        update_post_meta($book_id, '_publication_year', 2024);

        // Verify meta saved correctly
        $this->assertEquals('978-3-16-148410-0', get_post_meta($book_id, '_isbn', true));
        $this->assertEquals('John Doe', get_post_meta($book_id, '_author', true));
        $this->assertEquals(2024, get_post_meta($book_id, '_publication_year', true));
    }

    /**
     * Test shortcode output
     */
    public function test_book_shortcode_output() {
        $book_id = $this->factory->post->create([
            'post_type' => 'book',
            'post_title' => 'The Great Gatsby',
        ]);

        update_post_meta($book_id, '_author', 'F. Scott Fitzgerald');

        // Test shortcode
        $output = do_shortcode('[book id="' . $book_id . '"]');

        $this->assertStringContainsString('The Great Gatsby', $output);
        $this->assertStringContainsString('F. Scott Fitzgerald', $output);
    }

    /**
     * Test action hook fires correctly
     */
    public function test_book_published_action_fires() {
        $action_fired = false;

        // Add temporary hook to verify action fires
        add_action('my_plugin_book_published', function($post_id) use (&$action_fired) {
            $action_fired = true;
        });

        // Create published book (should trigger action)
        $book_id = $this->factory->post->create([
            'post_type' => 'book',
            'post_status' => 'publish',
        ]);

        // Manually trigger the action (simulating what plugin does)
        do_action('my_plugin_book_published', $book_id);

        $this->assertTrue($action_fired, 'Book published action did not fire');
    }

    /**
     * Test filter modifies content
     */
    public function test_reading_time_filter() {
        $content = str_repeat('word ', 200); // 200 words

        // Apply filter
        $filtered = apply_filters('my_plugin_content_filter', $content);

        $this->assertStringContainsString('reading time', strtolower($filtered));
        $this->assertStringContainsString('1 min', $filtered);
    }
}
```

---

## WP_Mock Unit Testing

### What is WP_Mock and When to Use It

**WP_Mock Purpose:**
- Test PHP code **without loading WordPress**
- Mock WordPress functions to return expected values
- Verify WordPress functions are called with correct arguments
- Much faster than integration tests (no database setup)

**When to Use WP_Mock:**

✅ **Perfect for:**
- Pure business logic that calls WordPress functions
- Data transformation/validation functions
- Service classes with WordPress dependencies
- Testing in continuous integration (faster CI builds)

❌ **NOT Suitable for:**
- Testing actual database operations
- Testing hook interactions between plugins
- Testing template rendering
- Testing functions that rely on WordPress state

### Installation and Setup

```bash
# Install WP_Mock and Mockery
composer require --dev mockery/mockery "^1.6"
composer require --dev 10up/wp_mock "^1.0"
composer require --dev phpunit/phpunit "^9.6"
```

**tests/bootstrap-wp-mock.php:**

```php
<?php
/**
 * Bootstrap file for WP_Mock tests
 */

require_once __DIR__ . '/../vendor/autoload.php';

// WP_Mock setup
WP_Mock::bootstrap();

// Define WordPress constants if needed
if (!defined('ABSPATH')) {
    define('ABSPATH', '/path/to/wordpress/');
}
```

**phpunit-wp-mock.xml.dist:**

```xml
<?xml version="1.0"?>
<phpunit
    bootstrap="tests/bootstrap-wp-mock.php"
    backupGlobals="false"
    colors="true"
    convertErrorsToExceptions="true"
    convertNoticesToExceptions="true"
    convertWarningsToExceptions="true"
>
    <testsuites>
        <testsuite name="unit">
            <directory prefix="test-" suffix=".php">./tests/unit/</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

### Mocking WordPress Functions

**tests/unit/test-data-processor.php:**

```php
<?php
use WP_Mock\Tools\TestCase;

class Test_Data_Processor extends TestCase {

    public function setUp(): void {
        WP_Mock::setUp();
    }

    public function tearDown(): void {
        WP_Mock::tearDown();
    }

    /**
     * Test sanitization function
     */
    public function test_sanitize_input() {
        // Mock sanitize_text_field
        WP_Mock::userFunction('sanitize_text_field', [
            'times' => 1,
            'args' => ['<script>alert("xss")</script>'],
            'return' => 'alert("xss")', // WordPress strips tags
        ]);

        $processor = new MyPlugin\DataProcessor();
        $result = $processor->sanitize_input('<script>alert("xss")</script>');

        $this->assertEquals('alert("xss")', $result);
    }

    /**
     * Test get_option is called
     */
    public function test_get_setting() {
        // Mock get_option call
        WP_Mock::userFunction('get_option', [
            'times' => 1,
            'args' => ['my_plugin_api_key', ''],
            'return' => 'test_api_key_12345',
        ]);

        $processor = new MyPlugin\DataProcessor();
        $api_key = $processor->get_api_key();

        $this->assertEquals('test_api_key_12345', $api_key);
    }

    /**
     * Test multiple function calls with different returns
     */
    public function test_user_data_retrieval() {
        $user_id = 42;

        // Mock get_user_meta
        WP_Mock::userFunction('get_user_meta', [
            'times' => 1,
            'args' => [$user_id, 'first_name', true],
            'return' => 'John',
        ]);

        WP_Mock::userFunction('get_user_meta', [
            'times' => 1,
            'args' => [$user_id, 'last_name', true],
            'return' => 'Doe',
        ]);

        $processor = new MyPlugin\DataProcessor();
        $full_name = $processor->get_user_full_name($user_id);

        $this->assertEquals('John Doe', $full_name);
    }

    /**
     * Test function with type matcher
     */
    public function test_save_data_with_array() {
        // Accept any array as second argument
        WP_Mock::userFunction('update_option', [
            'times' => 1,
            'args' => [
                'my_plugin_settings',
                WP_Mock\Functions::type('array'),
            ],
            'return' => true,
        ]);

        $processor = new MyPlugin\DataProcessor();
        $result = $processor->save_settings(['api_key' => 'test123']);

        $this->assertTrue($result);
    }
}
```

### Mocking Filters and Actions

**Testing add_filter() Calls:**

```php
<?php
class Test_Hook_Registration extends WP_Mock\Tools\TestCase {

    public function setUp(): void {
        WP_Mock::setUp();
    }

    public function tearDown(): void {
        WP_Mock::tearDown();
    }

    /**
     * Test that filter is registered
     */
    public function test_content_filter_registered() {
        // Expect filter to be added
        WP_Mock::expectFilterAdded(
            'the_content',
            'MyPlugin\ContentFilter::add_reading_time',
            10,
            1
        );

        // Execute function that adds the filter
        MyPlugin\Hooks::register_filters();

        // Verify expectations met
        $this->assertConditionsMet();
    }

    /**
     * Test that action is registered
     */
    public function test_init_action_registered() {
        WP_Mock::expectActionAdded(
            'init',
            'MyPlugin\PostTypes::register_custom_post_types',
            10,
            0
        );

        MyPlugin\Hooks::register_actions();

        $this->assertConditionsMet();
    }

    /**
     * Test apply_filters modifies value
     */
    public function test_apply_custom_filter() {
        $original_value = 100;
        $filtered_value = 150;

        // Mock apply_filters
        WP_Mock::onFilter('my_plugin_price')
            ->with($original_value)
            ->reply($filtered_value);

        $processor = new MyPlugin\PriceCalculator();
        $result = $processor->get_final_price($original_value);

        $this->assertEquals($filtered_value, $result);
    }

    /**
     * Test do_action is called
     */
    public function test_custom_action_fired() {
        $order_id = 12345;

        // Expect action to be fired with specific arguments
        WP_Mock::expectAction('my_plugin_order_processed', $order_id);

        $processor = new MyPlugin\OrderProcessor();
        $processor->process_order($order_id);

        $this->assertConditionsMet();
    }
}
```

### Testing in Isolation (No WordPress Dependency)

**Example: Email Service Class:**

```php
<?php
namespace MyPlugin;

class EmailService {

    public function send_notification(string $to, string $message): bool {
        $subject = $this->get_email_subject();
        $headers = $this->get_email_headers();

        return wp_mail($to, $subject, $message, $headers);
    }

    protected function get_email_subject(): string {
        $site_name = get_bloginfo('name');
        return sprintf('[%s] Notification', $site_name);
    }

    protected function get_email_headers(): array {
        $admin_email = get_option('admin_email');
        return [
            'From: ' . $admin_email,
            'Content-Type: text/html; charset=UTF-8',
        ];
    }
}
```

**Unit Test Without WordPress:**

```php
<?php
use WP_Mock\Tools\TestCase;

class Test_Email_Service extends TestCase {

    public function setUp(): void {
        WP_Mock::setUp();
    }

    public function tearDown(): void {
        WP_Mock::tearDown();
    }

    /**
     * Test email sending logic
     */
    public function test_send_notification_email() {
        // Mock get_bloginfo
        WP_Mock::userFunction('get_bloginfo', [
            'args' => 'name',
            'return' => 'My WordPress Site',
        ]);

        // Mock get_option
        WP_Mock::userFunction('get_option', [
            'args' => 'admin_email',
            'return' => 'admin@example.com',
        ]);

        // Mock wp_mail and verify arguments
        WP_Mock::userFunction('wp_mail', [
            'times' => 1,
            'args' => [
                'user@example.com',
                '[My WordPress Site] Notification',
                'Test message content',
                WP_Mock\Functions::type('array'),
            ],
            'return' => true,
        ]);

        $service = new MyPlugin\EmailService();
        $result = $service->send_notification(
            'user@example.com',
            'Test message content'
        );

        $this->assertTrue($result);
    }

    /**
     * Test email failure handling
     */
    public function test_email_send_failure() {
        WP_Mock::userFunction('get_bloginfo', [
            'return' => 'Test Site',
        ]);

        WP_Mock::userFunction('get_option', [
            'return' => 'admin@test.com',
        ]);

        // Simulate wp_mail failure
        WP_Mock::userFunction('wp_mail', [
            'return' => false,
        ]);

        $service = new MyPlugin\EmailService();
        $result = $service->send_notification('user@test.com', 'Message');

        $this->assertFalse($result);
    }
}
```

---

## PHPCS & Coding Standards

### Installing PHPCS and WPCS

**via Composer (Recommended):**

```bash
# Allow PHPCS composer installer plugin
composer config allow-plugins.dealerdirect/phpcodesniffer-composer-installer true

# Install WordPress Coding Standards
composer require --dev wp-coding-standards/wpcs:"^3.0"

# Install PHP Compatibility checker
composer require --dev phpcompatibility/phpcompatibility-wp:"*"

# Install PHPCS itself (if not already installed)
composer require --dev squizlabs/php_codesniffer:"^3.7"

# Verify installation
vendor/bin/phpcs -i
# Should show: WordPress, WordPress-Core, WordPress-Docs, WordPress-Extra
```

### .phpcs.xml.dist Configuration

**Complete Configuration File:**

```xml
<?xml version="1.0"?>
<ruleset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    name="WordPress Plugin Coding Standards"
    xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/squizlabs/PHP_CodeSniffer/master/phpcs.xsd">

    <description>Custom coding standards for WordPress plugin</description>

    <!-- What to scan -->
    <file>./includes</file>
    <file>./my-plugin.php</file>

    <!-- Exclude patterns -->
    <exclude-pattern>*/vendor/*</exclude-pattern>
    <exclude-pattern>*/node_modules/*</exclude-pattern>
    <exclude-pattern>*/tests/*</exclude-pattern>
    <exclude-pattern>*/build/*</exclude-pattern>
    <exclude-pattern>*/.git/*</exclude-pattern>

    <!-- Show progress -->
    <arg value="ps"/>
    <arg name="colors"/>
    <arg name="extensions" value="php"/>
    <arg name="parallel" value="8"/>

    <!-- Rules: Use WordPress-Extra ruleset -->
    <rule ref="WordPress-Extra">
        <!-- Allow short array syntax [] instead of array() -->
        <exclude name="Generic.Arrays.DisallowShortArraySyntax"/>

        <!-- Allow multiple assignments in single line -->
        <exclude name="Squiz.PHP.DisallowMultipleAssignments"/>

        <!-- Relax file comment requirements -->
        <exclude name="Squiz.Commenting.FileComment"/>
    </rule>

    <!-- WordPress.WP.I18n: Check text domain -->
    <rule ref="WordPress.WP.I18n">
        <properties>
            <property name="text_domain" type="array">
                <element value="my-plugin"/>
            </property>
        </properties>
    </rule>

    <!-- WordPress.NamingConventions.PrefixAllGlobals: Check function/class prefixes -->
    <rule ref="WordPress.NamingConventions.PrefixAllGlobals">
        <properties>
            <property name="prefixes" type="array">
                <element value="my_plugin"/>
                <element value="MyPlugin"/>
            </property>
        </properties>
    </rule>

    <!-- PHP version compatibility -->
    <config name="testVersion" value="8.1-"/>
    <rule ref="PHPCompatibilityWP"/>

    <!-- Minimum supported WordPress version -->
    <config name="minimum_wp_version" value="6.4"/>

    <!-- Exclude specific rules for test files -->
    <rule ref="WordPress.Files.FileName">
        <exclude-pattern>*/tests/*</exclude-pattern>
    </rule>

    <!-- Enforce line length limit (warning at 80, error at 120) -->
    <rule ref="Generic.Files.LineLength">
        <properties>
            <property name="lineLimit" value="120"/>
            <property name="absoluteLineLimit" value="150"/>
        </properties>
    </rule>

    <!-- Allow WordPress globals to be modified -->
    <rule ref="WordPress.WP.GlobalVariablesOverride">
        <type>error</type>
    </rule>
</ruleset>
```

### Running PHPCS and PHPCBF

**Command Line Usage:**

```bash
# Check all files
vendor/bin/phpcs

# Check specific file
vendor/bin/phpcs includes/Core.php

# Show error codes
vendor/bin/phpcs -s

# Show only errors (hide warnings)
vendor/bin/phpcs -n

# Generate report summary
vendor/bin/phpcs --report=summary

# Check single file with detailed output
vendor/bin/phpcs -v includes/Admin/Settings.php

# Auto-fix fixable issues
vendor/bin/phpcbf

# Auto-fix specific file
vendor/bin/phpcbf includes/Core.php

# Dry run (show what would be fixed)
vendor/bin/phpcbf --dry-run

# Use specific standard
vendor/bin/phpcs --standard=WordPress-Core includes/

# Generate different report formats
vendor/bin/phpcs --report=json > phpcs-report.json
vendor/bin/phpcs --report=xml > phpcs-report.xml
vendor/bin/phpcs --report=csv > phpcs-report.csv
```

**composer.json Scripts:**

```json
{
    "scripts": {
        "phpcs": "phpcs",
        "phpcbf": "phpcbf",
        "phpcs:check": "phpcs --report=summary",
        "phpcs:fix": "phpcbf",
        "test": [
            "@phpcs",
            "phpunit"
        ]
    }
}
```

### Pre-commit Hooks

**Install pre-commit hook (.git/hooks/pre-commit):**

```bash
#!/bin/bash

# Run PHPCS on changed PHP files
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '.php$')

if [ -z "$FILES" ]; then
    echo "No PHP files to check"
    exit 0
fi

echo "Running PHPCS on changed files..."

vendor/bin/phpcs $FILES

PHPCS_EXIT=$?

if [ $PHPCS_EXIT -ne 0 ]; then
    echo ""
    echo "PHPCS found coding standard violations."
    echo "Run 'composer phpcbf' to auto-fix issues."
    echo ""
    exit 1
fi

echo "PHPCS passed!"
exit 0
```

**Make hook executable:**

```bash
chmod +x .git/hooks/pre-commit
```

### IDE Integration

**Visual Studio Code (.vscode/settings.json):**

```json
{
    "phpcs.enable": true,
    "phpcs.standard": "WordPress",
    "phpcs.executablePath": "${workspaceFolder}/vendor/bin/phpcs",
    "phpcbf.enable": true,
    "phpcbf.executablePath": "${workspaceFolder}/vendor/bin/phpcbf",
    "phpcbf.onsave": false,
    "editor.formatOnSave": false,
    "[php]": {
        "editor.defaultFormatter": "bmewburn.vscode-intelephense-client",
        "editor.formatOnSave": true
    }
}
```

**PHPStorm Configuration:**

1. Go to **Settings → PHP → Quality Tools → PHP_CodeSniffer**
2. Set Configuration path: `{PROJECT_ROOT}/vendor/bin/phpcs`
3. Go to **Settings → Editor → Inspections → PHP → Quality Tools**
4. Enable "PHP_CodeSniffer validation"
5. Set Coding standard: "Custom"
6. Set Path: `{PROJECT_ROOT}/.phpcs.xml.dist`

---

## GitHub Actions CI/CD

### Workflow File Structure

**.github/workflows/tests.yml:**

```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  # Job 1: Coding Standards Check
  phpcs:
    name: PHPCS
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          tools: composer
          coverage: none

      - name: Install dependencies
        run: composer install --prefer-dist --no-progress --no-suggest

      - name: Run PHPCS
        run: vendor/bin/phpcs --report=summary

  # Job 2: PHPUnit Tests with Matrix
  phpunit:
    name: PHPUnit (PHP ${{ matrix.php }}, WP ${{ matrix.wordpress }})
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        php: ['8.1', '8.2', '8.3']
        wordpress: ['6.4', '6.5', '6.6', '6.7', 'latest']
        include:
          - php: '8.3'
            wordpress: 'trunk'

    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: wordpress_test
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          extensions: mysqli, zip
          tools: composer
          coverage: xdebug

      - name: Install Composer dependencies
        run: composer install --prefer-dist --no-progress

      - name: Install WordPress test suite
        run: |
          bash bin/install-wp-tests.sh wordpress_test root root 127.0.0.1:3306 ${{ matrix.wordpress }}

      - name: Run PHPUnit tests
        run: vendor/bin/phpunit --coverage-clover=coverage.xml

      - name: Upload coverage to Codecov
        if: matrix.php == '8.3' && matrix.wordpress == 'latest'
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          flags: unittests
          name: codecov-umbrella

  # Job 3: WP_Mock Unit Tests
  wp-mock:
    name: WP_Mock Unit Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          tools: composer
          coverage: none

      - name: Install dependencies
        run: composer install --prefer-dist --no-progress

      - name: Run WP_Mock tests
        run: vendor/bin/phpunit -c phpunit-wp-mock.xml.dist
```

### Matrix Testing (Multiple PHP/WP Versions)

**Strategy Explanation:**

```yaml
strategy:
  fail-fast: false  # Continue testing other versions even if one fails
  matrix:
    php: ['8.1', '8.2', '8.3']  # Test PHP versions
    wordpress: ['6.4', '6.5', '6.6', '6.7', 'latest']  # Test WP versions
    include:
      # Add specific combination not in default matrix
      - php: '8.3'
        wordpress: 'trunk'  # WordPress development version
    exclude:
      # Exclude incompatible combinations
      - php: '8.1'
        wordpress: 'trunk'
```

**Matrix Results:**
- Creates **18 test jobs** (3 PHP × 6 WordPress versions)
- Ensures compatibility across supported versions
- Identifies version-specific issues early

### PHPCS Checks in CI

**Dedicated PHPCS Job:**

```yaml
phpcs-detailed:
  name: Detailed PHPCS Report
  runs-on: ubuntu-latest

  steps:
    - uses: actions/checkout@v4

    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: '8.3'
        tools: composer, cs2pr

    - name: Install dependencies
      run: composer install --prefer-dist --no-progress

    - name: Run PHPCS with annotations
      run: vendor/bin/phpcs -q --report=checkstyle | cs2pr

    - name: Generate PHPCS report
      if: failure()
      run: vendor/bin/phpcs --report=summary --report-file=phpcs-report.txt

    - name: Upload PHPCS report
      if: failure()
      uses: actions/upload-artifact@v3
      with:
        name: phpcs-report
        path: phpcs-report.txt
```

### PHPUnit Test Execution

**With Code Coverage:**

```yaml
phpunit-coverage:
  name: PHPUnit with Coverage
  runs-on: ubuntu-latest

  services:
    mysql:
      image: mysql:8.0
      env:
        MYSQL_ROOT_PASSWORD: root
        MYSQL_DATABASE: wordpress_test
      ports:
        - 3306:3306
      options: --health-cmd="mysqladmin ping" --health-interval=10s

  steps:
    - uses: actions/checkout@v4

    - name: Setup PHP with Xdebug
      uses: shivammathur/setup-php@v2
      with:
        php-version: '8.3'
        extensions: mysqli, zip, gd
        tools: composer
        coverage: xdebug
        ini-values: xdebug.mode=coverage

    - name: Install dependencies
      run: composer install --prefer-dist --no-progress

    - name: Install WordPress test suite
      run: bash bin/install-wp-tests.sh wordpress_test root root 127.0.0.1:3306 latest

    - name: Run tests with coverage
      run: vendor/bin/phpunit --coverage-html coverage-html --coverage-clover coverage.xml

    - name: Upload coverage HTML report
      uses: actions/upload-artifact@v3
      with:
        name: coverage-report
        path: coverage-html

    - name: Check coverage threshold
      run: |
        COVERAGE=$(vendor/bin/phpunit --coverage-text | grep "Lines:" | awk '{print $2}' | sed 's/%//')
        if (( $(echo "$COVERAGE < 80" | bc -l) )); then
          echo "Coverage $COVERAGE% is below 80% threshold"
          exit 1
        fi
```

### Coverage Reporting

**Codecov Integration:**

```yaml
- name: Upload to Codecov
  uses: codecov/codecov-action@v4
  with:
    files: ./coverage.xml
    flags: unittests
    name: codecov-umbrella
    fail_ci_if_error: true
    verbose: true
```

**Coveralls Integration:**

```yaml
- name: Upload to Coveralls
  uses: coverallsapp/github-action@v2
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    path-to-lcov: ./coverage.xml
```

### Complete Workflow Example

**.github/workflows/ci.yml (Production-Ready):**

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  coding-standards:
    name: Coding Standards
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          tools: composer, cs2pr
      - run: composer install --prefer-dist --no-progress
      - run: vendor/bin/phpcs -q --report=checkstyle | cs2pr

  unit-tests:
    name: Unit Tests (WP_Mock)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          tools: composer
      - run: composer install --prefer-dist --no-progress
      - run: vendor/bin/phpunit -c phpunit-wp-mock.xml.dist --testdox

  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        php: ['8.1', '8.3']
        wordpress: ['6.5', 'latest']
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: wordpress_test
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          extensions: mysqli
          tools: composer
          coverage: xdebug
      - run: composer install --prefer-dist --no-progress
      - run: bash bin/install-wp-tests.sh wordpress_test root root 127.0.0.1:3306 ${{ matrix.wordpress }}
      - run: vendor/bin/phpunit --coverage-clover=coverage.xml
      - uses: codecov/codecov-action@v4
        if: matrix.php == '8.3' && matrix.wordpress == 'latest'
        with:
          files: ./coverage.xml

  deploy-ready:
    name: Deployment Check
    needs: [coding-standards, unit-tests, integration-tests]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - run: echo "All checks passed - ready for deployment"
```

---

## Testing Best Practices

### Test Naming Conventions

**Method Naming Pattern:**
```
test_[method_name]_[scenario]_[expected_result]
```

**Examples:**

```php
// ✅ GOOD: Descriptive test names
public function test_sanitize_email_with_valid_email_returns_email() {}
public function test_sanitize_email_with_invalid_email_returns_empty_string() {}
public function test_save_post_meta_with_valid_data_returns_true() {}
public function test_user_login_with_wrong_password_returns_wp_error() {}

// ❌ BAD: Vague test names
public function test_email() {}
public function test_function() {}
public function test_it_works() {}
```

**Class Naming:**
```php
// Pattern: Test_[ClassName]
class Test_Email_Service extends WP_UnitTestCase {}
class Test_Data_Validator extends WP_Mock\Tools\TestCase {}
class Test_Post_Meta_Handler extends WP_UnitTestCase {}
```

### Arrange-Act-Assert Pattern

**Structure Every Test:**

```php
public function test_calculate_discount() {
    // ARRANGE: Set up test data and conditions
    $original_price = 100;
    $discount_percent = 20;
    $calculator = new MyPlugin\PriceCalculator();

    // ACT: Execute the code being tested
    $discounted_price = $calculator->apply_discount($original_price, $discount_percent);

    // ASSERT: Verify expected outcome
    $this->assertEquals(80, $discounted_price);
}
```

**Complete Example:**

```php
public function test_save_user_preferences_updates_database() {
    // ARRANGE
    $user_id = $this->factory->user->create();
    $preferences = [
        'theme' => 'dark',
        'notifications' => true,
    ];
    $service = new MyPlugin\UserPreferences();

    // ACT
    $result = $service->save_preferences($user_id, $preferences);

    // ASSERT
    $this->assertTrue($result);
    $saved_prefs = get_user_meta($user_id, 'preferences', true);
    $this->assertEquals('dark', $saved_prefs['theme']);
    $this->assertTrue($saved_prefs['notifications']);
}
```

### Data Providers

**Purpose:** Test same logic with multiple inputs

```php
/**
 * @dataProvider email_validation_provider
 */
public function test_email_validation($email, $expected) {
    $validator = new MyPlugin\Validator();
    $result = $validator->is_valid_email($email);
    $this->assertEquals($expected, $result);
}

/**
 * Data provider for email validation tests
 */
public function email_validation_provider(): array {
    return [
        'valid email' => ['user@example.com', true],
        'invalid no at' => ['userexample.com', false],
        'invalid no domain' => ['user@', false],
        'invalid spaces' => ['user @example.com', false],
        'valid subdomain' => ['user@mail.example.com', true],
        'invalid special chars' => ['user#@example.com', false],
    ];
}
```

**Complex Data Provider:**

```php
/**
 * @dataProvider discount_calculation_provider
 */
public function test_discount_calculation($price, $discount, $expected) {
    $calculator = new MyPlugin\PriceCalculator();
    $result = $calculator->apply_discount($price, $discount);
    $this->assertEquals($expected, $result);
}

public function discount_calculation_provider(): array {
    return [
        '20% off 100' => [100, 20, 80],
        '50% off 100' => [100, 50, 50],
        '0% off 100' => [100, 0, 100],
        '100% off 100' => [100, 100, 0],
        '20% off 0' => [0, 20, 0],
    ];
}
```

### Testing Hooks and Filters

**Testing add_action/add_filter:**

```php
public function test_init_hooks_registered() {
    // Remove all hooks first
    remove_all_actions('init');

    // Register plugin hooks
    MyPlugin\Hooks::register();

    // Verify action was added
    $this->assertTrue(has_action('init', 'MyPlugin\PostTypes::register'));
    $this->assertEquals(10, has_action('init', 'MyPlugin\PostTypes::register'));
}

public function test_content_filter_registered() {
    remove_all_filters('the_content');

    MyPlugin\Hooks::register();

    $this->assertTrue(has_filter('the_content', 'MyPlugin\Content::add_reading_time'));
}
```

**Testing Hook Callbacks:**

```php
public function test_save_post_hook_saves_meta() {
    $post_id = $this->factory->post->create([
        'post_type' => 'book',
    ]);

    $_POST['book_isbn'] = '978-3-16-148410-0';
    $_POST['book_nonce'] = wp_create_nonce('save_book_meta');

    // Manually trigger the hook callback
    do_action('save_post', $post_id);

    // Verify meta was saved
    $isbn = get_post_meta($post_id, '_isbn', true);
    $this->assertEquals('978-3-16-148410-0', $isbn);
}
```

### Testing AJAX Handlers

**AJAX Test Setup:**

```php
public function test_ajax_load_more_posts() {
    // Create test posts
    $post_ids = $this->factory->post->create_many(5);

    // Set up AJAX request
    $_POST['action'] = 'load_more_posts';
    $_POST['page'] = 1;
    $_POST['nonce'] = wp_create_nonce('load_more_nonce');

    // Set current user (if authentication required)
    wp_set_current_user($this->factory->user->create(['role' => 'subscriber']));

    // Capture output
    try {
        $this->_handleAjax('load_more_posts');
    } catch (WPAjaxDieContinueException $e) {
        // Expected exception
    }

    // Get response
    $response = json_decode($this->_last_response, true);

    $this->assertTrue($response['success']);
    $this->assertCount(5, $response['data']['posts']);
}
```

---

## Common Testing Patterns

### Testing Custom Post Types

```php
class Test_Book_Post_Type extends WP_UnitTestCase {

    public function setUp(): void {
        parent::setUp();
        // Ensure CPT is registered
        MyPlugin\PostTypes::register_book();
    }

    public function test_book_post_type_exists() {
        $this->assertTrue(post_type_exists('book'));
    }

    public function test_book_supports_features() {
        $post_type = get_post_type_object('book');

        $this->assertTrue(post_type_supports('book', 'title'));
        $this->assertTrue(post_type_supports('book', 'editor'));
        $this->assertTrue(post_type_supports('book', 'thumbnail'));
        $this->assertFalse(post_type_supports('book', 'comments'));
    }

    public function test_book_has_rest_support() {
        $post_type = get_post_type_object('book');
        $this->assertTrue($post_type->show_in_rest);
    }

    public function test_create_book_post() {
        $book_id = $this->factory->post->create([
            'post_type' => 'book',
            'post_title' => 'The Great Gatsby',
        ]);

        $book = get_post($book_id);
        $this->assertEquals('book', $book->post_type);
        $this->assertEquals('The Great Gatsby', $book->post_title);
    }
}
```

### Testing Settings/Options

```php
class Test_Plugin_Settings extends WP_UnitTestCase {

    public function tearDown(): void {
        delete_option('my_plugin_settings');
        parent::tearDown();
    }

    public function test_default_settings_created() {
        $settings = MyPlugin\Settings::get_defaults();

        $this->assertIsArray($settings);
        $this->assertArrayHasKey('api_key', $settings);
        $this->assertEquals('', $settings['api_key']);
    }

    public function test_save_settings() {
        $new_settings = [
            'api_key' => 'test_key_123',
            'enabled' => true,
        ];

        $result = MyPlugin\Settings::save($new_settings);
        $this->assertTrue($result);

        $saved = get_option('my_plugin_settings');
        $this->assertEquals('test_key_123', $saved['api_key']);
        $this->assertTrue($saved['enabled']);
    }

    public function test_sanitize_settings() {
        $dirty_input = [
            'api_key' => '<script>alert("xss")</script>',
            'enabled' => 'yes',
        ];

        $clean = MyPlugin\Settings::sanitize($dirty_input);

        $this->assertEquals('alert("xss")', $clean['api_key']);
        $this->assertTrue($clean['enabled']);
    }
}
```

### Testing Database Operations

```php
class Test_Database_Operations extends WP_UnitTestCase {

    protected static $table_name;

    public static function setUpBeforeClass(): void {
        parent::setUpBeforeClass();

        global $wpdb;
        self::$table_name = $wpdb->prefix . 'plugin_logs';

        $charset_collate = $wpdb->get_charset_collate();
        $sql = "CREATE TABLE " . self::$table_name . " (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            user_id bigint(20) unsigned NOT NULL,
            action varchar(50) NOT NULL,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY  (id)
        ) $charset_collate;";

        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        dbDelta($sql);
    }

    public static function tearDownAfterClass(): void {
        global $wpdb;
        $wpdb->query("DROP TABLE IF EXISTS " . self::$table_name);
        parent::tearDownAfterClass();
    }

    public function test_insert_log_entry() {
        global $wpdb;

        $user_id = 1;
        $action = 'user_login';

        $result = $wpdb->insert(
            self::$table_name,
            [
                'user_id' => $user_id,
                'action' => $action,
            ],
            ['%d', '%s']
        );

        $this->assertEquals(1, $result);
        $this->assertGreaterThan(0, $wpdb->insert_id);

        // Verify data
        $log = $wpdb->get_row(
            $wpdb->prepare(
                "SELECT * FROM " . self::$table_name . " WHERE id = %d",
                $wpdb->insert_id
            )
        );

        $this->assertEquals($user_id, $log->user_id);
        $this->assertEquals($action, $log->action);
    }

    public function test_query_logs_by_user() {
        global $wpdb;

        $user_id = 42;

        // Insert test data
        $wpdb->insert(self::$table_name, ['user_id' => $user_id, 'action' => 'login'], ['%d', '%s']);
        $wpdb->insert(self::$table_name, ['user_id' => $user_id, 'action' => 'logout'], ['%d', '%s']);

        // Query logs
        $logs = $wpdb->get_results(
            $wpdb->prepare(
                "SELECT * FROM " . self::$table_name . " WHERE user_id = %d",
                $user_id
            )
        );

        $this->assertCount(2, $logs);
    }
}
```

### Testing REST API Endpoints

```php
class Test_REST_API extends WP_UnitTestCase {

    protected $server;

    public function setUp(): void {
        parent::setUp();

        global $wp_rest_server;
        $this->server = $wp_rest_server = new WP_REST_Server();
        do_action('rest_api_init');
    }

    public function test_endpoint_registered() {
        $routes = $this->server->get_routes();
        $this->assertArrayHasKey('/myplugin/v1/items', $routes);
    }

    public function test_get_items_endpoint() {
        // Create test posts
        $post_ids = $this->factory->post->create_many(3, ['post_type' => 'book']);

        $request = new WP_REST_Request('GET', '/myplugin/v1/items');
        $response = $this->server->dispatch($request);

        $this->assertEquals(200, $response->get_status());

        $data = $response->get_data();
        $this->assertCount(3, $data);
    }

    public function test_create_item_requires_authentication() {
        $request = new WP_REST_Request('POST', '/myplugin/v1/items');
        $request->set_body_params([
            'title' => 'New Item',
        ]);

        $response = $this->server->dispatch($request);

        $this->assertEquals(401, $response->get_status());
    }

    public function test_create_item_with_authentication() {
        $user_id = $this->factory->user->create(['role' => 'editor']);
        wp_set_current_user($user_id);

        $request = new WP_REST_Request('POST', '/myplugin/v1/items');
        $request->set_body_params([
            'title' => 'New Item',
            'content' => 'Item content',
        ]);

        $response = $this->server->dispatch($request);

        $this->assertEquals(201, $response->get_status());

        $data = $response->get_data();
        $this->assertEquals('New Item', $data['title']);
    }
}
```

---

**Related Skills:**
When testing WordPress applications, consider these complementary skills (available in the skill library):

- **WordPress Plugin Fundamentals**: Core plugin architecture and hooks - essential foundation for understanding what to test
- **WordPress Security & Validation**: Security patterns and data validation - critical for security testing strategies
- **Python pytest Testing**: Modern testing patterns - concepts applicable to WordPress testing approaches
- **GitHub Actions CI/CD**: CI/CD automation - integrate WordPress tests into automated pipelines

**Further Reading:**
- [WordPress PHPUnit Documentation](https://make.wordpress.org/core/handbook/testing/automated-testing/writing-phpunit-tests/)
- [WP_Mock GitHub Repository](https://github.com/10up/wp_mock)
- [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/)
- [PHPUnit Documentation](https://phpunit.de/documentation.html)
