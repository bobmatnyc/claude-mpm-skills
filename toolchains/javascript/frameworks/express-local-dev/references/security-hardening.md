# Security Hardening Checklist

> Comprehensive security guide for production Express applications

## Security Headers

### Complete Helmet Configuration

```javascript
// config/security.js
const helmet = require('helmet');

const securityHeaders = helmet({
  // Content Security Policy
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "trusted-cdn.com"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "api.example.com"],
      fontSrc: ["'self'", "fonts.gstatic.com"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
      sandbox: ['allow-forms', 'allow-scripts'],
      baseUri: ["'self'"],
      formAction: ["'self'"],
      frameAncestors: ["'none'"],
      upgradeInsecureRequests: []
    }
  },

  // HTTP Strict Transport Security
  hsts: {
    maxAge: 31536000, // 1 year in seconds
    includeSubDomains: true,
    preload: true
  },

  // Prevent clickjacking
  frameguard: {
    action: 'deny'
  },

  // Prevent MIME type sniffing
  noSniff: true,

  // Enable XSS filter
  xssFilter: true,

  // Hide X-Powered-By header
  hidePoweredBy: true,

  // Referrer Policy
  referrerPolicy: {
    policy: 'strict-origin-when-cross-origin'
  },

  // Expect-CT header
  expectCt: {
    maxAge: 86400,
    enforce: true
  }
});

module.exports = securityHeaders;
```

### Custom Security Headers

```javascript
// middleware/securityHeaders.js
module.exports = (req, res, next) => {
  // Permissions Policy (formerly Feature Policy)
  res.setHeader('Permissions-Policy',
    'geolocation=(), microphone=(), camera=()'
  );

  // Prevent information disclosure
  res.removeHeader('X-Powered-By');
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // Cache control for sensitive data
  if (req.path.startsWith('/api/')) {
    res.setHeader('Cache-Control', 'no-store, max-age=0');
  }

  next();
};
```

## Input Validation and Sanitization

### Comprehensive Validation Rules

```javascript
// validators/user.js
const { body, param, query } = require('express-validator');

// Email validation with security checks
exports.emailRules = body('email')
  .trim()
  .isEmail()
  .normalizeEmail()
  .custom(async (email) => {
    // Check for disposable email domains
    const disposableDomains = ['tempmail.com', 'throwaway.email'];
    const domain = email.split('@')[1];
    if (disposableDomains.includes(domain)) {
      throw new Error('Disposable email addresses not allowed');
    }
    return true;
  });

// Strong password requirements
exports.passwordRules = body('password')
  .isLength({ min: 12, max: 128 })
  .withMessage('Password must be 12-128 characters')
  .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
  .withMessage('Password must include: uppercase, lowercase, number, special char')
  .custom((value, { req }) => {
    // Prevent common passwords
    const commonPasswords = ['Password123!', 'Admin123!'];
    if (commonPasswords.includes(value)) {
      throw new Error('Password too common');
    }
    return true;
  });

// SQL injection prevention in search
exports.searchRules = query('q')
  .trim()
  .isLength({ max: 200 })
  .matches(/^[a-zA-Z0-9\s-]*$/)
  .withMessage('Invalid search characters');

// File upload validation
exports.fileUploadRules = body('file')
  .custom((value, { req }) => {
    if (!req.file) {
      throw new Error('File required');
    }

    // Check file type
    const allowedMimes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowedMimes.includes(req.file.mimetype)) {
      throw new Error('Invalid file type');
    }

    // Check file size (5MB max)
    if (req.file.size > 5 * 1024 * 1024) {
      throw new Error('File too large');
    }

    return true;
  });
```

### XSS Prevention

```javascript
// middleware/xssProtection.js
const xss = require('xss-clean');
const validator = require('validator');

// Apply XSS cleaning middleware
app.use(xss());

// Custom HTML escaping
const escapeHtml = (unsafe) => {
  return validator.escape(unsafe);
};

// Sanitize user-generated content
const sanitizeUserContent = (content) => {
  const xssOptions = {
    whiteList: {
      // Only allow specific safe tags
      p: [],
      br: [],
      strong: [],
      em: [],
      a: ['href', 'title']
    },
    stripIgnoreTag: true,
    stripIgnoreTagBody: ['script', 'style']
  };

  return xss(content, xssOptions);
};

module.exports = { escapeHtml, sanitizeUserContent };
```

## Authentication Security

### Secure Password Hashing

```javascript
// utils/password.js
const bcrypt = require('bcrypt');
const crypto = require('crypto');

// Use high cost factor for bcrypt
const SALT_ROUNDS = 12;

exports.hashPassword = async (password) => {
  return bcrypt.hash(password, SALT_ROUNDS);
};

exports.verifyPassword = async (password, hash) => {
  return bcrypt.compare(password, hash);
};

// Constant-time comparison to prevent timing attacks
exports.secureCompare = (a, b) => {
  return crypto.timingSafeEqual(
    Buffer.from(a),
    Buffer.from(b)
  );
};
```

