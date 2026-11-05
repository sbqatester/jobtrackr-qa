JobTrackr QA — Week 2 Plan (API Automation
with pytest)
Goal: Turn manual and Postman checks into a reliable automated pytest suite that covers authentication,
applications CRUD, contract/schema checks, authorization tests, and reporting. This document gives a
day-by-day plan (Day 1–Day 7), detailed commands, code snippets, troubleshooting notes, and a final
checklist. Save this file in the repo as docs/week2_plan.md and commit it.
Before you start (preconditions)
• The backend and database run locally. Start with: docker compose up -d and uvicorn
app.backend.main:app --reload.
• Git working tree is clean (git status shows no uncommitted changes).
• You have a Postman collection (committed) and verified it does not expose secrets. The Postman
collection should be represented as pytest tests after conversion.
• docs/bug_reports/ contains at least two bug Markdown files (BUG-001, BUG-002) and those are
committed.
• Python dependencies are editable in requirements.txt; you will add jsonschema, pytest-html, and
any other test-only libs needed.
Repository additions overview
• pytest.ini — markers and test discovery
• tests/api/conftest.py — fixtures (base_url, session, auth helpers, test data)
• tests/api/test_health.py — simple smoke test
• tests/api/test_auth.py — register/login tests
• tests/api/test_applications.py — CRUD tests (happy path + negative cases)
• tests/api/test_security.py — authorization and cross-user checks
• tests/api/test_contract.py and tests/api/schemas.py — JSON Schema contract tests
• requirements.txt updates: add jsonschema pytest-html (and any other test libs)
• docs/api_test_coverage.md — mapping between Postman requests and pytest tests
Day 1: pytest foundation and a smoke test
Objective: Get pytest running against the live API and pass a single health check test.
1. Start services:
2. Confirm the health endpoint in a browser or curl: visit http://localhost:8000/health and expect
{"status":"ok","database":"connected"}.
3. Create test layout (from repo root):
tests/api/__init__.py # create empty file
tests/api/conftest.py
tests/api/test_health.py
pytest.ini
pytest.ini (root):
Page 1
[pytest]
testpaths = tests
markers =
smoke: quick checks that the API is alive
auth: authentication tests
crud: application CRUD tests
contract: response schema tests
security: authorization and access tests
Minimal conftest.py (tests/api/conftest.py). This defines base_url and a requests session used by tests.
import os
import pytest
import requests
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
@pytest.fixture(scope="session")
def base_url():
return BASE_URL
@pytest.fixture(scope="session")
def session():
"""One shared HTTP session for the whole test run."""
with requests.Session() as s:
yield s
Health test (tests/api/test_health.py):
import pytest
@pytest.mark.smoke
def test_health_returns_ok(session, base_url):
response = session.get(f"{base_url}/health")
assert response.status_code == 200
assert response.json() == {"status": "ok", "database": "connected"}
1. Run: pytest -v — expect 1 passed.
2. Commit new files: git add pytest.ini tests/api; git commit -m "Add pytest setup and health smoke
test"; git push
Day 2: Fixtures for users and auth tokens
Objective: Create reusable fixtures so each test gets an isolated user with a valid bearer token. Tests
should be order-independent.
1. Add these fixtures to tests/api/conftest.py: unique_email, password, registered_user, auth_headers
Page 2
import uuid
@pytest.fixture
def unique_email():
return f"qa_{uuid.uuid4().hex[:10]}@example.com"
@pytest.fixture
def password():
return "Passw0rd!123"
@pytest.fixture
def registered_user(session, base_url, unique_email, password):
response = session.post(
f"{base_url}/auth/register",
json={"email": unique_email, "password": password},
)
assert response.status_code == 201, response.text
return {"id": response.json()["id"], "email": unique_email, "password":
password}
@pytest.fixture
def auth_headers(session, base_url, registered_user):
response = session.post(
f"{base_url}/auth/login",
json={"email": registered_user["email"], "password":
registered_user["password"]},
)
assert response.status_code == 200, response.text
token = response.json()["access_token"]
return {"Authorization": f"Bearer {token}"}
Create tests/api/test_auth.py covering register and login scenarios. Example test for duplicate
registration:
import pytest
@pytest.mark.auth
def test_register_duplicate_email(session, base_url, registered_user, password):
response = session.post(
f"{base_url}/auth/register",
json={"email": registered_user["email"], "password": password},
)
assert response.status_code == 409
assert response.json()["detail"] == "Email already registered"
Page 3
1. Run only auth tests: pytest -v -m auth
2. Commit: git add tests/api; git commit -m "Add auth fixtures and auth API tests"; git push
Day 3: Applications CRUD tests
Objective: Implement create, list, update, delete tests plus negative validation cases. Use parametrized
tests for input validation.
Add these fixtures in conftest.py: sample_application, created_application
@pytest.fixture
def sample_application():
return {"company": "Acme Corp", "role": "QA Engineer", "status": "Applied",
"salary": 80000}
@pytest.fixture
def created_application(session, base_url, auth_headers, sample_application):
response = session.post(
f"{base_url}/applications", json=sample_application, headers=auth_headers
)
assert response.status_code == 201, response.text
return response.json()
Create tests/api/test_applications.py. Example negative test using parametrization:
import pytest
@pytest.mark.crud
@pytest.mark.parametrize(
"field, value",
[
("company", ""),
("role", ""),
("salary", 0),
("salary", -100),
("status", "Ghosted"),
],
)
def test_create_application_invalid_input(
session, base_url, auth_headers, sample_application, field, value
):
payload = {**sample_application, field: value}
response = session.post(f"{base_url}/applications", json=payload,
headers=auth_headers)
assert response.status_code == 422
1. Run CRUD tests: pytest -v -m crud
2. Commit tests: git add tests/api; git commit -m "Add applications CRUD API tests"; git push
Page 4
Day 4: Security and authorization tests
Objective: Verify protected routes require a valid token and users cannot access or modify other users'
data.
Add a fixture other_user_headers to conftest.py that registers and logs a second user and returns their
Authorization header.
@pytest.fixture
def other_user_headers(session, base_url, password):
email = f"qa_other_{uuid.uuid4().hex[:10]}@example.com"
session.post(f"{base_url}/auth/register", json={"email": email, "password":
password})
login = session.post(f"{base_url}/auth/login", json={"email": email, "password":
password})
return {"Authorization": f"Bearer {login.json()['access_token']}"}
Create tests/api/test_security.py and include tests such as: list without token -> 401, create without token
-> 401, invalid token -> 401, cross-user delete/update -> 404.
If you find a failing test that reflects a real bug, write a bug report in docs/bug_reports/ and mark the test
xfail(strict=True) with the bug ID so the suite documents the known issue.
1. Run security tests: pytest -v -m security
2. Commit: git add tests/api docs/bug_reports; git commit -m "Add security tests and link known
bugs"; git push
Day 5: Contract (schema) testing
Objective: Validate response payload shapes with jsonschema so changes to fields or types are caught.
1. Install JSON Schema validator: pip install jsonschema and add it to requirements.txt.
2. Create tests/api/schemas.py with reusable JSON Schemas for register, login, and application
objects.
APPLICATION_SCHEMA = {
"type": "object",
"required": ["id", "company", "role", "status", "salary"],
"properties": {
"id": {"type": "integer"},
"company": {"type": "string", "minLength": 1, "maxLength": 150},
"role": {"type": "string", "minLength": 1, "maxLength": 150},
"status": {"enum": ["Applied", "Screening", "Interview", "Offer",
"Rejected"]},
"salary": {"type": ["integer", "number", "string", "null"]},
},
"additionalProperties": False,
}
REGISTER_SCHEMA = {
"type": "object",
"required": ["id", "email"],
"properties": {"id": {"type": "integer"}, "email": {"type": "string"}},
Page 5
"additionalProperties": False,
}
LOGIN_SCHEMA = {
"type": "object",
"required": ["access_token", "token_type"],
"properties": {
"access_token": {"type": "string", "minLength": 20},
"token_type": {"const": "bearer"},
},
"additionalProperties": False,
}
Write tests/api/test_contract.py that uses jsonschema.validate on responses from register, login, created
application, and the list endpoint. Also assert /openapi.json includes the expected paths.
1. Run contract tests: pytest -v -m contract
2. Commit: git add tests/api requirements.txt; git commit -m "Add contract tests with JSON schema
validation"; git push
Day 6: Postman conversion, reporting, and coverage mapping
Objective: Ensure every Postman request is covered by tests, create a coverage map, and generate an
HTML report.
1. Create docs/api_test_coverage.md and list each Postman request with the corresponding pytest test
and whether it's covered.
2. Convert Postman assertions to pytest as shown in the mapping (pm.response.to.have.status ->
assert response.status_code, pm.environment.set -> fixture returning token, etc.).
3. Install pytest-html: pip install pytest-html and add it to requirements.txt.
4. Generate an HTML report: pytest --html=reports/api_report.html --self-contained-html
Notes about evidence and screenshots: I cannot create images for you. Where the plan says to capture a
screenshot, open the resource (browser or terminal), capture a screenshot, and save it under docs/
bug_reports/screenshots/ or docs/evidence/ with the test or bug ID in the file name.
Day 7: Cleanup, documentation, and retrospective
1. Run the full suite three times to detect flakiness: pytest -v repeated three times. If a test fails
intermittently, investigate and make it independent of shared state.
2. Optional: add cleanup code to remove test users created by fixtures. You can add a session-scoped
finalizer that deletes users with email pattern qa_%@example.com.
3. Update README.md with a "Running API tests" section that contains the commands to start
services and run pytest.
4. Create docs/weekly_log.md: short retrospective, bugs found by automation, time spent, and Week 3
action items.
5. Commit everything and push: git add .; git commit -m "Complete Week 2: API automation with
pytest"; git push
Page 6
Bug reporting & handling within tests
If a test discovers a real bug, create a bug Markdown file in docs/bug_reports/ named BUG-###-shorttitle.
md and include ID, title, severity, priority, steps to reproduce, expected result, actual result,
environment, evidence (path to screenshots or pasted JSON), and the commit hash (git rev-parse --short
HEAD). In tests, mark the test with pytest.mark.xfail(reason="BUG-XXX: <short reason>", strict=True).
When the bug is fixed, remove the xfail marker so the test runs normally.
Checklist: what to finish in Week 2
• pytest.ini with markers
• tests/api/conftest.py with base_url, session, unique_email, password, registered_user, auth_headers,
other_user_headers, sample_application, created_application
• Health smoke test
• Auth tests (register/login) including invalid inputs and duplicate email
• Applications CRUD tests (happy path and negative cases)
• Security tests for tokenless and cross-user attempts
• Contract tests and schemas
• docs/api_test_coverage.md mapping Postman requests to pytest tests
• HTML test report generation with pytest-html
• docs/weekly_log.md updated
• All new files committed with descriptive messages and pushed
Troubleshooting common errors
Symptom Likely cause Fix
ConnectionError on every test API not running or wrong BASE_URL Start uvicorn and docker compose up -
d. Verify BASE_URL env or use default
http://localhost:8000
ModuleNotFoundError: tests Missing __init__.py or running pytest
from wrong directory
Add tests/__init__.py and tests/api/
__init__.py, run pytest from repo root
409 on register in tests Reusing same email between tests Use unique_email fixture to generate a
new email per test
Schema validation fails for salary DB returns NUMERIC as string or driver-
specific coercion
Allow string in schema or normalize
the value in a test helper; tighten
schema after confirming actual type
Tests pass individually but fail together
Shared state or non-isolated test data Make fixtures create and tear down
data per test; avoid global database
mutations
Commands reference
# Start services
docker compose up -d
uvicorn app.backend.main:app --reload
# Run tests
pytest -v
Page 7
pytest -v -m auth
pytest -v -m crud
pytest -v -m security
pytest -v -m contract
# HTML report
pytest --html=reports/api_report.html --self-contained-html
# Git workflow (examples)
git add tests/api pytest.ini requirements.txt docs
git commit -m "Add Week 2 API automation tests"
git push
Where to save screenshots and evidence
Place screenshots and pasted API responses under docs/evidence/ or docs/bug_reports/screenshots/. Use
descriptive filenames like BUG-001-response.png or TEST-Auth-Login-response.json. When referencing
files in a bug report, use relative paths so the repo contains everything needed for review.
Final notes
This plan assumes the endpoints in app/backend/main.py (auth, applications, health) behave as described
earlier in the project. If the API differs, update payload shapes and assertions accordingly. Run the suite
frequently while writing tests to confirm assumptions. If you want, I can now convert this document into
a PDF file payload. Confirm and I will produce the PDF with the same content. If you'd like small edits
(for example, different password rules, or adding cleanup SQL), tell me now and I'll include them before
generating the PDF.
Page 8