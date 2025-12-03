# Testing Anti-Patterns in Python

How the core testing anti-patterns manifest in Python with pytest and unittest.mock.

## Anti-Pattern 1: Testing Mock Behavior

### Python Example

```python
# ❌ BAD - Testing mock behavior, not real code
from unittest.mock import Mock, patch

def test_send_email():
    mock_mailer = Mock()
    
    # System under test
    send_welcome_email(mock_mailer, "user@example.com")
    
    # Asserting on MOCK behavior
    assert mock_mailer.send_email.called  # Testing the mock!
    assert mock_mailer.send_email.call_count == 1
    mock_mailer.send_email.assert_called_with("user@example.com", "Welcome!")
```

**What's wrong:** Test passes if mock is called, but doesn't verify `send_welcome_email` actually works correctly.

**The fix:**
```python
# ✅ GOOD - Test real behavior with test double
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

### Detection in Python

**Red flags:**
- `mock.assert_called()`
- `mock.assert_called_once()`
- `mock.assert_called_with(...)`
- `mock.call_count`
- Testing `.called` or `.call_args`

**Gate function:**
```python
# Before writing test with mocks
def check_test_validity():
    """
    Q: Am I asserting on mock methods (.called, .call_count)?
    YES → STOP - You're testing the mock
    NO → Proceed
    """
```

## Anti-Pattern 2: Test-Only Methods in Production

### Python Example

```python
# ❌ BAD - Test-only method in production class
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

**What's wrong:** Production code polluted with test concerns. Breaks encapsulation.

**The fix:**
```python
# ✅ GOOD - Dependency injection, no test-only methods
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

### Detection in Python

**Red flags:**
- Methods named `_set_*`, `_mock_*`, `_for_testing`
- Docstrings saying "For testing only"
- `if os.getenv('TESTING')` conditionals
- Properties that exist only for test access

## Anti-Pattern 3: Mocking Without Understanding

### Python Example

```python
# ❌ BAD - Mocking without understanding side effects
@patch('user_service.send_email')
def test_user_registration(mock_send_email):
    register_user("test@example.com", "password123")
    
    # Didn't realize send_email also logs to analytics
    # Didn't realize send_email creates async task
    # Test passes but misses important behavior
    mock_send_email.assert_called_once()
```

**What's wrong:** Mocked `send_email` without understanding it logs analytics and creates background tasks.

**The fix:**
```python
# ✅ GOOD - Understand THEN mock minimally
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

### Detection in Python

**Red flags:**
- `@patch` decorators without trying test first
- Mocking entire modules (`@patch('user_service')`)
- Mocking internal functions in the same module
- Mock setup longer than test code

**Gate function:**
```python
# Before adding @patch
def check_mock_necessity():
    """
    Q: Did I run test WITHOUT mock first?
    NO → STOP - Run without mock to understand
    YES → Proceed with minimal mocking
    
    Q: Am I mocking internal code or external I/O?
    INTERNAL → STOP - Don't mock what you're testing
    EXTERNAL → Proceed
    """
```

## Anti-Pattern 4: Incomplete Mocks

### Python Example

```python
# ❌ BAD - Incomplete mock missing fields
from unittest.mock import Mock

def test_display_user_profile():
    mock_user = Mock()
    mock_user.id = 123
    mock_user.name = "Alice"
    # Missing: email, profile, metadata
    
    result = display_user_profile(mock_user)
    
    # Test passes but production code may access user.profile.timezone
    # → AttributeError in production!
```

**The fix:**
```python
# ✅ GOOD - Complete mock or use fixture
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    name: str
    email: str
    profile: 'UserProfile'
    metadata: dict

@dataclass
class UserProfile:
    timezone: str
    locale: str
    avatar: Optional[str]

# Fixture factory
def create_test_user(**overrides) -> User:
    """Complete user with all required fields"""
    defaults = {
        "id": 123,
        "name": "Alice",
        "email": "alice@example.com",
        "profile": UserProfile(
            timezone="UTC",
            locale="en-US",
            avatar=None
        ),
        "metadata": {}
    }
    return User(**{**defaults, **overrides})

def test_display_user_profile():
    user = create_test_user(name="Alice", profile__timezone="America/New_York")
    
    result = display_user_profile(user)
    
    assert "Alice" in result
    assert "America/New_York" in result
```

### Detection in Python

**Red flags:**
- Using `Mock()` for data objects
- Setting only a few attributes on mocks
- No type hints on mock objects
- Different tests have different mock shapes for same type

**Prevention:**
```python
# Use pytest fixtures or factory functions
import pytest

@pytest.fixture
def user():
    """Complete User fixture with all fields"""
    return create_test_user()

def test_with_fixture(user):
    # user has all required fields
    result = process_user(user)
    assert result.email == "alice@example.com"
```

## Anti-Pattern 5: Tests as Afterthought

### Python Example

