# Case Study — QA Test Automation

A complete QA automation suite covering:

1. **UI Tests** — Insider careers page (Selenium + POM + pytest)
2. **Load Tests** — n11.com search module (Locust)
3. **API Tests** — PetStore CRUD operations (requests + pytest)

---

## Project Structure

```
Case_Study_Insider/
├── conftest.py                  # Browser fixture, screenshot-on-fail hook
├── pytest.ini                   # pytest configuration
├── requirements.txt
│
├── pages/                       # Page Object Model
│   ├── base_page.py
│   ├── home_page.py
│   ├── careers_page.py
│   ├── qa_jobs_page.py
│   └── lever_page.py
│
├── tests/
│   ├── ui/
│   │   └── test_insider_careers.py
│   ├── load/
│   │   └── locustfile.py
│   └── api/
│       └── test_petstore_api.py
│
└── screenshots/                 # Auto-created; contains failure screenshots
```

---

## Prerequisites

- Python 3.10+
- Google Chrome and/or Firefox installed
- ChromeDriver / GeckoDriver handled automatically by `webdriver-manager`

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Running the Tests

### UI Tests (Chrome — default)

```bash
pytest tests/ui/ --browser=chrome -v
```

### UI Tests (Firefox)

```bash
pytest tests/ui/ --browser=firefox -v
```

### UI Tests (Headless)

```bash
pytest tests/ui/ --browser=chrome --headless -v
```

### API Tests

```bash
pytest tests/api/ -v
```

### All Tests (UI + API)

```bash
pytest tests/ui/ tests/api/ --browser=chrome -v
```

---

## Load Tests (Locust)

### Headless mode (1 user, 60 seconds)

```bash
locust -f tests/load/locustfile.py \
       --headless -u 1 -r 1 --run-time 60s \
       --host https://www.n11.com
```

### Interactive Web UI

```bash
locust -f tests/load/locustfile.py --host https://www.n11.com
# Open http://localhost:8089 in your browser
```

---

## Screenshots on Failure

If any UI test step fails, a screenshot is automatically saved to the `screenshots/` directory:

```
screenshots/
└── test_step2_navigate_and_filter_jobs_20240305_143021.png
```

---

## UI Test Flow

The 4 test steps share a **single browser session** and run in order:

| Step | Test Method | Description |
|------|-------------|-------------|
| 1 | `test_step1_home_page_loaded` | Opens insiderone.com, verifies navbar, hero, footer |
| 2 | `test_step2_navigate_and_filter_jobs` | Goes to QA careers page, clicks "See all QA jobs", filters by Istanbul + QA dept |
| 3 | `test_step3_jobs_content_validation` | Asserts every job has correct Position, Department, Location |
| 4 | `test_step4_view_role_redirects_to_lever` | Clicks "View Role", verifies redirect to lever.co |

---

## API Test Coverage

| Type | Test | Endpoint |
|------|------|----------|
| Positive | Create pet | `POST /pet` |
| Positive | Read pet by ID | `GET /pet/{id}` |
| Positive | Update pet | `PUT /pet` |
| Positive | Delete pet | `DELETE /pet/{id}` |
| Positive | Find by status (available) | `GET /pet/findByStatus` |
| Positive | Find by status (sold) | `GET /pet/findByStatus` |
| Negative | Get non-existent pet | `GET /pet/9999999999` → 404 |
| Negative | Delete non-existent pet | `DELETE /pet/9999999999` → 404 |
| Negative | Invalid ID (string) | `GET /pet/not-a-valid-id` → 400/404 |
| Negative | Empty request body | `POST /pet` `{}` → 4xx/5xx |
| Negative | Invalid JSON | `POST /pet` plain text → 4xx/5xx |
| Negative | Update non-existent pet | `PUT /pet` non-existent ID → no 5xx |
| Negative | Invalid status filter | `GET /pet/findByStatus?status=xyz` → 400 |

---

## Load Test Scenarios

| Scenario | Class | Tasks |
|----------|-------|-------|
| Keyword Search | `KeywordSearchUser` | laptop, kulaklık, ayakkabı |
| Category Search | `CategorySearchUser` | telefon, bilgisayar, kıyafet |
| Edge/Empty Search | `EdgeSearchUser` | empty string, whitespace |
