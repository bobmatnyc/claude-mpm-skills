# Skill Restructuring Action Plan
**Date:** 2025-11-30  
**Based on:** anthropic-skills-structure-analysis-2025-11-30.md  
**Objective:** Align claude-mpm-skills with Anthropic's official structure patterns

## Quick Reference

**Problem:** Our SKILL.md files are 2-3x larger than Anthropic's, with all code inline instead of in separate runnable files.

**Solution:** Extract code samples to examples/, create utility scripts/, slim down SKILL.md files.

**Impact:** 25 high-priority skills, ~4-5 weeks timeline.

## Prioritized Action List

### Phase 1: Template & Pilot (Week 1)

#### Day 1-2: Create Templates

**Task 1.1: Framework Skill Template**
```bash
# Create template structure
mkdir -p .templates/framework-skill/{examples/{basic,intermediate,advanced},scripts}

# Create template files
cat > .templates/framework-skill/SKILL.md << 'TEMPLATE'
---
name: framework-name
description: Brief description and when to use
---

# Framework Name

## Overview
[Conceptual explanation - 100-200 lines]

## Core Concepts
[Key principles - 100-200 lines]

## Quick Start
[Minimal getting started - 50-100 lines]

## Patterns
[Common patterns with short snippets - 200-300 lines]

## Examples
See examples/ directory:
- basic/ - Simple starter projects
- intermediate/ - Common use cases  
- advanced/ - Complex scenarios

## Scripts
See scripts/ directory:
- setup.sh - Environment setup
- run_example.sh - Quick example runner
TEMPLATE

cat > .templates/framework-skill/examples/README.md << 'TEMPLATE'
# Examples

## Structure
- basic/ - Simple getting started examples
- intermediate/ - Common patterns and use cases
- advanced/ - Complex real-world scenarios

## Running Examples
Each example directory contains:
- Complete working code
- README.md with instructions
- requirements.txt or package.json (if applicable)

## Usage
```bash
cd basic/
# Follow README.md instructions
```
TEMPLATE
```

**Task 1.2: Multi-Language Skill Template**
```bash
# Create template
mkdir -p .templates/multi-language-skill/{examples/{python,javascript,typescript,go},references}

cat > .templates/multi-language-skill/SKILL.md << 'TEMPLATE'
---
name: skill-name
description: Cross-language skill description
---

# Skill Name

## Principles
[Language-agnostic principles - 200-300 lines]

## Language-Specific Examples
See examples/ directory:
- python/ - Python implementation
- javascript/ - JavaScript implementation
- typescript/ - TypeScript implementation
- go/ - Go implementation

## References
See references/ directory for detailed guides.
TEMPLATE
```

**Task 1.3: Document Standards**
```bash
cat > .templates/TEMPLATE_USAGE.md << 'GUIDE'
# Skill Template Usage Guide

## When to Use Each Template

### Framework Skill Template
Use for: Django, FastAPI, React, Next.js, Express, etc.
Characteristics:
- Single language/framework focus
- Need runnable starter projects
- Complexity progression (basic → advanced)

### Multi-Language Skill Template  
Use for: TDD, debugging, design patterns, etc.
Characteristics:
- Universal concepts across languages
- Need language-specific implementations
- Focus on principles over frameworks

## File Size Guidelines

### SKILL.md
- Simple: 200-500 lines
- Framework: 400-800 lines
- Complex: 800-1,200 lines (absolute max)

### Code Blocks
- Snippets only: 5-15 lines
- Max 20-30 blocks per SKILL.md
- Longer code → separate file

### Examples
- Each example: Complete, runnable project
- Include README.md with setup/run instructions
- Add requirements/dependencies file

### Scripts
- Executable (chmod +x)
- Documented with comments
- Handle errors gracefully
GUIDE
```

#### Day 3-4: Pilot Skill 1 - FastAPI

**Task 2.1: Create Structure**
```bash
cd toolchains/python/frameworks/fastapi-local-dev/

# Create directories
mkdir -p examples/{basic,database,testing,authentication}
mkdir -p scripts
```

