# Testing Strategies

> Comprehensive testing guide for Express applications

## Test Structure

### Recommended Test Organization

```
tests/
├── setup.js                 # Global test setup
├── fixtures/
│   ├── users.json          # Test data
│   └── posts.json
├── factories/
│   ├── userFactory.js      # Test data generators
│   └── postFactory.js
├── helpers/
│   ├── authHelper.js       # Auth test utilities
│   └── dbHelper.js         # Database test utilities
├── unit/
│   ├── models/
│   ├── services/
│   └── utils/
├── integration/
│   ├── routes/
│   │   ├── users.test.js
│   │   ├── auth.test.js
│   │   └── posts.test.js
│   └── middleware/
└── e2e/
    └── userFlows.test.js
```

## Unit Testing

### Testing Services

```javascript
// tests/unit/services/userService.test.js
const userService = require('../../../src/services/userService');
const User = require('../../../src/models/User');

jest.mock('../../../src/models/User');

describe('UserService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('createUser', () => {
    it('should create user with hashed password', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'Password123'
      };

      const mockUser = {
        id: 1,
        email: userData.email,
        password: 'hashed_password'
      };

      User.create.mockResolvedValue(mockUser);

      const result = await userService.createUser(userData);

      expect(User.create).toHaveBeenCalledWith(
        expect.objectContaining({
          email: userData.email,
          password: expect.not.stringMatching(userData.password)
        })
      );
      expect(result).toEqual(mockUser);
    });

    it('should throw error for duplicate email', async () => {
      const userData = {
        email: 'duplicate@example.com',
        password: 'Password123'
      };

      User.create.mockRejectedValue(
        new Error('Duplicate email')
      );

      await expect(
        userService.createUser(userData)
      ).rejects.toThrow('Duplicate email');
    });
  });

  describe('validatePassword', () => {
    it('should return true for valid password', async () => {
      const user = {
        password: '$2b$12$hashed_password'
      };
      const plainPassword = 'Password123';

      const isValid = await userService.validatePassword(
        plainPassword,
        user.password
      );

      expect(isValid).toBe(true);
    });

    it('should return false for invalid password', async () => {
      const user = {
        password: '$2b$12$hashed_password'
      };
      const plainPassword = 'WrongPassword';

      const isValid = await userService.validatePassword(
        plainPassword,
        user.password
      );

      expect(isValid).toBe(false);
    });
  });
});
```

### Testing Utilities

```javascript
// tests/unit/utils/validation.test.js
const { validateEmail, validatePassword } = require('../../../src/utils/validation');

describe('Validation Utils', () => {
  describe('validateEmail', () => {
    it('should accept valid email', () => {
      expect(validateEmail('user@example.com')).toBe(true);
    });

    it('should reject invalid email', () => {
      expect(validateEmail('invalid-email')).toBe(false);
      expect(validateEmail('user@')).toBe(false);
      expect(validateEmail('@example.com')).toBe(false);
    });
  });

  describe('validatePassword', () => {
    it('should accept strong password', () => {
      expect(validatePassword('Password123!')).toBe(true);
    });

    it('should reject weak password', () => {
      expect(validatePassword('weak')).toBe(false);
      expect(validatePassword('password')).toBe(false);
      expect(validatePassword('12345678')).toBe(false);
    });
  });
});
```

## Integration Testing

### Testing Routes with Supertest

```javascript
// tests/integration/routes/users.test.js
const request = require('supertest');
const app = require('../../../src/app');
const { createUser } = require('../../factories/userFactory');
const { getAuthToken } = require('../../helpers/authHelper');

describe('User Routes', () => {
  describe('GET /api/users', () => {
    it('should return paginated users', async () => {
      await createUser({ email: 'user1@example.com' });
      await createUser({ email: 'user2@example.com' });
      await createUser({ email: 'user3@example.com' });

      const response = await request(app)
        .get('/api/users')
        .query({ page: 1, limit: 2 })
        .expect(200);

      expect(response.body).toHaveProperty('users');
      expect(response.body.users).toHaveLength(2);
      expect(response.body).toHaveProperty('total', 3);
      expect(response.body).toHaveProperty('page', 1);
      expect(response.body).toHaveProperty('pages', 2);
    });

    it('should filter users by query', async () => {
      await createUser({ name: 'John Doe' });
      await createUser({ name: 'Jane Smith' });

      const response = await request(app)
        .get('/api/users')
        .query({ search: 'John' })
        .expect(200);

      expect(response.body.users).toHaveLength(1);
      expect(response.body.users[0].name).toBe('John Doe');
    });
  });

  describe('POST /api/users', () => {
    it('should create user with valid data', async () => {
      const userData = {
        email: 'newuser@example.com',
        name: 'New User',
        password: 'Password123!'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body.user).toMatchObject({
        email: userData.email,
        name: userData.name
      });
      expect(response.body.user).not.toHaveProperty('password');
      expect(response.body).toHaveProperty('token');
    });

    it('should return 400 for invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'invalid-email',
          name: 'User',
          password: 'Password123!'
        })
        .expect(400);

      expect(response.body).toHaveProperty('errors');
      expect(response.body.errors).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            field: 'email',
            message: expect.stringContaining('valid email')
          })
        ])
      );
    });

    it('should return 409 for duplicate email', async () => {
      await createUser({ email: 'existing@example.com' });

      await request(app)
        .post('/api/users')
        .send({
          email: 'existing@example.com',
          name: 'User',
          password: 'Password123!'
        })
        .expect(409);
    });
  });

  describe('PUT /api/users/:id', () => {
    it('should update user with valid token', async () => {
      const user = await createUser();
      const token = await getAuthToken(user);

      const response = await request(app)
        .put(`/api/users/${user.id}`)
        .set('Authorization', `Bearer ${token}`)
        .send({ name: 'Updated Name' })
        .expect(200);

      expect(response.body.user.name).toBe('Updated Name');
    });

    it('should return 401 without token', async () => {
      const user = await createUser();

      await request(app)
        .put(`/api/users/${user.id}`)
        .send({ name: 'Updated Name' })
        .expect(401);
    });

    it('should return 403 when updating other user', async () => {
      const user1 = await createUser({ email: 'user1@example.com' });
      const user2 = await createUser({ email: 'user2@example.com' });
      const token = await getAuthToken(user1);

      await request(app)
        .put(`/api/users/${user2.id}`)
        .set('Authorization', `Bearer ${token}`)
        .send({ name: 'Hacked' })
        .expect(403);
    });
  });
});
```

