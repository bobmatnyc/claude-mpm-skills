# Core Testing Anti-Patterns

The three most critical testing anti-patterns that violate fundamental testing principles. These patterns test mock behavior instead of real behavior, pollute production code with test concerns, or mock without understanding dependencies.

## Anti-Pattern 1: Testing Mock Behavior

### The Violation

**[TypeScript/Jest]**
```typescript
// ❌ BAD: Testing that the mock exists
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**[Python/pytest]**
```python
# ❌ BAD: Testing mock behavior, not real code
from unittest.mock import Mock

def test_send_email():
    mock_mailer = Mock()

    send_welcome_email(mock_mailer, "user@example.com")

    # Asserting on MOCK behavior
    assert mock_mailer.send_email.called  # Testing the mock!
    assert mock_mailer.send_email.call_count == 1
    mock_mailer.send_email.assert_called_with("user@example.com", "Welcome!")
```

**Why this is wrong:**
- You're verifying the mock works, not that the component/function works
- Test passes when mock is present, fails when it's not
- Tells you nothing about real behavior
- False confidence - production may still be broken

**your human partner's correction:** "Are we testing the behavior of a mock?"

### The Fix

**[TypeScript/Jest]**
```typescript
// ✅ GOOD: Test real component or don't mock it
test('renders sidebar', () => {
  render(<Page />);  // Don't mock sidebar
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});

// OR if sidebar must be mocked for isolation:
// Don't assert on the mock - test Page's behavior with sidebar present
test('page layout includes sidebar area', () => {
  render(<Page />);  // Sidebar mocked for speed
  expect(screen.getByRole('main')).toHaveClass('with-sidebar-layout');
});
```

**[Python/pytest]**
```python
# ✅ GOOD: Test real behavior with test double
class FakeMailer:
    def __init__(self):
        self.sent_emails = []

    def send_email(self, to: str, subject: str, body: str):
        self.sent_emails.append({"to": to, "subject": subject, "body": body})

def test_send_welcome_email_sends_correct_content():
    mailer = FakeMailer()

    send_welcome_email(mailer, "user@example.com")

    # Assert on REAL behavior
    assert len(mailer.sent_emails) == 1
    email = mailer.sent_emails[0]
    assert email["to"] == "user@example.com"
    assert email["subject"] == "Welcome!"
    assert "Thank you for signing up" in email["body"]
```

### Detection Strategy

**Red flags (TypeScript/Jest):**
- Assertions check for `*-mock` in test IDs
- Test IDs contain "mock", "stub", "fake"
- Test fails when you remove the mock
- Can't explain what real behavior you're testing

**Red flags (Python/pytest):**
- `mock.assert_called()`
- `mock.assert_called_once()`
- `mock.assert_called_with(...)`
- `mock.call_count` assertions
- Testing `.called` or `.call_args` attributes

**Gate Function:**

```
BEFORE asserting on any mock element:
  Ask: "Am I testing real component behavior or just mock existence?"

  IF testing mock existence:
    STOP - Delete the assertion or unmock the component

  Ask: "What would this test verify in production?"

  IF answer is "nothing" or unclear:
    STOP - Rethink what you're testing

  Test real behavior instead
```

### When Mocking is Appropriate

**Good reasons to mock:**
- Isolate slow external dependencies (network, filesystem, DB)
- Control non-deterministic behavior (time, randomness)
- Simulate error conditions hard to trigger
- Speed up test execution

**Bad reasons to mock:**
- "Might be slow" (without measuring)
- "To be safe"
- "Everyone mocks this"
- To avoid understanding dependencies

**Rule:** Mock at the boundary of slow/external operations, not high-level application logic.

## Anti-Pattern 2: Test-Only Methods in Production

### The Violation

**[TypeScript/Jest]**
```typescript
// ❌ BAD: destroy() only used in tests
class Session {
  async destroy() {  // Looks like production API!
    await this._workspaceManager?.destroyWorkspace(this.id);
    await this._messageRouter?.cleanup();
    this._isDestroyed = true;
  }
}

// In tests
afterEach(() => session.destroy());
```

**[Python/pytest]**
```python
# ❌ BAD: Test-only method in production class
class UserService:
    def __init__(self, db: Database):
        self._db = db

    def create_user(self, email: str) -> User:
        return self._db.insert_user(email)

    # Test-only method!
    def _set_mock_db(self, mock_db):
        """For testing only"""
        self._db = mock_db
```

**Why this is wrong:**
- Production class polluted with test-only code
- Dangerous if accidentally called in production
- Violates YAGNI (You Aren't Gonna Need It)
- Violates separation of concerns
- Breaks encapsulation
- Creates maintenance burden (unused code in production)

### The Fix

**[TypeScript/Jest]**
```typescript
// ✅ GOOD: Test utilities handle test cleanup
// Session has no destroy() - it's stateless in production

// In test-utils/session-helpers.ts
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }

  const router = session.getMessageRouter();
  if (router) {
    await router.cleanup();
  }
}