**Task 2.2: Extract Basic Example**
```bash
cat > examples/basic/main.py << 'CODE'
"""
Basic FastAPI Application
Demonstrates: app setup, routes, request/response
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Basic Example", version="1.0.0")

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item, "status": "created"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
CODE

cat > examples/basic/README.md << 'README'
# Basic FastAPI Example

## What This Demonstrates
- App initialization
- GET/POST endpoints
- Pydantic models
- Path and body parameters

## Setup
```bash
pip install fastapi uvicorn pydantic
```

## Run
```bash
python main.py
# Or: uvicorn main:app --reload
```

## Test
```bash
curl http://localhost:8000/
curl http://localhost:8000/items/42
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget","price":9.99}'
```

## Next Steps
See ../database/ for async database integration.
README

cat > examples/basic/requirements.txt << 'REQS'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
REQS
```

**Task 2.3: Extract Database Example**
```bash
cat > examples/database/main.py << 'CODE'
"""
FastAPI with Async SQLAlchemy
Demonstrates: async database, sessions, CRUD operations
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from contextlib import asynccontextmanager

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]

# Lifespan for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# Dependency
async def get_session():
    async with async_session_maker() as session:
        yield session

# Routes
@app.post("/users/")
async def create_user(name: str, email: str, session: AsyncSession = Depends(get_session)):
    user = User(name=name, email=email)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@app.get("/users/")
async def list_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
CODE

cat > examples/database/README.md << 'README'
# FastAPI Async Database Example

## What This Demonstrates
- Async SQLAlchemy integration
- Database sessions with dependency injection
- Lifespan events for startup/shutdown
- CRUD operations

## Setup
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Test
```bash
# Create users
curl -X POST "http://localhost:8000/users/?name=Alice&email=alice@example.com"
curl -X POST "http://localhost:8000/users/?name=Bob&email=bob@example.com"

# List users
curl http://localhost:8000/users/
```

## Database File
SQLite database will be created as `test.db` in current directory.
README

cat > examples/database/requirements.txt << 'REQS'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy[asyncio]==2.0.23
aiosqlite==0.19.0
REQS
```

**Task 2.4: Create Setup Script**
```bash
cat > scripts/setup.sh << 'SCRIPT'
#!/bin/bash
# FastAPI Development Environment Setup

set -e

echo "FastAPI Development Setup"
echo "========================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if [[ ! "$python_version" > "3.8" ]]; then
    echo "Error: Python 3.8+ required"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install FastAPI
echo "Installing FastAPI and dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn[standard] pydantic sqlalchemy[asyncio] aiosqlite

echo ""
echo "Setup complete!"
echo "To activate: source venv/bin/activate"
echo "To run example: cd examples/basic && python main.py"
SCRIPT

chmod +x scripts/setup.sh
```

**Task 2.5: Slim Down SKILL.md**
```bash
# Backup original
cp SKILL.md SKILL.md.backup

# Create slimmed version (manually edit to):
# 1. Remove large code blocks (replace with references)
# 2. Keep only short snippets (5-15 lines)
# 3. Add "See examples/" sections
# 4. Target: reduce from 1,200 lines to 600 lines
```

#### Day 5: Pilot Skill 2 - TDD

