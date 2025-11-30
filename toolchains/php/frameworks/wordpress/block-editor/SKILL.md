---
name: wordpress-block-editor-fse
description: Modern WordPress block development and Full Site Editing with theme.json, block themes, and custom blocks for WordPress 6.7+. Use this skill when building block themes with FSE architecture, creating custom Gutenberg blocks, or implementing centralized styling with theme.json.
version: 1.0.0
category: development
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "WordPress 6.7+ block development: FSE with theme.json, custom blocks (block.json + render.php), HTML templates"
    when_to_use:
      - "Block themes with FSE (WP 6.2+)"
      - "Custom Gutenberg blocks"
      - "Centralized theme.json styling"
    quick_start:
      - "theme.json for design tokens"
      - "block.json + render.php"
      - "HTML templates not PHP"
  references:
    - theme-json-schema.md
    - custom-blocks-guide.md
    - fse-architecture.md
    - migration-guide.md
context_limit: 6000
tags:
  - wordpress
  - gutenberg
  - blocks
  - fse
  - theme-json
  - php
  - react
requires_tools: []
---

# WordPress Block Editor & Full Site Editing

## Overview

Full Site Editing (FSE) is production-ready (since WP 6.2) and treats everything as blocks—headers, footers, templates, not just content. Block themes use HTML templates + theme.json instead of PHP files + style.css.

**Key Components:**
- **theme.json**: Centralized colors, typography, spacing, layout
- **HTML Templates**: Block-based files (index.html, single.html)
- **Template Parts**: Reusable components (header.html, footer.html)
- **Block Patterns**: Pre-designed block layouts
- **Site Editor**: Visual template customization

**When to Use:**
✅ New themes, consistent design systems, non-technical user customization
❌ Complex server logic, team unfamiliar with blocks, heavy PHP dependencies

## Full Site Editing Architecture

### Block Themes vs Classic Themes

| Block Themes | Classic Themes |
|-------------|----------------|
| HTML files with blocks | PHP files with template tags |
| theme.json + CSS | functions.php + style.css |
| Site Editor (visual) | Customizer (settings) |
| User edits templates | Limited customization |

### Site Editor Capabilities
- Template editing (pages, posts, archives)
- Template parts (header/footer variations)
- Global styles (colors, typography site-wide)
- Pattern library (save/reuse block compositions)
- Navigation menus (block-based)
- Style variations (alternate design presets)

## theme.json Configuration

theme.json v3 (WP 6.7) provides centralized design control. WordPress auto-generates CSS custom properties.