### JWT Security Best Practices

```javascript
// utils/jwt.js
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

// Generate strong secret (run once, store in env)
const generateSecret = () => {
  return crypto.randomBytes(64).toString('hex');
};

// Secure JWT configuration
exports.signToken = (payload) => {
  return jwt.sign(payload, process.env.JWT_SECRET, {
    expiresIn: '15m', // Short-lived access tokens
    algorithm: 'HS256',
    issuer: 'your-app',
    audience: 'your-api'
  });
};

exports.signRefreshToken = (payload) => {
  return jwt.sign(payload, process.env.JWT_REFRESH_SECRET, {
    expiresIn: '7d',
    algorithm: 'HS256',
    issuer: 'your-app',
    audience: 'your-api'
  });
};

exports.verifyToken = (token) => {
  try {
    return jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],
      issuer: 'your-app',
      audience: 'your-api'
    });
  } catch (error) {
    throw new Error('Invalid token');
  }
};

// Token rotation for refresh tokens
exports.rotateRefreshToken = async (oldToken) => {
  const decoded = jwt.verify(oldToken, process.env.JWT_REFRESH_SECRET);

  // Blacklist old token
  await redis.setEx(`blacklist:${oldToken}`, 7 * 24 * 60 * 60, '1');

  // Issue new refresh token
  return exports.signRefreshToken({ userId: decoded.userId });
};
```

### Rate Limiting Strategies

```javascript
// middleware/advancedRateLimit.js
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const redis = require('redis');

const redisClient = redis.createClient();

// Tier-based rate limiting
exports.apiLimiter = rateLimit({
  store: new RedisStore({ client: redisClient }),
  windowMs: 15 * 60 * 1000,
  max: async (req) => {
    // Different limits based on user tier
    if (req.user?.tier === 'premium') return 1000;
    if (req.user?.tier === 'standard') return 500;
    return 100; // Free tier
  },
  keyGenerator: (req) => {
    return req.user?.id || req.ip;
  },
  skip: (req) => {
    // Skip for internal IPs
    const internalIPs = ['127.0.0.1', '::1'];
    return internalIPs.includes(req.ip);
  }
});

// Exponential backoff for failed auth
exports.authLimiter = rateLimit({
  store: new RedisStore({ client: redisClient }),
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true,
  onLimitReached: async (req) => {
    // Log potential brute force attack
    logger.warn('Rate limit reached', {
      ip: req.ip,
      endpoint: req.path
    });

    // Temporarily ban IP after multiple limit hits
    const key = `ban:${req.ip}`;
    const banCount = await redis.incr(key);

    if (banCount > 3) {
      await redis.setEx(key, 60 * 60, banCount); // 1 hour ban
    }
  }
});

// Distributed DoS protection
exports.ddosProtection = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 60,
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too many requests',
      retryAfter: Math.ceil(req.rateLimit.resetTime / 1000)
    });
  }
});
```

## Session Security

### Secure Session Configuration

```javascript
// config/session.js
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const redis = require('redis');

const redisClient = redis.createClient({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
  password: process.env.REDIS_PASSWORD
});

const sessionConfig = session({
  store: new RedisStore({
    client: redisClient,
    prefix: 'sess:',
    ttl: 60 * 60 * 24 // 24 hours
  }),

  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  rolling: true, // Reset expiration on activity

  cookie: {
    secure: process.env.NODE_ENV === 'production', // HTTPS only
    httpOnly: true, // No client-side JS access
    maxAge: 1000 * 60 * 60 * 24, // 24 hours
    sameSite: 'strict', // CSRF protection
    domain: process.env.COOKIE_DOMAIN
  },

  name: 'sessionId' // Don't use default 'connect.sid'
});

module.exports = sessionConfig;
```

## CSRF Protection

```javascript
// middleware/csrf.js
const csrf = require('csurf');
const crypto = require('crypto');

// Standard CSRF protection
exports.csrfProtection = csrf({
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict'
  }
});

// Double submit cookie pattern
exports.doubleSubmitCsrf = (req, res, next) => {
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
    // Generate token for safe methods
    const token = crypto.randomBytes(32).toString('hex');
    res.cookie('csrf-token', token, {
      httpOnly: false, // Client needs to read this
      secure: true,
      sameSite: 'strict'
    });
    return next();
  }

  // Verify token for unsafe methods
  const cookieToken = req.cookies['csrf-token'];
  const headerToken = req.headers['x-csrf-token'];

  if (!cookieToken || cookieToken !== headerToken) {
    return res.status(403).json({ error: 'CSRF token invalid' });
  }

  next();
};
```

