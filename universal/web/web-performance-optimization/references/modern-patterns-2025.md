# Modern Performance Patterns (2025)

Cutting-edge browser APIs and patterns for optimal web performance in 2025.

## View Transitions API (2024+)

**Purpose:** Smooth page transitions without JavaScript framework overhead

**Browser support:** Chrome 111+, Edge 111+ (March 2023+)

### Basic Implementation

```css
/* Enable automatic view transitions for navigation */
@view-transition {
  navigation: auto;
}
```

That's it! This single line enables smooth cross-document transitions.

### How It Works

1. Browser captures current page state (screenshot)
2. Navigate to new page
3. Browser animates between states
4. Zero JavaScript required

**Impact:**
- Perceived performance boost (feels instant)
- No runtime JavaScript cost
- Native browser optimization
- Works across page navigations

### Custom Animations

```css
/* Customize transition animations */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}

/* Slide animation */
::view-transition-old(root) {
  animation-name: slide-out-to-left;
}

::view-transition-new(root) {
  animation-name: slide-in-from-right;
}

@keyframes slide-out-to-left {
  to {
    transform: translateX(-100%);
  }
}

@keyframes slide-in-from-right {
  from {
    transform: translateX(100%);
  }
}
```

### Element-Specific Transitions

```css
/* Target specific elements */
.card {
  view-transition-name: card-transition;
}

::view-transition-old(card-transition),
::view-transition-new(card-transition) {
  animation-duration: 0.5s;
  animation-timing-function: ease-in-out;
}
```

### JavaScript Control (Optional)

```javascript
// Programmatic control
document.startViewTransition(() => {
  // Update DOM here
  updateContent();
});

// With promise
async function navigate() {
  const transition = document.startViewTransition(() => {
    // DOM updates
  });

  await transition.finished;
  console.log('Transition complete');
}
```

### Use Cases

- **Multi-page applications (MPA)** - Native smooth navigation
- **SPA-like experience** - Without SPA complexity
- **Image galleries** - Smooth image transitions
- **Product pages** - Seamless category navigation

### Performance Characteristics

- **Runtime cost:** ~0ms (native browser feature)
- **Compatibility:** Progressive enhancement (graceful degradation)
- **Network impact:** None (purely visual)

---

## Speculation Rules API (Chrome 121+, December 2023)

**Purpose:** Prerender pages for instant navigation

**Browser support:** Chrome 121+, Edge 121+

### Prefetch vs Prerender Decision Tree

```
Is the page likely to be visited?
├─ YES, very likely (>50% probability)
│  └─ Use PRERENDER (full page load in background)
└─ NO, maybe (20-50% probability)
   └─ Use PREFETCH (fetch resources only)
```

### Basic Prefetch

```html
<script type="speculationrules">
{
  "prefetch": [
    {
      "urls": ["/about", "/contact"]
    }
  ]
}
</script>
```

**What happens:** Browser fetches HTML, CSS, JS (no execution)

### Prerender for Instant Navigation

```html
<script type="speculationrules">
{
  "prerender": [
    {
      "urls": ["/product/123"]
    }
  ]
}
</script>
```

**What happens:** Full page render in background, instant show on navigation

**Impact:** 0ms navigation time (feels instant)

### Dynamic Rules Based on User Behavior

```html
<script type="speculationrules">
{
  "prerender": [
    {
      "where": {
        "and": [
          {"href_matches": "/products/*"},
          {"selector_matches": "a:hover"}
        ]
      }
    }
  ]
}
</script>
```

This prerenders product pages when user hovers over links!

### Budget Constraints

```javascript
// Set limits to avoid resource waste
{
  "prerender": [
    {
      "urls": ["/important-page"],
      "requires": ["anonymous-client-ip-when-cross-origin"]
    }
  ],
  "prefetch": [
    {
      "urls": ["/maybe-visited"],
      "eagerness": "moderate"  // conservative | moderate | eager
    }
  ]
}
```

### Eagerness Levels

| Level | When Triggered | Use Case |
|-------|----------------|----------|
| `immediate` | On page load | Critical next page |
| `eager` | Link visible in viewport | High probability |
| `moderate` | Mouse pointer near link | Medium probability |
| `conservative` | Mouse/touch down on link | Low resource use |

### Measuring Impact

```javascript
// Track prerender success
document.addEventListener('prerenderingchange', () => {
  if (document.prerendering) {
    console.log('Page is prerendering');
  } else {
    console.log('Page activated from prerender');
    // Track instant navigation
    analytics.track('instant_navigation');
  }
});

// Check if page was prerendered
if (document.wasPrerendered) {
  console.log('This page was prerendered');
}
```