### Production Example

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "appearanceTools": true,
    "useRootPaddingAwareAlignments": true,
    "layout": {
      "contentSize": "800px",
      "wideSize": "1200px"
    },
    "color": {
      "palette": [
        { "slug": "primary", "color": "#0073aa", "name": "Primary" },
        { "slug": "secondary", "color": "#005177", "name": "Secondary" },
        { "slug": "base", "color": "#ffffff", "name": "Base" },
        { "slug": "contrast", "color": "#000000", "name": "Contrast" }
      ],
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
        { "slug": "small", "size": "0.875rem", "name": "Small" },
        { "slug": "medium", "size": "1rem", "name": "Medium" },
        {
          "slug": "large",
          "size": "1.5rem",
          "name": "Large",
          "fluid": { "min": "1.25rem", "max": "1.5rem" }
        }
      ],
      "fontWeight": true,
      "lineHeight": true
    },
    "spacing": {
      "units": ["px", "em", "rem", "vh", "vw", "%"],
      "padding": true,
      "margin": true,
      "spacingSizes": [
        { "slug": "30", "size": "0.5rem", "name": "XS" },
        { "slug": "40", "size": "1rem", "name": "S" },
        { "slug": "50", "size": "1.5rem", "name": "M" },
        { "slug": "60", "size": "2rem", "name": "L" }
      ]
    },
    "border": { "radius": true, "color": true, "width": true }
  },
  "styles": {
    "color": {
      "background": "var(--wp--preset--color--base)",
      "text": "var(--wp--preset--color--contrast)"
    },
    "typography": {
      "fontFamily": "var(--wp--preset--font-family--system)",
      "fontSize": "var(--wp--preset--font-size--medium)",
      "lineHeight": "1.6"
    },
    "elements": {
      "link": {
        "color": { "text": "var(--wp--preset--color--primary)" },
        ":hover": {
          "color": { "text": "var(--wp--preset--color--secondary)" }
        }
      },
      "h1": {
        "typography": {
          "fontSize": "var(--wp--preset--font-size--large)",
          "fontWeight": "700"
        }
      },
      "button": {
        "color": {
          "background": "var(--wp--preset--color--primary)",
          "text": "var(--wp--preset--color--base)"
        },
        "border": { "radius": "4px" },
        ":hover": {
          "color": { "background": "var(--wp--preset--color--secondary)" }
        }
      }
    },
    "blocks": {
      "core/quote": {
        "border": {
          "width": "0 0 0 4px",
          "color": "var(--wp--preset--color--primary)"
        },
        "spacing": { "padding": { "left": "var(--wp--preset--spacing--60)" } }
      }
    }
  },
  "customTemplates": [
    {
      "name": "page-wide",
      "title": "Full Width Page",
      "postTypes": ["page"]
    }
  ]
}
```

### CSS Custom Properties Auto-Generated
- Colors: `var(--wp--preset--color--primary)`
- Fonts: `var(--wp--preset--font-family--system)`
- Sizes: `var(--wp--preset--font-size--large)`
- Spacing: `var(--wp--preset--spacing--50)`

### Fluid Typography
Font sizes with `fluid: { min, max }` auto-scale using `clamp()`:
```json
{
  "slug": "large",
  "size": "1.5rem",
  "fluid": { "min": "1.25rem", "max": "1.5rem" }
}
```

## Block Theme Architecture

### Required Files

```
my-block-theme/
├── style.css                 # Theme metadata (REQUIRED)
├── theme.json                # Settings/styles (REQUIRED)
├── templates/
│   ├── index.html           # Fallback (REQUIRED)
│   ├── single.html
│   ├── page.html
│   └── archive.html
├── parts/
│   ├── header.html
│   └── footer.html
├── patterns/                 # Block patterns
│   └── hero.php
└── functions.php             # Optional setup
```

### style.css Metadata

```css
/*
Theme Name: My Block Theme
Requires at least: 6.4
Requires PHP: 8.1
Version: 1.0.0
*/
```

### HTML Template Structure

**templates/single.html:**
```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
  <!-- wp:post-title {"level":1} /-->
  <!-- wp:post-featured-image /-->
  <!-- wp:post-content /-->
  <!-- wp:post-date /-->
</div>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

**templates/index.html (with query loop):**
```html
<!-- wp:template-part {"slug":"header"} /-->

<!-- wp:group {"tagName":"main"} -->
<main class="wp-block-group">
  <!-- wp:query {"queryId":1,"query":{"perPage":10,"postType":"post"}} -->
  <div class="wp-block-query">
    <!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->
      <!-- wp:post-featured-image {"isLink":true} /-->
      <!-- wp:post-title {"isLink":true} /-->
      <!-- wp:post-excerpt /-->
    <!-- /wp:post-template -->

    <!-- wp:query-pagination -->
      <!-- wp:query-pagination-previous /-->
      <!-- wp:query-pagination-numbers /-->
      <!-- wp:query-pagination-next /-->
    <!-- /wp:query-pagination -->
  </div>
  <!-- /wp:query -->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer"} /-->
```

### Template Parts

**parts/header.html:**
```html
<!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between"}} -->
<div class="wp-block-group">
  <!-- wp:site-logo {"width":60} /-->
  <!-- wp:navigation /-->
</div>
<!-- /wp:group -->
```

### Block Patterns

**patterns/hero.php:**
```php
<?php
/**
 * Title: Hero Section
 * Slug: my-theme/hero
 * Categories: featured
 */
?>
<!-- wp:cover {"url":"<?php echo esc_url(get_template_directory_uri()); ?>/assets/images/hero.jpg","dimRatio":50,"minHeight":500,"align":"full"} -->
<div class="wp-block-cover alignfull">
  <div class="wp-block-cover__inner-container">
    <!-- wp:heading {"textAlign":"center","level":1,"fontSize":"xx-large"} -->
    <h1>Welcome to Our Site</h1>
    <!-- /wp:heading -->

    <!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
    <div class="wp-block-buttons">
      <!-- wp:button -->
      <div class="wp-block-button"><a class="wp-block-button__link">Get Started</a></div>
      <!-- /wp:button -->
    </div>
    <!-- /wp:buttons -->
  </div>
</div>
<!-- /wp:cover -->
```

