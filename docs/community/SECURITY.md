# Security Policy

## Supported Versions

We provide security updates for skills in the current version of this repository. Since this is a living skill library, only the latest version of each skill receives security updates.

| Version | Supported          |
| ------- | ------------------ |
| Latest (main branch) | :white_check_mark: |
| Older commits | :x: |

## Reporting a Vulnerability

We take security vulnerabilities seriously, especially those that could affect users who deploy these skills to their projects.

### How to Report

**For security vulnerabilities**, please use one of these methods:

1. **Preferred**: Use GitHub's [Security Advisory](https://github.com/bobmatnyc/claude-mpm-skills/security/advisories/new) feature (private disclosure)
2. **Alternative**: Open a private issue by contacting the repository owner directly through GitHub

**Please do NOT** open public issues for security vulnerabilities until they have been addressed.

### What to Include

When reporting a security vulnerability, please provide:

- **Skill Name**: Which skill contains the vulnerability
- **Vulnerability Type**: See categories below
- **Impact**: How this could affect users
- **Reproduction Steps**: How to verify the vulnerability
- **Suggested Fix**: If you have recommendations (optional)

## Security Concerns Specific to Skills

This repository contains code examples and AI agent instructions. The following security concerns are particularly relevant:

### 1. Credential Leakage in Code Examples

**Risk**: Skills containing hardcoded credentials, API keys, or secrets in examples.

**Examples**:
- API keys in code snippets
- Database passwords in configuration examples
- OAuth tokens in demonstration code
- Private keys or certificates

**What We Monitor**:
- All code examples for hardcoded secrets
- Configuration file templates for placeholder credentials
- Environment variable usage patterns

**If You Find**: Report immediately if you discover actual credentials (not placeholder examples).

### 2. Malicious Code Patterns

**Risk**: Skills that teach or demonstrate insecure coding practices.

**Examples**:
- SQL injection vulnerabilities in examples
- Command injection patterns
- Unsafe deserialization
- Path traversal vulnerabilities
- Cross-site scripting (XSS) examples without proper context

**What We Monitor**:
- Code examples that could be copy-pasted into production
- Skills that don't warn about security implications
- Patterns that bypass security controls

**If You Find**: Report code patterns that could lead to security vulnerabilities when used without modification.

### 3. Insecure Defaults or Anti-Patterns

**Risk**: Skills promoting insecure configurations or practices.

**Examples**:
- Disabling authentication in production code
- Recommending weak cryptography
- Unsafe file permissions
- Insecure network configurations
- Missing input validation

**What We Monitor**:
- Default configurations in skills
- Security best practices in documentation
- Warnings about production vs. development settings

**If You Find**: Report skills that recommend insecure defaults without clear warnings.

### 4. Dependency Vulnerabilities

**Risk**: Skills referencing vulnerable packages or outdated dependencies.

**Examples**:
- Skills teaching deprecated libraries with known CVEs
- Package versions with security advisories
- Unmaintained dependencies
- Transitive dependency vulnerabilities

**What We Monitor**:
- Package versions mentioned in skills
- Known vulnerabilities in recommended dependencies
- Maintenance status of suggested tools

**If You Find**: Report if a skill recommends packages with known security vulnerabilities.

### 5. Prompt Injection Risks

**Risk**: AI agent instructions that could be manipulated through prompt injection.

**Examples**:
- Skills that execute user input without validation
- Instructions that don't sanitize file paths
- Agent behaviors that trust user-provided code

**What We Monitor**:
- Agent instruction patterns that could be exploited
- Skills that handle untrusted input
- Command execution patterns in agent workflows

**If You Find**: Report agent instructions that could be manipulated to perform unintended actions.

## Response Timeline

- **Initial Response**: Within 48 hours of vulnerability report
- **Assessment**: 7 days for vulnerability assessment and triage
- **Resolution**:
  - Critical vulnerabilities: 7 days
  - High severity: 14 days
  - Medium/Low severity: 30 days
- **Disclosure**: Coordinated disclosure after fix is merged and users notified

## Security Update Process

When a security vulnerability is confirmed:

1. **Private Fix**: Develop fix in private repository or branch
2. **Coordinated Disclosure**: Work with reporter on disclosure timeline
3. **Patch Release**: Merge fix to main branch
4. **Public Advisory**: Publish security advisory with:
   - Affected skills
   - Severity rating
   - Impact description
   - Remediation steps
5. **User Notification**: Update affected skill documentation with security notice

## Scope

### In Scope

- Code examples in skill files
- Agent instructions in SKILL.md files
- Configuration templates
- Dependencies and package references
- Security best practices in documentation

### Out of Scope

- Security vulnerabilities in third-party tools/frameworks (report to upstream)
- Theoretical vulnerabilities without practical exploit path
- Social engineering attacks unrelated to code

## Recognition

We appreciate security researchers who responsibly disclose vulnerabilities. With your permission, we will acknowledge your contribution in:

- Security advisory credits
- CONTRIBUTORS.md (if you prefer)
- Commit messages for security fixes

## Questions?

If you're unsure whether something is a security vulnerability, please reach out. We'd rather investigate a false positive than miss a real issue.

For general security questions or best practices, feel free to open a public GitHub Discussion.
