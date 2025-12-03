# Core Web Vitals Deep Dive

Comprehensive guide to understanding and optimizing Google's Core Web Vitals metrics.

## Overview

Core Web Vitals are user-centric performance metrics that measure:
- **Loading performance** (LCP - Largest Contentful Paint)
- **Interactivity** (INP - Interaction to Next Paint)
- **Visual stability** (CLS - Cumulative Layout Shift)

These metrics are SEO ranking factors (since June 2021) and directly correlate with user satisfaction and conversions.

**Business Impact:**
- 100ms improvement in LCP = 1% increase in conversion rate
- CLS >0.25 = 24% higher bounce rate
- Poor Core Web Vitals = lower Google search rankings

---

## Table of Contents

1. [LCP (Largest Contentful Paint)](#lcp-largest-contentful-paint)
2. [INP (Interaction to Next Paint)](#inp-interaction-to-next-paint)
3. [CLS (Cumulative Layout Shift)](#cls-cumulative-layout-shift)
4. [TTFB (Time to First Byte)](#ttfb-time-to-first-byte)
5. [FCP (First Contentful Paint)](#fcp-first-contentful-paint)
6. [TBT (Total Blocking Time)](#tbt-total-blocking-time)

---

## LCP (Largest Contentful Paint)

**What it measures:** Time until the largest content element becomes visible in the viewport

**Targets:**
- ✅ **Good:** ≤2.5 seconds
- ⚠️ **Needs Improvement:** 2.5-4.0 seconds
- ❌ **Poor:** >4.0 seconds

**Weight in Lighthouse:** 25%

**SEO Impact:** Direct ranking factor for Google search

### What Counts as LCP Element

The LCP element is the largest visible element in the viewport:
- `<img>` elements
- `<image>` elements inside `<svg>`
- `<video>` elements (poster image or first frame)
- Background images loaded via `url()`
- Block-level text elements

**Finding your LCP element:**

```javascript
// In Chrome DevTools Console
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP element:', lastEntry.element);
  console.log('LCP time:', lastEntry.startTime);
  console.log('LCP size:', lastEntry.size);
}).observe({ entryTypes: ['largest-contentful-paint'] });

// Or use web-vitals library
import { onLCP } from 'web-vitals';

onLCP((metric) => {
  console.log('LCP:', metric.value);
  console.log('Rating:', metric.rating);
  console.log('Element:', metric.entries[0].element);
});
```

### LCP Breakdown (Diagnostic Workflow)

**LCP consists of 4 phases:**

1. **TTFB** (Time to First Byte) - Server response time
2. **Resource load delay** - Time from TTFB to resource load start
3. **Resource load time** - Time to download resource
4. **Render delay** - Time from resource loaded to rendered

**How to break down LCP:**

```bash
# Use curl to measure TTFB
curl -w "@curl-format.txt" -o /dev/null -s https://yoursite.com

# Look in Chrome DevTools Performance panel:
# - TTFB: Time from navigation to first byte received
# - Resource load delay: Gap before LCP resource fetch starts
# - Resource load time: Network tab (resource timing)
# - Render delay: Performance panel (rendering time)
```

**Example breakdown for 4.43s LCP:**
- TTFB: 3.67s (83% of LCP time) ← **PRIMARY BOTTLENECK**
- Resource load delay: 0.2s
- Resource load time: 0.4s
- Render delay: 0.16s

**Optimization priority:** Fix the largest component first (TTFB in this case)

---

### LCP Optimization Strategies

#### Strategy 1: Optimize TTFB (if TTFB >800ms)

**If TTFB is the bottleneck (common for server-rendered pages):**

See [TTFB section](#ttfb-time-to-first-byte) for detailed strategies.

**Quick wins:**
- Enable CDN edge caching
- Add Redis caching layer for API responses
- Optimize database queries (fix N+1 queries, add indexes)
- Enable HTTP/2 or HTTP/3
- Enable compression (Brotli)

---

#### Strategy 2: Preload LCP Resource (if resource load delay is high)

**Problem:** Browser doesn't discover LCP resource until late (after parsing CSS/JS)

```html
<!-- ❌ BAD: Browser discovers image late (after parsing CSS) -->
<style>
  .hero { background: url('hero.jpg'); }
</style>
<div class="hero"></div>
<!-- Discovery delay: 200-500ms -->

<!-- ✅ GOOD: Preload LCP resource -->
<link rel="preload" as="image" href="hero.jpg" fetchpriority="high">
<style>
  .hero { background: url('hero.jpg'); }
</style>
<div class="hero"></div>
<!-- Browser starts loading immediately -->

<!-- ✅ BEST: Use <img> with fetchpriority="high" -->
<img src="hero.jpg" alt="Hero" width="1200" height="600"
     fetchpriority="high" loading="eager">
```

**Impact:** Reduces LCP by 200-400ms

---

#### Strategy 3: Optimize Image (if resource load time is high)

**Use modern formats (WebP, AVIF):**

```html
<picture>
  <!-- AVIF: 50% smaller than JPEG -->
  <source srcset="hero.avif" type="image/avif">

  <!-- WebP: 30% smaller than JPEG -->
  <source srcset="hero.webp" type="image/webp">

  <!-- JPEG fallback -->
  <img src="hero.jpg" alt="Hero" width="1200" height="600">
</picture>
```

**Convert images:**

```bash
# JPEG → WebP (30% smaller)
cwebp -q 85 hero.jpg -o hero.webp

# JPEG → AVIF (50% smaller)
avifenc -s 5 hero.jpg hero.avif

# Batch conversion
for img in *.jpg; do
  cwebp -q 85 "$img" -o "${img%.jpg}.webp"
  avifenc -s 5 "$img" "${img%.jpg}.avif"
done
```

**Optimize compression:**

```bash
# JPEG optimization (lossless)
jpegoptim --strip-all hero.jpg

# JPEG optimization (lossy, better compression)
jpegoptim --max=85 --strip-all hero.jpg
```

**Use CDN for automatic optimization:**
- Cloudflare Images: `https://yoursite.com/cdn-cgi/image/format=auto,quality=85/hero.jpg`
- Cloudinary: `https://res.cloudinary.com/yourcloud/image/upload/f_auto,q_auto/hero.jpg`
- imgix: `https://yoursite.imgix.net/hero.jpg?auto=format,compress`

**Impact:** 30-50% faster image load time

---

#### Strategy 4: Eliminate Render-Blocking Resources (if render delay is high)

**Problem:** CSS/JS blocking LCP rendering

```html
<!-- ❌ BAD: Render-blocking CSS/JS in <head> -->
<head>
  <link rel="stylesheet" href="styles.css">  <!-- Blocks rendering -->
  <script src="app.js"></script>  <!-- Blocks parsing -->
</head>
<!-- Render delay: 200-500ms -->

<!-- ✅ GOOD: Inline critical CSS, defer non-critical -->
<head>
  <!-- Inline critical above-fold CSS (5-10KB) -->
  <style>
    .hero { height: 100vh; background: #333; }
    /* ... other critical styles */
  </style>

  <!-- Load non-critical CSS asynchronously -->
  <link rel="preload" href="styles.css" as="style"
        onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>

  <!-- Defer JavaScript -->
  <script src="app.js" defer></script>
</head>
```

**Extract critical CSS automatically:**

```bash
npm install -g critical

critical index.html --base ./public --inline --minify > index-optimized.html
```

**Impact:** Reduces LCP by 100-300ms

---

#### Strategy 5: Responsive Images (reduce download size)

**Serve appropriately sized images:**

```html
<!-- ❌ BAD: Same large image for all devices -->
<img src="hero-2000.jpg" alt="Hero">
<!-- Mobile downloads 2MB desktop image for 400px screen -->

<!-- ✅ GOOD: Responsive images with srcset -->
<img
    src="hero-800.jpg"
    srcset="
        hero-400.jpg 400w,
        hero-800.jpg 800w,
        hero-1200.jpg 1200w,
        hero-1600.jpg 1600w
    "
    sizes="
        (max-width: 600px) 400px,
        (max-width: 900px) 800px,
        1200px
    "
    alt="Hero"
    width="1600"
    height="900"
>
<!-- Mobile downloads only 400px version (150KB vs 2MB) -->
```

**Impact:** 70-90% smaller downloads for mobile users

---

### Advanced LCP Techniques

#### Early Hints (103 Status Code)

**Send preload hints before final response:**

```nginx
# Nginx configuration
location / {
    # Send early hints (HTTP 103)
    add_header Link "</hero.jpg>; rel=preload; as=image; fetchpriority=high";
    add_header Link "</styles.css>; rel=preload; as=style";

    proxy_pass http://backend;
}
```

**Impact:** 100-200ms faster LCP (browser starts loading resources earlier)

**Browser support:** Chrome 103+, Firefox 103+

---

#### Adaptive Loading (Network-Aware)

**Serve different images based on connection speed:**

```javascript
const connection = navigator.connection || navigator.mozConnection;

let imageSrc = 'hero-hq.jpg';  // Default: high quality

if (connection) {
  if (connection.effectiveType === '4g') {
    imageSrc = 'hero-hq.avif';  // Fast: AVIF
  } else if (connection.effectiveType === '3g') {
    imageSrc = 'hero-mq.webp';  // Medium: WebP
  } else {
    imageSrc = 'hero-lq.jpg';  // Slow: Low quality JPEG
  }
}

document.querySelector('.hero img').src = imageSrc;
```

**Impact:** 50% faster LCP on slow networks

---

### LCP Debugging Checklist

- [ ] Identify LCP element (use Performance Observer)
- [ ] Break down LCP into 4 phases (TTFB, load delay, load time, render)
- [ ] Optimize bottleneck phase first
- [ ] If TTFB >800ms: See [TTFB section](#ttfb-time-to-first-byte)
- [ ] If load delay high: Preload LCP resource with fetchpriority="high"
- [ ] If load time high: Use modern formats (WebP/AVIF), optimize compression, use CDN
- [ ] If render delay high: Eliminate render-blocking resources, inline critical CSS
- [ ] Verify LCP <2.5s in field data (web-vitals library)

---

## INP (Interaction to Next Paint)

**What it measures:** Responsiveness - time from user interaction to visual update

**Replaces:** FID (First Input Delay) as of March 2024

**Targets:**
- ✅ **Good:** ≤200ms
- ⚠️ **Needs Improvement:** 200-500ms
- ❌ **Poor:** >500ms

**Weight in Lighthouse:** 10%

**User Experience Impact:**
- INP >200ms: Users perceive UI as sluggish
- INP >500ms: Users perceive UI as broken
- Every 100ms improvement = 2% increase in engagement

### What INP Measures

**INP tracks ALL interactions during page lifetime:**
- Clicks
- Taps
- Keyboard presses

**INP breakdown:**
1. **Input delay** - Time from interaction to event handler start
2. **Processing time** - Event handler execution time
3. **Presentation delay** - Time from handler end to visual update

**Worst interaction wins** - INP reports 98th percentile interaction

---

### Finding Slow Interactions

```javascript
// Use web-vitals library
import { onINP } from 'web-vitals';

onINP((metric) => {
  console.log('INP:', metric.value);
  console.log('Rating:', metric.rating);
  console.log('Attribution:', metric.attribution);

  // Log slow interactions (>200ms)
  if (metric.value > 200) {
    console.log('Slow interaction detected!');
    console.log('Element:', metric.attribution.interactionTarget);
    console.log('Type:', metric.attribution.interactionType);
    console.log('Input delay:', metric.attribution.inputDelay);
    console.log('Processing time:', metric.attribution.processingDuration);
    console.log('Presentation delay:', metric.attribution.presentationDelay);

    // Send to analytics
    sendToAnalytics({
      name: 'INP',
      value: metric.value,
      element: metric.attribution.interactionTarget,
      type: metric.attribution.interactionType
    });
  }
});
```

**Chrome DevTools Performance panel:**
1. Record interaction
2. Look for long "Task" blocks (>50ms)
3. Identify which event handlers are slow

---

### INP Optimization Strategies

#### Strategy 1: Break Up Long Tasks

**Problem:** Long-running tasks block main thread, causing input delay

**JavaScript runs single-threaded** - long tasks prevent UI updates

```javascript
// ❌ BAD: Long task blocks main thread (300ms)
function processItems(items) {
  items.forEach(item => {
    // Each iteration takes 10ms
    // 30 items × 10ms = 300ms blocked
    heavyComputation(item);
  });
}

// User clicks button → Waits 300ms → Handler runs → INP: 300ms+

// ✅ GOOD: Break into chunks with scheduler.yield()
async function processItems(items) {
  for (const item of items) {
    heavyComputation(item);

    // Yield to main thread every item
    if ('scheduler' in window && 'yield' in scheduler) {
      await scheduler.yield();  // Let browser handle pending interactions
    } else {
      // Fallback: setTimeout
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  }
}

// User clicks button → Handled immediately → INP: <50ms

// ✅ BETTER: Batch processing (yield every N items)
async function processItems(items) {
  for (let i = 0; i < items.length; i++) {
    heavyComputation(items[i]);

    // Yield every 5 items
    if (i % 5 === 0) {
      await scheduler.yield();
    }
  }
}
```

**Rule of thumb:** Tasks should run <50ms. Break longer tasks into chunks.

**Impact:** Reduces INP by 50-80% for CPU-heavy operations

---

#### Strategy 2: Debounce/Throttle Event Handlers

**Problem:** Event handlers firing too frequently (scroll, resize, input)

```javascript
// ❌ BAD: Handler runs on every scroll event (hundreds per second)
window.addEventListener('scroll', () => {
  updateParallaxEffect();  // Expensive computation
});
// INP: 200-500ms (constant main thread blocking)

// ✅ GOOD: Debounce (run after user stops scrolling)
import { debounce } from 'lodash-es';

window.addEventListener('scroll', debounce(() => {
  updateParallaxEffect();
}, 100));  // Run 100ms after last scroll event

// ✅ ALSO GOOD: Throttle (run at most once per N ms)
import { throttle } from 'lodash-es';

window.addEventListener('scroll', throttle(() => {
  updateParallaxEffect();
}, 100));  // Run at most once every 100ms
```

**When to use:**
- **Debounce:** Search input, window resize (wait until user finishes)
- **Throttle:** Scroll events, mouse move (limit frequency)

**Impact:** 80-95% reduction in event handler calls

---

#### Strategy 3: Use Web Workers for CPU-Intensive Tasks

**Offload heavy computations to background thread:**

```javascript
// ❌ BAD: CPU-intensive task on main thread
function processData(data) {
  const result = complexCalculation(data);  // Blocks main thread for 500ms
  return result;
}

button.addEventListener('click', () => {
  const result = processData(largeDataset);  // INP: 500ms+
  updateUI(result);
});

// ✅ GOOD: Use Web Worker
// worker.js
self.addEventListener('message', (e) => {
  const result = complexCalculation(e.data);
  self.postMessage(result);
});

// main.js
const worker = new Worker('worker.js');

button.addEventListener('click', () => {
  worker.postMessage(largeDataset);  // Non-blocking
  // INP: <50ms (main thread free)
});

worker.addEventListener('message', (e) => {
  updateUI(e.data);  // Update UI when ready
});
```

**What to offload to Web Workers:**
- Data processing (sorting, filtering, transforming large arrays)
- Image manipulation
- Cryptography
- Complex calculations

**What NOT to offload:**
- DOM manipulation (workers can't access DOM)
- Very small tasks (overhead not worth it)

**Impact:** Reduces INP to <50ms for heavy computations

---

#### Strategy 4: Optimize Event Handler Logic

**Reduce processing time by optimizing handler code:**

```javascript
// ❌ BAD: Expensive DOM queries in handler
button.addEventListener('click', () => {
  const items = document.querySelectorAll('.item');  // Query every click
  items.forEach(item => {
    item.classList.add('active');
  });
});

// ✅ GOOD: Cache DOM queries
const items = document.querySelectorAll('.item');  // Query once

button.addEventListener('click', () => {
  items.forEach(item => {
    item.classList.add('active');
  });
});

// ✅ BETTER: Event delegation (single listener)
container.addEventListener('click', (e) => {
  if (e.target.matches('.item')) {
    e.target.classList.add('active');
  }
});
// Reduces listeners from N to 1
```

**Impact:** 30-60% faster event handlers

---

#### Strategy 5: Use requestIdleCallback for Non-Critical Work

**Defer non-critical work until browser is idle:**

```javascript
// ❌ BAD: Analytics tracking blocks interaction
button.addEventListener('click', () => {
  // Critical: Update UI
  updateUI();

  // Non-critical: Send analytics (blocks for 50ms)
  sendAnalytics();  // INP: 50ms penalty
});

// ✅ GOOD: Defer non-critical work
button.addEventListener('click', () => {
  // Critical: Update UI immediately
  updateUI();  // INP: <10ms

  // Non-critical: Schedule for idle time
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      sendAnalytics();
    });
  } else {
    setTimeout(sendAnalytics, 0);
  }
});
```

**Impact:** 20-50ms faster INP

---

### INP Debugging Checklist

- [ ] Identify slow interactions with web-vitals library
- [ ] Record interaction in Chrome DevTools Performance panel
- [ ] Look for long tasks (>50ms)
- [ ] Break up long tasks with scheduler.yield()
- [ ] Debounce/throttle frequent event handlers
- [ ] Offload CPU-intensive work to Web Workers
- [ ] Optimize event handler logic (cache DOM queries, event delegation)
- [ ] Defer non-critical work with requestIdleCallback
- [ ] Verify INP <200ms in field data

---

## CLS (Cumulative Layout Shift)

**What it measures:** Visual stability - how much content shifts unexpectedly during page load

**Targets:**
- ✅ **Good:** ≤0.1
- ⚠️ **Needs Improvement:** 0.1-0.25
- ❌ **Poor:** >0.25

**Weight in Lighthouse:** 25%

**SEO Impact:** Direct ranking factor for Google search (since June 2021)

**User Experience Impact:**
- CLS >0.1: Users find layout shifts annoying
- CLS >0.25: 24% higher bounce rate
- Each 0.1 increase = 3% decrease in conversions

### How CLS is Calculated

```
CLS = Impact Fraction × Distance Fraction
```

- **Impact Fraction:** % of viewport affected by shift
- **Distance Fraction:** Distance element moved / viewport height

**Example:**
- Element takes up 50% of viewport (impact fraction = 0.5)
- Element shifts down by 25% of viewport height (distance fraction = 0.25)
- CLS = 0.5 × 0.25 = 0.125 (Poor)

**CLS is cumulative:** All layout shifts during page lifetime are added up

---

### Diagnostic Workflow

#### Step 1: Enable Layout Shift Regions in Chrome DevTools

1. Open DevTools (F12)
2. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows)
3. Type "Show Layout Shift Regions"
4. Enable the setting
5. Reload page - shifted elements will be highlighted in blue

#### Step 2: Record Performance Trace

1. Go to Performance panel in DevTools
2. Click Record (Cmd+E)
3. Load your page (or trigger interactions)
4. Stop recording
5. Look for red "Layout Shift" bars in the Experience section
6. Click each bar to see which element shifted

#### Step 3: Identify Shifting Elements

```javascript
// Log layout shifts in console
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.hadRecentInput) continue;  // Ignore user-initiated shifts

    console.log('Layout shift detected!');
    console.log('Value:', entry.value);
    console.log('Sources:', entry.sources);

    entry.sources.forEach(source => {
      console.log('Element:', source.node);
      console.log('Previous rect:', source.previousRect);
      console.log('Current rect:', source.currentRect);
    });
  }
}).observe({ entryTypes: ['layout-shift'] });
```

#### Step 4: Measure CLS in Production

```javascript
import { onCLS } from 'web-vitals';

onCLS((metric) => {
  console.log('CLS:', metric.value);
  console.log('Rating:', metric.rating);

  // Log details for poor CLS
  if (metric.value > 0.1) {
    console.log('Poor CLS detected!');
    console.log('Entries:', metric.entries);

    // Send to analytics
    sendToAnalytics({
      name: 'CLS',
      value: metric.value,
      rating: metric.rating,
      entries: metric.entries.map(entry => ({
        value: entry.value,
        sources: entry.sources.map(source => ({
          node: source.node?.outerHTML.substring(0, 100),
          previousRect: source.previousRect,
          currentRect: source.currentRect
        }))
      }))
    });
  }
});
```

---

### Common Causes and Fixes

#### Cause 1: Images Without Dimensions (MOST COMMON)

**Impact:** 50-80% of CLS issues

**Problem:**

```html
<!-- ❌ BAD: Browser doesn't know image size until loaded -->
<img src="hero.jpg" alt="Hero">
<!-- Page loads → Text appears → Image loads → Text shifts down → CLS: 0.25+ -->
```

**Solution 1: Set explicit dimensions**

```html
<!-- ✅ GOOD: Browser reserves space before image loads -->
<img src="hero.jpg" alt="Hero" width="1200" height="600">
<!-- Page loads → Space reserved → Image loads → No shift! CLS: 0 -->
```

**Solution 2: Use aspect-ratio CSS (modern)**

```html
<img src="hero.jpg" alt="Hero" style="aspect-ratio: 16/9; width: 100%;">
<!-- Responsive + prevents CLS -->
```

**Solution 3: CSS for all images**

```css
img {
  max-width: 100%;
  height: auto;
  /* aspect-ratio preserved from width/height attributes */
}

/* Or use aspect-ratio for responsive images */
.responsive-img {
  aspect-ratio: 16/9;
  width: 100%;
  object-fit: cover;
}
```

**For background images:**

```css
.hero {
  background: url('hero.jpg') center/cover;
  aspect-ratio: 16/9;
  /* Reserve space with aspect ratio */
}
```

**Impact:** Reduces CLS by 0.2-0.4 (50-80% improvement)

---

#### Cause 2: Web Fonts Loading

**Impact:** 20-40% of CLS issues

**Problem:**

```css
/* ❌ BAD: FOIT (Flash of Invisible Text) or FOUT (Flash of Unstyled Text) */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  /* No font-display → Default causes layout shift */
}

body {
  font-family: 'CustomFont', sans-serif;
}
/* Page loads → Invisible text (FOIT) → Font loads → Text appears → Shift! */
```

**Solution 1: Use font-display: swap**

```css
/* ✅ GOOD: Show fallback immediately, swap when custom font loads */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;  /* Show fallback immediately */
}
```

**font-display values:**
- `swap`: Show fallback immediately, swap when font loads (best for CLS)
- `optional`: Use custom font if loaded quickly, otherwise use fallback
- `fallback`: Brief invisible period, then show fallback if font not loaded
- `block`: Invisible text until font loads (causes CLS, avoid!)

**Solution 2: Preload critical fonts**

```html
<!-- Preload fonts to load them earlier -->
<link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin>

<style>
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;
}
</style>
```

**Solution 3: Match fallback font metrics (advanced)**

```css
/* Adjust fallback font to match custom font dimensions */
@font-face {
  font-family: 'CustomFont-Fallback';
  src: local('Arial');
  ascent-override: 105%;
  descent-override: 35%;
  line-gap-override: 10%;
  size-adjust: 95%;
}

body {
  font-family: 'CustomFont', 'CustomFont-Fallback', sans-serif;
}
/* Minimizes layout shift when swapping fonts */
```

**Solution 4: Use system fonts (zero CLS)**

```css
/* ✅ BEST: System fonts load instantly, zero CLS */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'Helvetica Neue', Arial, sans-serif;
}
```

**Impact:** Reduces CLS by 0.1-0.2

---

#### Cause 3: Ads Without Reserved Space

**Impact:** 30-50% of CLS issues (especially on content sites)

**Problem:**

```html
<!-- ❌ BAD: Ad loads dynamically, pushes content down -->
<div id="ad-slot"></div>
<script>loadAd('ad-slot');</script>
<p>Content below ad...</p>
<!-- Content loads → Ad loads → Content shifts → CLS: 0.3+ -->
```

**Solution: Reserve space with min-height and aspect-ratio**

```html
<!-- ✅ GOOD: Reserve space before ad loads -->
<div class="ad-container" style="min-height: 250px; aspect-ratio: 16/9;">
  <div id="ad-slot"></div>
</div>
<p>Content below ad...</p>
<!-- Space reserved → Ad loads into reserved space → No shift! -->
```

**CSS approach:**

```css
.ad-container {
  min-height: 250px;  /* Minimum height for ad slot */
  aspect-ratio: 16/9;  /* Maintain aspect ratio */
  background: #f0f0f0;  /* Placeholder background */
  display: flex;
  align-items: center;
  justify-content: center;
}

.ad-container::before {
  content: 'Advertisement';
  color: #999;
  font-size: 14px;
}
```

**For multiple ad sizes:**

```css
/* Mobile: 300×250 */
@media (max-width: 767px) {
  .ad-container {
    min-height: 250px;
    aspect-ratio: 6/5;
  }
}

/* Desktop: 728×90 */
@media (min-width: 768px) {
  .ad-container {
    min-height: 90px;
    aspect-ratio: 728/90;
  }
}
```

**Impact:** Reduces CLS by 0.2-0.3

---

#### Cause 4: Dynamic Content Injection

**Impact:** 20-40% of CLS issues

**Problem:**

```javascript
// ❌ BAD: Insert content above existing content
fetch('/api/banner')
  .then(response => response.text())
  .then(html => {
    document.getElementById('header').insertAdjacentHTML('afterbegin', html);
    // Existing content shifts down → CLS!
  });
```

**Solution 1: Reserve space with min-height**

```html
<div id="banner-slot" style="min-height: 100px;">
  <!-- Banner loads here -->
</div>

<script>
fetch('/api/banner')
  .then(response => response.text())
  .then(html => {
    document.getElementById('banner-slot').innerHTML = html;
    // No shift - space already reserved
  });
</script>
```

**Solution 2: Append instead of prepend**

```javascript
// ✅ BETTER: Append at end (doesn't shift existing content)
fetch('/api/related-articles')
  .then(response => response.text())
  .then(html => {
    document.getElementById('content').insertAdjacentHTML('beforeend', html);
    // No shift for existing content
  });
```

**Solution 3: Use skeleton screens**

```html
<!-- Skeleton while loading -->
<div class="banner-skeleton" style="height: 100px; background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%);">
  <div class="skeleton-line"></div>
</div>

<script>
fetch('/api/banner')
  .then(response => response.text())
  .then(html => {
    // Replace skeleton with real content (same height → no shift)
    document.querySelector('.banner-skeleton').outerHTML = html;
  });
</script>
```

**Impact:** Reduces CLS by 0.1-0.3

---

#### Cause 5: Animations Causing Layout

**Impact:** 10-20% of CLS issues

**Problem:**

```css
/* ❌ BAD: Animating properties that trigger layout */
.modal {
  transition: height 0.3s, width 0.3s;
}

.modal.open {
  height: 500px;  /* Triggers layout recalculation */
  width: 600px;   /* Triggers layout recalculation */
}
/* Every frame recalculates layout → CLS */
```

**Solution: Use transform and opacity only**

```css
/* ✅ GOOD: Transform/opacity don't trigger layout */
.modal {
  transform: scale(0) translateY(-50%);
  opacity: 0;
  transition: transform 0.3s, opacity 0.3s;
  will-change: transform, opacity;  /* GPU acceleration hint */
}

.modal.open {
  transform: scale(1) translateY(0);  /* GPU-accelerated */
  opacity: 1;
}
/* No layout recalculation → No CLS */
```

**Properties that DON'T cause layout shifts (GPU-accelerated):**
- ✅ `transform` (translate, scale, rotate)
- ✅ `opacity`
- ✅ `filter`

**Properties that DO cause layout shifts (AVOID in animations):**
- ❌ `width`, `height`
- ❌ `top`, `left`, `right`, `bottom` (use `transform: translate()` instead)
- ❌ `margin`, `padding`
- ❌ `border-width`
- ❌ `font-size`

**Impact:** Reduces CLS by 0.05-0.15

---

### Complete Example: Zero-CLS Page

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Zero-CLS Page Example</title>

  <!-- Preload critical fonts -->
  <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>

  <style>
    /* System fonts fallback to prevent FOIT */
    @font-face {
      font-family: 'MainFont';
      src: url('/fonts/main.woff2') format('woff2');
      font-display: swap;  /* Show fallback immediately */
    }

    body {
      font-family: 'MainFont', -apple-system, BlinkMacSystemFont, sans-serif;
      margin: 0;
    }

    /* All images have dimensions */
    img {
      max-width: 100%;
      height: auto;
    }

    /* Reserve space for ads */
    .ad-container {
      min-height: 250px;
      aspect-ratio: 16/9;
      background: #f0f0f0;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* GPU-accelerated animations only */
    .modal {
      transform: translateY(100%);
      opacity: 0;
      transition: transform 0.3s, opacity 0.3s;
      will-change: transform, opacity;
    }

    .modal.open {
      transform: translateY(0);
      opacity: 1;
    }

    /* Reserve space for dynamic content */
    .banner-slot {
      min-height: 100px;
      background: #f5f5f5;
    }
  </style>
</head>
<body>
  <!-- Hero image with explicit dimensions -->
  <img src="hero.jpg" alt="Hero" width="1200" height="600" fetchpriority="high">

  <!-- Banner with reserved space -->
  <div id="banner-slot" class="banner-slot"></div>

  <!-- Ad slot with reserved space -->
  <div class="ad-container">
    <div id="ad-slot"></div>
  </div>

  <!-- Main content -->
  <main>
    <h1>Welcome</h1>
    <p>Your content here...</p>

    <!-- More images with dimensions -->
    <img src="content-1.jpg" alt="Content 1" width="800" height="600" loading="lazy">
    <img src="content-2.jpg" alt="Content 2" width="800" height="600" loading="lazy">
  </main>

  <script>
    // Load dynamic content into reserved space
    fetch('/api/banner')
      .then(r => r.text())
      .then(html => {
        document.getElementById('banner-slot').innerHTML = html;
      });

    // Load ads into reserved space
    loadAd('ad-slot');
  </script>
</body>
</html>
```

**Expected CLS:** <0.05 (Good) ✅

---

### CLS Debugging Checklist

- [ ] All images have width/height attributes or aspect-ratio CSS
- [ ] Fonts use font-display: swap (or system fonts)
- [ ] Critical fonts preloaded
- [ ] Ads have reserved space (min-height + aspect-ratio)
- [ ] Dynamic content uses skeleton screens or reserved space
- [ ] Animations use transform/opacity only (no layout properties)
- [ ] Layout Shift Regions enabled in DevTools to identify shifts
- [ ] CLS measured in production with web-vitals library
- [ ] CLS <0.1 for 75th percentile of users

---

## TTFB (Time to First Byte)

**What it measures:** Server response time - time from navigation start to first byte received

**Targets:**
- ✅ **Good:** ≤800ms
- ⚠️ **Needs Improvement:** 800-1800ms
- ❌ **Poor:** >1800ms

**Weight in Lighthouse:** Not directly scored, but affects LCP and FCP

**Critical because:** TTFB is the foundation for all other metrics. Slow TTFB delays everything.

### TTFB Breakdown

**TTFB consists of:**
1. **DNS lookup** - Resolve domain to IP (~20-120ms)
2. **TCP connection** - Establish connection (~20-100ms)
3. **TLS handshake** - SSL/TLS negotiation (~100-200ms for TLS 1.2, ~50-100ms for TLS 1.3)
4. **Server processing** - Backend generates response (varies widely: 50ms to 5s+)

**Measuring TTFB breakdown:**

```bash
# Create curl timing format
cat > curl-format.txt << 'EOF'
    DNS lookup:        %{time_namelookup}s\n
    TCP connection:    %{time_connect}s\n
    TLS handshake:     %{time_appconnect}s\n
    Server processing: %{time_starttransfer}s (TTFB)\n
    Total time:        %{time_total}s\n
EOF

# Measure TTFB
curl -w "@curl-format.txt" -o /dev/null -s https://yoursite.com

# Example output:
# DNS lookup:        0.023s  ✅ Good
# TCP connection:    0.045s  ✅ Good
# TLS handshake:     0.128s  ✅ Good (TLS 1.2)
# Server processing: 3.670s  ❌ PROBLEM - This is TTFB
# Total time:        4.234s
```

---

### Diagnostic Workflow

**Step 1: Identify bottleneck phase**

| Phase | Time | Status | Fix |
|-------|------|--------|-----|
| DNS lookup >100ms | ❌ Slow | Use faster DNS provider (Cloudflare, Google) |
| TCP connection >100ms | ❌ Slow | Enable Keep-Alive, use CDN |
| TLS handshake >200ms | ❌ Slow | Enable TLS 1.3, optimize certificate chain |
| Server processing >500ms | ❌ Slow | **MOST COMMON - See optimization strategies below** |

**Step 2: Profile backend (if server processing is slow)**

Use Application Performance Monitoring (APM) tools:
- New Relic
- Datadog
- Sentry Performance
- AWS X-Ray (for AWS)
- Google Cloud Profiler

**What to look for:**
- Slow database queries (>100ms)
- N+1 query problems
- Missing database indexes
- External API call latency
- Cold start penalties (serverless functions)
- Cache miss ratios

**Step 3: Optimize bottleneck**

---

### TTFB Optimization Strategies

For detailed implementation, see [optimization-techniques.md](optimization-techniques.md#backend-optimization).

#### Strategy 1: Database Optimization

**Fix N+1 queries:**

```python
# ❌ BAD: 1 + N queries (2000ms for 100 posts)
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # N queries

# ✅ GOOD: 1 query with JOIN (50ms for 100 posts)
posts = Post.objects.select_related('author').all()
for post in posts:
    print(post.author.name)  # No additional query
```

**Add indexes:**

```sql
-- ❌ BAD: Full table scan (2300ms)
SELECT * FROM orders WHERE user_id = 123 AND created_at > '2025-01-01';

-- ✅ GOOD: Index scan (15ms)
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);
SELECT * FROM orders WHERE user_id = 123 AND created_at > '2025-01-01';
```

**Impact:** 10-100x faster queries

---

#### Strategy 2: Server-Side Caching (Redis)

**Cache expensive operations:**

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379)

def get_user_profile(user_id):
    # Check cache first
    cache_key = f"user_profile:{user_id}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)  # Cache hit (1-2ms)

    # Cache miss - query database
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")  # 100ms

    # Cache for 5 minutes
    redis_client.setex(cache_key, 300, json.dumps(user))

    return user

# Performance: 95% cache hit rate → 50x faster (2ms vs 100ms)
```

**Impact:** 50-100x faster for frequently accessed data

---

#### Strategy 3: CDN Edge Caching

**Cache static and semi-static content at edge:**

```nginx
# Nginx cache configuration
location ~* \.(jpg|jpeg|png|gif|webp|avif|css|js|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, max-age=31536000, immutable";
}

# API responses: short cache with stale-while-revalidate
location /api/ {
    add_header Cache-Control "max-age=60, stale-while-revalidate=600";
    proxy_pass http://backend;
}
```

**Impact:** 90-95% of requests served from edge (50-200ms faster)

---

#### Strategy 4: HTTP/2 or HTTP/3

**Enable multiplexing and header compression:**

```nginx
server {
    listen 443 ssl http2;  # Enable HTTP/2
    server_name yoursite.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
```

**Impact:** 30-50% faster for multiple resources

---

#### Strategy 5: Compression (Brotli)

```nginx
http {
    brotli on;
    brotli_comp_level 6;
    brotli_types text/plain text/css text/javascript application/json;

    # Fallback to gzip
    gzip on;
    gzip_types text/plain text/css text/javascript application/json;
}
```

**Impact:** 20-30% smaller responses, 5-10% faster TTFB

---

#### Strategy 6: Cold Start Mitigation (Serverless)

**Reuse database connections:**

```javascript
// ❌ BAD: New connection every invocation (1-2s cold start)
exports.handler = async (event) => {
    const db = await connectToDatabase();
    const result = await db.query('SELECT * FROM users');
    await db.close();
    return result;
};

// ✅ GOOD: Reuse connection across invocations
let db;

exports.handler = async (event) => {
    if (!db) {
        db = await connectToDatabase();  // Only on cold start
    }
    const result = await db.query('SELECT * FROM users');
    return result;
};
```

**Impact:** Eliminates 1-3s cold start penalty

---

### TTFB Debugging Checklist

- [ ] Measure TTFB breakdown with curl
- [ ] Identify bottleneck phase (DNS, TCP, TLS, or server)
- [ ] If server processing >500ms:
  - [ ] Profile with APM tool
  - [ ] Fix N+1 database queries
  - [ ] Add missing indexes
  - [ ] Implement Redis caching
  - [ ] Enable CDN edge caching
  - [ ] Enable HTTP/2 or HTTP/3
  - [ ] Enable compression (Brotli)
  - [ ] Fix cold start issues (serverless)
- [ ] Verify TTFB <800ms

**Target:** TTFB <800ms (Good), <1800ms (Acceptable)

---

## FCP (First Contentful Paint)

**What it measures:** Time until first text or image is rendered

**Targets:**
- ✅ **Good:** ≤1.8 seconds
- ⚠️ **Needs Improvement:** 1.8-3.0 seconds
- ❌ **Poor:** >3.0 seconds

**Weight in Lighthouse:** 10%

**User Experience:** FCP is when user sees "something" - indicates page is loading

### FCP vs LCP

- **FCP:** First content (any text/image)
- **LCP:** Largest content (main hero image/text block)

**Example:**
- FCP: 0.8s (navigation bar appears)
- LCP: 2.2s (hero image appears)

---

### FCP Optimization Strategies

#### Strategy 1: Eliminate Render-Blocking Resources

**Problem:** CSS/JS in `<head>` blocks rendering

```html
<!-- ❌ BAD: Blocking CSS -->
<head>
    <link rel="stylesheet" href="styles.css">  <!-- Blocks FCP -->
</head>

<!-- ✅ GOOD: Inline critical CSS, defer non-critical -->
<head>
    <style>
        /* Inline critical CSS (above-fold styles, 5-10KB) */
        nav { background: #333; }
        .hero { height: 100vh; }
    </style>

    <!-- Load non-critical CSS asynchronously -->
    <link rel="preload" href="styles.css" as="style"
          onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="styles.css"></noscript>
</head>
```

**Impact:** 200-500ms faster FCP

---

#### Strategy 2: Defer Non-Critical JavaScript

```html
<!-- ❌ BAD: Blocking JS -->
<head>
    <script src="app.js"></script>  <!-- Blocks parsing and FCP -->
</head>

<!-- ✅ GOOD: Defer JS -->
<head>
    <script src="app.js" defer></script>  <!-- Doesn't block FCP -->

    <!-- Or async for non-dependent scripts -->
    <script src="analytics.js" async></script>
</head>
```

**Impact:** 100-300ms faster FCP

---

#### Strategy 3: Optimize Font Loading

```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>

<style>
@font-face {
    font-family: 'MainFont';
    src: url('/fonts/main.woff2') format('woff2');
    font-display: swap;  /* Show fallback immediately */
}
</style>
```

**Impact:** 100-300ms faster FCP

---

#### Strategy 4: Reduce Server Response Time (TTFB)

**FCP depends on TTFB** - see [TTFB section](#ttfb-time-to-first-byte) for optimization strategies.

---

### FCP Debugging Checklist

- [ ] Inline critical CSS (<10KB)
- [ ] Defer non-critical CSS
- [ ] Defer/async JavaScript
- [ ] Preload critical fonts with font-display: swap
- [ ] Optimize TTFB <800ms
- [ ] Verify FCP <1.8s

---

## TBT (Total Blocking Time)

**What it measures:** Total time main thread is blocked during page load

**Targets:**
- ✅ **Good:** ≤200ms
- ⚠️ **Needs Improvement:** 200-600ms
- ❌ **Poor:** >600ms

**Weight in Lighthouse:** 30% (highest weight!)

**User Experience:** TBT indicates how responsive page is during load

### How TBT is Calculated

**TBT = Sum of blocking time for all long tasks (>50ms) between FCP and TTI**

**Example:**
- Task 1: 70ms → Blocking time: 20ms (70 - 50)
- Task 2: 120ms → Blocking time: 70ms (120 - 50)
- Task 3: 40ms → Blocking time: 0ms (below threshold)
- **TBT = 20 + 70 = 90ms**

**Long task threshold:** 50ms

**Why 50ms?** Human perception threshold - tasks <50ms feel instant

---

### TBT Optimization Strategies

#### Strategy 1: Code Splitting

**Break large bundles into smaller chunks:**

```javascript
// ❌ BAD: Large bundle (500KB) = long tasks
import { HeavyComponent } from './heavy';

// ✅ GOOD: Code split by route
const HeavyComponent = lazy(() => import('./heavy'));
```

**Impact:** 30-50% TBT reduction

---

#### Strategy 2: Defer Non-Critical JavaScript

```html
<!-- Load non-critical JS after page interactive -->
<script src="analytics.js" defer></script>
<script src="chat-widget.js" defer></script>
```

**Impact:** 20-40% TBT reduction

---

#### Strategy 3: Break Up Long Tasks

**Use scheduler.yield() to split work:**

```javascript
// ❌ BAD: Long task (300ms)
items.forEach(item => processItem(item));

// ✅ GOOD: Break into chunks
for (const item of items) {
    processItem(item);
    await scheduler.yield();  // Let browser breathe
}
```

**Impact:** 50-80% TBT reduction

---

#### Strategy 4: Use requestIdleCallback

**Defer non-critical work:**

```javascript
// Critical: Render UI immediately
renderUI();

// Non-critical: Process in idle time
requestIdleCallback(() => {
    processAnalytics();
});
```

**Impact:** 30-60% TBT reduction

---

### TBT Debugging Checklist

- [ ] Code split by route
- [ ] Defer non-critical JavaScript
- [ ] Break up long tasks (>50ms) with scheduler.yield()
- [ ] Use requestIdleCallback for non-critical work
- [ ] Tree shake unused code
- [ ] Verify TBT <200ms in Lighthouse

---

## Tools for Debugging Core Web Vitals

### Chrome DevTools

**Performance Panel:**
- Record page load
- Identify long tasks (>50ms)
- See layout shifts
- Analyze rendering bottlenecks

**Lighthouse:**
- Run performance audit
- Get specific recommendations
- See metric scores and weights

**Coverage Tool:**
- Identify unused CSS/JS
- Find code splitting opportunities

### Web-Vitals Library

```javascript
import { onCLS, onFCP, onINP, onLCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
    const body = JSON.stringify({
        name: metric.name,
        value: metric.value,
        rating: metric.rating,
        id: metric.id
    });

    navigator.sendBeacon('/analytics', body);
}

// Measure all Core Web Vitals
onCLS(sendToAnalytics);
onFCP(sendToAnalytics);
onINP(sendToAnalytics);
onLCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

### WebPageTest

**Features:**
- Filmstrip view
- Waterfall chart
- Connection view
- Test from multiple locations

**URL:** https://www.webpagetest.org

### PageSpeed Insights

**Features:**
- Real user data (CrUX)
- Lab data (Lighthouse)
- Field data comparison
- Mobile vs desktop

**URL:** https://pagespeed.web.dev

---

## Summary: Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor | Fix Priority |
|--------|------|-------------------|------|--------------|
| **LCP** | ≤2.5s | 2.5-4.0s | >4.0s | HIGH |
| **INP** | ≤200ms | 200-500ms | >500ms | MEDIUM |
| **CLS** | ≤0.1 | 0.1-0.25 | >0.25 | HIGH |
| **TTFB** | ≤800ms | 800-1800ms | >1800ms | **CRITICAL** |
| **FCP** | ≤1.8s | 1.8-3.0s | >3.0s | MEDIUM |
| **TBT** | ≤200ms | 200-600ms | >600ms | HIGH |

**Optimization Priority:**
1. **TTFB** (foundation for everything)
2. **CLS** (SEO + UX impact)
3. **LCP** (depends on TTFB)
4. **TBT** (highest Lighthouse weight)
5. **INP** (responsiveness)
6. **FCP** (perceived performance)

**Next Steps:**
- See [optimization-techniques.md](optimization-techniques.md) for detailed implementation
- See [monitoring.md](monitoring.md) for continuous monitoring setup
- See [quick-wins.md](quick-wins.md) for time-boxed optimizations

---

**Remember:** Core Web Vitals are about user experience, not just scores. Focus on real-world impact, not gaming the metrics.
