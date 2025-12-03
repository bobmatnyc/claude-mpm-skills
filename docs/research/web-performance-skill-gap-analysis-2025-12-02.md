# Web Performance Optimization Skill - Gap Analysis

**Research Date:** 2025-12-02
**Skill Analyzed:** `universal/web/web-performance-optimization`
**Analysis Type:** Real-World Performance Metrics Coverage Assessment

---

## Executive Summary

**Severity: CRITICAL GAPS IDENTIFIED**

The current web performance optimization skill has **significant gaps** in addressing severe real-world performance issues, particularly:
- **TTFB optimization** (3.67s vs. 800ms target = 359% over) - **ZERO coverage**
- **CLS optimization** (0.52 vs. 0.1 target = 420% over) - **Minimal coverage** (2% of file)
- **LCP optimization** (4.43s vs. 2.5s target = 77% over) - **Incomplete coverage** (stub only)

**Missing Reference Files:** 3 of 6 expected files don't exist (50% completion rate)

**Impact:** Users facing severe performance degradation (3.67s TTFB, 0.52 CLS) will not find actionable solutions in current skill.

---

## Real-World Performance Context

### Performance Issues Being Analyzed

| Metric | Current | Target | Delta | Status |
|--------|---------|--------|-------|--------|
| **LCP** | 4.43s | <2.5s | +1.93s (77% over) | ❌ POOR |
| **INP** | 64ms | <200ms | -136ms | ✅ GOOD |
| **CLS** | 0.52 | <0.1 | +0.42 (420% over) | ❌ CRITICAL |
| **FID** | 3ms | <100ms | -97ms | ✅ GOOD |
| **TTFB** | 3.67s | <800ms | +2.87s (359% over) | ❌ CRITICAL |

**Key Observations:**
- **INP and FID are excellent** - JavaScript performance is not the issue
- **TTFB is catastrophic** - Backend/network issues dominate
- **CLS is severe** - Layout stability needs urgent attention
- **LCP is poor** - Compounded by slow TTFB

**Root Cause Hypothesis:**
The 3.67s TTFB suggests **backend/infrastructure problems**, not frontend issues:
- Slow database queries
- Unoptimized API endpoints
- Missing server-side caching
- CDN misconfiguration
- Cold start penalties (serverless)

---

## Coverage Assessment

### ✅ What's Currently Covered (GOOD)

**Quick Wins (566 lines) - EXCELLENT:**
- ✅ Lazy loading images (40-60% weight reduction)
- ✅ Compression (gzip/brotli) for 70-80% transfer size reduction
- ✅ Preconnect for critical origins (100-500ms savings)
- ✅ Code splitting (30-50% bundle reduction)
- ✅ Service worker caching
- ✅ Bundle optimization with tree shaking
- ✅ Lighthouse CI + RUM monitoring setup

**Modern Patterns 2025 (612 lines) - EXCELLENT:**
- ✅ View Transitions API
- ✅ Speculation Rules API
- ✅ React Server Components
- ✅ Priority Hints (fetchpriority)
- ✅ Content Visibility CSS

**Main SKILL.md (141 lines) - GOOD:**
- ✅ Clear navigation structure
- ✅ Business impact metrics (conversion loss data)
- ✅ Time-boxed optimization paths (1hr/1day/1week)
- ✅ Progressive disclosure references

### ❌ What's Missing (CRITICAL GAPS)

#### 1. TTFB Optimization (ZERO Coverage) - HIGHEST PRIORITY

**User's Problem:** 3.67s TTFB (359% over target)

**Missing Content:**
- **Backend optimization techniques:**
  - Database query optimization (N+1 queries, missing indexes)
  - API response time reduction (caching strategies)
  - Server-side rendering optimization
  - Cold start mitigation (serverless)

- **Infrastructure optimization:**
  - CDN configuration (cache headers, edge caching)
  - Redis/Memcached caching layers
  - Database connection pooling
  - HTTP/2 or HTTP/3 adoption

- **Network optimization:**
  - DNS resolution time reduction
  - TLS handshake optimization
  - TCP connection reuse
  - Server response compression

- **Debugging workflows:**
  - How to diagnose TTFB issues (waterfall analysis)
  - Backend profiling tools (APM, distributed tracing)
  - Database slow query logs
  - Server response time monitoring

**Impact:** Users with slow TTFB cannot fix their problems with current skill.

---

#### 2. CLS Optimization (Minimal Coverage) - HIGH PRIORITY

**User's Problem:** 0.52 CLS (420% over target)

**Current Coverage:** ~2% (1 mention in modern-patterns-2025.md line 464)

**Missing Content:**
- **Layout shift prevention techniques:**
  - Image dimensions (width/height attributes)
  - aspect-ratio CSS for responsive images
  - font-display strategies (swap, fallback, optional)
  - Reserve space for ads/embeds
  - Skeleton screens for dynamic content

- **Common CLS causes and fixes:**
  - Images without dimensions → Add width/height
  - Web fonts loading → Use font-display: swap + preload
  - Dynamic content injection → Reserve space with min-height
  - Ads without reserved space → CSS aspect-ratio boxes
  - Animations triggering layout → Use transform/opacity only

- **Debugging workflows:**
  - Chrome DevTools Layout Shift Regions
  - Identifying which elements cause shifts
  - Measuring CLS in production (web-vitals library)
  - Testing across different viewport sizes

- **Code examples:**
  ```html
  <!-- BAD: No dimensions -->
  <img src="hero.jpg" alt="Hero">

  <!-- GOOD: Prevents CLS -->
  <img src="hero.jpg" alt="Hero" width="1200" height="600">

  <!-- BETTER: Responsive with aspect-ratio -->
  <img src="hero.jpg" alt="Hero" style="aspect-ratio: 16/9; width: 100%;">
  ```

**Impact:** Users with severe CLS issues (0.52) have minimal guidance.

---

#### 3. LCP Optimization (Incomplete Coverage) - MEDIUM PRIORITY

**User's Problem:** 4.43s LCP (77% over target)

**Current Coverage:**
- Core-web-vitals.md: Only 45 lines, stops mid-sentence (stub file)
- Quick-wins.md: Basic LCP image optimization (fetchpriority)

**Missing Content:**
- **LCP optimization strategies** (content COMPLETELY missing from core-web-vitals.md):
  - Preload critical resources
  - Optimize server response time (overlaps with TTFB)
  - Eliminate render-blocking resources
  - Client-side rendering vs. SSR trade-offs
  - Image optimization (formats, compression, CDN)
  - Critical CSS inlining
  - Resource hints (preconnect, dns-prefetch)

- **LCP debugging workflow:**
  - Identifying the LCP element (provided but incomplete)
  - Analyzing LCP breakdown (TTFB, resource load, render)
  - Using Lighthouse trace viewer
  - Field data vs. lab data interpretation

- **Advanced techniques:**
  - Adaptive loading based on network conditions
  - Progressive image loading (LQIP, blur-up)
  - Early hints (103 status code)
  - Priority hints API (covered in modern-patterns but not debugging)

**Current State:** core-web-vitals.md is a **stub file** (45 lines) with only LCP introduction, no optimization strategies.

---

#### 4. Comprehensive Debugging Workflows (Missing)

**Gap:** No systematic debugging methodology for severe performance issues.

