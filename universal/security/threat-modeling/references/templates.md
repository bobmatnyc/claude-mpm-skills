# Threat Modeling Templates

## Threat Model Doc (Markdown)

```md
# Threat Model: <System/Feature>

Date: YYYY-MM-DD
Owner: <name/team>
Scope: <what is in scope / out of scope>

## Assets
- <asset 1>
- <asset 2>

## Data Flows and Trust Boundaries
<diagram link or table>

## Assumptions
- <assumption 1>

## Threat Register
| Element | STRIDE | Threat | Impact | Likelihood | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Security Requirements
- <requirement 1>
- <requirement 2>

## Verification
- <test/alert/logging checks>
```

## Threat Register (CSV-Friendly)

```csv
element,stride,threat,impact,likelihood,mitigation,owner,status
```

## PR Checklist Additions

- Threat model updated for new trust boundaries and data stores
- Authn/authz checks added for new endpoints and resources
- Abuse cases and negative tests added for critical flows
- Audit logging added for privileged actions