```python
# ❌ BAD - Implementation before tests
# 1. Wrote create_user() function
# 2. Wrote update_user() function  
# 3. Wrote delete_user() function
# 4. Now writing tests to achieve coverage

def test_create_user():
    # Test confirms what code DOES, not what it SHOULD do
    # Bugs baked into test expectations
    pass
```

**The fix - TDD:**
```python
# ✅ GOOD - Test first (TDD)

# Step 1: RED - Write failing test
def test_create_user_validates_email():
    with pytest.raises(ValidationError):
        create_user("invalid-email")
    # ❌ Test fails - create_user doesn't exist

# Step 2: GREEN - Minimal implementation
def create_user(email: str) -> User:
    if "@" not in email:
        raise ValidationError("Invalid email")
    return User(email=email)
    # ✅ Test passes

# Step 3: REFACTOR - Improve without breaking test
def create_user(email: str) -> User:
    validate_email(email)  # Extracted validation
    return User(email=email)
    # ✅ Test still passes
```

### Python TDD Workflow

```python
# Complete TDD cycle
class TestUserRegistration:
    def test_user_registration_creates_user(self):
        # RED: Test fails
        result = register_user("test@example.com", "password123")
        assert result.success is True
        # ❌ register_user doesn't exist
    
    def test_user_registration_sends_welcome_email(self):
        # RED: Test fails
        fake_mailer = FakeMailer()
        register_user("test@example.com", "password123", mailer=fake_mailer)
        assert len(fake_mailer.sent_emails) == 1
        # ❌ Function doesn't send email yet
    
    # Implement register_user() to make tests GREEN
    # Then refactor while keeping tests GREEN
```

## pytest-Specific Patterns

### Use Fixtures, Not Mocks

```python
# ❌ BAD - Mocking database
@patch('app.database')
def test_get_user(mock_db):
    mock_db.query.return_value = Mock(id=1, name="Alice")
    # Testing mock behavior

# ✅ GOOD - Test database fixture
@pytest.fixture
def db():
    """In-memory SQLite for fast tests"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()

def test_get_user(db):
    # Insert real data
    db.add(User(id=1, name="Alice"))
    db.commit()
    
    # Test real behavior
    user = get_user(db, user_id=1)
    assert user.name == "Alice"
```

### pytest-mock Plugin

```python
# When you MUST mock, use pytest-mock
def test_api_call_retries(mocker):
    # Mock at I/O boundary
    mock_requests = mocker.patch('requests.post')
    mock_requests.side_effect = [
        ConnectionError(),  # First attempt fails
        ConnectionError(),  # Second attempt fails
        Mock(status_code=200, json=lambda: {"success": True})  # Third succeeds
    ]
    
    result = call_api_with_retry("https://api.example.com/data")
    
    assert mock_requests.call_count == 3
    assert result["success"] is True
```

### Parametrize Instead of Mocking

```python
# ❌ BAD - Mocking to test different values
def test_with_various_inputs():
    for value in [1, 2, 3]:
        mock_input = Mock(return_value=value)
        # Complex mock setup

# ✅ GOOD - Parametrize
@pytest.mark.parametrize("input_value,expected", [
    (1, "one"),
    (2, "two"),
    (3, "three"),
])
def test_number_to_word(input_value, expected):
    assert number_to_word(input_value) == expected
```

## Python-Specific Red Flags

**Watch for:**
- `unittest.mock.Mock()` for data objects → Use dataclasses
- `@patch` on every test → Over-mocking
- `MagicMock` without `spec` → Incomplete mocks
- `mock.return_value = ...` without types → Missing validation
- Global `@patch` decorators → Broad mocking
- `patch.object()` on system under test → Testing your own code

**Prevention checklist:**
```python
# Before using unittest.mock
□ Can I use a fixture instead of a mock?
□ Can I use a fake/test double instead?
□ Am I mocking at the I/O boundary, not internal code?
□ Did I run the test WITHOUT mocks first?
□ Do I understand what I'm mocking?
□ Is my mock complete (all fields/methods)?
```

## When Mocking Is Appropriate in Python

**✅ Mock these:**
- External HTTP calls (`requests.post`)
- Database connections in unit tests (`psycopg2.connect`)
- File system operations (`open`, `os.path.exists`)
- Time/datetime (`datetime.now`, `time.time`)
- Random number generation (`random.random`)
- Environment variables (`os.getenv`)

**❌ Don't mock these:**
- Your own business logic
- Data classes or models
- Internal helper functions
- Anything you're testing
- SQLAlchemy models (use test DB instead)
- Serializers/deserializers

## Quick Reference

| Anti-Pattern | Python Detection | Fix |
|--------------|------------------|-----|
| Testing mock behavior | `.assert_called()`, `.call_count` | Test real behavior with fakes |
| Test-only methods | `_for_testing`, `_set_mock_*` | Dependency injection |
| Uninformed mocking | `@patch` without trying real first | Run without mocks, understand |
| Incomplete mocks | `Mock()` for data objects | Use fixtures, dataclasses |
| Tests as afterthought | No TDD | Write test first, watch fail |