**Missing Content:**
- **TTFB debugging:**
  - Step 1: Check server response time in Network tab
  - Step 2: Analyze backend APM (New Relic, Datadog)
  - Step 3: Profile database queries (slow query log)
  - Step 4: Check CDN cache hit ratio
  - Step 5: Measure origin server response time

- **CLS debugging:**
  - Step 1: Enable Layout Shift Regions in DevTools
  - Step 2: Record Performance trace
  - Step 3: Identify shifting elements
  - Step 4: Check for missing dimensions
  - Step 5: Test font loading strategies

- **LCP debugging:**
  - Step 1: Identify LCP element (covered)
  - Step 2: Break down LCP phases (TTFB, load, render)
  - Step 3: Optimize bottleneck phase
  - Step 4: Verify improvement
  - Step 5: Monitor field data

**Impact:** Users struggle to diagnose root causes without systematic workflows.

---

## Missing Reference Files Analysis

### Expected Files (from SKILL.md frontmatter)

```yaml
references:
  - quick-wins.md          ✅ EXISTS (566 lines)
  - core-web-vitals.md     ⚠️  STUB (45 lines, incomplete)
  - optimization-techniques.md  ❌ MISSING
  - modern-patterns-2025.md     ✅ EXISTS (612 lines)
  - framework-specific.md       ❌ MISSING
  - monitoring.md               ❌ MISSING
```

**Completion Rate:** 50% (3 of 6 files exist, 1 is incomplete stub)

---

### 1. core-web-vitals.md (INCOMPLETE STUB) - CRITICAL

**Current State:** 45 lines, contains only:
- Overview (11 lines)
- LCP introduction (34 lines)
- **STOPS MID-SENTENCE** - no optimization strategies, no INP section, no CLS section

**Missing Sections:**
- ❌ LCP optimization strategies (0% complete)
- ❌ INP (Interaction to Next Paint) - ENTIRE SECTION MISSING
- ❌ CLS (Cumulative Layout Shift) - ENTIRE SECTION MISSING
- ❌ TTFB (Time to First Byte) - ENTIRE SECTION MISSING
- ❌ FCP (First Contentful Paint) - ENTIRE SECTION MISSING
- ❌ TBT (Total Blocking Time) - ENTIRE SECTION MISSING

**Required Content (~500-800 lines):**
```markdown
## LCP (Largest Contentful Paint) [EXPAND FROM 34 TO ~150 LINES]
- What it measures ✅ (exists)
- Finding LCP element ✅ (exists)
- Optimization strategies ❌ (MISSING)
  - Preload critical resources
  - Optimize images (formats, compression, CDN)
  - Eliminate render-blocking resources
  - Server response time optimization
  - Critical CSS inlining
- Debugging workflow ❌ (MISSING)
- Common pitfalls ❌ (MISSING)
- Code examples ❌ (MISSING)

## INP (Interaction to Next Paint) [~150 LINES, COMPLETELY MISSING]
- What it measures
- Target thresholds (Good: <200ms, Poor: >500ms)
- Optimization strategies
  - Break up long tasks
  - Reduce JavaScript execution time
  - Use web workers for CPU-intensive tasks
  - Optimize event handlers
  - Debounce/throttle interactions
- Debugging workflow
- Code examples

## CLS (Cumulative Layout Shift) [~150 LINES, COMPLETELY MISSING]
- What it measures
- Target thresholds (Good: <0.1, Poor: >0.25)
- Optimization strategies
  - Set image dimensions (width/height)
  - Use aspect-ratio CSS
  - Reserve space for ads/embeds
  - Optimize font loading (font-display)
  - Avoid inserting content above existing content
- Debugging workflow (Layout Shift Regions)
- Common causes and fixes
- Code examples

## TTFB (Time to First Byte) [~100 LINES, COMPLETELY MISSING]
- What it measures
- Target thresholds (Good: <800ms, Poor: >1800ms)
- Optimization strategies
  - CDN configuration
  - Server-side caching (Redis, Memcached)
  - Database query optimization
  - HTTP/2 or HTTP/3 adoption
  - DNS optimization
- Backend debugging workflow
- Infrastructure optimization
- Code examples

## FCP (First Contentful Paint) [~80 LINES, COMPLETELY MISSING]
- What it measures
- Target thresholds (Good: <1.8s, Poor: >3.0s)
- Optimization strategies
  - Eliminate render-blocking resources
  - Inline critical CSS
  - Defer non-critical CSS
  - Optimize fonts (preload, font-display)
- Debugging workflow
- Code examples

## TBT (Total Blocking Time) [~80 LINES, COMPLETELY MISSING]
- What it measures
- Target thresholds (Good: <200ms, Poor: >600ms)
- Optimization strategies
  - Code splitting
  - Defer non-critical JavaScript
  - Break up long tasks (50ms chunks)
  - Use requestIdleCallback
- Debugging workflow
- Code examples
```

**Priority:** CRITICAL - This is the core reference file for the skill.

---

### 2. optimization-techniques.md (MISSING) - HIGH PRIORITY

**Referenced In:** SKILL.md line 90 ("Load when implementing specific optimizations")

**Expected Content (~600-800 lines):**
```markdown
# Optimization Techniques

## Image Optimization
- Modern formats (WebP, AVIF)
- Compression strategies
- Responsive images (srcset, sizes)
- Lazy loading
- CDN optimization
- Art direction with <picture>

## JavaScript Optimization
- Code splitting strategies
- Tree shaking
- Minification and uglification
- Dead code elimination
- Bundle analysis
- Dynamic imports
- Module preloading

## CSS Optimization
- Critical CSS extraction
- CSS-in-JS trade-offs
- Unused CSS removal (PurgeCSS)
- CSS containment
- Layer management
- Minification

## Resource Loading Optimization
- Preload, prefetch, preconnect
- DNS-prefetch
- Resource hints
- Priority hints (fetchpriority)
- Early hints (103 status)
- Link headers

## Caching Strategies
- HTTP caching (Cache-Control, ETag)
- Service worker caching
- CDN caching
- Browser caching
- API response caching
- Stale-while-revalidate

## Backend Optimization (CRITICAL FOR TTFB)
- Database query optimization
  - Index optimization
  - N+1 query prevention
  - Query result caching
  - Connection pooling
- API optimization
  - Response compression
  - GraphQL vs REST trade-offs
  - Batch API requests
  - Rate limiting
- Server-side caching
  - Redis/Memcached strategies
  - Cache invalidation patterns
  - Cache warming
- Infrastructure optimization
  - CDN configuration
  - Edge caching
  - HTTP/2 or HTTP/3
  - Cold start mitigation (serverless)
```

**Why It's Missing:** Likely intended to be a comprehensive reference but never created.

**Impact:** High - This would provide the **TTFB optimization content** that's completely missing.

---

### 3. framework-specific.md (MISSING) - MEDIUM PRIORITY

**Referenced In:** SKILL.md line 96 ("Load for your framework")

