# Framework-Specific Performance Patterns

Optimization strategies tailored to popular web frameworks and build tools.

---

## Table of Contents

1. [Next.js Optimization](#nextjs-optimization)
2. [React Optimization](#react-optimization)
3. [Vue Optimization](#vue-optimization)
4. [Vite Optimization](#vite-optimization)
5. [Astro Optimization](#astro-optimization)
6. [SvelteKit Optimization](#sveltekit-optimization)

---

## Next.js Optimization

**Version:** Next.js 14+ (App Router and Pages Router)

### Image Optimization

Next.js Image component provides automatic optimization:

```jsx
import Image from 'next/image';

// ❌ BAD: Standard img tag
<img src="/hero.jpg" alt="Hero" />

// ✅ GOOD: Next.js Image component
<Image
    src="/hero.jpg"
    alt="Hero"
    width={1200}
    height={600}
    priority  // Preload LCP image
/>

// ✅ BETTER: Responsive images
<Image
    src="/hero.jpg"
    alt="Hero"
    fill
    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    priority
/>
```

**next.config.js optimization:**

```javascript
module.exports = {
    images: {
        formats: ['image/avif', 'image/webp'],  // Modern formats
        deviceSizes: [640, 750, 828, 1080, 1200, 1920],
        imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
        minimumCacheTTL: 60,
        remotePatterns: [
            {
                protocol: 'https',
                hostname: 'cdn.example.com',
            },
        ],
    },
};
```

**Impact:** Automatic WebP/AVIF, responsive sizes, lazy loading

---

### Font Optimization

**App Router (`app/layout.tsx`):**

```tsx
import { Inter, Roboto_Mono } from 'next/font/google';

// Load Google Fonts with automatic optimization
const inter = Inter({
    subsets: ['latin'],
    display: 'swap',  // Prevent FOIT
    variable: '--font-inter',
});

const robotoMono = Roboto_Mono({
    subsets: ['latin'],
    display: 'swap',
    variable: '--font-roboto-mono',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
            <body>{children}</body>
        </html>
    );
}
```

**Custom fonts (local):**

```tsx
import localFont from 'next/font/local';

const myFont = localFont({
    src: './fonts/my-font.woff2',
    display: 'swap',
    variable: '--font-custom',
});
```

**Impact:** Zero CLS, automatic preloading, self-hosted fonts

---

### Static Generation vs SSR vs ISR

**Performance trade-offs:**

| Strategy | TTFB | Build Time | Use Case |
|----------|------|------------|----------|
| **Static (SSG)** | <100ms | Long | Blog posts, marketing pages |
| **ISR** | <200ms | Medium | E-commerce, dynamic content with caching |
| **SSR** | 500-2000ms | Fast | User-specific pages, real-time data |
| **Client-side** | <100ms (HTML) | Fast | SPAs, dashboards |

**Static Generation (fastest TTFB):**

```tsx
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
    const posts = await getPosts();
    return posts.map((post) => ({ slug: post.slug }));
}

export default async function BlogPost({ params }: { params: { slug: string } }) {
    const post = await getPost(params.slug);
    return <article>{post.content}</article>;
}
```

**ISR (balanced):**

```tsx
// Revalidate every 60 seconds
export const revalidate = 60;

export default async function ProductPage({ params }: { params: { id: string } }) {
    const product = await getProduct(params.id);
    return <div>{product.name}</div>;
}
```

**SSR (dynamic data):**

```tsx
// Force dynamic rendering
export const dynamic = 'force-dynamic';

export default async function UserDashboard() {
    const session = await getSession();
    const userData = await getUserData(session.userId);
    return <Dashboard data={userData} />;
}
```

---

### Route Prefetching

Next.js automatically prefetches routes on `<Link>`:

```tsx
import Link from 'next/link';

// ✅ GOOD: Automatic prefetching
<Link href="/about" prefetch>About</Link>

// Disable prefetching for less important routes
<Link href="/legal" prefetch={false}>Legal</Link>

// Programmatic prefetching
import { useRouter } from 'next/navigation';

const router = useRouter();
router.prefetch('/products');
```

**Impact:** Instant navigation for prefetched routes

---

### Bundle Analysis

```bash
# Install bundle analyzer
npm install --save-dev @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
    enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
    // ... config
});

# Run analysis
ANALYZE=true npm run build
```

---

### Edge Runtime (App Router)

**Deploy performance-critical routes to edge:**

```tsx
// app/api/data/route.ts
export const runtime = 'edge';  // Run on Edge, not Node.js

export async function GET() {
    const data = await fetch('https://api.example.com/data');
    return Response.json(data);
}
```

**Impact:** 50-200ms faster TTFB (served from edge locations)

---

### Caching Strategies

**App Router caching:**

```tsx
// Aggressive caching (static data)
const data = await fetch('https://api.example.com/static', {
    cache: 'force-cache',
});

// Revalidate every 60 seconds
const data = await fetch('https://api.example.com/products', {
    next: { revalidate: 60 },
});

// No caching (always fresh)
const data = await fetch('https://api.example.com/user', {
    cache: 'no-store',
});
```

---

## React Optimization

### Component Memoization

**Prevent unnecessary re-renders:**

```jsx
import { memo, useMemo, useCallback } from 'react';

// ❌ BAD: Re-renders on every parent update
function ExpensiveComponent({ data }) {
    const processed = processData(data);  // Expensive computation runs every render
    return <div>{processed}</div>;
}

// ✅ GOOD: Memoize component
const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
    const processed = useMemo(() => processData(data), [data]);
    return <div>{processed}</div>;
});

// ✅ GOOD: Memoize callbacks
function Parent() {
    const [count, setCount] = useState(0);

    // ❌ BAD: New function every render
    const handleClick = () => setCount(count + 1);

    // ✅ GOOD: Memoized callback
    const handleClick = useCallback(() => setCount(c => c + 1), []);

    return <Child onClick={handleClick} />;
}
```

**When to memoize:**
- Components that render frequently with same props
- Expensive computations
- Callbacks passed to memoized child components

**When NOT to memoize:**
- Simple components (overhead not worth it)
- Props change frequently
- Premature optimization

---

### Code Splitting and Lazy Loading

```jsx
import { lazy, Suspense } from 'react';

// ❌ BAD: Load everything upfront
import HeavyChart from './HeavyChart';
import Dashboard from './Dashboard';

// ✅ GOOD: Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));
const Dashboard = lazy(() => import('./Dashboard'));

function App() {
    return (
        <Suspense fallback={<LoadingSpinner />}>
            <Dashboard />
            <HeavyChart />
        </Suspense>
    );
}
```

**Route-based code splitting:**

```jsx
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./routes/Home'));
const About = lazy(() => import('./routes/About'));
const Contact = lazy(() => import('./routes/Contact'));

function App() {
    return (
        <BrowserRouter>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/about" element={<About />} />
                    <Route path="/contact" element={<Contact />} />
                </Routes>
            </Suspense>
        </BrowserRouter>
    );
}
```

**Impact:** 30-50% smaller initial bundle

---

### Virtual Scrolling

**For long lists (1000+ items):**

```jsx
import { FixedSizeList } from 'react-window';

// ❌ BAD: Render all 10,000 items (slow!)
function List({ items }) {
    return (
        <div>
            {items.map(item => (
                <div key={item.id}>{item.name}</div>
            ))}
        </div>
    );
}

// ✅ GOOD: Virtual scrolling (only render visible items)
function VirtualizedList({ items }) {
    const Row = ({ index, style }) => (
        <div style={style}>{items[index].name}</div>
    );

    return (
        <FixedSizeList
            height={600}
            itemCount={items.length}
            itemSize={50}
            width="100%"
        >
            {Row}
        </FixedSizeList>
    );
}
```

**Impact:** 10-100x faster for long lists

---

### React Profiler

**Identify performance bottlenecks:**

```jsx
import { Profiler } from 'react';

function onRenderCallback(
    id,
    phase,  // "mount" or "update"
    actualDuration,  // Time spent rendering
    baseDuration,  // Estimated time without memoization
    startTime,
    commitTime
) {
    console.log(`${id} (${phase}) took ${actualDuration}ms`);
}

<Profiler id="Dashboard" onRender={onRenderCallback}>
    <Dashboard />
</Profiler>
```

---

## Vue Optimization

### Component Lazy Loading

```vue
<script setup>
import { defineAsyncComponent } from 'vue';

// ❌ BAD: Load everything upfront
import HeavyChart from './HeavyChart.vue';

// ✅ GOOD: Lazy load heavy components
const HeavyChart = defineAsyncComponent(() => import('./HeavyChart.vue'));
</script>

<template>
    <Suspense>
        <HeavyChart />
        <template #fallback>
            <LoadingSpinner />
        </template>
    </Suspense>
</template>
```

---

### Computed Properties vs Methods

```vue
<script setup>
import { ref, computed } from 'vue';

const items = ref([1, 2, 3, 4, 5]);

// ❌ BAD: Method runs on every render
function filteredItems() {
    return items.value.filter(i => i > 2);
}

// ✅ GOOD: Computed property cached
const filteredItems = computed(() => {
    return items.value.filter(i => i > 2);
});
</script>
```

---

### v-once for Static Content

```vue
<template>
    <!-- Render once, never update -->
    <div v-once>
        <h1>{{ staticTitle }}</h1>
        <p>{{ staticContent }}</p>
    </div>

    <!-- Render once per item -->
    <div v-for="item in items" :key="item.id">
        <div v-once>{{ item.staticData }}</div>
        <div>{{ item.dynamicData }}</div>
    </div>
</template>
```

**Impact:** 50-80% faster re-renders for static content

---

### Virtual Scrolling (Vue)

```vue
<script setup>
import { VirtualScroller } from 'vue-virtual-scroller';
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css';

const items = ref([...Array(10000).keys()]);
</script>

<template>
    <VirtualScroller
        :items="items"
        :item-size="50"
        class="scroller"
    >
        <template #default="{ item }">
            <div class="item">{{ item }}</div>
        </template>
    </VirtualScroller>
</template>
```

---

## Vite Optimization

### Build Optimization

```javascript
// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
    build: {
        // Chunk splitting strategy
        rollupOptions: {
            output: {
                manualChunks: {
                    // Vendor chunk
                    vendor: ['react', 'react-dom'],
                    // UI library chunk
                    ui: ['@mui/material'],
                },
            },
        },
        // Production optimizations
        minify: 'terser',
        terserOptions: {
            compress: {
                drop_console: true,  // Remove console.log
                drop_debugger: true,
            },
        },
        // Source map (disable in production)
        sourcemap: false,
        // Chunk size warnings
        chunkSizeWarningLimit: 500,
    },
    // CSS code splitting
    css: {
        devSourcemap: false,
    },
});
```

---

### Legacy Browser Support

```javascript
// vite.config.js
import legacy from '@vitejs/plugin-legacy';

export default defineConfig({
    plugins: [
        legacy({
            targets: ['defaults', 'not IE 11'],
            modernPolyfills: true,
            renderLegacyChunks: false,
        }),
    ],
});
```

---

### Preview Mode (Production Testing)

```bash
# Build for production
npm run build

# Preview production build locally
npm run preview
```

---

## Astro Optimization

### Partial Hydration (Component Islands)

**Astro's killer feature: Zero JS by default**

```astro
---
// src/pages/index.astro
import HeavyInteractive from '../components/HeavyInteractive.jsx';
import StaticComponent from '../components/StaticComponent.astro';
---

<html>
    <body>
        <!-- Static component: Zero JS shipped -->
        <StaticComponent />

        <!-- Interactive component: Only load when visible -->
        <HeavyInteractive client:visible />

        <!-- Interactive component: Load immediately -->
        <ChatWidget client:load />

        <!-- Interactive component: Load when idle -->
        <Analytics client:idle />
    </body>
</html>
```

**Client directives:**
- `client:load` - Load immediately (critical interactivity)
- `client:idle` - Load when browser idle (non-critical)
- `client:visible` - Load when scrolled into view (below fold)
- `client:media` - Load based on media query
- `client:only` - Only render on client (skip SSR)

**Impact:** 90-99% less JavaScript shipped

---

### Zero-JS Pages

```astro
---
// Completely static page - ZERO JavaScript
const posts = await getPosts();
---

<html>
    <head>
        <title>Blog</title>
    </head>
    <body>
        {posts.map(post => (
            <article>
                <h2>{post.title}</h2>
                <p>{post.excerpt}</p>
            </article>
        ))}
    </body>
</html>
```

**Impact:** LCP <1s, perfect Lighthouse scores

---

### Build Optimization

```javascript
// astro.config.mjs
export default defineConfig({
    output: 'static',  // or 'server' for SSR
    build: {
        inlineStylesheets: 'auto',
    },
    vite: {
        build: {
            cssCodeSplit: true,
        },
    },
});
```

---

## SvelteKit Optimization

### Prerendering (SSG)

```javascript
// src/routes/blog/[slug]/+page.js
export const prerender = true;

export async function load({ params }) {
    const post = await getPost(params.slug);
    return { post };
}
```

---

### Server-Side Rendering

```javascript
// src/routes/+page.server.js
export async function load() {
    const data = await fetchData();
    return { data };
}
```

---

### Hydration Strategies

```svelte
<!-- +page.svelte -->
<script>
    // Only runs on client after hydration
    import { browser } from '$app/environment';

    if (browser) {
        // Client-only code
        initializeAnalytics();
    }
</script>
```

---

### Build Optimization

```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-auto';

export default {
    kit: {
        adapter: adapter(),
        prerender: {
            crawl: true,
            entries: ['*'],
        },
    },
    compilerOptions: {
        immutable: true,  // Performance optimization
    },
};
```

---

## Framework Comparison

| Framework | Bundle Size | TTFB | Hydration | Best For |
|-----------|-------------|------|-----------|----------|
| **Next.js** | Medium | Fast (SSG/ISR) | Full | Full-stack apps, SEO |
| **React** | Large | Slow (CSR) | Full | SPAs, dashboards |
| **Vue** | Medium | Medium | Full | Progressive enhancement |
| **Vite** | Small | Fast | Full | Modern build tool |
| **Astro** | Tiny | Very Fast | Partial | Content sites, blogs |
| **SvelteKit** | Small | Fast | Full | High-performance apps |

---

## Framework-Agnostic Tips

### Bundle Size Budgets

```json
{
    "budgets": [
        {
            "type": "bundle",
            "name": "main",
            "baseline": "150kb",
            "warning": "200kb",
            "error": "250kb"
        }
    ]
}
```

---

### Performance Monitoring

**All frameworks can use web-vitals:**

```javascript
import { onCLS, onFCP, onINP, onLCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
    // Send to your analytics provider
    console.log(metric.name, metric.value);
}

onCLS(sendToAnalytics);
onFCP(sendToAnalytics);
onINP(sendToAnalytics);
onLCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

---

## Summary Checklist

### Next.js
- [ ] Use Image component with `priority` for LCP images
- [ ] Optimize fonts with `next/font`
- [ ] Choose appropriate rendering strategy (SSG/ISR/SSR)
- [ ] Enable bundle analyzer
- [ ] Use Edge runtime for API routes

### React
- [ ] Memoize expensive components
- [ ] Code split by route
- [ ] Use virtual scrolling for long lists
- [ ] Profile with React DevTools
- [ ] Implement lazy loading

### Vue
- [ ] Use computed properties instead of methods
- [ ] Lazy load heavy components
- [ ] Use `v-once` for static content
- [ ] Implement virtual scrolling
- [ ] Code split by route

### Vite
- [ ] Configure chunk splitting
- [ ] Enable minification
- [ ] Disable source maps in production
- [ ] Use legacy plugin if needed
- [ ] Preview production builds locally

### Astro
- [ ] Use partial hydration (client directives)
- [ ] Prefer zero-JS pages
- [ ] Prerender static routes
- [ ] Inline critical CSS
- [ ] Use component islands pattern

### SvelteKit
- [ ] Prerender static routes
- [ ] Use server-side data loading
- [ ] Optimize hydration strategy
- [ ] Enable compiler optimizations
- [ ] Configure adapter for deployment

---

**Next:** See [core-web-vitals.md](core-web-vitals.md) for metric-specific optimization strategies.
