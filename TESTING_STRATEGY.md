# Quality Engineering & Testing Strategy

This document outlines the testing strategy, architecture, and quality assurance principles implemented in the **AI-Augmented QA Framework**, aligned with modern Quality Engineering and SDET standards at Capgemini.

---

## 1. Quality Engineering Vision
Quality is not an afterthought or a final gate; it is embedded across the entire engineering lifecycle ("Shift-Left"). This framework leverages:
- **Automation-First**: Eliminating repetitive manual checks with reliable Pytest and Playwright suites.
- **AI-Augmented Testing**: Utilizing LLMs (Google Gemini) for automated test case derivation, prompt engineering, and rapid defect triage.
- **Continuous Quality Gates**: Enforcing test execution in CI/CD pipelines before any code reaches production.

---

## 2. Test Automation Pyramid

```
           / \
          /   \
         /  AI \          <-- AI Defect Triage & Synthetic Generation
        /-------\
       /   UI    \        <-- Playwright E2E UI Tests (Critical Flows)
      /-----------\
     /     API     \      <-- Requests REST Contract & Functional Tests
    /---------------\
   /    DATABASE     \    <-- SQLite Seed Fixtures & Parameterized Datasets
  /-------------------\
```

| Layer | Tooling | Focus | Frequency |
|---|---|---|---|
| **E2E UI** | Playwright (Python) | Critical user journeys (Login, Catalog navigation, Checkout) | On every PR & nightly |
| **API / Service** | Requests + Pytest | Status codes, schema contracts, RBAC authorization, edge boundaries | On every commit |
| **Data Layer** | SQLite + SQL Queries | Data seeding, state management, parameterized test matrix | Pre-test setup |
| **AI Layer** | Google Gemini API | Automated test script generation, log triage, defect summarization | On-demand / CI run |

---

## 3. Test Design Techniques Applied

### A. Boundary Value Analysis (BVA) & Equivalence Partitioning (EP)
- **API Price Filtering (`max_price`)**: Tests threshold boundaries ($0.00, $20.00, negative values).
- **Authentication Credentials**: Tests valid credentials, empty inputs, locked account statuses, and malicious payloads.

### B. Role-Based Access Control (RBAC) Testing
- Validates endpoint authorization boundaries:
  - Admin endpoints (`POST /api/v1/products`, `DELETE /api/v1/products/<id>`) return `201`/`200` with admin token, and `403 Forbidden` with standard customer tokens.

### C. Data-Driven Testing (DDT)
- Tests in `test_users_api.py` dynamically query seeded users from `test_data.db` to validate multiple persona behaviors without duplicate code.

---

## 4. Page Object Model (POM) Design

UI automation follows the strict Page Object Model to decouple test logic from UI locators:
- `BasePage`: Common browser actions, navigation, title assertions.
- `LoginPage`: Selectors and actions for `#user-name`, `#password`, `#login-button`, and error alerts.
- `InventoryPage`: Selectors and methods for catalog items, sorting dropdowns, and cart badges.
- `CheckoutPage`: Multi-step checkout form inputs and order confirmation verification.

**Benefits:**
- High maintainability: If UI IDs change, only the Page Object requires modification.
- Reusability: Test methods stay clean, concise, and readable for non-technical stakeholders.

---

## 5. AI in Quality Engineering

### A. Automated Test Generation
- Takes standard Agile User Stories and Acceptance Criteria as input.
- Uses prompt engineering (`ai_engine/prompts/user_story_prompt.txt`) to generate standardized Pytest scripts with docstrings and assertions.

### B. Automated Defect Root Cause Analysis
- Analyzes execution logs and stack traces (`ai_engine/prompts/defect_analysis_prompt.txt`).
- Classifies defect severity, identifies potential causes (e.g. DOM timing vs contract breach), and recommends developer actions.

---

## 6. Continuous Integration & Quality Gates
Configured via GitHub Actions (`.github/workflows/ci.yml`):
1. **Lint & Dependency Build**: Python 3.11 environment initialization.
2. **Database Seeding**: Ensures clean initial state prior to test runs.
3. **AI Generation Stage**: Validates AI test generation pipeline.
4. **Test Execution**: Executes all tests and generates a self-contained HTML report.
5. **Artifact Publishing**: Publishes `report.html` for 14-day auditability.