**Task 3.1: Create Multi-Language Examples**
```bash
cd universal/testing/test-driven-development/

mkdir -p examples/{python,javascript,typescript,go}

# Python example
cat > examples/python/test_calculator.py << 'CODE'
"""
TDD Example: Calculator
Language: Python with pytest
"""
import pytest
from calculator import Calculator

def test_should_add_two_numbers():
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5

def test_should_subtract_two_numbers():
    calc = Calculator()
    result = calc.subtract(5, 3)
    assert result == 2

def test_should_multiply_two_numbers():
    calc = Calculator()
    result = calc.multiply(4, 3)
    assert result == 12

def test_should_divide_two_numbers():
    calc = Calculator()
    result = calc.divide(10, 2)
    assert result == 5.0

def test_should_raise_error_on_division_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)
CODE

cat > examples/python/calculator.py << 'CODE'
"""
Calculator Implementation
Developed using TDD (test-first approach)
"""

class Calculator:
    def add(self, a: float, b: float) -> float:
        """Add two numbers"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Divide a by b"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
CODE

cat > examples/python/README.md << 'README'
# Python TDD Example

## Red-Green-Refactor Workflow

1. **Red**: Write failing test
   ```bash
   pytest test_calculator.py::test_should_add_two_numbers
   # FAIL - Calculator class doesn't exist
   ```

2. **Green**: Make it pass
   ```python
   # Add minimal implementation to calculator.py
   class Calculator:
       def add(self, a, b):
           return a + b
   ```

3. **Refactor**: Improve code
   ```python
   # Add type hints, docstrings
   def add(self, a: float, b: float) -> float:
       """Add two numbers"""
       return a + b
   ```

## Run Tests
```bash
pip install pytest
pytest test_calculator.py -v
```

## Key Concepts Demonstrated
- Test function naming: test_should_<behavior>_when_<condition>
- Arrange-Act-Assert pattern
- Exception testing with pytest.raises
- Type hints and documentation
README

# JavaScript example
cat > examples/javascript/calculator.test.js << 'CODE'
/**
 * TDD Example: Calculator
 * Language: JavaScript with Jest
 */
const Calculator = require('./calculator');

describe('Calculator', () => {
  let calc;
  
  beforeEach(() => {
    calc = new Calculator();
  });

  test('should add two numbers', () => {
    const result = calc.add(2, 3);
    expect(result).toBe(5);
  });

  test('should subtract two numbers', () => {
    const result = calc.subtract(5, 3);
    expect(result).toBe(2);
  });

  test('should multiply two numbers', () => {
    const result = calc.multiply(4, 3);
    expect(result).toBe(12);
  });

  test('should divide two numbers', () => {
    const result = calc.divide(10, 2);
    expect(result).toBe(5);
  });

  test('should throw error on division by zero', () => {
    expect(() => {
      calc.divide(10, 0);
    }).toThrow('Cannot divide by zero');
  });
});
CODE

cat > examples/javascript/calculator.js << 'CODE'
/**
 * Calculator Implementation
 * Developed using TDD (test-first approach)
 */

class Calculator {
  add(a, b) {
    return a + b;
  }

  subtract(a, b) {
    return a - b;
  }

  multiply(a, b) {
    return a * b;
  }

  divide(a, b) {
    if (b === 0) {
      throw new Error('Cannot divide by zero');
    }
    return a / b;
  }
}

module.exports = Calculator;
CODE

cat > examples/javascript/package.json << 'JSON'
{
  "name": "tdd-calculator-example",
  "version": "1.0.0",
  "scripts": {
    "test": "jest"
  },
  "devDependencies": {
    "jest": "^29.7.0"
  }
}
JSON
```

#### Day 6-7: Review & Document

**Task 4.1: Test All Examples**
```bash
# Test FastAPI examples
cd toolchains/python/frameworks/fastapi-local-dev/examples/basic
python main.py &
sleep 2
curl http://localhost:8000/
kill %1

# Test TDD examples
cd universal/testing/test-driven-development/examples/python
pytest test_calculator.py -v

cd ../javascript
npm install
npm test
```

**Task 4.2: Document Learnings**
```bash
cat > docs/restructuring-pilot-results.md << 'DOC'
# Pilot Restructuring Results

## Skills Restructured
1. fastapi-local-dev/
2. test-driven-development/

## Metrics
- FastAPI SKILL.md: 1,200 → 600 lines (50% reduction)
- TDD SKILL.md: 380 → 300 lines (21% reduction)
- Examples added: 6 working projects
- Scripts added: 1 setup script

## Time Investment
- Template creation: 4 hours
- FastAPI restructuring: 6 hours
- TDD restructuring: 4 hours
- Testing and docs: 2 hours
- Total: 16 hours (~2 days)

## Learnings
[To be filled after pilot]

## Challenges
[To be filled after pilot]

## Recommendations for Bulk Phase
[To be filled after pilot]
DOC
```

### Phase 2: Bulk Restructuring (Weeks 2-3)

#### High-Priority Skills (Week 2)

**Day 8-9: LangGraph**
- [ ] Extract graph definition examples
- [ ] Extract agent examples
- [ ] Create testing utilities
- [ ] Reduce SKILL.md from 2,432 to ~800 lines

**Day 10-11: Django**
- [ ] Extract project setup
- [ ] Extract model/view/template examples
- [ ] Create quick start script
- [ ] Reduce SKILL.md from 1,600 to ~600 lines

**Day 12: TanStack Query**
- [ ] Extract query examples
- [ ] Extract mutation patterns
- [ ] Add optimization examples
- [ ] Reduce SKILL.md from 2,397 to ~700 lines

#### Medium-Priority Skills (Week 3)

**Day 13-14:**
- [ ] GraphQL (2,311 lines → 700)
- [ ] tRPC (2,091 lines → 650)
- [ ] Celery (2,089 lines → 700)

