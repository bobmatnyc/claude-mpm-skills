---
name: cypress
description: "Cypress end-to-end and component testing patterns for web apps: reliable selectors, stable waits, network stubbing, auth handling, CI parallelization, and flake reduction"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Write reliable Cypress E2E and component tests with stable selectors, deterministic waits, and network control"
    when_to_use: "When building browser E2E suites, debugging flaky UI tests, validating critical user flows, or adding component tests to a modern frontend"
    quick_start: "1. Install Cypress 2. Add data-testid selectors 3. Use cy.intercept for network control 4. Avoid fixed sleeps 5. Run in CI with artifacts"
  token_estimate:
    entry: 130
    full: 5200
context_limit: 900
tags:
  - javascript
  - testing
  - cypress
  - e2e
  - component-testing
  - ci
  - flake-reduction
requires_tools: []
---

# Cypress (E2E + Component Testing)

## Overview

Cypress runs browser automation with first-class network control, time-travel debugging, and a strong local dev workflow. Use it for critical path E2E tests and for component tests when browser-level rendering matters.

## Quick Start

### Install and open

```bash
npm i -D cypress
npx cypress open
```

### Minimal spec

```ts
// cypress/e2e/health.cy.ts
describe("health", () => {
  it("loads", () => {
    cy.visit("/");
    cy.contains("Hello").should("be.visible");
  });
});
```

## Core Patterns

### 1) Stable selectors

Prefer `data-testid` (or `data-cy`) attributes for selectors. Avoid brittle CSS chains and text-only selectors for critical interactions.

```html
<button data-testid="save-user">Save</button>
```

```ts
cy.get('[data-testid="save-user"]').click();
```

### 2) Deterministic waiting (avoid fixed sleeps)

Wait on app-visible conditions or network aliases rather than `cy.wait(1000)`.

```ts
cy.intercept("GET", "/api/users/*").as("getUser");
cy.visit("/users/1");
cy.wait("@getUser");
cy.get('[data-testid="user-email"]').should("not.be.empty");
```

### 3) Network control with `cy.intercept`

Stub responses for deterministic tests and speed. Keep a small set of “real backend” smoke tests separate.

```ts
cy.intercept("GET", "/api/users/1", {
  statusCode: 200,
  body: { id: "1", email: "a@example.com" },
}).as("getUser");
```

### 4) Authentication strategies

Prefer `cy.session` to cache login for speed and stability.

```ts
// cypress/support/commands.ts
Cypress.Commands.add("login", () => {
  cy.session("user", () => {
    cy.request("POST", "/api/auth/login", {
      email: "test@example.com",
      password: "password",
    });
  });
});
```

```ts
// e2e spec
beforeEach(() => {
  cy.login();
});
```

## Component Testing

Run component tests to validate UI behavior in isolation while keeping browser rendering.

```bash
npx cypress open --component
```

```ts
// cypress/component/Button.cy.tsx
import React from "react";
import Button from "../../src/Button";

describe("<Button />", () => {
  it("clicks", () => {
    cy.mount(<Button onClick={cy.stub().as("onClick")}>Save</Button>);
    cy.contains("Save").click();
    cy.get("@onClick").should("have.been.calledOnce");
  });
});
```

## CI Patterns

### Artifacts (videos/screenshots)

Store artifacts for failed runs and keep videos optional to reduce storage.

```ts
// cypress.config.ts
import { defineConfig } from "cypress";

export default defineConfig({
  video: false,
  screenshotOnRunFailure: true,
  retries: { runMode: 2, openMode: 0 },
});
```

### Parallelization (Cypress Cloud)

Parallelize long E2E suites via Cypress Cloud when runtime dominates feedback loops.

## Anti-Patterns

- Use `cy.wait(1000)` as a synchronization mechanism.
- Select elements via deep CSS paths.
- Mix heavy network stubbing with “real backend” assertions in the same spec.
- Depend on test order; isolate state with `cy.session` and per-test setup.

## Troubleshooting

### Symptom: flaky click or element not found

Actions:
- Add a `data-testid` hook for the element.
- Assert visibility before interaction (`should("be.visible")`).
- Wait on network alias for the data that renders the element.

### Symptom: tests fail only in CI

Actions:
- Increase run-mode retries and record screenshots on failure.
- Verify viewport and baseUrl config match CI environment.
- Eliminate reliance on local-only seed data; create data via API calls.

## Resources

- Cypress docs: https://docs.cypress.io/
- Best practices: https://docs.cypress.io/guides/references/best-practices