**Register pattern categories:**
```php
add_action('init', 'register_pattern_categories');
function register_pattern_categories() {
  register_block_pattern_category('hero', [
    'label' => __('Hero Sections', 'my-theme')
  ]);
  register_block_pattern_category('cta', [
    'label' => __('Call to Action', 'my-theme')
  ]);
}
```

## Custom Block Development

### block.json Metadata (Block API v3)

**blocks/testimonial/block.json:**
```json
{
  "$schema": "https://schemas.wp.org/trunk/block.json",
  "apiVersion": 3,
  "name": "my-theme/testimonial",
  "title": "Testimonial",
  "category": "widgets",
  "icon": "format-quote",
  "attributes": {
    "content": {
      "type": "string",
      "source": "html",
      "selector": ".testimonial-content"
    },
    "author": { "type": "string", "default": "" },
    "role": { "type": "string", "default": "" },
    "rating": { "type": "number", "default": 5 }
  },
  "supports": {
    "html": false,
    "align": ["wide", "full"],
    "color": { "background": true, "text": true },
    "spacing": { "padding": true, "margin": true }
  },
  "render": "file:./render.php"
}
```

### Attribute Sources

Different ways to extract data from HTML:
```json
"attributes": {
  "title": {
    "type": "string",
    "source": "html",
    "selector": "h2"
  },
  "linkUrl": {
    "type": "string",
    "source": "attribute",
    "selector": "a",
    "attribute": "href"
  },
  "isActive": {
    "type": "boolean",
    "default": false
  },
  "items": {
    "type": "array",
    "source": "query",
    "selector": ".item",
    "query": {
      "text": { "type": "string", "source": "text" }
    }
  }
}
```

### Server-Side Rendering (render.php)

**blocks/testimonial/render.php:**
```php
<?php
$content = $attributes['content'] ?? '';
$author = $attributes['author'] ?? '';
$role = $attributes['role'] ?? '';
$rating = absint($attributes['rating'] ?? 5);

$wrapper_attributes = get_block_wrapper_attributes([
  'class' => 'testimonial-block',
]);
?>

<div <?php echo $wrapper_attributes; ?>>
  <blockquote class="testimonial-content">
    <?php echo wp_kses_post($content); ?>
  </blockquote>

  <?php if ($rating > 0) : ?>
    <div class="testimonial-rating">
      <?php for ($i = 1; $i <= 5; $i++) : ?>
        <span class="star <?php echo $i <= $rating ? 'filled' : 'empty'; ?>">
          <?php echo $i <= $rating ? '★' : '☆'; ?>
        </span>
      <?php endfor; ?>
    </div>
  <?php endif; ?>

  <?php if ($author || $role) : ?>
    <cite class="testimonial-author">
      <span class="author-name"><?php echo esc_html($author); ?></span>
      <?php if ($role) : ?>
        <span class="author-role"><?php echo esc_html($role); ?></span>
      <?php endif; ?>
    </cite>
  <?php endif; ?>
</div>
```

### Client-Side Rendering (React)

**blocks/testimonial/index.js:**
```javascript
import { registerBlockType } from '@wordpress/blocks';
import { useBlockProps, RichText, InspectorControls } from '@wordpress/block-editor';
import { PanelBody, RangeControl, TextControl } from '@wordpress/components';
import { __ } from '@wordpress/i18n';

registerBlockType('my-theme/testimonial', {
  edit: ({ attributes, setAttributes }) => {
    const { content, author, role, rating } = attributes;
    const blockProps = useBlockProps();

    return (
      <>
        <InspectorControls>
          <PanelBody title={__('Settings', 'my-theme')}>
            <TextControl
              label={__('Author', 'my-theme')}
              value={author}
              onChange={(v) => setAttributes({ author: v })}
            />
            <TextControl
              label={__('Role', 'my-theme')}
              value={role}
              onChange={(v) => setAttributes({ role: v })}
            />
            <RangeControl
              label={__('Rating', 'my-theme')}
              value={rating}
              onChange={(v) => setAttributes({ rating: v })}
              min={1}
              max={5}
            />
          </PanelBody>
        </InspectorControls>

        <div {...blockProps}>
          <RichText
            tagName="blockquote"
            value={content}
            onChange={(v) => setAttributes({ content: v })}
            placeholder={__('Testimonial text...', 'my-theme')}
          />

          <div className="testimonial-rating">
            {[1, 2, 3, 4, 5].map((star) => (
              <span
                key={star}
                onClick={() => setAttributes({ rating: star })}
              >
                {star <= rating ? '★' : '☆'}
              </span>
            ))}
          </div>

          <cite>
            <RichText
              tagName="span"
              value={author}
              onChange={(v) => setAttributes({ author: v })}
              placeholder={__('Author', 'my-theme')}
            />
          </cite>
        </div>
      </>
    );
  },
  save: () => null, // Server-side rendering
});
```