**Day 15-16:**
- [ ] Session Compression (2,028 lines → 600)
- [ ] WordPress Testing (1,956 lines → 600)
- [ ] Turborepo (1,769 lines → 650)

**Day 17:**
- [ ] WordPress Architecture (1,688 lines → 600)
- [ ] WordPress Security (1,610 lines → 600)

### Phase 3: Universal Skills Enhancement (Week 4)

#### Add Examples to Multi-Language Skills

**Day 18-19:**
- [ ] web-performance-optimization/
- [ ] systematic-debugging/
- [ ] dispatching-parallel-agents/

**Day 20:**
- [ ] root-cause-tracing/
- [ ] verification-before-completion/

### Phase 4: Validation & Documentation (Week 5)

**Day 21-22: Testing**
- [ ] Run all examples
- [ ] Verify scripts work
- [ ] Check documentation references
- [ ] Test progressive disclosure

**Day 23: Documentation**
- [ ] Update STRUCTURE.md
- [ ] Update README.md
- [ ] Create contributor guide for new skills
- [ ] Document example patterns

**Day 24-25: Final Review**
- [ ] Code review all changes
- [ ] Verify consistency across skills
- [ ] Update manifest.json if needed
- [ ] Create migration summary

## Success Criteria

### Per-Skill Criteria
- [ ] SKILL.md reduced by 30-50%
- [ ] Examples are complete and runnable
- [ ] Scripts are executable and documented
- [ ] No broken references in SKILL.md
- [ ] README.md in examples/ directory

### Repository-Wide Criteria
- [ ] All 25 target skills restructured
- [ ] Templates documented and reusable
- [ ] Examples tested and working
- [ ] Documentation updated
- [ ] No regression in skill functionality

## Risk Mitigation

### Backup Strategy
```bash
# Before each skill restructuring
git checkout -b restructure-<skill-name>
cp <skill-dir>/SKILL.md <skill-dir>/SKILL.md.backup
```

### Rollback Plan
```bash
# If restructuring fails
git checkout main
# Or restore from backup
cp SKILL.md.backup SKILL.md
```

### Testing Protocol
1. Test examples independently
2. Verify SKILL.md references are correct
3. Check Claude Code loads skill without errors
4. Validate progressive disclosure works

## Tools and Automation

### Script: Extract Code Blocks
```bash
#!/bin/bash
# extract_code_blocks.sh - Helper to extract code blocks from SKILL.md

SKILL_FILE=$1
OUTPUT_DIR=$2

mkdir -p "$OUTPUT_DIR"

# Extract code blocks with language tags
awk '/```python/,/```/ {if (!/```/) print}' "$SKILL_FILE" > "$OUTPUT_DIR/extracted_python.txt"
awk '/```javascript/,/```/ {if (!/```/) print}' "$SKILL_FILE" > "$OUTPUT_DIR/extracted_js.txt"

echo "Extracted code blocks to $OUTPUT_DIR"
```

### Script: Validate Examples
```bash
#!/bin/bash
# validate_examples.sh - Test all examples in a skill

SKILL_DIR=$1

for example in "$SKILL_DIR"/examples/*/; do
    echo "Testing $(basename $example)..."
    cd "$example"
    
    if [ -f "requirements.txt" ]; then
        pip install -q -r requirements.txt
        python -m pytest . || python main.py --help
    elif [ -f "package.json" ]; then
        npm install --silent
        npm test
    fi
    
    cd - > /dev/null
done
```

## Monitoring Progress

### Dashboard (Update Weekly)
```markdown
## Restructuring Progress

### Completed (0/25)
- [ ] fastapi-local-dev
- [ ] test-driven-development

### In Progress (0/25)

### Pending (25/25)
- [ ] langgraph
- [ ] django
- [ ] tanstack-query
... (full list)

### Metrics
- Total lines reduced: 0
- Examples added: 0
- Scripts created: 0
- Time invested: 0 hours
```

## Next Actions

**Immediate (This Week):**
1. Review and approve this action plan
2. Create templates (.templates/ directory)
3. Start pilot with fastapi-local-dev

**Short-term (Week 2-3):**
4. Complete pilot evaluation
5. Begin bulk restructuring based on learnings

**Long-term (Week 4-5):**
6. Enhance universal skills
7. Final validation and documentation

---

**Status:** Ready for Execution  
**Dependencies:** Approval of analysis and plan  
**Estimated Effort:** 4-5 weeks, ~80-100 hours total