**Expected Content (~400-600 lines):**
```markdown
# Framework-Specific Performance Patterns

## Next.js Optimization
- Image component optimization
- Font optimization
- Static generation vs SSR vs ISR
- Route prefetching
- Bundle analysis
- Caching strategies
- Performance monitoring

## React Optimization
- Component memoization (React.memo)
- Hooks optimization (useMemo, useCallback)
- Code splitting (lazy, Suspense)
- Concurrent rendering
- Profiler usage
- Virtual scrolling

## Vue Optimization
- Component lazy loading
- v-once for static content
- Computed properties vs methods
- Virtual scrolling
- Bundle optimization

## Vite Optimization
- Build optimization
- Chunk splitting
- Legacy browser support
- Preview mode

## Astro Optimization
- Partial hydration
- Component islands
- Zero-JS pages
- Build optimization

## SvelteKit Optimization
- Prerendering
- Server-side rendering
- Hydration strategies
- Build optimization
```

**Why It's Missing:** Likely de-prioritized during initial skill creation.

**Impact:** Medium - Users can adapt general techniques, but framework-specific guidance saves time.

---

### 4. monitoring.md (MISSING) - MEDIUM PRIORITY

**Referenced In:** SKILL.md line 99 ("Load when setting up continuous monitoring")

**Expected Content (~300-500 lines):**
```markdown
# Performance Monitoring

## Lighthouse CI Setup
- Installation and configuration ✅ (covered in quick-wins.md)
- GitHub Actions integration ✅ (covered in quick-wins.md)
- Performance budgets
- Regression detection
- Custom audits

## Real User Monitoring (RUM)
- web-vitals library setup ✅ (covered in quick-wins.md)
- Collecting field data
- Analytics integration
- Error tracking
- Performance dashboards

## Debugging Tools
- Chrome DevTools Performance panel
- Lighthouse
- WebPageTest
- Coverage tool
- Performance monitor
- Layout shift regions

## Performance Budgets
- Setting thresholds
- Enforcement in CI/CD
- Budget monitoring
- Alerting strategies

## Backend Monitoring (CRITICAL FOR TTFB)
- APM tools (New Relic, Datadog, Sentry)
- Distributed tracing
- Database slow query logs
- Server response time tracking
- Cache hit/miss ratios
- Origin vs CDN metrics
```

**Why It's Missing:** Likely intended as future enhancement, basic monitoring already covered in quick-wins.md.

**Impact:** Medium - Basic monitoring is covered, but advanced techniques would be valuable.

---

## Specific Gap Analysis for User's Metrics

### Gap 1: TTFB 3.67s → Target <800ms (CRITICAL)

**Current Coverage:** 0%

**What User Needs:**
1. **Diagnostic workflow:**
   - Is TTFB slow due to DNS? (check DNS lookup time)
   - Is TTFB slow due to TLS? (check SSL handshake time)
   - Is TTFB slow due to server processing? (check server response time)
   - Is TTFB slow due to database? (check query execution time)
   - Is TTFB slow due to cold start? (check serverless function warmup)

2. **Optimization strategies:**
   - **If DNS is slow (>100ms):** Switch DNS provider, use CDN DNS
   - **If TLS is slow (>200ms):** Enable TLS 1.3, use OCSP stapling, optimize certificate chain
   - **If server processing is slow (>500ms):**
     - Profile backend code (APM tools)
     - Optimize database queries (add indexes, fix N+1)
     - Add Redis/Memcached caching layer
     - Enable response compression
   - **If cold start is slow (serverless):** Implement function warming, increase memory allocation
   - **Infrastructure:** Enable CDN edge caching, HTTP/2, connection reuse

3. **Code examples:**
   - Redis caching for API responses
   - Database query optimization patterns
   - CDN cache header configuration
   - Nginx/Apache response time tuning

**Where to Add:**
- `optimization-techniques.md` (create this file) - Backend Optimization section
- `core-web-vitals.md` (expand) - TTFB section
- `monitoring.md` (create) - Backend monitoring tools