## SQL and NoSQL Injection Prevention

```javascript
// Always use parameterized queries or ORMs

// ❌ WRONG - SQL Injection vulnerable
const query = `SELECT * FROM users WHERE email = '${req.body.email}'`;

// ✅ CORRECT - Parameterized query
const query = 'SELECT * FROM users WHERE email = ?';
db.query(query, [req.body.email]);

// ✅ CORRECT - ORM (Sequelize)
const user = await User.findOne({
  where: { email: req.body.email }
});

// ❌ WRONG - NoSQL Injection vulnerable
const user = await User.findOne({ email: req.body.email });
// If req.body.email = { $gt: "" }, returns all users!

// ✅ CORRECT - Validate and sanitize
const { body } = require('express-validator');

const emailValidator = body('email')
  .isEmail()
  .normalizeEmail()
  .trim();

// ✅ CORRECT - Explicitly reject objects
const sanitizeInput = (input) => {
  if (typeof input === 'object' && input !== null) {
    throw new Error('Invalid input type');
  }
  return input;
};
```

## File Upload Security

```javascript
// middleware/secureUpload.js
const multer = require('multer');
const path = require('path');
const crypto = require('crypto');
const sharp = require('sharp');

// Secure file storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    // Use random filename to prevent path traversal
    const randomName = crypto.randomBytes(16).toString('hex');
    const ext = path.extname(file.originalname);
    cb(null, `${randomName}${ext}`);
  }
});

// File filter with security checks
const fileFilter = (req, file, cb) => {
  // Whitelist allowed MIME types
  const allowedMimes = [
    'image/jpeg',
    'image/png',
    'image/webp',
    'application/pdf'
  ];

  if (!allowedMimes.includes(file.mimetype)) {
    return cb(new Error('Invalid file type'), false);
  }

  // Check file extension
  const ext = path.extname(file.originalname).toLowerCase();
  const allowedExts = ['.jpg', '.jpeg', '.png', '.webp', '.pdf'];

  if (!allowedExts.includes(ext)) {
    return cb(new Error('Invalid file extension'), false);
  }

  cb(null, true);
};

const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB max
    files: 1 // Single file upload
  }
});

// Image validation and sanitization
exports.processImage = async (filePath) => {
  try {
    // Re-encode image to strip metadata and validate
    await sharp(filePath)
      .jpeg({ quality: 85 })
      .toFile(filePath + '.processed');

    // Replace original with processed
    fs.renameSync(filePath + '.processed', filePath);
  } catch (error) {
    // Invalid image, delete it
    fs.unlinkSync(filePath);
    throw new Error('Invalid image file');
  }
};

module.exports = upload;
```

## Secrets Management

```javascript
// config/secrets.js
const AWS = require('aws-sdk');

// Load secrets from AWS Secrets Manager
exports.loadSecrets = async () => {
  const client = new AWS.SecretsManager({
    region: process.env.AWS_REGION
  });

  try {
    const data = await client.getSecretValue({
      SecretId: process.env.SECRET_NAME
    }).promise();

    const secrets = JSON.parse(data.SecretString);

    // Set environment variables
    process.env.DATABASE_PASSWORD = secrets.DATABASE_PASSWORD;
    process.env.JWT_SECRET = secrets.JWT_SECRET;
    process.env.API_KEY = secrets.API_KEY;
  } catch (error) {
    console.error('Failed to load secrets:', error);
    process.exit(1);
  }
};

// Validate secrets exist and are strong
exports.validateSecrets = () => {
  const required = [
    'DATABASE_PASSWORD',
    'JWT_SECRET',
    'SESSION_SECRET'
  ];

  required.forEach(secret => {
    if (!process.env[secret]) {
      throw new Error(`Missing required secret: ${secret}`);
    }

    if (process.env[secret].length < 32) {
      throw new Error(`Weak secret: ${secret} (min 32 chars)`);
    }
  });
};
```

## Security Checklist

### Pre-Production Checklist

- [ ] All secrets in environment variables (not code)
- [ ] Secrets are strong (32+ characters)
- [ ] HTTPS enforced (HSTS enabled)
- [ ] Security headers configured (Helmet)
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitization + CSP)
- [ ] CSRF protection enabled
- [ ] Authentication uses bcrypt (12+ rounds)
- [ ] JWT tokens short-lived (15min access, 7day refresh)
- [ ] Session cookies secure + httpOnly + sameSite
- [ ] File uploads validated and sanitized
- [ ] Error messages don't leak info
- [ ] Logging excludes sensitive data
- [ ] Dependencies scanned (`npm audit`)
- [ ] Security headers tested (securityheaders.com)
- [ ] Penetration testing completed

## Related Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