### Performance Characteristics

- **0ms navigation** for prerendered pages
- **CPU cost** during prerender (user not waiting)
- **Memory cost** per prerendered page
- **Network cost** if page not visited

### Best Practices

1. **Prerender high-probability pages only** (>50% visit rate)
2. **Prefetch medium-probability pages** (20-50% visit rate)
3. **Monitor resource usage** (CPU, memory, network)
4. **Respect user data preferences** (check `navigator.connection`)
5. **Consider Analytics impact** (prerendered pages trigger page views)

---

## React Server Components (RSC)

**Purpose:** Zero-bundle server-only components

**Availability:** Next.js 13+ (App Router), React 19+

### The Problem

Traditional React: **All components ship to browser**

```jsx
// Traditional Client Component - 100KB bundle
import { Chart } from 'heavy-charting-library';  // 80KB

export default function Dashboard() {
  const data = fetchData();  // This runs client-side
  return <Chart data={data} />;
}
```

Bundle includes: React + Chart library + your code = **100KB+**

### The Solution: Server Components

```jsx
// Server Component - 0KB JavaScript!
import { Chart } from 'heavy-charting-library';  // Runs server-side only

export default async function Dashboard() {
  const data = await fetchData();  // Server-side data fetching
  return <Chart data={data} />;  // Rendered to HTML
}
```

Bundle: **0KB JavaScript** (Chart library never sent to client)

### When to Use Each

```jsx
// app/layout.tsx - Server Component (default)
export default function Layout({ children }) {
  return (
    <html>
      <body>
        <Header />  {/* Server Component */}
        {children}
        <Footer />  {/* Server Component */}
      </body>
    </html>
  );
}

// app/interactive-widget.tsx - Client Component
'use client';  // Opt into client rendering

import { useState } from 'react';

export default function InteractiveWidget() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Decision Tree

```
Does component need:
- Browser APIs (window, localStorage)?
- Event handlers (onClick, onChange)?
- React hooks (useState, useEffect)?
- Third-party interactive libraries?

├─ YES → Client Component ('use client')
└─ NO → Server Component (default, zero JS)
```

### Bundle Impact Analysis

**Before (All Client Components):**
- React core: 45KB
- Component libraries: 80KB
- Application code: 120KB
- **Total:** 245KB

**After (Server Components + Selective Client):**
- React core: 45KB
- Interactive widgets only: 20KB
- Application code (client): 30KB
- **Total:** 95KB (61% reduction)

### Streaming SSR with Suspense

```jsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <>
      <Header />  {/* Renders immediately */}

      <Suspense fallback={<Skeleton />}>
        <SlowComponent />  {/* Streams in when ready */}
      </Suspense>

      <Footer />  {/* Renders immediately */}
    </>
  );
}
```

**Performance gain:** Time to First Byte unaffected, progressive rendering

---

## Priority Hints API

**Purpose:** Control resource loading priority

**Browser support:** Chrome 101+, Edge 101+, Safari 17.2+

### `fetchpriority` Attribute

```html
<!-- ❌ BAD: All images same priority -->
<img src="hero.jpg" alt="Hero">
<img src="thumbnail-1.jpg" alt="Thumbnail">
<img src="thumbnail-2.jpg" alt="Thumbnail">

<!-- ✅ GOOD: Prioritize LCP image -->
<img src="hero.jpg" alt="Hero" fetchpriority="high">
<img src="thumbnail-1.jpg" alt="Thumbnail" fetchpriority="low">
<img src="thumbnail-2.jpg" alt="Thumbnail" fetchpriority="low">
```

**Impact on LCP:** 200-400ms improvement

### Script Prioritization

```html
<!-- High priority: Critical scripts -->
<script src="critical.js" fetchpriority="high"></script>

<!-- Low priority: Analytics, ads -->
<script src="analytics.js" fetchpriority="low" async></script>
```

### CSS Prioritization

```html
<!-- High priority: Critical styles -->
<link rel="stylesheet" href="critical.css" fetchpriority="high">

<!-- Low priority: Print styles -->
<link rel="stylesheet" href="print.css" fetchpriority="low" media="print">
```

### Preload with Priority

```html
<!-- High priority preload for LCP image -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high">

<!-- Low priority preload for below-fold -->
<link rel="preload" as="image" href="footer-logo.webp" fetchpriority="low">
```

---

## `blocking="render"` for Critical CSS

**Purpose:** Block rendering until critical CSS loads (better than inline)

**Browser support:** Chrome 105+, Firefox 120+

```html
<!-- ❌ OLD: Inline critical CSS -->
<style>
  /* Thousands of lines of CSS... */