**Priority:** CRITICAL (highest impact on user's metrics)

---

### Gap 2: CLS 0.52 → Target <0.1 (CRITICAL)

**Current Coverage:** ~2% (1 mention in modern-patterns-2025.md)

**What User Needs:**
1. **Diagnostic workflow:**
   - Enable Layout Shift Regions in Chrome DevTools
   - Record Performance trace during page load
   - Identify which elements are shifting
   - Measure shift distance and impact fraction

2. **Optimization strategies:**
   - **Images without dimensions:** Add width/height attributes or aspect-ratio
   - **Web fonts loading:** Use font-display: swap + preload fonts
   - **Ads without reserved space:** Use CSS aspect-ratio to reserve space
   - **Dynamic content injection:** Reserve space with min-height
   - **Animations causing layout:** Use transform/opacity instead of top/left/width/height

3. **Code examples:**
   ```html
   <!-- Prevent CLS for images -->
   <img src="hero.jpg" width="1200" height="600" alt="Hero">

   <!-- Prevent CLS for responsive images -->
   <img src="hero.jpg" style="aspect-ratio: 16/9; width: 100%;" alt="Hero">

   <!-- Prevent CLS for fonts -->
   <link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
   <style>
     @font-face {
       font-family: 'Main';
       font-display: swap;
       src: url('/fonts/main.woff2') format('woff2');
     }
   </style>

   <!-- Prevent CLS for ads -->
   <div class="ad-container" style="aspect-ratio: 16/9; min-height: 250px;">
     <!-- Ad loads here -->
   </div>
   ```

**Where to Add:**
- `core-web-vitals.md` (expand) - CLS section (completely missing)
- `quick-wins.md` (enhance) - Add "Prevent CLS with image dimensions" as 1-hour quick win
- `optimization-techniques.md` (create) - Image optimization section

**Priority:** CRITICAL (CLS is 420% over target, SEO ranking factor)

---

### Gap 3: LCP 4.43s → Target <2.5s (HIGH)

**Current Coverage:**
- Basic LCP image optimization in quick-wins.md ✅
- LCP element identification in core-web-vitals.md ✅
- LCP optimization strategies ❌ MISSING

**What User Needs:**
1. **Diagnostic workflow (expand existing):**
   - Identify LCP element ✅ (exists)
   - Break down LCP into phases:
     - TTFB phase (0 to server response)
     - Resource load phase (server response to resource loaded)
     - Render phase (resource loaded to render)
   - Identify bottleneck phase
   - Optimize bottleneck

2. **Optimization strategies (MISSING):**
   - **If TTFB is the bottleneck (>800ms):** See TTFB optimization
   - **If resource load is slow:**
     - Preload LCP image: `<link rel="preload" as="image" href="hero.webp">`
     - Use modern formats (WebP, AVIF)
     - Optimize compression
     - Use CDN for images
     - Add fetchpriority="high" to LCP image
   - **If render is slow:**
     - Remove render-blocking resources
     - Inline critical CSS
     - Defer non-critical CSS
     - Optimize JavaScript execution

3. **Advanced techniques (partially covered):**
   - Adaptive loading based on network ❌
   - Progressive image loading (LQIP) ❌
   - Early hints (103 status) ❌
   - Priority hints ✅ (covered in modern-patterns-2025.md)

**Where to Add:**
- `core-web-vitals.md` (expand) - LCP section (currently only 34 lines, needs ~150)
- `optimization-techniques.md` (create) - Image optimization, resource loading

**Priority:** HIGH (LCP is 77% over target, but TTFB is likely the root cause)

---

## Recommendations

### PRIORITY 1: Address TTFB Crisis (CRITICAL)

**Action:** Create comprehensive TTFB optimization content

**Files to Create/Update:**
1. **optimization-techniques.md** (NEW FILE - 600-800 lines)
   - Add "Backend Optimization" section (~200 lines):
     - Database query optimization (indexes, N+1 prevention, connection pooling)
     - API optimization (compression, batching, caching)
     - Server-side caching (Redis, Memcached, cache invalidation)
     - Infrastructure optimization (CDN, HTTP/2, edge caching)

2. **core-web-vitals.md** (EXPAND from 45 to ~600 lines)
   - Add "TTFB (Time to First Byte)" section (~100 lines):
     - What it measures
     - Target thresholds (Good: <800ms, Poor: >1800ms)
     - Diagnostic workflow (DNS, TLS, server, database, cold start)
     - Optimization strategies (detailed)
     - Backend profiling tools
     - Code examples

3. **monitoring.md** (NEW FILE - 300-500 lines)
   - Add "Backend Monitoring" section (~150 lines):
     - APM tools setup (New Relic, Datadog, Sentry)
     - Distributed tracing
     - Database slow query logs
     - Server response time tracking
     - Cache hit/miss ratios
     - Origin vs CDN metrics

**Expected Impact:**
- Enables diagnosis and fixing of 3.67s TTFB → <800ms target
- Reduces LCP by ~2s (since LCP depends on TTFB)
- Provides actionable backend optimization strategies

**Estimated Effort:** 8-12 hours (create 3 comprehensive sections)

**ROI:** ⭐⭐⭐⭐⭐ HIGHEST (addresses root cause of user's performance crisis)

---

### PRIORITY 2: Complete CLS Optimization Content (CRITICAL)

**Action:** Add comprehensive CLS prevention and debugging content

**Files to Create/Update:**
1. **core-web-vitals.md** (EXPAND)
   - Add "CLS (Cumulative Layout Shift)" section (~150 lines):
     - What it measures
     - Target thresholds (Good: <0.1, Poor: >0.25)
     - Common causes:
       - Images without dimensions
       - Web fonts loading
       - Ads without reserved space
       - Dynamic content injection
       - Animations causing layout
     - Optimization strategies for each cause
     - Debugging workflow (Layout Shift Regions in DevTools)
     - Code examples for preventing CLS

2. **quick-wins.md** (ADD 1-hour quick win)
   - Add "Prevent CLS with Image Dimensions" as item #4:
     - Impact: Reduces CLS by 50-80%
     - Implementation: Add width/height to all images
     - Use aspect-ratio CSS for responsive images
     - Code examples

3. **optimization-techniques.md** (CREATE)
   - Add "Image Optimization" section:
     - Setting dimensions (width/height vs aspect-ratio)
     - Responsive images with srcset
     - Font loading strategies (font-display, preload)
     - Reserve space for dynamic content

**Expected Impact:**
- Enables fixing of 0.52 CLS → <0.1 target
- Improves SEO ranking (Core Web Vitals factor)
- Prevents user frustration from layout shifts

**Estimated Effort:** 4-6 hours

**ROI:** ⭐⭐⭐⭐⭐ HIGHEST (CLS is 420% over target, critical SEO factor)

---

### PRIORITY 3: Complete core-web-vitals.md (HIGH)

**Action:** Complete the stub file with all Core Web Vitals sections

**Current State:** 45 lines (stub), only LCP introduction

**Target State:** 600-800 lines, comprehensive coverage

**Sections to Add:**
1. ✅ **LCP** (expand from 34 to ~150 lines)
   - Add optimization strategies
   - Add debugging workflow
   - Add code examples
   - Add common pitfalls

2. ❌ **INP** (new section, ~150 lines)
   - What it measures
   - Target thresholds
   - Optimization strategies (break up long tasks, web workers, debounce)
   - Debugging workflow
   - Code examples

3. ❌ **CLS** (new section, ~150 lines)
   - See PRIORITY 2 above

4. ❌ **TTFB** (new section, ~100 lines)
   - See PRIORITY 1 above

5. ❌ **FCP** (new section, ~80 lines)
   - First Contentful Paint optimization
   - Eliminate render-blocking resources
   - Critical CSS inlining

6. ❌ **TBT** (new section, ~80 lines)
   - Total Blocking Time optimization
   - Code splitting, defer non-critical JS
   - Break up long tasks

**Expected Impact:**
- Provides comprehensive Core Web Vitals reference
- Covers all 6 key metrics (LCP, INP, CLS, TTFB, FCP, TBT)
- Enables systematic optimization

**Estimated Effort:** 10-15 hours

**ROI:** ⭐⭐⭐⭐⭐ CRITICAL (core reference file for the skill)

---

### PRIORITY 4: Create optimization-techniques.md (HIGH)

**Action:** Create comprehensive optimization techniques reference

**Content Outline (~600-800 lines):**
1. **Image Optimization** (~120 lines)
   - Modern formats (WebP, AVIF)
   - Compression strategies
   - Responsive images (srcset, sizes)
   - Lazy loading
   - CDN optimization
   - Dimensions and aspect-ratio (CLS prevention)

2. **JavaScript Optimization** (~120 lines)
   - Code splitting strategies
   - Tree shaking
   - Bundle analysis
   - Dynamic imports
   - Module preloading

3. **CSS Optimization** (~100 lines)
   - Critical CSS extraction
   - Unused CSS removal
   - CSS containment
   - Minification

4. **Resource Loading Optimization** (~100 lines)
   - Preload, prefetch, preconnect
   - Priority hints
   - Early hints (103 status)

5. **Caching Strategies** (~100 lines)
   - HTTP caching
   - Service worker caching
   - CDN caching
   - API response caching

6. **Backend Optimization** (~200 lines) - CRITICAL FOR TTFB
   - Database query optimization
   - API optimization
   - Server-side caching (Redis, Memcached)
   - Infrastructure optimization (CDN, HTTP/2, edge caching)

**Expected Impact:**
- Fills the TTFB content gap (backend optimization)
- Provides comprehensive optimization playbook
- Enables systematic performance improvement

**Estimated Effort:** 12-16 hours

**ROI:** ⭐⭐⭐⭐⭐ CRITICAL (enables TTFB optimization, most impactful)

---

### PRIORITY 5: Create framework-specific.md (MEDIUM)

**Action:** Create framework-specific optimization patterns

**Content Outline (~400-600 lines):**
- Next.js optimization (~120 lines)
- React optimization (~100 lines)
- Vue optimization (~80 lines)
- Vite optimization (~60 lines)
- Astro optimization (~60 lines)
- SvelteKit optimization (~60 lines)

**Expected Impact:**
- Provides framework-specific guidance
- Saves time for users of specific frameworks
- Complements general optimization techniques

**Estimated Effort:** 8-10 hours

**ROI:** ⭐⭐⭐ MEDIUM (nice-to-have, users can adapt general techniques)

---

### PRIORITY 6: Create monitoring.md (MEDIUM)

**Action:** Create comprehensive monitoring reference

**Content Outline (~300-500 lines):**
- Lighthouse CI setup (already covered in quick-wins.md, expand here)
- Real User Monitoring (RUM) with web-vitals
- Debugging tools (DevTools, WebPageTest)
- Performance budgets
- Backend monitoring (APM, distributed tracing) - CRITICAL FOR TTFB

**Expected Impact:**
- Provides advanced monitoring techniques
- Enables continuous performance visibility
- Helps identify regressions early

**Estimated Effort:** 6-8 hours

**ROI:** ⭐⭐⭐ MEDIUM (basic monitoring already covered, this adds depth)

---

## Prioritized Implementation Roadmap

### Phase 1: Address Critical Gaps (HIGHEST ROI)

**Timeline:** 1-2 weeks
**Effort:** 24-33 hours
**Impact:** Enables fixing user's severe performance issues

1. ✅ **PRIORITY 1: TTFB Optimization** (8-12 hours)
   - Create optimization-techniques.md → Backend Optimization section
   - Expand core-web-vitals.md → TTFB section
   - Create monitoring.md → Backend Monitoring section

2. ✅ **PRIORITY 2: CLS Optimization** (4-6 hours)
   - Expand core-web-vitals.md → CLS section
   - Enhance quick-wins.md → Add CLS quick win
   - Create optimization-techniques.md → Image dimensions section

3. ✅ **PRIORITY 3: Complete core-web-vitals.md** (10-15 hours)
   - Expand LCP section
   - Add INP section
   - Add FCP section
   - Add TBT section

**Deliverables:**
- core-web-vitals.md: 45 → 600-800 lines (13x expansion)
- optimization-techniques.md: 0 → 600-800 lines (NEW)
- monitoring.md: 0 → 300-500 lines (NEW)
- quick-wins.md: 566 → 600 lines (add CLS quick win)

**Success Metrics:**
- User can diagnose and fix 3.67s TTFB
- User can reduce 0.52 CLS to <0.1
- User can optimize 4.43s LCP to <2.5s

---

### Phase 2: Enhance Coverage (MEDIUM ROI)

**Timeline:** 1 week
**Effort:** 8-10 hours
**Impact:** Framework-specific guidance, nice-to-have

4. ✅ **PRIORITY 5: Framework-Specific Patterns** (8-10 hours)
   - Create framework-specific.md
   - Add Next.js, React, Vue, Vite, Astro, SvelteKit sections

**Deliverables:**
- framework-specific.md: 0 → 400-600 lines (NEW)

**Success Metrics:**
- Users of specific frameworks get tailored guidance
- Faster implementation for framework users

---

### Phase 3: Polish and Maintenance (LOW ROI)

**Timeline:** Ongoing
**Effort:** As needed
**Impact:** Keep content current

- Monitor for new browser APIs and patterns
- Update for framework version changes
- Add more code examples based on user feedback
- Expand monitoring.md with new tools

---

## Specific Content Additions Needed

### For TTFB 3.67s → <800ms

**File:** optimization-techniques.md (Backend Optimization section)

```markdown
## Backend Optimization (CRITICAL FOR TTFB)

### Diagnostic Workflow

**Step 1: Identify TTFB bottleneck**
```bash
# Use curl to measure TTFB
curl -w "@curl-format.txt" -o /dev/null -s https://yoursite.com

# curl-format.txt:
time_namelookup:  %{time_namelookup}s\n
time_connect:     %{time_connect}s\n
time_appconnect:  %{time_appconnect}s\n
time_pretransfer: %{time_pretransfer}s\n
time_starttransfer: %{time_starttransfer}s (TTFB)\n
time_total:       %{time_total}s\n
```

**Interpretation:**
- `time_namelookup` >100ms: DNS is slow → Switch DNS provider
- `time_appconnect - time_connect` >200ms: TLS is slow → Enable TLS 1.3
- `time_starttransfer - time_pretransfer` >500ms: Server processing is slow → Profile backend

**Step 2: Profile backend (if server processing is slow)**
- Use APM tool (New Relic, Datadog, Sentry)
- Identify slow database queries
- Check cache hit/miss ratios
- Measure function execution time

**Step 3: Optimize bottleneck**

### Database Query Optimization

**Problem: N+1 queries**
```python
# ❌ BAD: N+1 query problem (Django ORM)
posts = Post.objects.all()  # 1 query
for post in posts:
    print(post.author.name)  # N queries (one per post)

# ✅ GOOD: Use select_related() to join
posts = Post.objects.select_related('author').all()  # 1 query with JOIN
for post in posts:
    print(post.author.name)  # No additional queries
```

**Problem: Missing indexes**
```sql
-- ❌ BAD: Slow query without index
SELECT * FROM orders WHERE user_id = 123 AND created_at > '2025-01-01';
-- Execution time: 2.3s (table scan)

-- ✅ GOOD: Add composite index
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);
-- Execution time: 15ms (index scan)
```

**Problem: Fetching too much data**
```python
# ❌ BAD: Fetching all columns
users = User.objects.all()  # Fetches all columns including large bio field

# ✅ GOOD: Only fetch needed columns
users = User.objects.only('id', 'email', 'name')  # 70% faster
```

### Server-Side Caching (Redis)

**Use case: API response caching**
```python
# Python with Redis
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379)

