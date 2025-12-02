# Python Advanced Patterns - Comprehensive Guide

**Created:** 2025-12-01
**Focus:** Moderate to difficult use cases with real-world examples
**Target Frameworks:** FastAPI, Django, pytest, Pydantic v2

## Table of Contents

1. [Async/Concurrency Patterns](#1-asyncconcurrency-patterns)
2. [Type System Mastery](#2-type-system-mastery)
3. [Design Patterns](#3-design-patterns)
4. [Testing & Quality](#4-testing--quality)
5. [Performance Optimization](#5-performance-optimization)

---

## 1. Async/Concurrency Patterns

### 1.1 Task Management with asyncio.gather()

**Complexity:** ⭐⭐⭐
**Use Case:** Execute multiple async operations concurrently and collect results
**Common Pitfall:** Using sequential `await` instead of parallel execution

**Pattern:**

```python
import asyncio
import time
from typing import List

async def fetch_user(user_id: int) -> dict:
    """Simulate async API call."""
    await asyncio.sleep(1)  # Network latency
    return {"id": user_id, "name": f"User {user_id}"}

async def fetch_orders(user_id: int) -> List[dict]:
    """Simulate async database query."""
    await asyncio.sleep(0.5)
    return [{"order_id": i, "user_id": user_id} for i in range(3)]

# ❌ WRONG: Sequential execution (3.5 seconds)
async def get_user_data_slow(user_id: int):
    user = await fetch_user(user_id)
    orders = await fetch_orders(user_id)
    profile = await fetch_user_profile(user_id)
    return {"user": user, "orders": orders, "profile": profile}

# ✅ CORRECT: Parallel execution (1 second)
async def get_user_data_fast(user_id: int):
    user, orders, profile = await asyncio.gather(
        fetch_user(user_id),
        fetch_orders(user_id),
        fetch_user_profile(user_id)
    )
    return {"user": user, "orders": orders, "profile": profile}

# Run
asyncio.run(get_user_data_fast(123))
```

**Performance Impact:** 3.5x faster in this example

---

### 1.2 Error Handling with asyncio.gather()

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Handle partial failures in concurrent operations
**Common Pitfall:** Entire operation fails if one task raises exception

**Pattern:**

```python
import asyncio
from typing import List, Union

async def fetch_with_error(url: str) -> dict:
    """Simulate API call that might fail."""
    await asyncio.sleep(0.5)
    if "bad" in url:
        raise ValueError(f"Failed to fetch {url}")
    return {"url": url, "data": "success"}

# ❌ WRONG: First error stops everything
async def fetch_all_fail_fast(urls: List[str]):
    return await asyncio.gather(*[fetch_with_error(url) for url in urls])

# ✅ CORRECT: Collect all results including errors
async def fetch_all_with_errors(urls: List[str]) -> List[Union[dict, Exception]]:
    """Return all results, converting exceptions to values."""
    results = await asyncio.gather(
        *[fetch_with_error(url) for url in urls],
        return_exceptions=True  # Key parameter
    )

    # Process results
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"URL {urls[i]} failed: {result}")
        else:
            print(f"URL {urls[i]} succeeded: {result}")

    return results

# Usage
urls = ["good1.com", "bad-url.com", "good2.com"]
results = asyncio.run(fetch_all_with_errors(urls))
# Output: 2 successes, 1 error (all URLs attempted)
```

**Key Takeaway:** Always use `return_exceptions=True` for fault-tolerant concurrent operations.

---

### 1.3 Semaphore for Rate Limiting

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Limit concurrent operations (API rate limits, database connections)
**Real-World:** Prevent overwhelming external services with too many requests

**Pattern:**

```python
import asyncio
from typing import List
import aiohttp

class RateLimitedClient:
    """HTTP client with built-in rate limiting."""

    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    async def fetch(self, url: str) -> dict:
        """Fetch URL with rate limiting."""
        async with self.semaphore:  # Only N concurrent requests
            async with self.session.get(url) as response:
                return await response.json()

    async def fetch_all(self, urls: List[str]) -> List[dict]:
        """Fetch multiple URLs with rate limiting."""
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Usage
async def main():
    urls = [f"https://api.example.com/items/{i}" for i in range(100)]

    async with RateLimitedClient(max_concurrent=5) as client:
        results = await client.fetch_all(urls)

    print(f"Fetched {len(results)} results")

asyncio.run(main())
```

**Performance Note:** Prevents 429 errors while maximizing throughput within rate limits.

---

### 1.4 Background Tasks with asyncio.create_task()

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Fire-and-forget operations without blocking main flow
**Common Pitfall:** Task gets garbage collected before completion

**Pattern:**

```python
import asyncio
from typing import Set

class BackgroundTaskManager:
    """Manage background tasks to prevent premature garbage collection."""

    def __init__(self):
        self.tasks: Set[asyncio.Task] = set()

    def create_task(self, coro) -> asyncio.Task:
        """Create background task and track it."""
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)  # Auto-cleanup
        return task

    async def shutdown(self):
        """Wait for all background tasks to complete."""
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)

# FastAPI Integration Example
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()
task_manager = BackgroundTaskManager()

async def send_email(email: str, message: str):
    """Async email sending (takes 2 seconds)."""
    await asyncio.sleep(2)
    print(f"Email sent to {email}: {message}")

@app.post("/orders")
async def create_order(order_id: int, email: str):
    # Process order synchronously
    order = {"id": order_id, "status": "created"}

    # Send email in background (don't wait)
    task_manager.create_task(
        send_email(email, f"Order {order_id} created")
    )

    # Return immediately
    return order  # Response in <50ms, email sent in background

@app.on_event("shutdown")
async def shutdown_event():
    """Wait for background tasks before shutdown."""
    await task_manager.shutdown()
```

**Performance Impact:** Response time drops from 2000ms to <50ms.

---

## 2. Type System Mastery

### 2.1 Generic Types with TypeVar

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Create reusable, type-safe data structures and functions
**Framework Integration:** FastAPI dependency injection, repository patterns

**Pattern:**

```python
from typing import TypeVar, Generic, List, Optional, Protocol
from abc import ABC, abstractmethod

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# Generic Repository Pattern
class Entity(Protocol):
    """Protocol for entities with ID."""
    id: int

class Repository(Generic[T], ABC):
    """Abstract repository for any entity type."""

    @abstractmethod
    async def get(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        pass

    @abstractmethod
    async def list(self, limit: int = 100) -> List[T]:
        """List entities."""
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create new entity."""
        pass

# Concrete Implementation
from pydantic import BaseModel

class User(BaseModel):
    """User model."""
    id: int
    email: str
    name: str

class UserRepository(Repository[User]):
    """User-specific repository."""

    def __init__(self):
        self._store: dict[int, User] = {}

    async def get(self, id: int) -> Optional[User]:
        return self._store.get(id)

    async def list(self, limit: int = 100) -> List[User]:
        return list(self._store.values())[:limit]

    async def create(self, user: User) -> User:
        self._store[user.id] = user
        return user

# Type-safe usage
async def get_user_safely(repo: Repository[User], user_id: int) -> Optional[User]:
    user = await repo.get(user_id)
    # Type checker knows 'user' is Optional[User]
    if user:
        print(user.email)  # ✅ Type-safe
    return user
```

**Key Benefit:** Full type safety across different entity types with shared repository logic.

---

### 2.2 Protocol for Structural Typing

**Complexity:** ⭐⭐⭐⭐⭐
**Use Case:** Duck typing with type safety, avoiding inheritance hierarchies
**Advantage:** More flexible than ABC, enables gradual typing

**Pattern:**

```python
from typing import Protocol, runtime_checkable, List
import json

# Define protocol (interface)
@runtime_checkable
class Serializable(Protocol):
    """Protocol for objects that can be serialized."""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        ...

    @classmethod
    def from_dict(cls, data: dict) -> 'Serializable':
        """Create from dictionary."""
        ...

# Implementations (no inheritance needed!)
class User:
    """User class that happens to implement Serializable."""

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(data["id"], data["name"])

class Product:
    """Product class also implements Serializable."""

    def __init__(self, sku: str, price: float):
        self.sku = sku
        self.price = price

    def to_dict(self) -> dict:
        return {"sku": self.sku, "price": self.price}

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        return cls(data["sku"], data["price"])

# Generic function works with any Serializable
def serialize_to_json(obj: Serializable) -> str:
    """Serialize any Serializable object to JSON."""
    return json.dumps(obj.to_dict())

def deserialize_from_json(cls: type[Serializable], json_str: str) -> Serializable:
    """Deserialize JSON to any Serializable type."""
    data = json.loads(json_str)
    return cls.from_dict(data)

# Type-safe usage
user = User(1, "Alice")
product = Product("ABC123", 29.99)

# Both work with same function!
user_json = serialize_to_json(user)  # ✅
product_json = serialize_to_json(product)  # ✅

# Runtime check
assert isinstance(user, Serializable)  # ✅ True
```

**Key Advantage:** No need to modify existing classes to fit into type system.

---

### 2.3 Advanced Pydantic v2 Validation

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Complex validation rules, custom validators, computed fields
**Framework:** FastAPI request validation, Django settings

**Pattern:**

```python
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Optional
from datetime import datetime, date

class User(BaseModel):
    """User model with advanced validation."""

    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=0, le=150)
    password: str = Field(..., min_length=8)
    password_confirm: Optional[str] = None
    birth_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Field validator (Pydantic v2 syntax)
    @field_validator('email')
    @classmethod
    def email_must_be_lowercase(cls, v: str) -> str:
        """Ensure email is lowercase."""
        return v.lower()

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

    # Model validator (cross-field validation)
    @model_validator(mode='after')
    def check_passwords_match(self):
        """Ensure passwords match."""
        if self.password_confirm and self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self

    @model_validator(mode='after')
    def check_age_matches_birth_date(self):
        """Validate age against birth date."""
        if self.birth_date:
            today = date.today()
            calculated_age = today.year - self.birth_date.year
            if abs(calculated_age - self.age) > 1:
                raise ValueError('Age does not match birth date')
        return self

    # Computed field (v2 feature)
    @computed_field
    @property
    def is_adult(self) -> bool:
        """Check if user is adult."""
        return self.age >= 18

    # Pydantic v2 configuration
    model_config = {
        "str_strip_whitespace": True,
        "validate_assignment": True,
        "populate_by_name": True,
    }

# FastAPI integration
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/users")
async def create_user(user: User):
    """Create user with automatic validation."""
    # Validation happens automatically!
    # No need for manual checks
    return {
        "email": user.email,
        "age": user.age,
        "is_adult": user.is_adult  # Computed field
    }

# Usage
try:
    user = User(
        email="ALICE@EXAMPLE.COM",  # Will be lowercased
        age=25,
        password="SecureP@ss123",
        password_confirm="SecureP@ss123",
        birth_date=date(1999, 1, 1)
    )
    print(user.email)  # "alice@example.com"
    print(user.is_adult)  # True
except ValueError as e:
    print(f"Validation error: {e}")
```

**Key Features:**
- Field-level validation with `@field_validator`
- Cross-field validation with `@model_validator`
- Computed fields with `@computed_field`
- Automatic type coercion and validation

---

### 2.4 TypedDict for Structured Dictionaries

**Complexity:** ⭐⭐⭐
**Use Case:** Type-safe dictionary structures (API responses, configs)
**Advantage:** Better than plain dict, lighter than Pydantic

**Pattern:**

```python
from typing import TypedDict, NotRequired, Required
from datetime import datetime

# Basic TypedDict
class UserDict(TypedDict):
    """Type-safe user dictionary."""
    id: int
    email: str
    name: str

# TypedDict with optional fields (Python 3.11+)
class UserProfile(TypedDict):
    """User profile with optional fields."""
    id: Required[int]  # Always required
    email: Required[str]
    name: NotRequired[str]  # Optional field
    bio: NotRequired[str]
    avatar_url: NotRequired[str]

# Nested TypedDict
class Address(TypedDict):
    street: str
    city: str
    country: str

class UserWithAddress(TypedDict):
    id: int
    email: str
    address: Address

# Usage in function signatures
def get_user(user_id: int) -> UserDict:
    """Get user as typed dict."""
    return {
        "id": user_id,
        "email": "alice@example.com",
        "name": "Alice"
    }

def format_user(user: UserDict) -> str:
    """Format user - type checker knows structure."""
    return f"{user['name']} <{user['email']}>"  # ✅ Type-safe

# Django/FastAPI integration
from typing import List

async def get_users_from_db() -> List[UserDict]:
    """Return raw SQL results as typed dicts."""
    # Direct database query (no ORM)
    results = await db.fetch_all("SELECT id, email, name FROM users")
    return [dict(row) for row in results]  # Type-safe!

# Type checking catches errors
def broken_function(user: UserDict):
    print(user['invalid_key'])  # ❌ Type checker error!
```

**When to use TypedDict vs Pydantic:**
- TypedDict: Database queries, API responses, lightweight typing
- Pydantic: Validation, serialization, complex business logic

---

## 3. Design Patterns

### 3.1 Context Managers for Resource Management

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Database connections, file handles, locks, transactions
**Common Pitfall:** Forgetting to release resources in error cases

**Pattern:**

```python
from contextlib import contextmanager, asynccontextmanager
from typing import AsyncGenerator, Generator
import asyncio

# Synchronous Context Manager
@contextmanager
def database_transaction(connection) -> Generator:
    """Manage database transaction with automatic rollback."""
    try:
        yield connection
        connection.commit()
        print("Transaction committed")
    except Exception as e:
        connection.rollback()
        print(f"Transaction rolled back: {e}")
        raise
    finally:
        connection.close()
        print("Connection closed")

# Usage
with database_transaction(get_connection()) as conn:
    conn.execute("INSERT INTO users ...")
    # Automatically commits on success, rolls back on error

# Async Context Manager
@asynccontextmanager
async def async_database_session() -> AsyncGenerator:
    """Async database session management."""
    session = await create_async_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

# FastAPI Lifespan Context Manager
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    print("Starting up...")
    db_pool = await create_db_pool()
    redis_client = await create_redis_client()

    # Store in app state
    app.state.db = db_pool
    app.state.redis = redis_client

    yield  # Application runs

    # Shutdown
    print("Shutting down...")
    await db_pool.close()
    await redis_client.close()

app = FastAPI(lifespan=lifespan)

# Class-based Context Manager
class FileWriter:
    """Context manager for safe file writing."""

    def __init__(self, filename: str):
        self.filename = filename
        self.file = None
        self.temp_filename = f"{filename}.tmp"

    def __enter__(self):
        """Open temp file for writing."""
        self.file = open(self.temp_filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close and rename on success, delete on error."""
        self.file.close()

        if exc_type is None:
            # Success: rename temp to final
            import os
            os.rename(self.temp_filename, self.filename)
        else:
            # Error: delete temp file
            import os
            os.remove(self.temp_filename)

        return False  # Don't suppress exceptions

# Usage
with FileWriter("data.json") as f:
    f.write('{"data": "value"}')
    # File atomically written on success
```

**Key Benefit:** Resources always cleaned up, even on exceptions.

---

### 3.2 Dependency Injection Pattern

**Complexity:** ⭐⭐⭐⭐⭐
**Use Case:** Testable code, flexible architecture, FastAPI dependencies
**Framework Integration:** FastAPI Depends(), pytest fixtures

**Pattern:**

```python
from typing import Protocol, AsyncGenerator
from abc import abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Define interfaces (protocols)
class UserRepository(Protocol):
    """User repository interface."""

    @abstractmethod
    async def get(self, user_id: int) -> Optional[User]:
        ...

    @abstractmethod
    async def create(self, user: User) -> User:
        ...

class EmailService(Protocol):
    """Email service interface."""

    @abstractmethod
    async def send(self, to: str, subject: str, body: str):
        ...

# Concrete implementations
class SQLAlchemyUserRepository:
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        db_user = UserModel(**user.dict())
        self.session.add(db_user)
        await self.session.commit()
        return user

class SMTPEmailService:
    """SMTP email service implementation."""

    def __init__(self, smtp_host: str, smtp_port: int):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    async def send(self, to: str, subject: str, body: str):
        # Send email via SMTP
        print(f"Sending email to {to}: {subject}")

# FastAPI Dependency Injection
from fastapi import Depends, FastAPI

app = FastAPI()

# Database session dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide database session."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

# Repository dependency
def get_user_repository(
    session: AsyncSession = Depends(get_db)
) -> UserRepository:
    """Provide user repository."""
    return SQLAlchemyUserRepository(session)

# Service dependency
def get_email_service() -> EmailService:
    """Provide email service."""
    return SMTPEmailService(
        smtp_host="smtp.example.com",
        smtp_port=587
    )

# Endpoint with dependency injection
@app.post("/users")
async def create_user(
    user_data: UserCreate,
    user_repo: UserRepository = Depends(get_user_repository),
    email_service: EmailService = Depends(get_email_service)
):
    """Create user with injected dependencies."""
    # Use injected dependencies
    user = await user_repo.create(User(**user_data.dict()))

    await email_service.send(
        to=user.email,
        subject="Welcome!",
        body=f"Welcome {user.name}"
    )

    return user

# Testing with dependency override
from fastapi.testclient import TestClient

class MockUserRepository:
    """Mock repository for testing."""

    async def create(self, user: User) -> User:
        return user  # No database access

class MockEmailService:
    """Mock email service for testing."""

    async def send(self, to: str, subject: str, body: str):
        print(f"Mock email sent to {to}")

def test_create_user():
    """Test with mocked dependencies."""
    # Override dependencies
    app.dependency_overrides[get_user_repository] = lambda: MockUserRepository()
    app.dependency_overrides[get_email_service] = lambda: MockEmailService()

    client = TestClient(app)
    response = client.post("/users", json={"email": "test@example.com", "name": "Test"})

    assert response.status_code == 200
```

**Key Benefits:**
- Testable code (easy to mock dependencies)
- Loose coupling (depend on interfaces, not implementations)
- Flexible (swap implementations without changing business logic)

---

### 3.3 Abstract Base Classes (ABC)

**Complexity:** ⭐⭐⭐
**Use Case:** Define contracts, enforce implementation, plugin systems
**Difference from Protocol:** ABC requires inheritance, Protocol uses structural typing

**Pattern:**

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar

T = TypeVar('T')

# Abstract base class
class DataStore(ABC, Generic[T]):
    """Abstract data storage interface."""

    @abstractmethod
    async def save(self, key: str, value: T) -> None:
        """Save value to store."""
        pass

    @abstractmethod
    async def load(self, key: str) -> Optional[T]:
        """Load value from store."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from store."""
        pass

    @abstractmethod
    async def list_keys(self) -> List[str]:
        """List all keys."""
        pass

    # Concrete method (provided by ABC)
    async def exists(self, key: str) -> bool:
        """Check if key exists (default implementation)."""
        return await self.load(key) is not None

# Concrete implementations
import json
from pathlib import Path

class FileDataStore(DataStore[dict]):
    """File-based data store."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(exist_ok=True)

    async def save(self, key: str, value: dict) -> None:
        file_path = self.base_path / f"{key}.json"
        with open(file_path, 'w') as f:
            json.dump(value, f)

    async def load(self, key: str) -> Optional[dict]:
        file_path = self.base_path / f"{key}.json"
        if not file_path.exists():
            return None
        with open(file_path, 'r') as f:
            return json.load(f)

    async def delete(self, key: str) -> bool:
        file_path = self.base_path / f"{key}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    async def list_keys(self) -> List[str]:
        return [f.stem for f in self.base_path.glob("*.json")]

import redis.asyncio as redis

class RedisDataStore(DataStore[dict]):
    """Redis-based data store."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def save(self, key: str, value: dict) -> None:
        await self.redis.set(key, json.dumps(value))

    async def load(self, key: str) -> Optional[dict]:
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def delete(self, key: str) -> bool:
        return await self.redis.delete(key) > 0

    async def list_keys(self) -> List[str]:
        keys = await self.redis.keys("*")
        return [k.decode() for k in keys]

# Factory pattern with ABC
class DataStoreFactory:
    """Factory for creating data stores."""

    @staticmethod
    def create(store_type: str, **kwargs) -> DataStore:
        """Create data store based on type."""
        if store_type == "file":
            return FileDataStore(Path(kwargs['path']))
        elif store_type == "redis":
            return RedisDataStore(kwargs['redis_client'])
        else:
            raise ValueError(f"Unknown store type: {store_type}")

# Usage - polymorphic behavior
async def save_user_data(store: DataStore[dict], user_id: str, data: dict):
    """Save user data to any store implementation."""
    await store.save(f"user:{user_id}", data)
    print(f"Saved to {type(store).__name__}")

# Works with any DataStore implementation!
file_store = DataStoreFactory.create("file", path="/tmp/data")
await save_user_data(file_store, "123", {"name": "Alice"})

redis_store = DataStoreFactory.create("redis", redis_client=redis_client)
await save_user_data(redis_store, "123", {"name": "Alice"})
```

**When to use ABC vs Protocol:**
- ABC: When you control implementations and want strict contracts
- Protocol: When working with existing code or third-party libraries

---

## 4. Testing & Quality

### 4.1 Pytest Fixtures with Dependency Injection

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Set up test dependencies, share resources, teardown
**Integration:** FastAPI TestClient, database sessions, mocks

**Pattern:**

```python
import pytest
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Fixture scopes: function (default), class, module, session

# Session-scoped fixture (created once per test session)
@pytest.fixture(scope="session")
def engine():
    """Create database engine for entire test session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

# Module-scoped fixture (created once per test module)
@pytest.fixture(scope="module")
def session_factory(engine) -> sessionmaker:
    """Create session factory for test module."""
    return sessionmaker(bind=engine)

# Function-scoped fixture (created for each test)
@pytest.fixture
def db_session(session_factory) -> Generator[Session, None, None]:
    """Provide database session with rollback."""
    session = session_factory()
    try:
        yield session
    finally:
        session.rollback()  # Rollback after each test
        session.close()

# Fixture with parameters
@pytest.fixture
def test_user(db_session: Session):
    """Create test user in database."""
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

# FastAPI client fixture
@pytest.fixture
def client(db_session: Session) -> TestClient:
    """Create FastAPI test client with overridden dependencies."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

# Async fixture
@pytest.fixture
async def async_client() -> AsyncGenerator:
    """Create async HTTP client."""
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Using fixtures in tests
def test_create_user(client: TestClient, db_session: Session):
    """Test user creation endpoint."""
    response = client.post("/users", json={"email": "new@example.com", "name": "New User"})

    assert response.status_code == 201
    assert response.json()["email"] == "new@example.com"

    # Verify in database
    user = db_session.query(User).filter_by(email="new@example.com").first()
    assert user is not None
    assert user.name == "New User"

def test_get_user(client: TestClient, test_user: User):
    """Test get user endpoint (uses test_user fixture)."""
    response = client.get(f"/users/{test_user.id}")

    assert response.status_code == 200
    assert response.json()["id"] == test_user.id
```

**Key Concepts:**
- Fixture scopes control lifetime
- Fixtures can depend on other fixtures
- `yield` enables setup/teardown pattern
- Override app dependencies for testing

---

### 4.2 Parametrized Tests

**Complexity:** ⭐⭐⭐
**Use Case:** Test same logic with multiple inputs
**Benefit:** Reduce test duplication, increase coverage

**Pattern:**

```python
import pytest
from typing import Any

# Simple parametrization
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (-2, 4),
])
def test_square(input: int, expected: int):
    """Test square function with multiple inputs."""
    assert square(input) == expected

# Multiple parameters
@pytest.mark.parametrize("email,is_valid", [
    ("user@example.com", True),
    ("invalid.email", False),
    ("user@", False),
    ("@example.com", False),
    ("user+tag@example.com", True),
])
def test_email_validation(email: str, is_valid: bool):
    """Test email validation."""
    result = validate_email(email)
    assert result == is_valid

# Parametrize with fixture
@pytest.mark.parametrize("user_role", ["admin", "user", "guest"])
def test_access_control(client: TestClient, user_role: str):
    """Test access control for different roles."""
    # Create user with specific role
    user = create_user_with_role(user_role)

    response = client.get("/protected", headers={"Authorization": f"Bearer {user.token}"})

    if user_role == "admin":
        assert response.status_code == 200
    else:
        assert response.status_code == 403

# Parametrize fixture itself
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def db_engine(request):
    """Provide different database engines."""
    engine_type = request.param

    if engine_type == "sqlite":
        engine = create_engine("sqlite:///:memory:")
    elif engine_type == "postgresql":
        engine = create_engine("postgresql://localhost/test")
    else:
        engine = create_engine("mysql://localhost/test")

    yield engine
    engine.dispose()

def test_user_repository(db_engine):
    """Test repository with all database types."""
    repo = UserRepository(db_engine)
    # Test runs 3 times (once per database type)
    user = repo.create(User(email="test@example.com"))
    assert user.id is not None

# Complex parametrization with pytest.param
@pytest.mark.parametrize("input_data,expected,should_raise", [
    pytest.param({"email": "valid@example.com"}, 201, False, id="valid_email"),
    pytest.param({"email": "invalid"}, None, True, id="invalid_email", marks=pytest.mark.xfail),
    pytest.param({"email": ""}, None, True, id="empty_email"),
])
def test_user_creation(client: TestClient, input_data: dict, expected: int, should_raise: bool):
    """Test user creation with various inputs."""
    if should_raise:
        with pytest.raises(ValueError):
            client.post("/users", json=input_data)
    else:
        response = client.post("/users", json=input_data)
        assert response.status_code == expected
```

**Key Benefits:**
- Test coverage increases with minimal code
- Clear test cases with descriptive IDs
- Easy to add new test cases

---

### 4.3 Mocking with pytest-mock

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Isolate unit tests from external dependencies
**Common Pitfall:** Over-mocking (testing mocks instead of real behavior)

**Pattern:**

```python
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Any

# Basic mock
def test_send_email(mocker):
    """Test email sending without actually sending."""
    # Mock the email service
    mock_smtp = mocker.patch('smtplib.SMTP')

    # Call function that sends email
    send_welcome_email("user@example.com")

    # Verify email was "sent"
    mock_smtp.assert_called_once()
    mock_smtp.return_value.send_message.assert_called_once()

# Async mock
@pytest.mark.asyncio
async def test_async_api_call(mocker):
    """Test async function with mocked HTTP call."""
    # Create async mock
    mock_response = AsyncMock()
    mock_response.json.return_value = {"data": "mocked"}

    # Patch async HTTP client
    mocker.patch('httpx.AsyncClient.get', return_value=mock_response)

    # Call function
    result = await fetch_user_data(123)

    assert result == {"data": "mocked"}

# Mock with side effects
def test_retry_logic(mocker):
    """Test retry logic with failing then succeeding calls."""
    mock_api = mocker.patch('api_client.call')

    # First 2 calls fail, 3rd succeeds
    mock_api.side_effect = [
        ConnectionError("Network error"),
        ConnectionError("Network error"),
        {"status": "success"}
    ]

    # Should retry and eventually succeed
    result = call_with_retry(max_retries=3)

    assert result == {"status": "success"}
    assert mock_api.call_count == 3

# Spy on real function
def test_cache_hit(mocker):
    """Test that cached results don't call expensive function."""
    # Spy on expensive function
    spy = mocker.spy(module, 'expensive_computation')

    # First call - should compute
    result1 = get_cached_result("key1")
    assert spy.call_count == 1

    # Second call - should use cache
    result2 = get_cached_result("key1")
    assert spy.call_count == 1  # No additional call
    assert result1 == result2

# Mock database session
def test_user_service_with_mock_db(mocker):
    """Test service layer with mocked database."""
    # Create mock session
    mock_session = MagicMock()
    mock_user = User(id=1, email="test@example.com")

    # Configure mock to return user
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user

    # Test service
    service = UserService(mock_session)
    user = service.get_user_by_email("test@example.com")

    assert user.id == 1
    mock_session.query.assert_called_once_with(User)

# Context manager mock
def test_file_processing(mocker):
    """Test file processing with mocked file operations."""
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='file content'))

    result = process_file('test.txt')

    mock_open.assert_called_once_with('test.txt', 'r')
    assert result == 'processed: file content'

# FastAPI dependency override (better than mocking)
def test_endpoint_with_mocked_service():
    """Test FastAPI endpoint with mocked service."""
    mock_service = Mock()
    mock_service.get_user.return_value = User(id=1, email="test@example.com")

    # Override dependency
    app.dependency_overrides[get_user_service] = lambda: mock_service

    with TestClient(app) as client:
        response = client.get("/users/1")

    assert response.status_code == 200
    mock_service.get_user.assert_called_once_with(1)

    app.dependency_overrides.clear()
```

**Best Practices:**
- Mock external dependencies (APIs, databases, file systems)
- Don't mock what you own (test real code)
- Use dependency injection to make mocking easier
- Verify mock interactions with assertions

---

### 4.4 Integration Testing with pytest-asyncio

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Test async code, database transactions, API endpoints
**Framework:** FastAPI, async SQLAlchemy, aiohttp

**Pattern:**

```python
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Async fixtures
@pytest_asyncio.fixture
async def async_engine():
    """Create async database engine."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()

@pytest_asyncio.fixture
async def async_session(async_engine) -> AsyncSession:
    """Provide async database session."""
    async_session_factory = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_factory() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture
async def async_client(async_session: AsyncSession) -> AsyncClient:
    """Create async test client."""

    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_async_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()

# Async tests
@pytest.mark.asyncio
async def test_create_user_async(async_client: AsyncClient, async_session: AsyncSession):
    """Test async user creation."""
    # Create user via API
    response = await async_client.post(
        "/users",
        json={"email": "async@example.com", "name": "Async User"}
    )

    assert response.status_code == 201
    user_id = response.json()["id"]

    # Verify in database
    from sqlalchemy import select
    result = await async_session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one()

    assert user.email == "async@example.com"

@pytest.mark.asyncio
async def test_concurrent_requests(async_client: AsyncClient):
    """Test handling concurrent requests."""
    import asyncio

    # Create 10 concurrent requests
    tasks = [
        async_client.post("/users", json={"email": f"user{i}@example.com", "name": f"User {i}"})
        for i in range(10)
    ]

    responses = await asyncio.gather(*tasks)

    # All should succeed
    assert all(r.status_code == 201 for r in responses)

    # All should have unique IDs
    ids = [r.json()["id"] for r in responses]
    assert len(ids) == len(set(ids))

@pytest.mark.asyncio
async def test_transaction_rollback(async_session: AsyncSession):
    """Test transaction rollback on error."""
    from sqlalchemy import select

    try:
        # Create user
        user = User(email="test@example.com", name="Test")
        async_session.add(user)
        await async_session.flush()

        # Simulate error
        raise ValueError("Simulated error")

    except ValueError:
        await async_session.rollback()

    # Verify user was not saved
    result = await async_session.execute(
        select(User).where(User.email == "test@example.com")
    )
    assert result.scalar_one_or_none() is None

# Test async background tasks
@pytest.mark.asyncio
async def test_background_task_execution():
    """Test background task completes."""
    import asyncio

    result = []

    async def background_task():
        await asyncio.sleep(0.1)
        result.append("completed")

    # Start background task
    task = asyncio.create_task(background_task())

    # Wait for completion
    await task

    assert result == ["completed"]
```

**Key Points:**
- Use `@pytest.mark.asyncio` for async tests
- Use `pytest_asyncio.fixture` for async fixtures
- Test concurrent operations with `asyncio.gather`
- Verify async transactions and rollbacks

---

## 5. Performance Optimization

### 5.1 Efficient Data Processing with Generators

**Complexity:** ⭐⭐⭐
**Use Case:** Process large datasets without loading into memory
**Memory Savings:** 100x+ for large files

**Pattern:**

```python
from typing import Generator, Iterator
import csv

# ❌ WRONG: Loads entire file into memory
def read_csv_bad(filename: str) -> list[dict]:
    """Load entire CSV into memory."""
    with open(filename) as f:
        return list(csv.DictReader(f))  # Loads all rows

# ✅ CORRECT: Generator processes one row at a time
def read_csv_good(filename: str) -> Generator[dict, None, None]:
    """Process CSV one row at a time."""
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row  # Memory-efficient

# Processing pipeline with generators
def filter_active_users(rows: Iterator[dict]) -> Generator[dict, None, None]:
    """Filter for active users."""
    for row in rows:
        if row.get('status') == 'active':
            yield row

def transform_user_data(rows: Iterator[dict]) -> Generator[dict, None, None]:
    """Transform user data."""
    for row in rows:
        yield {
            'user_id': int(row['id']),
            'email': row['email'].lower(),
            'created': row['created_at']
        }

# Chained generators (lazy evaluation)
def process_users(filename: str) -> Generator[dict, None, None]:
    """Process users with chained generators."""
    rows = read_csv_good(filename)
    active = filter_active_users(rows)
    transformed = transform_user_data(active)
    return transformed

# Usage - processes one row at a time
for user in process_users('users.csv'):
    # Only one row in memory at a time
    save_to_database(user)

# Generator expression (even more concise)
def get_user_emails(filename: str) -> Generator[str, None, None]:
    """Extract emails using generator expression."""
    return (row['email'] for row in read_csv_good(filename) if row.get('verified'))

# Async generator for I/O operations
async def fetch_user_pages(page_count: int) -> AsyncGenerator[list[dict], None]:
    """Fetch pages asynchronously."""
    async with httpx.AsyncClient() as client:
        for page in range(1, page_count + 1):
            response = await client.get(f"https://api.example.com/users?page={page}")
            yield response.json()

# Usage
async for users in fetch_user_pages(10):
    for user in users:
        print(user['name'])
```

**Performance Impact:**
- Memory: O(1) instead of O(n)
- Can process files larger than available RAM
- Starts producing results immediately (no wait for entire file)

---

### 5.2 Caching with functools.lru_cache

**Complexity:** ⭐⭐⭐
**Use Case:** Cache expensive function results
**Performance:** 100x+ speedup for repeated calls

**Pattern:**

```python
from functools import lru_cache, cache
from typing import Optional
import time

# Simple cache (Python 3.9+)
@cache  # Unlimited cache size
def fibonacci(n: int) -> int:
    """Cached fibonacci calculation."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# LRU cache with size limit
@lru_cache(maxsize=128)
def expensive_computation(x: int, y: int) -> int:
    """Expensive function with LRU cache."""
    time.sleep(1)  # Simulate expensive operation
    return x ** y

# First call: 1 second
result1 = expensive_computation(2, 10)

# Second call: instant (cached)
result2 = expensive_computation(2, 10)

# Cache info
print(expensive_computation.cache_info())
# CacheInfo(hits=1, misses=1, maxsize=128, currsize=1)

# Clear cache
expensive_computation.cache_clear()

# Cache with custom key function
from functools import wraps

def cache_with_ttl(ttl_seconds: int):
    """Cache with time-to-live."""
    def decorator(func):
        cache = {}
        timestamps = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()

            # Check if cached and not expired
            if key in cache and (now - timestamps[key]) < ttl_seconds:
                return cache[key]

            # Compute and cache
            result = func(*args, **kwargs)
            cache[key] = result
            timestamps[key] = now
            return result

        return wrapper
    return decorator

@cache_with_ttl(ttl_seconds=60)
def get_user_from_api(user_id: int) -> dict:
    """Fetch user with 60-second cache."""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# FastAPI route-level caching
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

app = FastAPI()

@app.get("/users/{user_id}")
@cache(expire=60)  # Cache response for 60 seconds
async def get_user(user_id: int):
    """Cached endpoint."""
    # Expensive database query
    user = await db.query(User).filter(User.id == user_id).first()
    return user

# Async LRU cache (Python 3.11+)
from functools import lru_cache

@lru_cache(maxsize=100)
async def cached_async_function(key: str) -> dict:
    """Async function with cache."""
    await asyncio.sleep(1)
    return {"key": key, "data": "expensive"}
```

**Best Practices:**
- Use `@cache` for unlimited cache (small result sets)
- Use `@lru_cache(maxsize=N)` for bounded cache (large result sets)
- Don't cache functions with mutable arguments (dict, list)
- Clear cache periodically for long-running processes

---

### 5.3 Database Query Optimization

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Avoid N+1 queries, optimize joins
**Framework:** SQLAlchemy, Django ORM

**Pattern:**

```python
from sqlalchemy import select, joinedload, selectinload
from sqlalchemy.orm import Session, relationship

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")

# ❌ WRONG: N+1 query problem
def get_users_with_posts_bad(session: Session):
    """N+1 queries - very slow!"""
    users = session.query(User).all()  # 1 query

    for user in users:
        for post in user.posts:  # N additional queries!
            print(f"{user.name}: {post.title}")

# ✅ CORRECT: Eager loading with joinedload
def get_users_with_posts_good(session: Session):
    """Single query with JOIN."""
    users = session.query(User).options(
        joinedload(User.posts)  # Load posts in same query
    ).all()

    for user in users:
        for post in user.posts:  # No additional queries!
            print(f"{user.name}: {post.title}")

# ✅ CORRECT: selectinload for one-to-many relationships
def get_users_with_posts_and_comments(session: Session):
    """Efficient loading of nested relationships."""
    users = session.query(User).options(
        selectinload(User.posts).selectinload(Post.comments)
    ).all()

    for user in users:
        for post in user.posts:
            print(f"{user.name}: {post.title} ({len(post.comments)} comments)")

# Async SQLAlchemy optimization
from sqlalchemy.ext.asyncio import AsyncSession

async def get_users_async(session: AsyncSession):
    """Async query with eager loading."""
    stmt = select(User).options(
        selectinload(User.posts)
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users

# Django ORM equivalent
from django.db import models

# ❌ WRONG: N+1 in Django
users = User.objects.all()
for user in users:
    for post in user.posts.all():  # N queries!
        print(post.title)

# ✅ CORRECT: select_related (one-to-one, foreign key)
users = User.objects.select_related('profile').all()

# ✅ CORRECT: prefetch_related (many-to-many, reverse FK)
users = User.objects.prefetch_related('posts').all()

# ✅ CORRECT: nested prefetch
from django.db.models import Prefetch

users = User.objects.prefetch_related(
    Prefetch('posts', queryset=Post.objects.prefetch_related('comments'))
).all()

# Only() and defer() for column optimization
# ❌ WRONG: Loads all columns
users = User.objects.all()

# ✅ CORRECT: Only load needed columns
users = User.objects.only('id', 'email').all()

# ✅ CORRECT: Defer large columns
users = User.objects.defer('profile_picture', 'bio').all()
```

**Performance Impact:**
- N+1 query: 101 queries for 100 users
- Eager loading: 1-2 queries for 100 users
- 50x+ speedup for large datasets

---

### 5.4 FastAPI Response Optimization

**Complexity:** ⭐⭐⭐⭐
**Use Case:** Fast API responses, efficient serialization
**Optimization:** Response models, orjson, streaming

**Pattern:**

```python
from fastapi import FastAPI, Response
from fastapi.responses import ORJSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, AsyncGenerator
import orjson

app = FastAPI(default_response_class=ORJSONResponse)  # Faster JSON

# Response model (excludes unneeded fields)
class UserResponse(BaseModel):
    """Optimized response model."""
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True  # Pydantic v2

class UserListResponse(BaseModel):
    """Paginated response."""
    users: List[UserResponse]
    total: int
    page: int

# ❌ WRONG: Returns entire ORM object
@app.get("/users/{user_id}")
async def get_user_bad(user_id: int):
    user = await db.query(User).filter(User.id == user_id).first()
    return user  # Serializes all fields, slow

# ✅ CORRECT: Use response model
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user_good(user_id: int):
    user = await db.query(User).filter(User.id == user_id).first()
    return user  # Only serializes specified fields

# Streaming large responses
async def generate_users() -> AsyncGenerator[bytes, None]:
    """Stream users without loading all into memory."""
    async for user in db.stream_query(User):
        yield orjson.dumps({
            "id": user.id,
            "email": user.email,
            "name": user.name
        }) + b"\n"

@app.get("/users/export")
async def export_users():
    """Export users as streaming response."""
    return StreamingResponse(
        generate_users(),
        media_type="application/x-ndjson"
    )

# Background tasks for slow operations
from fastapi import BackgroundTasks

def send_email_notification(email: str):
    """Slow email sending."""
    time.sleep(2)
    print(f"Email sent to {email}")

@app.post("/users")
async def create_user(user: UserCreate, background_tasks: BackgroundTasks):
    """Create user with background email."""
    # Create user (fast)
    db_user = User(**user.dict())
    await db.add(db_user)
    await db.commit()

    # Send email in background (doesn't block response)
    background_tasks.add_task(send_email_notification, user.email)

    return db_user  # Returns immediately

# Efficient pagination
from fastapi_pagination import Page, add_pagination, paginate

@app.get("/users", response_model=Page[UserResponse])
async def list_users(page: int = 1, size: int = 50):
    """Paginated user list."""
    query = select(User).order_by(User.id)
    return await paginate(db, query)

add_pagination(app)

# Response caching
from fastapi_cache.decorator import cache

@app.get("/expensive-computation")
@cache(expire=300)  # Cache for 5 minutes
async def expensive_endpoint():
    """Expensive computation with caching."""
    await asyncio.sleep(2)  # Simulate expensive work
    return {"result": "expensive computation"}
```

**Performance Improvements:**
- ORJSONResponse: 2-3x faster JSON serialization
- Streaming: Constant memory usage for large datasets
- Background tasks: 10x+ faster response times
- Caching: 100x+ speedup for cacheable responses

---

## Summary

This guide covered **20 advanced Python patterns** across 5 categories:

**Async/Concurrency (4 patterns):**
1. asyncio.gather() for parallel execution
2. Error handling with return_exceptions=True
3. Semaphore for rate limiting
4. Background tasks with create_task()

**Type System (4 patterns):**
1. Generic types with TypeVar
2. Protocol for structural typing
3. Pydantic v2 validation patterns
4. TypedDict for structured dictionaries

**Design Patterns (3 patterns):**
1. Context managers for resource management
2. Dependency injection with FastAPI
3. Abstract base classes (ABC)

**Testing (4 patterns):**
1. Pytest fixtures with dependency injection
2. Parametrized tests
3. Mocking with pytest-mock
4. Async integration testing

**Performance (5 patterns):**
1. Generators for memory efficiency
2. Caching with lru_cache
3. Database query optimization (N+1 prevention)
4. FastAPI response optimization
5. Streaming responses

**Key Takeaways:**
- Use async/await for I/O-bound operations
- Leverage Python's type system for safer code
- Apply design patterns for maintainable architecture
- Write comprehensive tests with pytest
- Optimize performance with caching and generators

**Framework Integration Highlights:**
- FastAPI: Dependency injection, background tasks, ORJSONResponse
- Pydantic v2: field_validator, model_validator, computed_field
- SQLAlchemy: joinedload, selectinload, async queries
- pytest: fixtures, parametrize, async testing

All patterns include production-ready code examples with performance impact notes.