// In tests
afterEach(() => cleanupSession(session));
```

**[Python/pytest]**
```python
# ✅ GOOD: Dependency injection, no test-only methods
class UserService:
    def __init__(self, db: Database):
        self._db = db  # Injected dependency

    def create_user(self, email: str) -> User:
        return self._db.insert_user(email)

# test_user_service.py
class FakeDatabase:
    def __init__(self):
        self.users = []

    def insert_user(self, email: str) -> User:
        user = User(id=len(self.users) + 1, email=email)
        self.users.append(user)
        return user

def test_create_user():
    fake_db = FakeDatabase()
    service = UserService(fake_db)

    user = service.create_user("test@example.com")

    assert user.email == "test@example.com"
    assert len(fake_db.users) == 1
```

### When Test Utilities Make Sense

**Good candidates for test utilities:**
- Setup/teardown operations
- Test data builders
- Assertion helpers
- Test-specific configurations
- Lifecycle management for tests

**Keep in production:**
- Methods used by application code
- Proper public API
- Business logic
- Real lifecycle methods (close, dispose)

**Key distinction:** If it's never called outside test files, it shouldn't be in production code.

### Detection Strategy

**Red flags (TypeScript/Jest):**
- Method only called in `*.test.*` or `*.spec.*` files
- Method name suggests testing (reset, clear, destroy, mock)
- Comments say "for testing only"
- Method has no production use case

**Red flags (Python/pytest):**
- Methods named `_set_*`, `_mock_*`, `_for_testing`
- Docstrings saying "For testing only"
- `if os.getenv('TESTING')` conditionals
- Properties that exist only for test access

**Gate Function:**

```
BEFORE adding any method to production class:
  Ask: "Is this only used by tests?"

  IF yes:
    STOP - Don't add it
    Put it in test utilities instead (test-utils/, test-helpers/)

  Ask: "Does this class own this resource's lifecycle?"

  IF no:
    STOP - Wrong class for this method
    Resource owner should manage lifecycle

  Ask: "Would production code ever call this?"

  IF no:
    STOP - Belongs in test utilities
```

### Refactoring Existing Test-Only Methods

**Step-by-step:**

1. **Identify** - Find methods only called in test files
2. **Extract** - Create test utility function with same logic
3. **Migrate** - Update tests to use utility
4. **Remove** - Delete test-only method from production
5. **Verify** - Production builds/bundles are cleaner

**Example refactoring:**

```typescript
// Before: Production class polluted
class Database {
  async reset() { /* only for tests */ }
}

// After: Clean separation
// database.ts - production
class Database {
  // No reset() method
}

// test-utils/database.ts - tests only
export async function resetTestDatabase(db: Database) {
  // Use public API to achieve reset
  await db.executeRaw('TRUNCATE ALL TABLES');
}
```

## Anti-Pattern 3: Mocking Without Understanding

### The Violation

**[TypeScript/Jest]**
```typescript
// ❌ BAD: Mock breaks test logic
test('detects duplicate server', async () => {
  // Mock prevents config write that test depends on!
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));

  await addServer(config);
  await addServer(config);  // Should throw - but won't!
  // Test expects duplicate detection, but mock broke it
});
```

**[Python/pytest]**
```python
# ❌ BAD: Mocking without understanding side effects
@patch('user_service.send_email')
def test_user_registration(mock_send_email):
    register_user("test@example.com", "password123")

    # Didn't realize send_email also logs to analytics
    # Didn't realize send_email creates async task
    # Test passes but misses important behavior
    mock_send_email.assert_called_once()
```

**Why this is wrong:**
- Mocked method had side effects test depended on
- Over-mocking to "be safe" breaks actual behavior
- Test passes for wrong reason or fails mysteriously
- You're testing mock behavior, not real behavior

### The Fix

**[TypeScript/Jest]**
```typescript
// ✅ GOOD: Mock at correct level
test('detects duplicate server', async () => {
  // Mock the slow part, preserve behavior test needs
  vi.mock('MCPServerManager'); // Just mock slow server startup
  // Config writing preserved - duplicate detection works

  await addServer(config);  // Config written
  await expect(addServer(config)).rejects.toThrow('already exists');
});
```

**[Python/pytest]**
```python
# ✅ GOOD: Understand THEN mock minimally
def test_user_registration():
    # First, run WITHOUT mocks to understand behavior
    # Discovered: send_email logs analytics + creates task

    # Now mock only the external I/O
    with patch('user_service.EmailClient.send') as mock_smtp:
        register_user("test@example.com", "password123")

        # Verify real behavior (not just mock called)
        user = User.query.filter_by(email="test@example.com").first()
        assert user is not None
        assert user.email_verified is False

        # Analytics logged (real behavior preserved)
        assert Analytics.query.filter_by(event='user_registered').count() == 1

        # Email attempted (mock at I/O boundary)
        assert mock_smtp.called