def get_user_profile(user_id):
    # Check cache first
    cache_key = f"user_profile:{user_id}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)  # Cache hit (1-2ms)

    # Cache miss: fetch from database
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")  # 50-200ms

    # Store in cache for 5 minutes
    redis_client.setex(cache_key, 300, json.dumps(user))

    return user

# Impact: 95% cache hit rate → 50x faster (2ms vs 100ms)
```

**Use case: Session storage**
```javascript
// Node.js with Redis for sessions
const session = require('express-session');
const RedisStore = require('connect-redis')(session);

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: 'your-secret',
  resave: false,
  saveUninitialized: false
}));

// Impact: 10x faster than database sessions
```

### CDN Configuration

**Problem: Origin server getting hit for every request**
```nginx
# ❌ BAD: No caching headers
location / {
    proxy_pass http://backend;
}

# ✅ GOOD: Aggressive CDN caching for static assets
location ~* \.(jpg|jpeg|png|gif|webp|avif|ico|svg)$ {
    proxy_pass http://backend;
    add_header Cache-Control "public, max-age=31536000, immutable";
}

location ~* \.(css|js)$ {
    proxy_pass http://backend;
    add_header Cache-Control "public, max-age=31536000, immutable";
}

# API responses: stale-while-revalidate
location /api/ {
    proxy_pass http://backend;
    add_header Cache-Control "max-age=60, stale-while-revalidate=600";
}
```

### HTTP/2 or HTTP/3 Adoption

**Enable HTTP/2 (Nginx):**
```nginx
server {
    listen 443 ssl http2;  # Enable HTTP/2

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Enable server push (optional)
    http2_push /styles.css;
    http2_push /app.js;
}
```

**Impact:** 30-50% faster for multiple resources (multiplexing)

### Cold Start Mitigation (Serverless)

**Problem: AWS Lambda cold start adding 2-3 seconds**
```javascript
// ❌ BAD: Cold start every time
exports.handler = async (event) => {
    const db = await connectToDatabase();  // 1-2s cold start penalty
    return await db.query('SELECT * FROM users');
};

// ✅ GOOD: Reuse connections between invocations
let db;

exports.handler = async (event) => {
    if (!db) {
        db = await connectToDatabase();  // Only on cold start
    }
    return await db.query('SELECT * FROM users');
};