</style>

<!-- ✅ NEW: External critical CSS with render blocking -->
<link rel="stylesheet" href="critical.css" blocking="render">
```

**Benefits:**
- Cacheable (unlike inline CSS)
- Smaller HTML
- Still blocks render (prevents FOUC)

---

## `content-visibility` for Rendering Optimization

**Purpose:** Skip rendering off-screen content

**Browser support:** Chrome 85+, Edge 85+

### Basic Pattern

```css
.article-section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;  /* Estimated height */
}
```

**Impact:** 7x faster rendering for long pages

### How It Works

1. Browser skips rendering off-screen sections
2. Reserves space (contain-intrinsic-size) to prevent layout shifts
3. Renders sections as they enter viewport

### Use Cases

```css
/* Long list of items */
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 200px;
}

/* Blog articles with many sections */
.blog-section {
  content-visibility: auto;
  contain-intrinsic-size: 0 600px;
}

/* Product grid */
.product-card {
  content-visibility: auto;
  contain-intrinsic-size: 0 400px;
}
```

### Performance Metrics

**Without content-visibility:**
- Initial render: 450ms
- Layout time: 280ms

**With content-visibility:**
- Initial render: 65ms (85% faster)
- Layout time: 40ms (86% faster)

---

## Islands Architecture

**Purpose:** Selective hydration for minimal JavaScript

**Frameworks:** Astro, Qwik, Fresh

### The Problem

Traditional SSR: **Hydrate entire page** (all components become interactive)

```jsx
// Traditional: Everything hydrates (500KB JS)
<Header />          {/* Hydrates (static, why?) */}
<Hero />            {/* Hydrates (static, why?) */}
<InteractiveForm /> {/* Needs hydration */}
<Footer />          {/* Hydrates (static, why?) */}
```

Total JavaScript: **500KB**

### The Solution: Islands

```astro
---
import Header from './Header.astro';  // Static
import Hero from './Hero.astro';      // Static
import Form from './Form.jsx';        // Interactive island
import Footer from './Footer.astro';  // Static
---

<Header />
<Hero />
<Form client:visible />  {/* Only this hydrates! */}
<Footer />
```

Total JavaScript: **20KB** (96% reduction)

### Hydration Strategies

```astro
<!-- Load immediately -->
<Component client:load />

<!-- Load when idle (after page interactive) -->
<Component client:idle />

<!-- Load when visible in viewport -->
<Component client:visible />

<!-- Load on media query match -->
<Component client:media="(max-width: 768px)" />

<!-- Never hydrate (static HTML only) -->
<Component />
```

### Performance Comparison

| Approach | Initial JS | TTI | Use Case |
|----------|-----------|-----|----------|
| **Full SPA** | 500KB | 3.5s | Highly interactive apps |
| **Traditional SSR** | 500KB | 2.8s | Interactive pages |
| **Partial Hydration** | 150KB | 1.2s | Mixed static/interactive |
| **Islands** | 20KB | 0.3s | Mostly static content |

### Real-World Example: Blog

```astro
---
// Blog post page - 98% static content
---
<html>
  <StaticHeader />
  <StaticNav />

  <article>
    <StaticBlogContent />

    <!-- Only interactive parts hydrate -->
    <LikeButton client:visible />
    <CommentSection client:idle />
    <ShareButtons client:visible />
  </article>

  <StaticFooter />
</html>
```

**Result:** 
- Before: 450KB JavaScript
- After: 35KB JavaScript (92% reduction)
- TTI: 3.2s → 0.4s

---

## Summary: 2025 Performance Stack

| Pattern | Browser Support | Impact | Complexity |
|---------|----------------|--------|------------|
| **View Transitions** | Chrome 111+ | High (UX) | Low |
| **Speculation Rules** | Chrome 121+ | Extreme (0ms nav) | Low |
| **Server Components** | Next.js 13+, React 19+ | Very High (bundle) | Medium |
| **Priority Hints** | Chrome 101+, Safari 17.2+ | High (LCP) | Low |
| **blocking="render"** | Chrome 105+, Firefox 120+ | Medium (FOUC) | Low |
| **content-visibility** | Chrome 85+ | High (render) | Low |
| **Islands** | Framework-dependent | Extreme (bundle) | High |

**Recommendation:** Start with Priority Hints and View Transitions (low complexity, high impact). Progress to Speculation Rules and Server Components for maximum performance gains.

---

**Remember:** These patterns are progressive enhancements. Sites work without them, but users get dramatically better experience when supported.