```

### Understanding Dependencies Before Mocking

**Questions to ask BEFORE mocking:**

1. **What does the real method do?**
   - Read the implementation
   - Check for side effects
   - Identify return values
   - Note error conditions

2. **What side effects exist?**
   - Filesystem writes
   - Database updates
   - Cache modifications
   - State changes
   - Event emissions

3. **What does THIS test need?**
   - Which side effects matter?
   - What behavior am I testing?
   - What can be safely isolated?

4. **Where should I mock?**
   - At the boundary of slow operations
   - Below the logic being tested
   - At external system interfaces

### Dependency Analysis Example

```typescript
// Analyzing: Should I mock discoverAndCacheTools()?

// 1. Read implementation
async function discoverAndCacheTools(serverConfig) {
  const tools = await fetchToolsFromServer(serverConfig);  // Slow
  await cacheTools(serverConfig.id, tools);                // Side effect!
  return tools;
}

// 2. Identify side effects
// - Network call (slow)
// - Cache write (side effect tests may depend on)

// 3. Determine test needs
test('server registration prevents duplicates', () => {
  // Needs: Config persistence to detect duplicate
  // Doesn't need: Actual tool discovery (slow)
});

// 4. Mock at correct level
// ✅ Mock network, preserve cache
vi.mock('server-connection', () => ({
  fetchToolsFromServer: vi.fn().mockResolvedValue([])
}));
// cacheTools() runs - test logic intact
```

### Gate Function

```
BEFORE mocking any method:
  STOP - Don't mock yet

  1. Ask: "What side effects does the real method have?"
     Action: Read implementation, list all side effects

  2. Ask: "Does this test depend on any of those side effects?"
     Action: Identify which side effects test logic needs

  3. Ask: "Do I fully understand what this test needs?"
     Action: Write down test's dependencies

  IF depends on side effects:
    Mock at lower level (the actual slow/external operation)
    OR use test doubles that preserve necessary behavior
    NOT the high-level method the test depends on

  IF unsure what test depends on:
    Run test with real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level

  Red flags:
    - "I'll mock this to be safe"
    - "This might be slow, better mock it"
    - Mocking without reading implementation
    - Mocking without understanding dependency chain
```

### Levels of Mocking

**Choose the right level:**

**[TypeScript/Jest]**
```typescript
// ❌ Too high - breaks test logic
vi.mock('UserService');  // Mocks everything, including state changes

// ❌ Too high - over-mocking
vi.mock('DatabaseAdapter');  // Could use in-memory DB instead

// ✅ Right level - isolates slow operation
vi.mock('HTTPClient');  // Mock network, preserve business logic

// ✅ Right level - controls non-determinism
vi.spyOn(Date, 'now').mockReturnValue(fixedTimestamp);
```

**[Python/pytest]**
```python
# ❌ Too high - breaks test logic
@patch('user_service')  # Mocks entire module, including state

# ❌ Too high - over-mocking
@patch('user_service.UserRepository')  # Could use in-memory/test database

# ✅ Right level - isolates slow operation
@patch('requests.post')  # Mock network, preserve business logic

# ✅ Right level - controls non-determinism
@patch('time.time', return_value=1234567890)
```

**Mocking hierarchy (top to bottom):**
1. **Application logic** - Never mock (this is what you're testing)
2. **Business layer** - Rarely mock (needed for test assertions)
3. **Adapter layer** - Sometimes mock (if slow, use test doubles)
4. **I/O boundaries** - Usually mock (network, filesystem, external APIs)
5. **Infrastructure** - Always mock (actual servers, databases in unit tests)

### Common Mocking Mistakes

**Mistake 1: Mocking what you're testing**
```typescript
// ❌ BAD
test('user registration validates email', () => {
  vi.mock('UserValidator');  // You're testing this!
  await registerUser(email);
});

// ✅ GOOD
test('user registration validates email', () => {
  vi.mock('EmailService');  // Mock email sending, test validation
  await expect(registerUser('invalid')).rejects.toThrow();
});
```

**Mistake 2: Mocking too broadly**
```typescript
// ❌ BAD - mocks entire module
vi.mock('./user-service');

// ✅ GOOD - mocks specific slow operation
vi.mock('./email-client', () => ({
  sendEmail: vi.fn()  // Just the network call
}));
```

**Mistake 3: Mocking based on assumptions**
```typescript
// ❌ BAD - assumption without measurement
// "Database queries are slow, better mock"
vi.mock('./database');

// ✅ GOOD - measure first
// Run test unmocked: 2ms (fast enough!)
// Don't mock unless proven slow
```

## Prevention Through TDD

**How TDD prevents these anti-patterns:**

1. **Write test first** → Forces you to think about what you're actually testing
2. **Watch it fail** → Confirms test tests real behavior, not mocks
3. **Minimal implementation** → No test-only methods creep in
4. **Real dependencies** → You see what the test actually needs before mocking

**If you're testing mock behavior, you violated TDD** - you added mocks without watching test fail against real code first.

**TDD workflow prevents:**
- Testing mock behavior (test fails for real reasons first)
- Test-only methods (minimal implementation doesn't add them)
- Uninformed mocking (you understand needs before mocking)

See the Test-Driven Development skill for complete TDD workflow (available in the skill library for comprehensive TDD guidance).