### Testing Middleware

```javascript
// tests/integration/middleware/auth.test.js
const request = require('supertest');
const app = require('../../../src/app');
const { createUser } = require('../../factories/userFactory');
const { signToken } = require('../../../src/utils/jwt');

describe('Authentication Middleware', () => {
  describe('authenticate', () => {
    it('should allow request with valid token', async () => {
      const user = await createUser();
      const token = signToken({ id: user.id });

      const response = await request(app)
        .get('/api/protected')
        .set('Authorization', `Bearer ${token}`)
        .expect(200);

      expect(response.body.user.id).toBe(user.id);
    });

    it('should reject request without token', async () => {
      await request(app)
        .get('/api/protected')
        .expect(401);
    });

    it('should reject request with invalid token', async () => {
      await request(app)
        .get('/api/protected')
        .set('Authorization', 'Bearer invalid-token')
        .expect(401);
    });

    it('should reject request with expired token', async () => {
      const expiredToken = signToken(
        { id: 1 },
        { expiresIn: '-1h' }
      );

      await request(app)
        .get('/api/protected')
        .set('Authorization', `Bearer ${expiredToken}`)
        .expect(401);
    });
  });

  describe('authorize', () => {
    it('should allow admin access', async () => {
      const admin = await createUser({ role: 'admin' });
      const token = signToken({ id: admin.id, role: 'admin' });

      await request(app)
        .delete('/api/users/123')
        .set('Authorization', `Bearer ${token}`)
        .expect(204);
    });

    it('should deny non-admin access', async () => {
      const user = await createUser({ role: 'user' });
      const token = signToken({ id: user.id, role: 'user' });

      await request(app)
        .delete('/api/users/123')
        .set('Authorization', `Bearer ${token}`)
        .expect(403);
    });
  });
});
```

## Test Helpers and Utilities

### Authentication Helper

```javascript
// tests/helpers/authHelper.js
const { signToken } = require('../../src/utils/jwt');

exports.getAuthToken = (user) => {
  return signToken({
    id: user.id,
    email: user.email,
    role: user.role || 'user'
  });
};

exports.getExpiredToken = (user) => {
  return signToken(
    { id: user.id },
    { expiresIn: '-1h' }
  );
};

exports.authenticatedRequest = (request, user) => {
  const token = exports.getAuthToken(user);
  return request.set('Authorization', `Bearer ${token}`);
};
```

### Database Helper

```javascript
// tests/helpers/dbHelper.js
const mongoose = require('mongoose');

exports.cleanDatabase = async () => {
  const collections = mongoose.connection.collections;

  for (const key in collections) {
    await collections[key].deleteMany();
  }
};

exports.closeDatabase = async () => {
  await mongoose.connection.dropDatabase();
  await mongoose.connection.close();
};

exports.clearCollection = async (collectionName) => {
  const collection = mongoose.connection.collections[collectionName];
  if (collection) {
    await collection.deleteMany();
  }
};
```

### Test Factories

```javascript
// tests/factories/userFactory.js
const User = require('../../src/models/User');
const bcrypt = require('bcrypt');

let userCounter = 0;

exports.createUser = async (overrides = {}) => {
  userCounter++;

  const defaultData = {
    email: `user${userCounter}@example.com`,
    name: `User ${userCounter}`,
    password: await bcrypt.hash('Password123!', 10),
    role: 'user'
  };

  const userData = { ...defaultData, ...overrides };

  return User.create(userData);
};

exports.createUsers = async (count, overrides = {}) => {
  const users = [];
  for (let i = 0; i < count; i++) {
    users.push(await exports.createUser(overrides));
  }
  return users;
};

exports.createAdmin = async (overrides = {}) => {
  return exports.createUser({ role: 'admin', ...overrides });
};
```

