# Python Web Stack

**Version:** 1.0.0
**Category:** Python
**Deployment Mode:** flat (recommended)

## Bundle Purpose

Production-ready web development stack for Python featuring modern async frameworks, data validation, ORM, and background task processing. Optimized for FastAPI and Django projects requiring scalable, maintainable web applications.

## Included Skills

- **fastapi-local-dev** (toolchains/python/frameworks/fastapi-local-dev) - Modern async API framework with OpenAPI
- **pydantic** (toolchains/python/validation/pydantic) - Data validation with type hints
- **sqlalchemy** (toolchains/python/data/sqlalchemy) - ORM with 2.0 syntax and async support
- **celery** (toolchains/python/async/celery) - Distributed task queues and background jobs
- **pytest** (toolchains/python/testing/pytest) - Testing framework
- **database-migration** (universal/data/database-migration) - Schema evolution strategies

## Use Cases

**When to Deploy This Bundle:**
- Building REST APIs with FastAPI
- Django projects with async views and background tasks
- Projects requiring data validation and serialization
- Applications with database operations and migrations
- Systems with asynchronous background processing

**What You Get:**
- FastAPI app structure and dependency injection
- Pydantic models for request/response validation
- SQLAlchemy ORM patterns with Alembic migrations
- Celery task definitions and periodic jobs
- pytest integration for testing APIs
- Database migration best practices

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
| fastapi | ✅ Yes | 🚀 Enhanced | Pydantic (optional) |
| pydantic | ✅ Yes | 🚀 Enhanced | None |
| sqlalchemy | ✅ Yes | 🚀 Enhanced | None |
| celery | ✅ Yes | 🚀 Enhanced | None |
| pytest | ✅ Yes | 🚀 Enhanced | None |
| database-migration | ✅ Yes | 🚀 Enhanced | SQLAlchemy (recommended) |

**Bundle Synergies:**
- FastAPI + Pydantic: Automatic request/response validation
- SQLAlchemy + Pydantic: ORM models with Pydantic serialization
- FastAPI + Celery: Background task triggering from API endpoints
- pytest + FastAPI: TestClient for API integration tests

## Integration Example

```python
# FastAPI + Pydantic + SQLAlchemy + Celery
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from celery import Celery

app = FastAPI()
celery_app = Celery("tasks")

class UserCreate(BaseModel):
    email: str
    name: str

@app.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Validate with Pydantic (automatic)
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()

    # Trigger background task
    send_welcome_email.delay(user.email)

    return {"id": db_user.id}

@celery_app.task
def send_welcome_email(email: str):
    # Background task processing
    pass
```

## Version History

- **1.0.0** (2025-11-30): Initial release with 6 core web development skills