### Block Registration

**functions.php:**
```php
add_action('init', 'register_custom_blocks');
function register_custom_blocks() {
  register_block_type(__DIR__ . '/blocks/testimonial');
}
```

### InspectorControls (Settings Sidebar)

Common controls for block settings:
```javascript
import {
  InspectorControls,
  PanelColorSettings,
  MediaUpload
} from '@wordpress/block-editor';
import {
  PanelBody,
  SelectControl,
  ToggleControl,
  RangeControl,
  Button
} from '@wordpress/components';

<InspectorControls>
  <PanelBody title="Layout">
    <SelectControl
      label="Columns"
      value={columns}
      options={[
        { label: '2', value: 2 },
        { label: '3', value: 3 },
        { label: '4', value: 4 }
      ]}
      onChange={(v) => setAttributes({ columns: parseInt(v) })}
    />

    <ToggleControl
      label="Enable Shadow"
      checked={enableShadow}
      onChange={(v) => setAttributes({ enableShadow: v })}
    />

    <RangeControl
      label="Border Radius"
      value={borderRadius}
      onChange={(v) => setAttributes({ borderRadius: v })}
      min={0}
      max={50}
    />
  </PanelBody>

  <PanelBody title="Media">
    <MediaUpload
      onSelect={(media) => setAttributes({ imageUrl: media.url })}
      allowedTypes={['image']}
      render={({ open }) => (
        <Button onClick={open} variant="secondary">
          {imageUrl ? 'Change Image' : 'Select Image'}
        </Button>
      )}
    />
  </PanelBody>

  <PanelColorSettings
    title="Colors"
    colorSettings={[
      {
        value: bgColor,
        onChange: (v) => setAttributes({ bgColor: v }),
        label: 'Background'
      }
    ]}
  />
</InspectorControls>
```

### Block Supports

Enable WordPress features:
```json
"supports": {
  "html": false,
  "anchor": true,
  "align": ["wide", "full"],
  "color": {
    "background": true,
    "text": true,
    "gradients": true
  },
  "spacing": {
    "padding": true,
    "margin": true,
    "blockGap": true
  },
  "typography": {
    "fontSize": true,
    "lineHeight": true,
    "fontWeight": true
  }
}
```

## Custom Post Types with Block Editor

```php
add_action('init', 'register_book_cpt');
function register_book_cpt() {
  register_post_type('book', [
    'labels' => [
      'name' => __('Books', 'my-theme'),
      'singular_name' => __('Book', 'my-theme'),
    ],
    'public' => true,
    'has_archive' => true,
    'supports' => ['title', 'editor', 'thumbnail'],
    'show_in_rest' => true,  // REQUIRED for block editor
    'menu_icon' => 'dashicons-book',
    'template' => [          // Default blocks
      ['core/paragraph', ['placeholder' => 'Book description...']],
      ['core/image'],
      ['my-theme/book-details'],
    ],
    'template_lock' => 'insert', // Can't add/remove blocks
  ]);

  // Register taxonomy
  register_taxonomy('genre', 'book', [
    'labels' => ['name' => __('Genres', 'my-theme')],
    'hierarchical' => true,
    'show_in_rest' => true,  // REQUIRED
  ]);
}
```

### Template Locking
- `false`: No restrictions
- `'all'`: Cannot modify structure
- `'insert'`: Cannot add/remove, can reorder
- `'contentOnly'`: Content edits only

