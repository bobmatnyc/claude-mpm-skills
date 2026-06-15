# Turbopack in Next.js 16

Configuration, loader migration, and performance optimization for the new default bundler.

## Overview

Turbopack is now the **default bundler** in Next.js 16, replacing Webpack for both development and production builds.

### Performance Gains

| Metric | Webpack | Turbopack | Improvement |
|--------|---------|-----------|-------------|
| Cold start | ~15s | ~3s | **5x faster** |
| Fast Refresh | ~500ms | ~50ms | **10x faster** |
| Production build | ~60s | ~20s | **3x faster** |

## Configuration

### Basic Setup

```typescript
// next.config.ts
const nextConfig = {
  // Turbopack options moved from experimental to top-level
  turbopack: {
    // Alias modules
    resolveAlias: {
      'old-package': 'new-package',
    },
    // Resolve extensions
    resolveExtensions: ['.tsx', '.ts', '.jsx', '.js'],
  },
};

export default nextConfig;
```

### Experimental Features

```typescript
const nextConfig = {
  turbopack: {
    resolveAlias: {},
  },
  experimental: {
    // Persist build artifacts between restarts
    turbopackFileSystemCacheForDev: true,
    
    // Enable persistent caching in production
    turbopackPersistentCache: true,
  },
};
```

## Loader Migration

### SVG Handling

Webpack:
```javascript
// next.config.js (Webpack)
module.exports = {
  webpack: (config) => {
    config.module.rules.push({
      test: /\.svg$/,
      use: ['@svgr/webpack'],
    });
    return config;
  },
};
```

Turbopack alternatives:

**Option 1: Inline SVG Component**
```typescript
// components/icons.tsx
export function HomeIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" {...props}>
      <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
    </svg>
  );
}
```

**Option 2: @svgr/rollup with manual setup**
```bash
npm install @svgr/rollup
```

**Option 3: next/image for static SVGs**
```typescript
import Image from 'next/image';
import logo from '@/assets/logo.svg';

export function Logo() {
  return <Image src={logo} alt="Logo" />;
}
```

### CSS Modules

Works identically - no migration needed:

```typescript
// components/button.tsx
import styles from './button.module.css';

export function Button({ children }) {
  return <button className={styles.button}>{children}</button>;
}
```

### Sass/SCSS

```bash
npm install sass
```

```typescript
// next.config.ts
const nextConfig = {
  sassOptions: {
    includePaths: ['./styles'],
    prependData: `@import "variables.scss";`,
  },
};
```

### PostCSS

Works identically - `postcss.config.js` is respected:

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

### MDX

```bash
npm install @next/mdx @mdx-js/loader @mdx-js/react
```

```typescript
// next.config.ts
import createMDX from '@next/mdx';

const withMDX = createMDX({
  options: {
    remarkPlugins: [],
    rehypePlugins: [],
  },
});

export default withMDX({
  pageExtensions: ['js', 'jsx', 'ts', 'tsx', 'md', 'mdx'],
});
```

## Webpack Fallback

### When to Use Webpack

- Custom loaders without Turbopack equivalents
- Complex webpack plugins
- Build-time code generation
- Legacy configurations

### Opt-out Commands

```bash
# Development
next dev --webpack

# Production build
next build --webpack
```

### Conditional Configuration

```typescript
// next.config.ts
const nextConfig = {
  webpack: (config, { isServer }) => {
    // Only applied when using --webpack flag
    config.module.rules.push({
      test: /\.svg$/,
      use: ['@svgr/webpack'],
    });
    return config;
  },
  
  turbopack: {
    // Turbopack-specific config
  },
};
```

## Performance Optimization

### Development

```typescript
const nextConfig = {
  experimental: {
    // Cache compilation results
    turbopackFileSystemCacheForDev: true,
  },
};
```

### Production

```typescript
const nextConfig = {
  experimental: {
    // Incremental builds
    turbopackPersistentCache: true,
  },
  
  // Output optimization
  output: 'standalone', // Minimal production output
  
  // Compression
  compress: true,
};
```

### Monitoring Build Performance

```bash
# Analyze build
ANALYZE=true next build

# Verbose timing
next build --profile
```

## Troubleshooting

### Issue: Build Fails with Custom Loader

**Symptom:**
```
Error: Could not find loader for .xyz files
```

**Solutions:**

1. Check if Turbopack supports the file type natively
2. Find Turbopack-compatible alternative
3. Use `next build --webpack` temporarily
4. Convert to native solution

### Issue: Module Not Found

**Symptom:**
```
Error: Cannot find module 'xyz'
```

**Fix:** Add to resolveAlias:
```typescript
turbopack: {
  resolveAlias: {
    'xyz': './node_modules/xyz/dist/index.js',
  },
},
```

### Issue: CSS Not Loading

**Symptom:** Styles missing in development

**Fix:** Ensure CSS imports are at component level:
```typescript
// ✅ Correct
import './styles.css';

// ❌ Avoid dynamic imports for CSS
const styles = await import('./styles.css');
```

### Issue: Slow Initial Build

**Fix:** Enable filesystem cache:
```typescript
experimental: {
  turbopackFileSystemCacheForDev: true,
},
```

### Issue: Memory Issues

**Fix:** Increase Node.js memory:
```bash
NODE_OPTIONS="--max-old-space-size=8192" next build
```

## Migration Checklist

### Pre-Migration

- [ ] List all custom webpack loaders
- [ ] Identify webpack plugins in use
- [ ] Document build-time transformations
- [ ] Note any postcss/sass customizations

### Migration Steps

1. [ ] Remove or migrate SVG loaders
2. [ ] Update MDX configuration
3. [ ] Test CSS/SCSS compilation
4. [ ] Verify PostCSS plugins work
5. [ ] Check all asset imports
6. [ ] Test development server
7. [ ] Run production build
8. [ ] Compare bundle sizes
9. [ ] Verify all features work

### Post-Migration

- [ ] Enable persistent caching
- [ ] Remove webpack-specific code (if not needed)
- [ ] Update CI/CD to remove --webpack flags
- [ ] Monitor build times
- [ ] Document any workarounds

## Native Loaders

Turbopack natively supports:

| File Type | Support |
|-----------|---------|
| JavaScript/TypeScript | ✅ Full |
| JSX/TSX | ✅ Full |
| CSS | ✅ Full |
| CSS Modules | ✅ Full |
| Sass/SCSS | ✅ Full |
| JSON | ✅ Full |
| Images (png, jpg, gif, webp, svg) | ✅ Full |
| Fonts (woff, woff2, ttf, otf) | ✅ Full |
| MDX | ✅ Via @next/mdx |

## Best Practices

1. **Start fresh** - Try without webpack config first
2. **Use native solutions** - Prefer Turbopack-native features
3. **Enable caching** - Significant build time reduction
4. **Monitor metrics** - Compare build times and bundle sizes
5. **Keep webpack fallback** - For edge cases only
6. **Test thoroughly** - Especially CSS and asset handling
7. **Update dependencies** - Ensure compatibility with Turbopack