## Mocking Strategies

### Mocking External APIs

```javascript
// tests/integration/externalApi.test.js
const nock = require('nock');
const request = require('supertest');
const app = require('../../src/app');

describe('External API Integration', () => {
  afterEach(() => {
    nock.cleanAll();
  });

  it('should fetch data from external API', async () => {
    // Mock external API
    nock('https://api.example.com')
      .get('/data')
      .reply(200, {
        data: 'external data'
      });

    const response = await request(app)
      .get('/api/external-data')
      .expect(200);

    expect(response.body.data).toBe('external data');
  });

  it('should handle external API failure', async () => {
    nock('https://api.example.com')
      .get('/data')
      .reply(500);

    await request(app)
      .get('/api/external-data')
      .expect(503);
  });
});
```

### Mocking Database

```javascript
// Use mongodb-memory-server for integration tests
const { MongoMemoryServer } = require('mongodb-memory-server');
const mongoose = require('mongoose');

let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  await mongoose.connect(mongoServer.getUri());
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});

// Or mock Mongoose models for unit tests
jest.mock('../../src/models/User');
const User = require('../../src/models/User');

User.findById.mockResolvedValue({
  id: '123',
  email: 'test@example.com'
});
```

## Test Coverage

### Jest Configuration

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/tests/**',
    '!src/migrations/**'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  testMatch: [
    '**/tests/**/*.test.js'
  ],
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],
  clearMocks: true,
  resetMocks: true,
  restoreMocks: true
};
```

### Running Coverage

```bash
# Run tests with coverage
npm run test:coverage

# View coverage report
open coverage/lcov-report/index.html

# CI/CD coverage threshold enforcement
npm test -- --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80,"statements":80}}'
```

## E2E Testing

### User Flow Testing

```javascript
// tests/e2e/userFlows.test.js
const request = require('supertest');
const app = require('../../src/app');

describe('User Registration and Login Flow', () => {
  it('should complete full user lifecycle', async () => {
    const userData = {
      email: 'flow@example.com',
      name: 'Flow User',
      password: 'Password123!'
    };

    // 1. Register
    const registerResponse = await request(app)
      .post('/api/auth/register')
      .send(userData)
      .expect(201);

    expect(registerResponse.body).toHaveProperty('token');
    const userId = registerResponse.body.user.id;

    // 2. Login
    const loginResponse = await request(app)
      .post('/api/auth/login')
      .send({
        email: userData.email,
        password: userData.password
      })
      .expect(200);

    const token = loginResponse.body.token;

    // 3. Get profile
    const profileResponse = await request(app)
      .get('/api/auth/me')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);

    expect(profileResponse.body.user.email).toBe(userData.email);

    // 4. Update profile
    await request(app)
      .put(`/api/users/${userId}`)
      .set('Authorization', `Bearer ${token}`)
      .send({ name: 'Updated Name' })
      .expect(200);

    // 5. Logout
    await request(app)
      .post('/api/auth/logout')
      .set('Authorization', `Bearer ${token}`)
      .expect(204);

    // 6. Verify token invalidated
    await request(app)
      .get('/api/auth/me')
      .set('Authorization', `Bearer ${token}`)
      .expect(401);
  });
});
```

## Performance Testing

### Load Testing with Artillery

```yaml
# artillery.yml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10
      name: 'Warm up'
    - duration: 120
      arrivalRate: 50
      name: 'Sustained load'
    - duration: 60
      arrivalRate: 100
      name: 'Peak load'

scenarios:
  - name: 'API Load Test'
    flow:
      - get:
          url: '/api/users'
      - post:
          url: '/api/users'
          json:
            email: '{{ $randomString() }}@example.com'
            name: 'Test User'
            password: 'Password123!'
```

```bash
# Run load test
artillery run artillery.yml

# Generate HTML report
artillery run --output report.json artillery.yml
artillery report report.json
```

## Best Practices

1. **Test Structure**: Unit → Integration → E2E
2. **Test Independence**: Each test should be isolated
3. **Clear Naming**: Describe what, when, expected outcome
4. **Setup/Teardown**: Use beforeEach/afterEach for cleanup
5. **Factory Pattern**: Use factories for test data
6. **Mock External Deps**: Don't hit real APIs in tests
7. **Coverage Targets**: Aim for 80%+ coverage
8. **Fast Tests**: Keep test suite under 30 seconds
9. **Parallel Execution**: Run tests in parallel when possible
10. **CI Integration**: Run tests on every commit

## Related Resources

- [Supertest Documentation](https://github.com/visionmedia/supertest)
- [Jest Documentation](https://jestjs.io/)
- [mongodb-memory-server](https://github.com/nodkz/mongodb-memory-server)