### Register in theme.json
```json
"customTemplates": [
  {
    "name": "single-book",
    "title": "Book Template",
    "postTypes": ["book"]
  }
]
```

## Development Workflow

### @wordpress/scripts

**package.json:**
```json
{
  "scripts": {
    "start": "wp-scripts start",
    "build": "wp-scripts build"
  },
  "devDependencies": {
    "@wordpress/scripts": "^27.0.0"
  }
}
```

**Commands:**
```bash
npm install
npm run start  # Development with hot reload
npm run build  # Production build (minified)
```

### wp-env Setup

**.wp-env.json:**
```json
{
  "core": "WordPress/WordPress#6.7",
  "phpVersion": "8.3",
  "themes": ["./my-block-theme"],
  "config": {
    "WP_DEBUG": true,
    "SCRIPT_DEBUG": true
  }
}
```

**Usage:**
```bash
npx @wordpress/env start
# Access: http://localhost:8888
# Admin: admin / password

npx @wordpress/env stop
npx @wordpress/env clean  # Reset database
```

## Migration from Classic Themes

### Template Tag to Block Mapping

| Classic | Block Equivalent |
|---------|------------------|
| `the_title()` | `<!-- wp:post-title /-->` |
| `the_content()` | `<!-- wp:post-content /-->` |
| `the_post_thumbnail()` | `<!-- wp:post-featured-image /-->` |
| `the_date()` | `<!-- wp:post-date /-->` |
| `wp_nav_menu()` | `<!-- wp:navigation /-->` |
| `get_header()` | `<!-- wp:template-part {"slug":"header"} /-->` |
| `get_footer()` | `<!-- wp:template-part {"slug":"footer"} /-->` |
| `get_sidebar()` | `<!-- wp:template-part {"slug":"sidebar"} /-->` |

### Migration Steps

1. **Extract design tokens** from style.css → theme.json
2. **Convert PHP templates** to HTML block templates
3. **Add block support** in functions.php:
```php
add_theme_support('wp-block-styles');
add_theme_support('align-wide');
add_theme_support('responsive-embeds');
```
4. **Test thoroughly** with real content

### Block Validation

WordPress validates block markup against registered block definitions. Invalid blocks show errors in the editor:

**Common validation errors:**
- Attribute type mismatch (string vs number)
- Missing required attributes
- Incorrect HTML structure
- Changed attribute names

**Fix validation errors:**
```javascript
// Add deprecated versions for backward compatibility
const deprecated = [
  {
    attributes: {
      oldName: { type: 'string' }
    },
    migrate: (attributes) => ({
      newName: attributes.oldName
    }),
    save: (props) => {
      // Old save function
    }
  }
];
```

## Performance & Best Practices

### Performance
✅ Use server-side rendering (render.php) when possible
✅ Leverage block supports (reduces custom CSS)
✅ Disable unused features: `"defaultPalette": false`
✅ Use CSS custom properties for consistency
❌ Avoid client-side rendering for static content
❌ Don't override core blocks with `!important`

### Accessibility
✅ Semantic HTML (`<header>`, `<main>`, `<footer>`)
✅ Keyboard navigation for custom blocks
✅ WCAG AA color contrast (4.5:1 minimum)
✅ Alt text for all images
❌ Don't assume FSE = accessible (test required)

### Anti-Patterns
❌ Mixing classic and block approaches
❌ Hardcoding colors (use CSS variables)
❌ Reinventing block supports
❌ Skipping accessibility testing
❌ Using `get_header()` in HTML templates

## Related Skills
- **wordpress-plugin-fundamentals**: Hook system, CPTs
- **react**: Block editor components
- **typescript**: Type-safe block development
- **php-security**: Sanitize block attributes

## Key Reminders
1. theme.json is mandatory for block themes
2. HTML templates replace PHP in FSE
3. Server-side rendering often better than client-side
4. Block supports reduce custom code
5. Accessibility requires testing

## Red Flags
- More than 5 CSS files → Use theme.json
- PHP tags in HTML templates → Use blocks
- Client rendering for static content → Use render.php
- No keyboard testing → Accessibility issues
- Hardcoded values → Use CSS custom properties

---
**WordPress:** 6.7+ | **PHP:** 8.1+ | **Tools:** @wordpress/scripts, wp-env
