# Python Data Stack

**Version:** 1.0.0
**Category:** Python
**Deployment Mode:** flat (recommended)

## Bundle Purpose

Data-focused Python stack for projects requiring robust data validation, ORM capabilities, and database migrations. Optimized for data-intensive applications, ETL pipelines, and backend services with complex data models.

## Included Skills

- **pydantic** (toolchains/python/validation/pydantic) - Data validation with type hints
- **sqlalchemy** (toolchains/python/data/sqlalchemy) - ORM with 2.0 syntax and async support
- **database-migration** (universal/data/database-migration) - Schema evolution strategies
- **pytest** (toolchains/python/testing/pytest) - Testing framework
- **json-data-handling** (universal/data/json-data-handling) - JSON parsing and validation

## Use Cases

**When to Deploy This Bundle:**
- ETL (Extract, Transform, Load) pipelines
- Data validation and serialization projects
- Backend services with PostgreSQL/MySQL
- Projects requiring strict data schemas
- Data migration and transformation scripts

**What You Get:**
- Pydantic models for data validation
- SQLAlchemy ORM patterns (Core and ORM)
- Alembic migration workflows
- pytest integration for data layer testing
- JSON schema validation patterns

## Deployment

```bash
# Recommended: Flat deployment to .claude/
./deploy.sh --flat ~/.claude/

# Validate before deploying
./deploy.sh --validate
```

## Skill Compatibility Matrix

| Skill | Standalone | Bundle-Enhanced | Required Dependencies |
|-------|------------|-----------------|----------------------|
| pydantic | ✅ Yes | 🚀 Enhanced | None |
| sqlalchemy | ✅ Yes | 🚀 Enhanced | None |
| database-migration | ✅ Yes | 🚀 Enhanced | SQLAlchemy (recommended) |
| pytest | ✅ Yes | 🚀 Enhanced | None |
| json-data-handling | ✅ Yes | 🚀 Enhanced | Pydantic (recommended) |

**Bundle Synergies:**
- Pydantic + SQLAlchemy: Validate API input, persist with ORM
- SQLAlchemy + database-migration: Alembic migrations from models
- Pydantic + JSON handling: Type-safe JSON parsing
- pytest + Pydantic: Test data validation rules

## Integration Example

```python
# Pydantic + SQLAlchemy + Alembic
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

# Pydantic schema for API
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int

# SQLAlchemy model for database
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

# Validate with Pydantic, persist with SQLAlchemy
user_data = UserCreate(email="user@example.com", name="John", age=30)
db_user = User(**user_data.model_dump())
session.add(db_user)
session.commit()

# Migration with Alembic
# alembic revision --autogenerate -m "Add users table"
# alembic upgrade head
```

## Version History

- **1.0.0** (2025-11-30): Initial release with 5 data stack skills