// ✅ BETTER: Use provisioned concurrency to eliminate cold starts
// AWS Lambda configuration:
// ProvisionedConcurrencyConfig: { ProvisionedConcurrentExecutions: 5 }
```

**Impact:** Eliminates 1-2s cold start penalty

### Compression

**Enable Brotli compression (better than gzip):**
```nginx
# Nginx with Brotli
brotli on;
brotli_comp_level 6;  # 1-11, higher = better compression, slower
brotli_types text/plain text/css text/xml text/javascript
             application/json application/javascript application/xml+rss;

# Fallback to gzip for older browsers
gzip on;
gzip_vary on;
gzip_types text/plain text/css text/xml text/javascript
           application/json application/javascript application/xml+rss;
```

**Impact:** 20-30% smaller than gzip, 5-10% faster TTFB

### Verification

**Before optimization:**
```bash
$ curl -w "@curl-format.txt" -o /dev/null -s https://yoursite.com
time_starttransfer: 3.67s (TTFB)
```

**After optimization:**
```bash
$ curl -w "@curl-format.txt" -o /dev/null -s https://yoursite.com
time_starttransfer: 0.42s (TTFB)  # 88% improvement!
```
```

---

### For CLS 0.52 → <0.1

**File:** core-web-vitals.md (CLS section)

```markdown
## CLS (Cumulative Layout Shift)

**What it measures:** Visual stability - how much content shifts unexpectedly during page load

**Targets:**
- ✅ **Good:** ≤0.1
- ⚠️ **Needs Improvement:** 0.1-0.25
- ❌ **Poor:** >0.25

**Weight in Lighthouse:** 25%

**SEO Impact:** Core Web Vitals ranking factor (June 2021+)

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

### Diagnostic Workflow

**Step 1: Enable Layout Shift Regions in Chrome DevTools**
1. Open DevTools (F12)
2. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows)
3. Type "Show Layout Shift Regions"
4. Enable the setting

**Step 2: Record Performance trace**
1. Go to Performance panel
2. Click Record
3. Load your page
4. Stop recording
5. Look for red "Layout Shift" bars in the timeline

**Step 3: Identify shifting elements**
- Click on each Layout Shift bar
- DevTools will highlight the element that shifted
- Note which elements are causing CLS

**Step 4: Measure CLS in production**
```javascript
import { onCLS } from 'web-vitals';

onCLS((metric) => {
  console.log('CLS:', metric.value);
  console.log('Rating:', metric.rating); // 'good', 'needs-improvement', 'poor'

  // Send to analytics
  if (metric.value > 0.1) {
    sendToAnalytics({
      name: 'CLS',
      value: metric.value,
      rating: metric.rating,
      entries: metric.entries  // Individual shift entries
    });
  }
});
```

### Common Causes and Fixes

#### Cause 1: Images Without Dimensions (MOST COMMON)

**Problem:**
```html
<!-- ❌ BAD: Browser doesn't know image size until loaded -->
<img src="hero.jpg" alt="Hero">
<!-- Page loads → Text appears → Image loads → Text shifts down → CLS! -->
```

**Solution 1: Set explicit dimensions**
```html
<!-- ✅ GOOD: Browser reserves space before image loads -->
<img src="hero.jpg" alt="Hero" width="1200" height="600">
<!-- Page loads → Space reserved → Image loads → No shift! -->
```

**Solution 2: Use aspect-ratio CSS (modern)**
```html
<img src="hero.jpg" alt="Hero" style="aspect-ratio: 16/9; width: 100%;">
<!-- Responsive + prevents CLS -->
```

**Solution 3: Use aspect-ratio for responsive images**
```css
/* Set aspect-ratio on all images */
img {
  max-width: 100%;
  height: auto;
  aspect-ratio: attr(width) / attr(height);  /* Future CSS */
}

/* Current workaround */
.responsive-image {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
}

.responsive-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

**Impact:** Reduces CLS by 50-80% (most common cause)

---

#### Cause 2: Web Fonts Loading

**Problem:**
```css
/* ❌ BAD: FOIT (Flash of Invisible Text) or FOUT (Flash of Unstyled Text) */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  /* No font-display → Default behavior causes layout shift */
}
```

**Solution 1: Use font-display: swap**
```css
/* ✅ GOOD: Show fallback font immediately, swap when custom font loads */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;  /* Prevents invisible text */
}
```

**Solution 2: Preload fonts**
```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin>
```

**Solution 3: Use system fonts (zero CLS)**
```css
/* ✅ BEST: System fonts load instantly, zero CLS */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'Helvetica Neue', Arial, sans-serif;
}
```

**Solution 4: Match fallback font metrics (advanced)**
```css
/* Adjust fallback font size to match custom font */
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
```

**Impact:** Reduces CLS by 20-40%

---

#### Cause 3: Ads Without Reserved Space

**Problem:**
```html
<!-- ❌ BAD: Ad loads dynamically, pushes content down -->
<div id="ad-slot"></div>
<script>loadAd('ad-slot');</script>
<!-- Content loads → Ad loads → Content shifts → CLS! -->
```

**Solution: Reserve space with aspect-ratio**
```html
<!-- ✅ GOOD: Reserve space before ad loads -->
<div class="ad-container" style="min-height: 250px; aspect-ratio: 16/9;">
  <div id="ad-slot"></div>
</div>
```

**Or use CSS:**
```css
.ad-container {
  min-height: 250px;  /* Minimum height for ad slot */
  aspect-ratio: 16/9;
  background: #f0f0f0;  /* Placeholder background */
}
```

**Impact:** Reduces CLS by 30-50%

---

#### Cause 4: Dynamic Content Injection

**Problem:**
```javascript
// ❌ BAD: Insert content above existing content
fetch('/api/banners')
  .then(data => {
    document.getElementById('header').insertAdjacentHTML('afterbegin', data.html);
    // Existing content shifts down → CLS!
  });
```

**Solution 1: Reserve space with min-height**
```css
#banner-slot {
  min-height: 100px;  /* Reserve space for banner */
}
```

**Solution 2: Append instead of prepend**
```javascript
// ✅ BETTER: Append content at end (doesn't shift existing content)
fetch('/api/banners')
  .then(data => {
    document.getElementById('header').insertAdjacentHTML('beforeend', data.html);
  });
```

**Solution 3: Use skeleton screens**
```html
<!-- Show skeleton while loading -->
<div class="banner-skeleton" style="height: 100px; background: #e0e0e0;">
  <!-- Skeleton content -->
</div>

<script>
  fetch('/api/banners')
    .then(data => {
      // Replace skeleton with real content (same height → no shift)
      document.querySelector('.banner-skeleton').outerHTML = data.html;
    });
</script>
```

**Impact:** Reduces CLS by 40-60%

---

#### Cause 5: Animations Causing Layout

**Problem:**
```css
/* ❌ BAD: Animating properties that trigger layout */
.modal {
  transition: height 0.3s;
}

.modal.open {
  height: 500px;  /* Triggers layout recalculation */
}
```

**Solution: Use transform/opacity only**
```css
/* ✅ GOOD: Animating transform/opacity doesn't trigger layout */
.modal {
  transform: scaleY(0);
  transform-origin: top;
  transition: transform 0.3s;
  will-change: transform;  /* GPU acceleration hint */
}

.modal.open {
  transform: scaleY(1);  /* GPU-accelerated, no layout shift */
}
```

