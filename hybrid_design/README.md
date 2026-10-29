# SauceDemo Hybrid Automation Framework

A runnable teaching reference combining **POM + Factory + Strategy + Builder + Facade**, with **dependency injection via pytest fixtures** and **data-driven parameterization**.

## 1. Why these patterns?

| Pattern | Class/location | What it solves | Do not use when... |
|---|---|---|---|
| POM | `framework/pages/` | UI selectors and interactions live in one place | A tiny one-off test has no reuse requirement |
| Factory | `browser_factory.py` | Selects browser engine from configuration | There is only one possible implementation |
| Strategy | `login_strategy.py` | Selects login persona/behavior without changing workflow | Simple data parameterization would suffice |
| Builder | `customer_builder.py` | Creates readable, independent test-data objects | A literal tuple is clearer |
| Facade | `purchase_facade.py` | Coordinates multi-page business actions | Hiding every step would make diagnostics harder |
| Dependency injection | `tests/conftest.py` | Provides configured page objects with isolated test contexts | Avoid creating global browser/page singletons |
| Data driven | `pytest.mark.parametrize` | Exercises validation cases without duplicated code | Distinct workflows deserve separate tests |

This is *hybrid* because it combines architectural patterns and data-driven testing. It is **not** keyword-driven or BDD; those are possible later extensions, not necessary for this reference.

## 2. Prerequisites

- Python 3.10+
- Access to https://www.saucedemo.com/
- Local browsers supported by Playwright

## 3. Install (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m playwright install chromium
```

Linux/macOS: use `python3 -m venv .venv`, `source .venv/bin/activate`, and `python -m pip install -e .`.

## 4. Execute

```powershell
python -m pytest -v
python -m pytest -v -m smoke
python -m pytest -v -m "negative or regression"
python -m pytest -v --browser-name firefox
python -m pytest -v --headed --slow-mo 150
python -m pytest -v --base-url https://www.saucedemo.com
python -m pytest -v --junitxml artifacts/junit.xml
```

For Firefox/WebKit, install their browsers first, e.g. `python -m playwright install firefox webkit`.

Optional parallel and HTML reporting:

```powershell
python -m pip install -e ".[parallel,html]"
python -m pytest -n 2 --html=artifacts/report.html --self-contained-html
```

Failed test-call screenshots are saved into `artifacts/screenshots/`. Setup failures may not produce screenshots; this is a deliberate limit of the starter.

## 5. CI/CD and release validation

The GitHub Actions workflow in `.github/workflows/ci.yml` runs the Playwright suite on pushes to `main`/`master`, pull requests, and published releases. It can also be started manually with a target URL, browser, and optional pytest marker expression. Every run publishes a self-contained HTML report, JUnit XML, and any failure screenshots for 14 days.

This repository is a test framework rather than a deployable service, so the workflow provides the validation gate for continuous delivery instead of performing a deployment. A deployment repository can call it after deploying an environment:

```yaml
jobs:
  acceptance-tests:
    uses: your-org/saucedemo-hybrid-framework/.github/workflows/ci.yml@main
    with:
      base_url: https://dev.example.com
      browser: chromium
      marker: smoke
```

Configure the calling deployment job to depend on `acceptance-tests` before promoting a release. Keep protected environment secrets in GitHub Environments; this workflow needs no secrets for the public SauceDemo target.

## 6. Code walkthrough

1. `pytest` loads `conftest.py`, parses CLI options, and builds immutable `Settings`.
2. Async `page` fixture uses `BrowserFactory` to create a browser and a **fresh context per test**.
3. Page-object fixtures inject the same page into Login, Inventory, Cart, and Checkout objects.
4. Test chooses login behavior via Strategy; common paths use the Facade.
5. Builder constructs immutable customer data for checkout.
6. Pytest assertions and Playwright `expect` determine pass/fail; teardown saves failure screenshots.
7. `-m smoke` can later serve deployment checks; `-m regression` for manual or scheduled full coverage.

## 7. Intentional guardrails

- This learning framework uses public SauceDemo test credentials; do **not** hardcode real credentials.
- A single browser per test is straightforward and isolated but slower; future optimization could use a worker-scoped browser with test-scoped contexts.
- No singleton browser/page objects: parallel execution requires isolation.
- Only workflow actions used in more than one place belong in the Facade; keep verification in tests/page expectations.
- The Strategy classes demonstrate the pattern, but the current scenarios could also be represented by test data alone. Use Strategy when auth flows actually differ (e.g., password vs SSO/token).
- Running with xdist is supported, but SauceDemo is a shared public demo. Results can be affected by network or service conditions.
