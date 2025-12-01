# Python Testing Stack

**Version:** 1.0.0
**Category:** Python
**Deployment Mode:** flat (recommended)

## Bundle Purpose

Complete testing toolkit for Python projects combining synchronous/async testing, test-driven development methodology, and universal debugging practices. Ideal for FastAPI, Django, or any Python project requiring comprehensive test coverage.

## Included Skills

- **pytest** (toolchains/python/testing/pytest) - Fixtures, parametrization, FastAPI/Django integration
- **asyncio** (toolchains/python/async/asyncio) - Async/await patterns for testing async code
- **test-driven-development** (universal/testing/test-driven-development) - TDD methodology and workflows
- **systematic-debugging** (universal/debugging/systematic-debugging) - Root cause analysis
- **verification-before-completion** (universal/debugging/verification-before-completion) - Quality gates

## Use Cases

**When to Deploy This Bundle:**
- Starting a new Python project with testing requirements
- Adding comprehensive testing to existing Python codebase
- FastAPI or Django projects requiring async test support
- Teams adopting test-driven development practices
- Projects requiring high test coverage (80%+)

**What You Get:**
- Complete pytest configuration patterns
- Async testing with asyncio integration
- Fixtures and dependency injection patterns
- TDD workflow and red-green-refactor cycles
- Debugging methodologies for failing tests
- Verification checklists before deployment

## Deployment

```bash
# Recommended: Flat deployment to .claude/
./deploy.sh --flat ~/.claude/

# Validate before deploying
./deploy.sh --validate

# Alternative: Hierarchical (preserves paths)
./deploy.sh --hierarchical ~/.claude/
```

## Skill Compatibility Matrix

| Skill | Standalone | Bundle-Enhanced | Required Dependencies |
|-------|------------|-----------------|----------------------|
| pytest | ✅ Yes | 🚀 Enhanced | None |
| asyncio | ✅ Yes | 🚀 Enhanced | None (pairs with pytest) |
| test-driven-development | ✅ Yes | 🚀 Enhanced | None (methodology) |
| systematic-debugging | ✅ Yes | 🚀 Enhanced | None (methodology) |
| verification-before-completion | ✅ Yes | 🚀 Enhanced | None (methodology) |

**Bundle Synergies:**
- pytest + asyncio: Seamless async test integration with `pytest-asyncio`
- TDD + pytest: Red-green-refactor workflow with pytest fixtures
- systematic-debugging + pytest: Root cause tracing for test failures
- verification-before-completion: Quality gates before merging

## Integration Examples

### FastAPI Project
```python
# pytest fixtures for FastAPI testing
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.mark.asyncio
async def test_async_endpoint(client):
    response = await client.get("/api/data")
    assert response.status_code == 200
```

### Django Project
```python
# pytest-django integration
import pytest

@pytest.mark.django_db
def test_model_creation(user_factory):
    user = user_factory.create()
    assert user.is_active
```

### TDD Workflow
```bash
# Red: Write failing test
pytest tests/test_feature.py::test_new_feature  # FAIL

# Green: Implement minimal code
# Edit src/feature.py

# Refactor: Improve implementation
pytest tests/test_feature.py::test_new_feature  # PASS
```

## Performance Notes

- **Token Budget**: ~18,000 tokens total (all 5 skills fully loaded)
- **Entry Points**: ~400 tokens (progressive loading)
- **Deployment Size**: ~15-20 KB on disk

## Version History

- **1.0.0** (2025-11-30): Initial release with 5 core testing skills

## Related Bundles

- **python-web-stack**: Pairs with this for complete FastAPI/Django development
- **universal-development**: Broader development practices (includes TDD)

## Troubleshooting

**Issue**: pytest not finding tests
**Solution**: Check test file naming (`test_*.py` or `*_test.py`)

**Issue**: Async tests hanging
**Solution**: Install `pytest-asyncio` and use `@pytest.mark.asyncio`

**Issue**: Django fixtures not working
**Solution**: Install `pytest-django` and configure `pytest.ini`

## Maintenance

**Skill Updates**: Run `./deploy.sh --validate` to check for missing skills before updates

**Version Pinning**: Edit `skills.list` to pin specific versions (e.g., `toolchains/python/testing/pytest:1.2.0`)