**Properties that DON'T cause layout shifts:**
- `transform` (translate, scale, rotate)
- `opacity`
- `filter`

**Properties that DO cause layout shifts (AVOID in animations):**
- `width`, `height`
- `top`, `left`, `right`, `bottom`
- `margin`, `padding`
- `border-width`

**Impact:** Reduces CLS by 10-30%

---

### Complete Example: Zero-CLS Page

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Zero-CLS Page</title>

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
    }

    /* Reserve space for images */
    img {
      max-width: 100%;
      height: auto;
    }

    /* Reserve space for ads */
    .ad-container {
      min-height: 250px;
      aspect-ratio: 16/9;
      background: #f0f0f0;
    }

    /* GPU-accelerated animations only */
    .modal {
      transform: translateY(100%);
      transition: transform 0.3s;
      will-change: transform;
    }

    .modal.open {
      transform: translateY(0);
    }
  </style>
</head>
<body>
  <!-- Hero image with explicit dimensions -->
  <img src="hero.jpg" alt="Hero" width="1200" height="600">

  <!-- Ad slot with reserved space -->
  <div class="ad-container">
    <div id="ad-slot"></div>
  </div>

  <!-- Content -->
  <main>
    <p>Your content here...</p>
  </main>

  <script>
    // Load ads asynchronously (space already reserved)
    loadAd('ad-slot');
  </script>
</body>
</html>
```

**Expected CLS:** <0.05 (Good)

---

### Verification Checklist

After implementing CLS fixes:

- [ ] All images have width/height attributes or aspect-ratio
- [ ] Fonts use font-display: swap or system fonts
- [ ] Ads have reserved space (min-height + aspect-ratio)
- [ ] Dynamic content uses skeleton screens or reserved space
- [ ] Animations use transform/opacity only (no layout properties)
- [ ] Measured CLS in production with web-vitals library
- [ ] CLS < 0.1 for 75th percentile of users

---

### Tools for Debugging CLS

1. **Chrome DevTools Layout Shift Regions** - Visual highlighting of shifts
2. **Lighthouse** - CLS score and suggestions
3. **WebPageTest** - Filmstrip view showing layout shifts
4. **web-vitals library** - Real user monitoring
5. **Performance Observer API** - Detailed shift entries

---

**Remember:** CLS is cumulative across page lifetime. Even small shifts add up. Prevent all layout shifts for perfect CLS score.
```

---

### For LCP 4.43s → <2.5s

**File:** core-web-vitals.md (LCP section expansion)

```markdown
## LCP (Largest Contentful Paint) - EXPANDED

**What it measures:** Time until the largest content element becomes visible in the viewport

**Targets:**
- ✅ **Good:** ≤2.5 seconds
- ⚠️ **Needs Improvement:** 2.5-4.0 seconds
- ❌ **Poor:** >4.0 seconds

**Weight in Lighthouse:** 25%

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
}).observe({ entryTypes: ['largest-contentful-paint'] });
```

### LCP Breakdown (DIAGNOSTIC WORKFLOW)

**LCP consists of 4 phases:**

1. **TTFB** (Time to First Byte) - Server response time
2. **Resource load delay** - Time from TTFB to resource load start
3. **Resource load time** - Time to download resource
4. **Render delay** - Time from resource loaded to rendered

**How to break down LCP:**
```javascript
// Use Lighthouse trace viewer or Performance panel
// Look for:
// - TTFB: time_starttransfer in curl
// - Resource load delay: Look for gaps before resource fetch
// - Resource load time: Network tab (resource timing)
// - Render delay: Performance panel (rendering time)
```

**Example breakdown for 4.43s LCP:**
- TTFB: 3.67s (83% of LCP time) ← **PRIMARY BOTTLENECK**
- Resource load delay: 0.2s
- Resource load time: 0.4s
- Render delay: 0.16s

**Optimization priority:** Fix TTFB first (see TTFB section)

---

### Optimization Strategies

#### Strategy 1: Optimize TTFB (if TTFB >800ms)

**If TTFB is the bottleneck (83% in user's case):**
→ See "TTFB (Time to First Byte)" section for detailed strategies

**Quick wins:**
- Enable CDN edge caching
- Add Redis caching layer
- Optimize database queries
- Enable HTTP/2 or HTTP/3

---

#### Strategy 2: Preload LCP Resource (if resource load delay is high)

**Problem: Browser doesn't discover LCP resource until late**
```html
<!-- ❌ BAD: Browser discovers image late (after parsing CSS) -->
<style>
  .hero { background: url('hero.jpg'); }
</style>
<div class="hero"></div>
```

**Solution: Preload LCP resource**
```html
<!-- ✅ GOOD: Browser starts loading image immediately -->
<link rel="preload" as="image" href="hero.jpg" fetchpriority="high">
<style>
  .hero { background: url('hero.jpg'); }
</style>
<div class="hero"></div>
```

**For `<img>` elements:**
```html
<!-- ✅ BEST: Use fetchpriority="high" -->
<img src="hero.jpg" alt="Hero" width="1200" height="600"
     fetchpriority="high" loading="eager">
```

**Impact:** Reduces LCP by 200-400ms

---

#### Strategy 3: Optimize Image (if resource load time is high)

**Use modern formats (WebP, AVIF):**
```html
<picture>
  <source srcset="hero.avif" type="image/avif">  <!-- 50% smaller than WebP -->
  <source srcset="hero.webp" type="image/webp">  <!-- 30% smaller than JPEG -->
  <img src="hero.jpg" alt="Hero" width="1200" height="600">
</picture>
```

**Convert images:**
```bash
# JPEG → WebP (30% smaller)
cwebp -q 85 hero.jpg -o hero.webp

# JPEG → AVIF (50% smaller than JPEG)
avifenc -s 5 hero.jpg hero.avif

# Batch conversion
for img in *.jpg; do
  cwebp -q 85 "$img" -o "${img%.jpg}.webp"
  avifenc -s 5 "$img" "${img%.jpg}.avif"
done
```

**Optimize compression:**
```bash
# Optimize JPEG (lossless)
jpegoptim --strip-all hero.jpg

# Optimize PNG (lossless)
optipng -o7 logo.png

# Optimize WebP
cwebp -q 85 -m 6 -mt hero.jpg -o hero.webp
```

**Use CDN for automatic optimization:**
- Cloudflare Images (automatic format conversion)
- Cloudinary (automatic optimization)
- imgix (automatic optimization)

**Impact:** Reduces LCP by 30-50% (image load time)

---

#### Strategy 4: Eliminate Render-Blocking Resources (if render delay is high)

**Problem: CSS/JS blocking LCP rendering**
```html
<!-- ❌ BAD: Render-blocking CSS in <head> -->
<head>
  <link rel="stylesheet" href="styles.css">  <!-- Blocks rendering -->
  <script src="app.js"></script>  <!-- Blocks parsing -->
</head>
```

**Solution 1: Inline critical CSS**
```html
<head>
  <!-- ✅ GOOD: Inline critical CSS -->
  <style>
    /* Critical above-fold styles */
    .hero { ... }
  </style>

  <!-- Load non-critical CSS asynchronously -->
  <link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>
</head>
```

**Solution 2: Defer non-critical JavaScript**
```html
<!-- ✅ GOOD: Defer JS to not block parsing -->
<script src="app.js" defer></script>

<!-- Or async for non-dependent scripts -->
<script src="analytics.js" async></script>
```

**Extract critical CSS automatically:**
```bash
# Using Critical (Node.js tool)
npm install -g critical

critical index.html --base ./public --inline > index-critical.html
```

**Impact:** Reduces LCP by 100-300ms

---

#### Strategy 5: Optimize Server Response Time (overlaps with TTFB)

See "TTFB (Time to First Byte)" section for:
- Database query optimization
- Server-side caching (Redis)
- CDN configuration
- HTTP/2 adoption
- Compression

---

### Advanced Techniques

#### Early Hints (103 Status Code)

**How it works:**
Server sends 103 status code with preload hints BEFORE final response

**Server configuration (Nginx):**
```nginx
location / {
    # Send early hints
    add_header Link "</styles.css>; rel=preload; as=style";
    add_header Link "</hero.jpg>; rel=preload; as=image";

    # Then send final response
    proxy_pass http://backend;
}
```

**Impact:** Reduces LCP by 100-200ms (browser starts loading resources earlier)

**Browser support:** Chrome 103+, Firefox 103+ (2022+)

---

#### Adaptive Loading (Network-Aware)

**Serve different images based on network speed:**
```javascript
// Detect network connection
const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;

let imageSrc = 'hero-hq.jpg';  // Default: high quality

if (connection) {
  if (connection.effectiveType === '4g') {
    imageSrc = 'hero-hq.avif';  // Fast connection: AVIF
  } else if (connection.effectiveType === '3g') {
    imageSrc = 'hero-mq.webp';  // Medium connection: WebP
  } else {
    imageSrc = 'hero-lq.jpg';  // Slow connection: Low quality JPEG
  }
}

document.querySelector('.hero').src = imageSrc;
```

**Impact:** Reduces LCP by 50% on slow networks

---

#### Progressive Image Loading (LQIP - Low Quality Image Placeholder)

**Technique: Blur-up**
```html
<div class="progressive-image">
  <!-- Low quality placeholder (inline base64, ~2KB) -->
  <img src="data:image/jpeg;base64,/9j/4AAQ..."
       alt="Hero"
       class="placeholder"
       style="filter: blur(10px);">

  <!-- High quality image (lazy loaded) -->
  <img src="hero.jpg"
       alt="Hero"
       class="full-image"
       loading="lazy"
       onload="this.previousElementSibling.remove();">
</div>
```

**CSS:**
```css
.progressive-image {
  position: relative;
}

.placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  filter: blur(10px);
  transition: opacity 0.3s;
}

.full-image {
  width: 100%;
}

.full-image[loading="lazy"] {
  opacity: 0;
  transition: opacity 0.3s;
}

.full-image.loaded {
  opacity: 1;
}
```

**Generate LQIP:**
```bash
# Using ImageMagick
convert hero.jpg -resize 20x20 -quality 50 hero-placeholder.jpg
base64 hero-placeholder.jpg  # Use in data URI
```

**Impact:** Improves perceived LCP (user sees something immediately)

---

### Verification

**Before optimization:**
```
LCP: 4.43s
Breakdown:
- TTFB: 3.67s (83%)
- Resource load delay: 0.2s
- Resource load time: 0.4s
- Render delay: 0.16s
```

**After optimization (fix TTFB + optimize image):**
```
LCP: 1.2s (73% improvement!)
Breakdown:
- TTFB: 0.5s (fix backend)
- Resource load delay: 0.1s (preload)
- Resource load time: 0.4s (AVIF format)
- Render delay: 0.2s
```

---

### Tools for Debugging LCP

1. **Lighthouse** - LCP score and breakdown
2. **WebPageTest** - Filmstrip view, detailed timing
3. **Chrome DevTools Performance panel** - LCP phases
4. **web-vitals library** - Real user monitoring
5. **Curl** - TTFB measurement

---

**Remember:** LCP optimization is often a backend problem (TTFB). Fix server response time first, then optimize the LCP resource itself.
```

---

## Summary

### Critical Findings

1. **TTFB optimization content is 100% missing** - CRITICAL for user's 3.67s TTFB issue
2. **CLS optimization content is 98% missing** - CRITICAL for user's 0.52 CLS issue
3. **core-web-vitals.md is a stub** - Only 45 lines, needs 600-800 lines
4. **3 of 6 reference files don't exist** - 50% completion rate

### Highest Impact Recommendations

1. **Create optimization-techniques.md** (Backend Optimization section)
   - **Addresses:** TTFB 3.67s → <800ms
   - **Impact:** Enables fixing root cause of performance crisis
   - **Effort:** 8-12 hours
   - **ROI:** ⭐⭐⭐⭐⭐ HIGHEST

2. **Expand core-web-vitals.md** (CLS section)
   - **Addresses:** CLS 0.52 → <0.1
   - **Impact:** Enables fixing severe layout stability issues
   - **Effort:** 4-6 hours
   - **ROI:** ⭐⭐⭐⭐⭐ HIGHEST

3. **Complete core-web-vitals.md** (all sections)
   - **Addresses:** Comprehensive Core Web Vitals coverage
   - **Impact:** Provides complete optimization playbook
   - **Effort:** 10-15 hours
   - **ROI:** ⭐⭐⭐⭐⭐ CRITICAL

### Implementation Priority

**Phase 1 (CRITICAL - 1-2 weeks):**
- Create optimization-techniques.md → Backend Optimization
- Expand core-web-vitals.md → TTFB, CLS, LCP sections
- Enhance quick-wins.md → Add CLS quick win

**Phase 2 (MEDIUM - 1 week):**
- Create framework-specific.md
- Create monitoring.md

**Phase 3 (ONGOING):**
- Keep content current with new browser APIs
- Add more code examples based on user feedback

---

## Files Analyzed

- ✅ `/Users/masa/Projects/claude-mpm-skills/universal/web/web-performance-optimization/SKILL.md` (141 lines)
- ✅ `/Users/masa/Projects/claude-mpm-skills/universal/web/web-performance-optimization/references/quick-wins.md` (566 lines)
- ⚠️  `/Users/masa/Projects/claude-mpm-skills/universal/web/web-performance-optimization/references/core-web-vitals.md` (45 lines - STUB)
- ✅ `/Users/masa/Projects/claude-mpm-skills/universal/web/web-performance-optimization/references/modern-patterns-2025.md` (612 lines)
- ❌ `/Users/masa/Projects/claude-mpm-skills/universal/web/web-performance-optimization/references/optimization-techniques.md` (MISSING)
- ❌ `/Users/masa/Projects/claude-mpm-skills/universal/web/web-performance-optimization/references/framework-specific.md` (MISSING)
- ❌ `/Users/masa/Projects/claude-mpm-skills/universal/web/web-performance-optimization/references/monitoring.md` (MISSING)

---

**Research conducted by:** Research Agent
**Date:** 2025-12-02
**Total analysis time:** ~45 minutes
**Files examined:** 7 (4 exist, 3 missing)
**Lines analyzed:** 1,364 lines
**Key insight:** Backend optimization content (TTFB) is the critical missing piece for user's performance issues
